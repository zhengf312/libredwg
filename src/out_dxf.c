/*****************************************************************************/
/*  LibreDWG - free implementation of the DWG file format                    */
/*                                                                           */
/*  Copyright (C) 2018-2020 Free Software Foundation, Inc.                   */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

/*
 * out_dxf.c: write as Ascii DXF
 * written by Reini Urban
 */

/* Works for most r13+ files, but not for many r2014+ objects.
TODO:
* down-conversions from unsupported entities on older DXF versions.
  Since r13:
  Entities: LWPOLYLINE, HATCH, SPLINE, LEADER, DIMENSION, MTEXT, IMAGE,
  BLOCK_RECORD. Add CLASSES for those.
*/

#include "config.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>
#include <assert.h>
//#include <math.h>

#define IS_PRINT
#define IS_DXF
#include "common.h"
#include "bits.h"
#include "myalloca.h"
#include "dwg.h"
#include "decode.h"
#include "encode.h"
#include "out_dxf.h"

static unsigned int loglevel;
#define DWG_LOGLEVEL loglevel
#include "logging.h"

/* the current version per spec block */
static unsigned int cur_ver = 0;
static char buf[255];
static BITCODE_BL rcount1, rcount2;
// static int is_sorted = 0;

// imported
char *dwg_obj_table_get_name (const Dwg_Object *restrict obj,
                              int *restrict error);

// private
static int dxf_common_entity_handle_data (Bit_Chain *restrict dat,
                                          const Dwg_Object *restrict obj);
static int dwg_dxf_object (Bit_Chain *restrict dat,
                           const Dwg_Object *restrict obj, int *restrict);
static int dxf_3dsolid (Bit_Chain *restrict dat,
                        const Dwg_Object *restrict obj,
                        Dwg_Entity_3DSOLID *restrict _obj);
static void dxf_fixup_string (Bit_Chain *restrict dat, char *restrict str);
static void dxf_CMC (Bit_Chain *restrict dat, const Dwg_Color *restrict color, const int dxf);

/*--------------------------------------------------------------------------------
 * MACROS
 */

#define ACTION dxf

#define FIELD(nam, type) VALUE (_obj->nam, type, 0)
#define FIELDG(nam, type, dxf) VALUE (_obj->nam, type, dxf)
#define FIELD_CAST(nam, type, cast, dxf) FIELDG (nam, cast, dxf)
#define FIELD_TRACE(nam, type)
#define SUB_FIELD(o, nam, type, dxf) FIELDG (o.nam, type, dxf)
#define SUB_FIELD_CAST(o, nam, type, cast, dxf) FIELDG (o.nam, cast, dxf)

#define VALUE_TV(value, dxf)                                                  \
  {                                                                           \
    GROUP (dxf);                                                              \
    dxf_fixup_string (dat, (char *)value);                                    \
  }
#define VALUE_TU(wstr, dxf)                                                   \
    {                                                                         \
      char *u8 = bit_convert_TU ((BITCODE_TU)wstr);                           \
      GROUP (dxf);                                                            \
      if (u8)                                                                 \
        fprintf (dat->fh, "%s\r\n", u8);                                      \
      else                                                                    \
        fprintf (dat->fh, "\r\n");                                            \
      free (u8);                                                              \
    }
#define VALUE_TFF(str, dxf)                                                   \
  {                                                                           \
    GROUP (dxf);                                                              \
    fprintf (dat->fh, "%s\r\n", str);                                         \
  }
#define VALUE_BINARY(value, size, dxf)                                        \
  {                                                                           \
    long len = (long)size;                                                    \
    do                                                                        \
      {                                                                       \
        short j;                                                              \
        long l = len > 127 ? 127 : len;                                       \
        GROUP (dxf);                                                          \
        if (value)                                                            \
          for (j = 0; j < l; j++)                                             \
            {                                                                 \
              fprintf (dat->fh, "%02X", value[j]);                            \
            }                                                                 \
        fprintf (dat->fh, "\r\n");                                            \
        len -= 127;                                                           \
      }                                                                       \
    while (len > 127);                                                        \
  }
#define FIELD_BINARY(name, size, dxf) if (dxf) VALUE_BINARY (_obj->name, size, dxf)

#define FIELD_VALUE(nam) _obj->nam
#define ANYCODE -1
// the hex code
#define VALUE_HANDLE(value, nam, handle_code, dxf)                            \
  if (dxf)                                                                    \
    {                                                                         \
      fprintf (dat->fh, "%3i\r\n%lX\r\n", dxf,                                 \
               value != NULL ? ((BITCODE_H)value)->absolute_ref : 0);         \
    }
// the name in the table, referenced by the handle
// names on: 6 7 8. which else? there are more styles: plot, ...
// rather skip unknown handles
#define FIELD_HANDLE(nam, handle_code, dxf)                                   \
  if (dxf != 0 && _obj->nam != NULL)                                          \
    {                                                                         \
      if (dxf == 6)                                                           \
        FIELD_HANDLE_NAME (nam, dxf, LTYPE)                                   \
      else if (dxf == 2)                                                      \
        FIELD_HANDLE_NAME (nam, dxf, BLOCK_HEADER)                            \
      else if (dxf == 3)                                                      \
        FIELD_HANDLE_NAME (nam, dxf, DIMSTYLE)                                \
      else if (dxf == 7)                                                      \
        FIELD_HANDLE_NAME (nam, dxf, STYLE)                                   \
      else if (dxf == 8)                                                      \
        FIELD_HANDLE_NAME (nam, dxf, LAYER)                                   \
      else if (dat->version >= R_13)                                          \
        fprintf (dat->fh, "%3i\r\n%lX\r\n", dxf,                              \
                 _obj->nam->obj ? _obj->nam->absolute_ref : 0);               \
    }
#define SUB_FIELD_HANDLE(o, nam, handle_code, dxf)                            \
  if (dxf != 0 && _obj->o.nam)                                                \
    {                                                                         \
      if (dxf == 6)                                                           \
        SUB_FIELD_HANDLE_NAME (o, nam, dxf, LTYPE)                            \
      else if (dxf == 3)                                                      \
        SUB_FIELD_HANDLE_NAME (o, nam, dxf, DIMSTYLE)                         \
      else if (dxf == 7)                                                      \
        SUB_FIELD_HANDLE_NAME (o, nam, dxf, STYLE)                            \
      else if (dxf == 8)                                                      \
        SUB_FIELD_HANDLE_NAME (o, nam, dxf, LAYER)                            \
      else if (dat->version >= R_13)                                          \
        fprintf (dat->fh, "%3i\r\n%lX\r\n", dxf,                              \
                 _obj->o.nam->obj ? _obj->o.nam->absolute_ref : 0);           \
    }
#define FIELD_HANDLE0(nam, handle_code, dxf)                                  \
  if (_obj->nam && _obj->nam->absolute_ref)                                   \
    {                                                                         \
      FIELD_HANDLE (nam, handle_code, dxf);                                   \
    }
#define SUB_FIELD_HANDLE0(o, nam, handle_code, dxf)                           \
  if (_obj->o.nam && _obj->o.nam->absolute_ref)                               \
    {                                                                         \
      SUB_FIELD_HANDLE (o, nam, handle_code, dxf);                            \
    }
#define HEADER_9(nam)                                                         \
  GROUP (9);                                                                  \
  fprintf (dat->fh, "$%s\r\n", #nam)
#define VALUE_H(value, dxf)                                                   \
  if (dxf)                                                                    \
  fprintf (dat->fh, "%3i\r\n%lX\r\n", dxf, value ? value->absolute_ref : 0)
#define HEADER_H(nam, dxf)                                                    \
  HEADER_9 (nam);                                                             \
  VALUE_H (dwg->header_vars.nam, dxf)

#define HEADER_VALUE(nam, type, dxf, value)                                   \
  if (dxf)                                                                    \
    {                                                                         \
      GROUP (9);                                                              \
      fprintf (dat->fh, "$" #nam "\r\n");                                     \
      VALUE (value, type, dxf);                                               \
    }
#define HEADER_VAR(nam, type, dxf)                                            \
  HEADER_VALUE (nam, type, dxf, dwg->header_vars.nam)
#define HEADER_VALUE_TV(nam, dxf, value)                                      \
  if (dxf)                                                                    \
    {                                                                         \
      GROUP (9);                                                              \
      fprintf (dat->fh, "$" #nam "\r\n");                                     \
      VALUE_TV (value, dxf);                                                  \
    }
#define HEADER_VALUE_TU(nam, dxf, value)                                      \
  if (dxf)                                                                    \
    {                                                                         \
      GROUP (9);                                                              \
      fprintf (dat->fh, "$" #nam "\r\n");                                     \
      VALUE_TU (value, dxf);                                                  \
    }

#define HEADER_3D(nam)                                                        \
  HEADER_9 (nam);                                                             \
  POINT_3D (nam, header_vars.nam, 10, 20, 30)
#define HEADER_2D(nam)                                                        \
  HEADER_9 (nam);                                                             \
  POINT_2D (nam, header_vars.nam, 10, 20)
#define HEADER_BLL(nam, dxf)                                                  \
  HEADER_9 (nam);                                                             \
  VALUE_BLL (dwg->header_vars.nam, dxf)

#define SECTION(section)                                                      \
  LOG_INFO ("\nSection " #section "\n")                                       \
  fprintf (dat->fh, "  0\r\nSECTION\r\n  2\r\n" #section "\r\n")
#define ENDSEC() fprintf (dat->fh, "  0\r\nENDSEC\r\n")
#define TABLE(table) fprintf (dat->fh, "  0\r\nTABLE\r\n  2\r\n" #table "\r\n")
#define ENDTAB() fprintf (dat->fh, "  0\r\nENDTAB\r\n")
#define RECORD(record) fprintf (dat->fh, "  0\r\n" #record "\r\n")
#define record(record) fprintf (dat->fh, "  0\r\n%s\r\n", record)
#define SUBCLASS(text)                                                        \
  if (dat->from_version >= R_13)                                              \
    {                                                                         \
      VALUE_TV (#text, 100);                                                  \
    }

#define GROUP(dxf) fprintf (dat->fh, "%3i\r\n", dxf)
/* avoid empty numbers, and fixup some bad %f GNU/BSD libc formatting */
#define VALUE(value, type, dxf)                                               \
  if (dxf)                                                                    \
    {                                                                         \
      const char *_fmt = dxf_format (dxf);                                    \
      assert (_fmt);                                                          \
      if (strEQc (_fmt, "%-16.14f"))                                          \
        {                                                                     \
          dxf_print_rd (dat, (double)(value), dxf);                           \
        }                                                                     \
      else                                                                    \
        {                                                                     \
          GROUP (dxf);                                                        \
          GCC46_DIAG_IGNORE (-Wformat-nonliteral)                             \
          snprintf (buf, 255, _fmt, value);                                   \
          GCC46_DIAG_RESTORE                                                  \
          /* not a string, empty num. must be zero */                         \
          if (strEQc (_fmt, "%s") && !*buf)                                   \
            fprintf (dat->fh, "0\r\n");                                       \
          else if (90 <= dxf && dxf < 100)                                    \
            {                                                                 \
              /* -Wpointer-to-int-cast */                                     \
              const int32_t _si = (int32_t) (intptr_t) (value);               \
              fprintf (dat->fh, "%6i\r\n", _si);                              \
            }                                                                 \
          else                                                                \
            fprintf (dat->fh, "%s\r\n", buf);                                 \
        }                                                                     \
    }

static void
dxf_print_rd (Bit_Chain *dat, BITCODE_RD value, int dxf)
{
  if (dxf)
    {
      char _buf[128];
      int k;
      fprintf (dat->fh, "%3i\r\n", dxf);
#ifdef IS_RELEASE
      if (bit_isnan (value))
        value = 0.0;
#endif
        snprintf (_buf, 127, "%-16.14f", value);
      k = strlen (_buf);
      if (strrchr (_buf, '.') && _buf[k - 1] == '0')
        {
          for (k--; k > 1 && _buf[k - 1] != '.' && _buf[k] == '0'; k--)
            _buf[k] = '\0';
        }
      fprintf (dat->fh, "%s\r\n", _buf);
    }
}
#define VALUE_BSd(value, dxf)                                                 \
  if (dxf)                                                                    \
    {                                                                         \
      GROUP (dxf);                                                            \
      fprintf (dat->fh, "%6i\r\n", value);                                    \
    }
#define VALUE_RD(value, dxf) dxf_print_rd (dat, value, dxf)
#define VALUE_B(value, dxf)                                                   \
  if (dxf)                                                                    \
    {                                                                         \
      GROUP (dxf);                                                            \
      if (value == 0)                                                         \
        fprintf (dat->fh, "     0\r\n");                                      \
      else                                                                    \
        fprintf (dat->fh, "     1\r\n");                                      \
    }

#define FIELD_HANDLE_NAME(nam, dxf, table)                                    \
  {                                                                           \
    Dwg_Object_Ref *ref = _obj->nam;                                          \
    Dwg_Object *o = ref ? ref->obj : NULL;                                    \
    if (o && strEQc (o->dxfname, #table))                                     \
      dxf_cvt_tablerecord (                                                   \
          dat, o, o ? o->tio.object->tio.table->name : (char *)"0", dxf);     \
    else                                                                      \
      {                                                                       \
        VALUE_TFF ("", dxf)                                                   \
      }                                                                       \
  }
#define SUB_FIELD_HANDLE_NAME(ob, nam, dxf, table)                            \
  {                                                                           \
    Dwg_Object_Ref *ref = _obj->ob.nam;                                       \
    Dwg_Object *o = ref ? ref->obj : NULL;                                    \
    if (o && strEQc (o->dxfname, #table))                                     \
      dxf_cvt_tablerecord (                                                   \
          dat, o, o ? o->tio.object->tio.table->name : (char *)"0", dxf);     \
    else                                                                      \
      {                                                                       \
        VALUE_TFF ("", dxf)                                                   \
      }                                                                       \
  }
#define HEADER_HANDLE_NAME(nam, dxf, table)                                   \
  HEADER_9 (nam);                                                             \
  FIELD_HANDLE_NAME (nam, dxf, table)

#define FIELD_DATAHANDLE(nam, code, dxf) FIELD_HANDLE (nam, code, dxf)

#define HEADER_RC(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, RC, dxf)
#define HEADER_RS(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, RS, dxf)
#define HEADER_RD(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELD_RD (nam, dxf)
#define HEADER_RL(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, RL, dxf)
#define HEADER_RLL(nam, dxf)                                                  \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, RLL, dxf)
#define HEADER_TV(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  VALUE_TV (_obj->nam, dxf)
#define HEADER_TU(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  VALUE_TU (_obj->nam, dxf)
#define HEADER_T(nam, dxf)                                                    \
  HEADER_9 (nam);                                                             \
  VALUE_T ((char *)_obj->nam, dxf)
#define HEADER_B(nam, dxf)                                                    \
  HEADER_9 (nam);                                                             \
  FIELD_B (nam, dxf)
#define HEADER_BS(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, BS, dxf)
#define HEADER_BSd(nam, dxf)   HEADER_BS(nam, dxf)
#define HEADER_BD(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELD_BD (nam, dxf)
#define HEADER_BL(nam, dxf)                                                   \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, BL, dxf)
#define HEADER_BLd(nam, dxf)                                                  \
  HEADER_9 (nam);                                                             \
  FIELDG (nam, BLd, dxf)

#define VALUE_BB(value, dxf) VALUE (value, RC, dxf)
#define VALUE_3B(value, dxf) VALUE (value, RC, dxf)
#define VALUE_BS(value, dxf) VALUE (value, RS, dxf)
#define VALUE_BL(value, dxf) VALUE (value, BL, dxf)
#define VALUE_BLL(value, dxf) VALUE (value, RLL, dxf)
#define VALUE_BD(value, dxf)                                                  \
  {                                                                           \
    if (dxf >= 50 && dxf < 55)                                                \
      {                                                                       \
        BITCODE_RD _f = rad2deg (value);                                      \
        VALUE_RD (_f, dxf);                                                   \
      }                                                                       \
    else                                                                      \
      {                                                                       \
        VALUE_RD (value, dxf);                                                \
      }                                                                       \
  }
#define VALUE_RC(value, dxf) VALUE (value, RC, dxf)
#define VALUE_RS(value, dxf) VALUE (value, RS, dxf)
#define VALUE_RL(value, dxf) VALUE (value, RL, dxf)
#define VALUE_RLL(value, dxf) VALUE (value, RLL, dxf)
#define VALUE_MC(value, dxf) VALUE (value, MC, dxf)
#define VALUE_MS(value, dxf) VALUE (value, MS, dxf)
#define VALUE_3BD(pt, dxf)                                                    \
  {                                                                           \
    VALUE_RD (pt.x, dxf);                                                     \
    VALUE_RD (pt.y, dxf + 10);                                                \
    VALUE_RD (pt.z, dxf + 20);                                                \
  }

#define FIELD_RD(nam, dxf) VALUE_RD (_obj->nam, dxf)
#define FIELD_B(nam, dxf) VALUE_B (_obj->nam, dxf)
#define FIELD_BB(nam, dxf) FIELDG (nam, BB, dxf)
#define FIELD_3B(nam, dxf) FIELDG (nam, 3B, dxf)
#define FIELD_BS(nam, dxf) FIELDG (nam, BS, dxf)
#define FIELD_BSd(nam, dxf) FIELDG (nam, BSd, dxf)
#define FIELD_BL(nam, dxf) FIELDG (nam, BL, dxf)
#define FIELD_BLL(nam, dxf) FIELDG (nam, BLL, dxf)
#define FIELD_BD(nam, dxf) VALUE_BD (_obj->nam, dxf)
#define FIELD_RC(nam, dxf) FIELDG (nam, RC, dxf)
#define FIELD_RS(nam, dxf) FIELDG (nam, RS, dxf)
#define FIELD_RL(nam, dxf) FIELDG (nam, RL, dxf)
#define FIELD_RLL(nam, dxf) FIELDG (nam, RLL, dxf)
#define FIELD_MC(nam, dxf) FIELDG (nam, MC, dxf)
#define FIELD_MS(nam, dxf) FIELDG (nam, MS, dxf)
#define FIELD_TF(nam, len, dxf) VALUE_TV (_obj->nam, dxf)
#define FIELD_TFF(nam, len, dxf) VALUE_TV (_obj->nam, dxf)
#define FIELD_TV(nam, dxf)                                                    \
  if (dxf)                                                                    \
    {                                                                         \
      VALUE_TV (_obj->nam, dxf);                                              \
    }
#define FIELD_TU(nam, dxf)                                                    \
  if (dxf)                                                                    \
    {                                                                         \
      VALUE_TU ((BITCODE_TU)_obj->nam, dxf);                                  \
    }
#define FIELD_T(nam, dxf)                                                     \
  {                                                                           \
    if (dat->from_version >= R_2007)                                          \
      {                                                                       \
        FIELD_TU (nam, dxf);                                                  \
      }                                                                       \
    else                                                                      \
      {                                                                       \
        FIELD_TV (nam, dxf);                                                  \
      }                                                                       \
  }
#define VALUE_T(value, dxf)                                                   \
  {                                                                           \
    if (dat->from_version >= R_2007)                                          \
      {                                                                       \
        VALUE_TU (value, dxf);                                                \
      }                                                                       \
    else                                                                      \
      {                                                                       \
        VALUE_TV (value, dxf);                                                \
      }                                                                       \
  }
#define FIELD_BT(nam, dxf) FIELDG (nam, BT, dxf);
#define FIELD_4BITS(nam, dxf) FIELDG (nam, 4BITS, dxf)
#define FIELD_BE(nam, dxf)                                                    \
  {                                                                           \
    if (!(_obj->nam.x == 0.0 && _obj->nam.y == 0.0 && _obj->nam.z == 1.0))    \
      FIELD_3RD (nam, dxf)                                                    \
  }
// skip if 0
#define FIELD_BD0(nam, dxf)                                                   \
  {                                                                           \
    if (_obj->nam != 0.0)                                                     \
      FIELD_BD (nam, dxf)                                                     \
  }
#define FIELD_BL0(nam, dxf)                                                   \
  {                                                                           \
    if (_obj->nam != 0)                                                       \
      FIELD_BL (nam, dxf)                                                     \
  }
#define FIELD_BS0(nam, dxf)                                                   \
  {                                                                           \
    if (_obj->nam != 0)                                                       \
      FIELD_BS (nam, dxf)                                                     \
  }
#define FIELD_RC0(nam, dxf)                                                   \
  {                                                                           \
    if (_obj->nam != 0)                                                       \
      FIELD_RC (nam, dxf)                                                     \
  }
#define FIELD_BT0(nam, dxf)                                                   \
  {                                                                           \
    if (_obj->nam != 0)                                                       \
      FIELD_BT (nam, dxf)                                                     \
  }
#define FIELD_T0(nam, dxf)                                                    \
  {                                                                           \
    if (_obj->nam)                                                            \
      {                                                                       \
        if (dat->from_version >= R_2007)                                      \
          {                                                                   \
            char *u8 = bit_convert_TU ((BITCODE_TU)_obj->nam);                \
            if (u8 && *u8)                                                    \
              {                                                               \
                GROUP (dxf);                                                  \
                fprintf (dat->fh, "%s\r\n", u8);                              \
              }                                                               \
            free (u8);                                                        \
          }                                                                   \
        else if (*_obj->nam)                                                  \
          {                                                                   \
            FIELD_TV (nam, dxf);                                              \
          }                                                                   \
      }                                                                       \
  }
#define SUB_FIELD_BL0(o, nam, dxf)                                            \
  {                                                                           \
    if (_obj->o.nam != 0)                                                     \
      SUB_FIELD_BL (o, nam, dxf)                                              \
  }

#define FIELD_DD(nam, _default, dxf) FIELD_BD (nam, dxf)
#define FIELD_2DD(nam, d1, d2, dxf)                                           \
  {                                                                           \
    FIELD_DD (nam.x, d1, dxf);                                                \
    FIELD_DD (nam.y, d2, dxf + 10);                                           \
  }
#define FIELD_3DD(nam, def, dxf)                                              \
  {                                                                           \
    FIELD_DD (nam.x, FIELD_VALUE (def.x), dxf);                               \
    FIELD_DD (nam.y, FIELD_VALUE (def.y), dxf + 10);                          \
    FIELD_DD (nam.z, FIELD_VALUE (def.z), dxf + 20);                          \
  }
#define FIELD_2RD(nam, dxf)                                                   \
  {                                                                           \
    FIELD_RD (nam.x, dxf);                                                    \
    FIELD_RD (nam.y, dxf + 10);                                               \
  }
#define FIELD_2BD(nam, dxf)                                                   \
  {                                                                           \
    FIELD_BD (nam.x, dxf);                                                    \
    FIELD_BD (nam.y, dxf + 10);                                               \
  }
#define FIELD_2BD_1(nam, dxf)                                                 \
  {                                                                           \
    FIELD_BD (nam.x, dxf);                                                    \
    FIELD_BD (nam.y, dxf + 1);                                                \
  }
#define FIELD_3RD(nam, dxf)                                                   \
  {                                                                           \
    FIELD_RD (nam.x, dxf);                                                    \
    FIELD_RD (nam.y, dxf + 10);                                               \
    FIELD_RD (nam.z, dxf + 20);                                               \
  }
#define FIELD_3BD(nam, dxf)                                                   \
  {                                                                           \
    FIELD_BD (nam.x, dxf);                                                    \
    FIELD_BD (nam.y, dxf + 10);                                               \
    FIELD_BD (nam.z, dxf + 20);                                               \
  }
#define FIELD_3BD_1(nam, dxf)                                                 \
  {                                                                           \
    FIELD_BD (nam.x, dxf);                                                    \
    FIELD_BD (nam.y, dxf + 1);                                                \
    FIELD_BD (nam.z, dxf + 2);                                                \
  }
#define FIELD_3DPOINT(nam, dxf) FIELD_3BD (nam, dxf)

#define FIELD_CMC(color, dxf) dxf_CMC (dat, &_obj->color, dxf)
#define SUB_FIELD_CMC(o, color, dxf) dxf_CMC (dat, &_obj->o.color, dxf)

#define HEADER_TIMEBLL(nam, dxf)                                              \
  HEADER_9 (nam);                                                             \
  FIELD_TIMEBLL (nam, dxf)
#define FIELD_TIMEBLL(nam, dxf)                                               \
  GROUP (dxf);                                                                \
  fprintf (dat->fh, FORMAT_RL "." FORMAT_RL "\r\n", _obj->nam.days,           \
           (BITCODE_RL)(_obj->nam.ms / 86400.0))
#define HEADER_CMC(nam, dxf)                                                  \
  HEADER_9 (nam);                                                             \
  VALUE_RS (dwg->header_vars.nam.index, dxf)

#define POINT_3D(nam, var, c1, c2, c3)                                        \
  {                                                                           \
    VALUE_RD (dwg->var.x, c1);                                                \
    VALUE_RD (dwg->var.y, c2);                                                \
    VALUE_RD (dwg->var.z, c3);                                                \
  }
#define POINT_2D(nam, var, c1, c2)                                            \
  {                                                                           \
    VALUE_RD (dwg->var.x, c1);                                                \
    VALUE_RD (dwg->var.y, c2);                                                \
  }

// FIELD_VECTOR_N(nam, type, size):
// reads data of the type indicated by 'type' 'size' times and stores
// it all in the vector called 'nam'.
#define FIELD_VECTOR_N(nam, type, size, dxf)                                  \
  if (dxf && _obj->nam)                                                       \
    {                                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)size; vcount++)                   \
        {                                                                     \
          VALUE_##type (_obj->nam[vcount], dxf);                              \
        }                                                                     \
    }
#define FIELD_VECTOR_N1(nam, type, size, dxf)                                 \
  if (dxf && _obj->nam)                                                       \
    {                                                                         \
      int _dxf = dxf;                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)size; _dxf++, vcount++)           \
        {                                                                     \
          VALUE_##type (_obj->nam[vcount], _dxf);                             \
        }                                                                     \
    }
#define FIELD_VECTOR_T(nam, type, size, dxf)                                  \
  if (dxf && _obj->nam)                                                       \
    {                                                                         \
      PRE (R_2007)                                                            \
      {                                                                       \
        for (vcount = 0; vcount < (BITCODE_BL)_obj->size; vcount++)           \
          VALUE_TV (_obj->nam[vcount], dxf);                                  \
      }                                                                       \
      else                                                                    \
      {                                                                       \
        for (vcount = 0; vcount < (BITCODE_BL)_obj->size; vcount++)           \
          VALUE_TU (_obj->nam[vcount], dxf);                                  \
      }                                                                       \
    }

#define FIELD_VECTOR(nam, type, size, dxf)                                    \
  FIELD_VECTOR_N (nam, type, _obj->size, dxf)

#define FIELD_2RD_VECTOR(nam, size, dxf)                                      \
  if (dxf && _obj->nam)                                                       \
    {                                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)_obj->size; vcount++)             \
        {                                                                     \
          FIELD_2RD (nam[vcount], dxf);                                       \
        }                                                                     \
    }

#define FIELD_2DD_VECTOR(nam, size, dxf)                                      \
  FIELD_2RD (nam[0], dxf);                                                    \
  if (dxf && _obj->nam)                                                       \
    {                                                                         \
      for (vcount = 1; vcount < (BITCODE_BL)_obj->size; vcount++)             \
        {                                                                     \
          FIELD_2DD (nam[vcount], FIELD_VALUE (nam[vcount - 1].x),            \
                     FIELD_VALUE (nam[vcount - 1].y), dxf);                   \
        }                                                                     \
    }

#define FIELD_3DPOINT_VECTOR(nam, size, dxf)                                  \
  if (dxf)                                                                    \
    {                                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)_obj->size; vcount++)             \
        {                                                                     \
          FIELD_3DPOINT (nam[vcount], dxf);                                   \
        }                                                                     \
    }

#define VALUE_HANDLE_N(hdlptr, nam, vcount, handle_code, dxf)                 \
  if (dxf && hdlptr && size)                                                  \
    {                                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)size; vcount++)                   \
        {                                                                     \
          VALUE_HANDLE (hdlptr[vcount], nam, handle_code, dxf);               \
        }                                                                     \
    }
#define FIELD_HANDLE_N(nam, size, handle_code, dxf)                           \
  VALUE_HANDLE (_obj->nam, nam, handle_code, dxf)
#define HANDLE_VECTOR_N(nam, size, code, dxf)                                 \
  if (dxf && _obj->nam && size)                                               \
    {                                                                         \
      for (vcount = 0; vcount < (BITCODE_BL)size; vcount++)                   \
        {                                                                     \
          FIELD_HANDLE (nam[vcount], code, dxf);                              \
        }                                                                     \
    }

#define HANDLE_VECTOR(nam, sizefield, code, dxf)                              \
  HANDLE_VECTOR_N (nam, FIELD_VALUE (sizefield), code, dxf)

#define FIELD_NUM_INSERTS(num_inserts, type, dxf)                             \
  FIELDG (num_inserts, type, dxf)

#define FIELD_XDATA(nam, size)                                                \
  dxf_write_xdata (dat, obj, _obj->nam, _obj->size)

#define _XDICOBJHANDLE(code)                                                  \
  if (dat->version >= R_13 && obj->tio.object->xdicobjhandle                  \
      && obj->tio.object->xdicobjhandle->absolute_ref)                        \
    {                                                                         \
      fprintf (dat->fh, "102\r\n{ACAD_XDICTIONARY\r\n");                      \
      VALUE_HANDLE (obj->tio.object->xdicobjhandle, xdicobjhandle, code,      \
                    360);                                                     \
      fprintf (dat->fh, "102\r\n}\r\n");                                      \
    }
#define _REACTORS(code)                                                       \
  if (dat->version >= R_13 && obj->tio.object->num_reactors                   \
      && obj->tio.object->reactors)                                           \
    {                                                                         \
      fprintf (dat->fh, "102\r\n{ACAD_REACTORS\r\n");                         \
      for (vcount = 0; vcount < obj->tio.object->num_reactors; vcount++)      \
        { /* soft ptr */                                                      \
          VALUE_HANDLE (obj->tio.object->reactors[vcount], reactors, code,    \
                        330);                                                 \
        }                                                                     \
      fprintf (dat->fh, "102\r\n}\r\n");                                      \
    }
#define ENT_REACTORS(code)                                                    \
  if (dat->version >= R_13 && _obj->num_reactors && _obj->reactors)           \
    {                                                                         \
      fprintf (dat->fh, "102\r\n{ACAD_REACTORS\r\n");                         \
      for (vcount = 0; vcount < _obj->num_reactors; vcount++)                 \
        {                                                                     \
          VALUE_HANDLE (_obj->reactors[vcount], reactors, code, 330);         \
        }                                                                     \
      fprintf (dat->fh, "102\r\n}\r\n");                                      \
    }
#define REACTORS(code)
#define XDICOBJHANDLE(code)
#define ENT_XDICOBJHANDLE(code)                                               \
  if (dat->version >= R_13 && obj->tio.entity->xdicobjhandle                  \
      && obj->tio.entity->xdicobjhandle->absolute_ref)                        \
    {                                                                         \
      fprintf (dat->fh, "102\r\n{ACAD_XDICTIONARY\r\n");                      \
      VALUE_HANDLE (obj->tio.entity->xdicobjhandle, xdicobjhandle, code,      \
                    360);                                                     \
      fprintf (dat->fh, "102\r\n}\r\n");                                      \
    }
#define BLOCK_NAME(nam, dxf) dxf_cvt_blockname (dat, _obj->nam, dxf)

#define COMMON_ENTITY_HANDLE_DATA
#define SECTION_STRING_STREAM
#define START_STRING_STREAM
#define END_STRING_STREAM
#define START_HANDLE_STREAM

#ifndef DEBUG_CLASSES
static int
dwg_dxf_TABLECONTENT (Bit_Chain *restrict dat, const Dwg_Object *restrict obj)
{
  (void)dat;
  (void)obj;
  return 0;
}
#else
static int dwg_dxf_TABLECONTENT (Bit_Chain *restrict dat,
                                 const Dwg_Object *restrict obj);
#endif

// The strcmp is being optimized away at compile-time!
// https://godbolt.org/g/AqkhwL
#define DWG_ENTITY(token)                                                     \
  static int dwg_dxf_##token##_private (                                      \
      Bit_Chain *dat, Bit_Chain *hdl_dat, Bit_Chain *str_dat,                 \
      const Dwg_Object *restrict obj);                                        \
  static int dwg_dxf_##token (Bit_Chain *restrict dat,                        \
                              const Dwg_Object *restrict obj)                 \
  {                                                                           \
    int error = 0;                                                            \
    Bit_Chain *hdl_dat = dat;                                                 \
    Bit_Chain *str_dat = dat;                                                 \
    if (obj->fixedtype != DWG_TYPE_##token)                                   \
      {                                                                       \
        LOG_ERROR ("Invalid type 0x%x, expected 0x%x %s", obj->fixedtype,     \
                   DWG_TYPE_##token, #token);                                 \
        return DWG_ERR_INVALIDTYPE;                                           \
      }                                                                       \
    if (strEQc (#token, "GEOPOSITIONMARKER"))                                 \
      RECORD (POSITIONMARKER);                                                \
    else if (dat->version < R_13 && strlen (#token) == 10                     \
             && strEQc (#token, "LWPOLYLINE"))                                \
      RECORD (POLYLINE);                                                      \
    else if (strlen (#token) > 10 && !memcmp (#token, "DIMENSION_", 10))      \
      RECORD (DIMENSION);                                                     \
    else if (strlen (#token) > 9 && !memcmp (#token, "POLYLINE_", 9))         \
      RECORD (POLYLINE);                                                      \
    else if (strlen (#token) > 7 && !memcmp (#token, "VERTEX_", 7))           \
      RECORD (VERTEX);                                                        \
    else if (dat->version >= R_2010 && strEQc (#token, "TABLE"))              \
      {                                                                       \
        RECORD (ACAD_TABLE);                                                  \
        return dwg_dxf_TABLECONTENT (dat, obj);                               \
      }                                                                       \
    else if (strlen (#token) > 3 && !memcmp (#token, "_3D", 3))               \
      record (obj->dxfname);                                                  \
    else if (obj->type >= 500 && obj->dxfname)                                \
      record (obj->dxfname);                                                  \
    else                                                                      \
      RECORD (token);                                                         \
    LOG_INFO ("Entity " #token ":\n")                                         \
    SINCE (R_11)                                                              \
    {                                                                         \
      LOG_TRACE ("Entity handle: " FORMAT_H "\n", ARGS_H (obj->handle));      \
      fprintf (dat->fh, "%3i\r\n%lX\r\n", 5, obj->handle.value);              \
    }                                                                         \
    SINCE (R_13) { error |= dxf_common_entity_handle_data (dat, obj); }       \
    error |= dwg_dxf_##token##_private (dat, hdl_dat, str_dat, obj);          \
    error |= dxf_write_eed (dat, obj->tio.object);                            \
    return error;                                                             \
  }                                                                           \
  static int dwg_dxf_##token##_private (                                      \
      Bit_Chain *dat, Bit_Chain *hdl_dat, Bit_Chain *str_dat,                 \
      const Dwg_Object *restrict obj) {                                       \
    int error = 0;                                                            \
    BITCODE_BL vcount, rcount3, rcount4;                                      \
    Dwg_Data *dwg = obj->parent;                                              \
    Dwg_Entity_##token *_obj = obj->tio.entity->tio.token;                    \
    Dwg_Object_Entity *_ent = obj->tio.entity;

#define DWG_ENTITY_END                                                        \
    return error;                                                             \
  }

#define DWG_OBJECT(token)                                                     \
  static int dwg_dxf_##token##_private (                                      \
      Bit_Chain *dat, Bit_Chain *hdl_dat, Bit_Chain *str_dat,                 \
      const Dwg_Object *restrict obj);                                        \
  static int dwg_dxf_##token (Bit_Chain *restrict dat,                        \
                              const Dwg_Object *restrict obj)                 \
  {                                                                           \
    int error = 0;                                                            \
    Bit_Chain *hdl_dat = dat, *str_dat = dat;                                 \
    LOG_INFO ("Object " #token ":\n")                                         \
    if (obj->fixedtype != DWG_TYPE_##token)                                   \
      {                                                                       \
        LOG_ERROR ("Invalid type 0x%x, expected 0x%x %s", obj->fixedtype,     \
                   DWG_TYPE_##token, #token);                                 \
        return DWG_ERR_INVALIDTYPE;                                           \
      }                                                                       \
    if (!dwg_obj_is_control (obj))                                            \
      {                                                                       \
        if (obj->fixedtype == DWG_TYPE_TABLE)                                 \
          ;                                                                   \
        else if (obj->type >= 500 && obj->dxfname)                            \
          fprintf (dat->fh, "  0\r\n%s\r\n", obj->dxfname);                   \
        else if (obj->type == DWG_TYPE_PLACEHOLDER)                           \
          RECORD (ACDBPLACEHOLDER);                                           \
        else if (obj->type != DWG_TYPE_BLOCK_HEADER)                          \
          RECORD (token);                                                     \
                                                                              \
        SINCE (R_13)                                                          \
        {                                                                     \
          BITCODE_BL vcount;                                                  \
          const int dxf = obj->type == DWG_TYPE_DIMSTYLE ? 105 : 5;           \
          fprintf (dat->fh, "%3i\r\n%lX\r\n", dxf, obj->handle.value);        \
          _XDICOBJHANDLE (3);                                                 \
          _REACTORS (4);                                                      \
        }                                                                     \
        SINCE (R_14)                                                          \
        {                                                                     \
          VALUE_HANDLE (obj->tio.object->ownerhandle, ownerhandle, 3, 330);   \
        }                                                                     \
      }                                                                       \
    if (DWG_LOGLEVEL >= DWG_LOGLEVEL_TRACE)                                   \
      {                                                                       \
        if (dwg_obj_is_table (obj))                                           \
          {                                                                   \
            char *_name = dwg_obj_table_get_name (obj, &error);               \
            LOG_TRACE ("Object handle: " FORMAT_H ", name: %s\n",             \
                       ARGS_H (obj->handle), _name);                          \
            SINCE (R_2007)                                                    \
              free (_name);                                                   \
          }                                                                   \
        else                                                                  \
          LOG_TRACE ("Object handle: " FORMAT_H "\n", ARGS_H (obj->handle))   \
      }                                                                       \
    error |= dwg_dxf_##token##_private (dat, hdl_dat, str_dat, obj);          \
    error |= dxf_write_eed (dat, obj->tio.object);                            \
    return error;                                                             \
  }                                                                           \
  static int dwg_dxf_##token##_private (                                      \
      Bit_Chain *dat, Bit_Chain *hdl_dat, Bit_Chain *str_dat,                 \
      const Dwg_Object *restrict obj) {                                       \
    int error = 0;                                                            \
    BITCODE_BL vcount, rcount3, rcount4;                                      \
    Dwg_Data *dwg = obj->parent;                                              \
    Dwg_Object_##token *_obj = obj->tio.object->tio.token;

// then 330, SUBCLASS

#define DWG_OBJECT_END                                                        \
    return error;                                                             \
  }

#undef DXF_3DSOLID
#define DXF_3DSOLID dxf_3dsolid (dat, obj, (Dwg_Entity_3DSOLID *)_obj);

// skip index 256 bylayer
// if the dxf code is 90-99 rather emit the rgb only
static void dxf_CMC (Bit_Chain *restrict dat, const Dwg_Color *restrict color, const int dxf)
{
  if (dat->version >= R_2004)
    {
      if (dxf >= 90)
        {
          VALUE_RL (color->rgb & 0x00ffffff, dxf);
          return;
        }
      VALUE_RS (color->index, dxf);
      if (color->method != 0xc2)
        return;
      VALUE_RL (color->rgb & 0x00ffffff, dxf + 420 - 62);
      if (color->flag & 2 && color->book_name)
        {
          char name[80];
          if (dat->from_version >= R_2007)
            {
              char *u8 = bit_convert_TU ((BITCODE_TU)color->book_name);
              strcpy (name, u8);
              free (u8);
              u8 = bit_convert_TU ((BITCODE_TU)color->name);
              if (u8)
                {
                  strcat (name, "$");
                  strcpy (name, u8);
                  free (u8);
                }
            }
          else
            {
              strcpy (name, color->book_name);
              strcat (name, "$");
              strcpy (name, color->name);
            }
          VALUE_TV (name, dxf + 430 - 62);
        }
      else if (color->flag & 1 && color->name)
        {
          VALUE_T (color->name, dxf + 430 - 62);
        }
      else if (color->flag)
        {
          VALUE_TFF ("UNNAMED", dxf + 430 - 62);
        }
    }
  else
    {
      VALUE_RS (color->index, dxf);
    }
}

static char *
cquote (char *restrict dest, const char *restrict src, const int len)
{
  char c;
  char *d = dest;
  const char* endp = dest + len;
  char *s = (char *)src;
  while ((c = *s++))
    {
      if (dest >= endp)
        {
          *dest = 0;
          return d;
        }
      if (c == '\n' && dest+1 < endp)
        {
          *dest++ = '^';
          *dest++ = 'J';
        }
      else if (c == '\r' && dest+1 < endp)
        {
          *dest++ = '^';
          *dest++ = 'M';
        }
      else
        *dest++ = c;
    }
  if (dest < endp)
    *dest = 0; // add final delim, skipped above
  return d;
}

/* \n => ^J */
static void
dxf_fixup_string (Bit_Chain *restrict dat, char *restrict str)
{
  if (str)
    {
      if (strchr (str, '\n') || strchr (str, '\r'))
        {
          const int len = 2 * strlen (str) + 1;
          char *_buf = (char *)alloca (len);
          fprintf (dat->fh, "%s\r\n", cquote (_buf, str, len));
          freea (_buf);
        }
      else
        fprintf (dat->fh, "%s\r\n", str);
    }
  else
    fprintf (dat->fh, "\r\n");
}

static int
dxf_write_eed (Bit_Chain *restrict dat, const Dwg_Object_Object *restrict obj)
{
  int error = 0;
  Dwg_Data *dwg = obj->dwg;
  for (BITCODE_BL i = 0; i < obj->num_eed; i++)
    {
      const Dwg_Eed* _obj = &obj->eed[i];
      if (_obj->size)
        {
          // name of APPID
          Dwg_Object *appid = dwg_resolve_handle (dwg, _obj->handle.value);
          if (appid && appid->fixedtype == DWG_TYPE_APPID)
            VALUE_T (appid->tio.object->tio.APPID->name, 1001)
          else
            VALUE_TFF ("ACAD", 1001);
        }
      if (_obj->data)
        {
          const Dwg_Eed_Data *data = _obj->data;
          const int dxf = data->code + 1000;
          switch (data->code)
            {
            case 0:
              if (dwg->header.from_version >= R_2007)
                VALUE_TU (data->u.eed_0_r2007.string, 1000)
              else
                VALUE_TV (data->u.eed_0.string, 1000)
              break;
            case 2:
              if (data->u.eed_2.byte)
                VALUE_TFF ("}", 1002)
              else
                VALUE_TFF ("{", 1002)
              break;
            case 3:
              GROUP (dxf);
              fprintf (dat->fh, "%9li\r\n", (long)data->u.eed_3.layer);
              //VALUE_RL (data->u.eed_3.layer, dxf);
              break;
            case 4: VALUE_BINARY (data->u.eed_4.data, data->u.eed_4.length, dxf); break;
            case 5: break; // not in DXF. VALUE_RLL (data->u.eed_5.entity, dxf); break; (hex handle?)
            case 10:
            case 11:
            case 12:
            case 13:
            case 14:
            case 15: VALUE_3BD (data->u.eed_10.point, dxf); break;
            case 40:
            case 41:
            case 42: VALUE_RD (data->u.eed_40.real, dxf); break;
            case 70: VALUE_RS (data->u.eed_70.rs, dxf); break;
            case 71: VALUE_RL (data->u.eed_71.rl, dxf); break;
            default: VALUE_RC (0, dxf);
            }
        }
    }
  return error;
}

GCC30_DIAG_IGNORE (-Wformat-nonliteral)
static int
dxf_write_xdata (Bit_Chain *restrict dat, const Dwg_Object *restrict obj,
                 Dwg_Resbuf *restrict rbuf, BITCODE_BL size)
{
  Dwg_Resbuf *tmp;
  int i;

  while (rbuf)
    {
      const char *fmt;
      short type;
      int dxftype = rbuf->type;

      fmt = dxf_format (rbuf->type);
      type = get_base_value_type (rbuf->type);
      dxftype = (rbuf->type > 1000 || obj->fixedtype == DWG_TYPE_XRECORD)
                    ? rbuf->type
                    : rbuf->type + 1000;
      if (obj->fixedtype == DWG_TYPE_XRECORD && dxftype >= 80 && dxftype < 90)
        {
          fmt = "(unknown code)";
          type = VT_INVALID;
        }

      if (strEQc (fmt, "(unknown code)"))
        {
          if (type == VT_INVALID)
            {
              LOG_WARN ("Invalid xdata code %d", dxftype);
            }
          else
            {
              LOG_WARN ("Unknown xdata code %d => %d", dxftype,
                        (BITCODE_BL)type);
            }
        }

      tmp = rbuf->nextrb;
      switch (type)
        {
        case VT_STRING:
          UNTIL (R_2007) { VALUE_TV (rbuf->value.str.u.data, dxftype); }
          LATER_VERSIONS { VALUE_TU (rbuf->value.str.u.wdata, dxftype); }
          break;
        case VT_REAL:
          VALUE_RD (rbuf->value.dbl, dxftype);
          break;
        case VT_BOOL:
        case VT_INT8:
          VALUE_RC (rbuf->value.i8, dxftype);
          break;
        case VT_INT16:
          VALUE_RS (rbuf->value.i16, dxftype);
          break;
        case VT_INT32:
          VALUE_RL (rbuf->value.i32, dxftype);
          break;
        case VT_POINT3D:
          VALUE_RD (rbuf->value.pt[0], dxftype);
          VALUE_RD (rbuf->value.pt[1], dxftype + 10);
          VALUE_RD (rbuf->value.pt[2], dxftype + 20);
          break;
        case VT_BINARY:
          VALUE_BINARY (rbuf->value.str.u.data, rbuf->value.str.size, dxftype);
          break;
        case VT_HANDLE:
        case VT_OBJECTID:
          fprintf (dat->fh, "%3i\r\n%lX\r\n", dxftype,
                   (unsigned long)*(uint64_t *)rbuf->value.hdl);
          break;
        case VT_INVALID:
          break; // skip
        default:
          fprintf (dat->fh, "%3i\r\n\r\n", dxftype);
          break;
        }
      rbuf = tmp;
    }
  return 0;
}

// r13+ converts STANDARD to Standard, BYLAYER to ByLayer, BYBLOCK to ByBlock
static void
dxf_cvt_tablerecord (Bit_Chain *restrict dat, const Dwg_Object *restrict obj,
                     char *restrict name, const int dxf)
{
  if (obj && obj->supertype == DWG_SUPERTYPE_OBJECT && name != NULL)
    {
      if (dat->version >= R_2007) // r2007+ unicode names
        {
          name = bit_convert_TU ((BITCODE_TU)name);
        }
      if (dat->from_version >= R_13 && dat->version < R_13)
        { // convert the other way round, from newer to older
          if (strEQc (name, "Standard"))
            fprintf (dat->fh, "%3i\r\nSTANDARD\r\n", dxf);
          else if (strEQc (name, "ByLayer"))
            fprintf (dat->fh, "%3i\r\nBYLAYER\r\n", dxf);
          else if (strEQc (name, "ByBlock"))
            fprintf (dat->fh, "%3i\r\nBYBLOCK\r\n", dxf);
          else if (strEQc (name, "*Active"))
            fprintf (dat->fh, "%3i\r\n*ACTIVE\r\n", dxf);
          else
            fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
        }
      else
        { // convert some standard names
          if (dat->version >= R_13 && strEQc (name, "STANDARD"))
            fprintf (dat->fh, "%3i\r\nStandard\r\n", dxf);
          else if (dat->version >= R_13 && strEQc (name, "BYLAYER"))
            fprintf (dat->fh, "%3i\r\nByLayer\r\n", dxf);
          else if (dat->version >= R_13 && strEQc (name, "BYBLOCK"))
            fprintf (dat->fh, "%3i\r\nByBlock\r\n", dxf);
          else if (dat->version >= R_13 && strEQc (name, "*ACTIVE"))
            fprintf (dat->fh, "%3i\r\n*Active\r\n", dxf);
          else
            fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
        }
      if (dat->version >= R_2007)
        free (name);
    }
  else
    {
      fprintf (dat->fh, "%3i\r\n\r\n", dxf);
    }
}

/* pre-r13 mspace and pspace blocks have different names:
   *Model_Space => $MODEL_SPACE
   *Paper_Space => $PAPER_SPACE
   TODO: Better use proper EXTNAMES
 */
static void
dxf_cvt_blockname (Bit_Chain *restrict dat, char *restrict name, const int dxf)
{
  if (!name)
    {
      fprintf (dat->fh, "%3i\r\n\r\n", dxf);
      return;
    }
  if (dat->from_version >= R_2007) // r2007+ unicode names
    {
      name = bit_convert_TU ((BITCODE_TU)name);
    }
  if (dat->version == dat->from_version) // no conversion
    {
      fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
    }
  else if (dat->version < R_13 && dat->from_version >= R_13) // to older
    {
      if (strlen (name) < 10)
        fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
      else if (strEQc (name, "*Model_Space"))
        fprintf (dat->fh, "%3i\r\n$MODEL_SPACE\r\n", dxf);
      else if (strEQc (name, "*Paper_Space"))
        fprintf (dat->fh, "%3i\r\n$PAPER_SPACE\r\n", dxf);
      else if (!memcmp (name, "*Paper_Space", sizeof ("*Paper_Space") - 1))
        fprintf (dat->fh, "%3i\r\n$PAPER_SPACE%s\r\n", dxf, &name[12]);
      else
        fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
    }
  else if (dat->version >= R_13 && dat->from_version < R_13) // to newer
    {
      if (strlen (name) < 10)
        fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
      else if (strEQc (name, "$MODEL_SPACE"))
        fprintf (dat->fh, "%3i\r\n*Model_Space\r\n", dxf);
      else if (strEQc (name, "$PAPER_SPACE"))
        fprintf (dat->fh, "%3i\r\n*Paper_Space\r\n", dxf);
      else if (!memcmp (name, "$PAPER_SPACE", sizeof ("$PAPER_SPACE") - 1))
        fprintf (dat->fh, "%3i\r\n*Paper_Space%s\r\n", dxf, &name[12]);
      else
        fprintf (dat->fh, "%3i\r\n%s\r\n", dxf, name);
    }
  if (dat->from_version >= R_2007)
    free (name);
}

#define START_OBJECT_HANDLE_STREAM

// Handle 5 written here first
#define COMMON_TABLE_CONTROL_FLAGS                                            \
  if (ctrl)                                                                   \
    {                                                                         \
      SINCE (R_13)                                                            \
      {                                                                       \
        fprintf (dat->fh, "%3i\r\n%lX\r\n", 5, ctrl->handle.value);           \
      }                                                                       \
      SINCE (R_14)                                                            \
      {                                                                       \
        VALUE_HANDLE (ctrl->tio.object->ownerhandle, ownerhandle, 3, 330);    \
      }                                                                       \
    }                                                                         \
  SINCE (R_13) { VALUE_TV ("AcDbSymbolTable", 100); }

// TODO add 340
#define COMMON_TABLE_FLAGS(acdbname)                                          \
  SINCE (R_13)                                                                \
  {                                                                           \
    VALUE_TV ("AcDbSymbolTableRecord", 100);                                  \
    VALUE_TV ("AcDb" #acdbname "TableRecord", 100);                           \
  }                                                                           \
  if (strEQc (#acdbname, "Block") && dat->version >= R_13)                    \
    {                                                                         \
      Dwg_Object *blk = dwg_ref_object (                                      \
          dwg, ((Dwg_Object_BLOCK_HEADER *)_obj)->block_entity);              \
      if (blk && blk->type == DWG_TYPE_BLOCK)                                 \
        {                                                                     \
          Dwg_Entity_BLOCK *_blk = blk->tio.entity->tio.BLOCK;                \
          if (dat->from_version >= R_2007)                                    \
            VALUE_TU (_blk->name, 2)                                          \
          else                                                                \
            VALUE_TV (_blk->name, 2)                                          \
        }                                                                     \
      else if (_obj->name)                                                    \
        {                                                                     \
          if (dat->from_version >= R_2007)                                    \
            VALUE_TU (_obj->name, 2)                                          \
          else                                                                \
            VALUE_TV (_obj->name, 2)                                          \
        }                                                                     \
      else                                                                    \
        VALUE_TV ("*", 2)                                                     \
    }                                                                         \
  else if (_obj->name)                                                        \
    dxf_cvt_tablerecord (dat, obj, _obj->name, 2);                            \
  else                                                                        \
    VALUE_TV ("*", 2)                                                         \
  FIELD_RC (flag, 70);

#define LAYER_TABLE_FLAGS(acdbname)                                           \
  SINCE (R_13)                                                                \
  {                                                                           \
    VALUE_TV ("AcDbSymbolTableRecord", 100);                                  \
    VALUE_TV ("AcDb" #acdbname "TableRecord", 100);                           \
  }                                                                           \
  if (_obj->name)                                                             \
    dxf_cvt_tablerecord (dat, obj, _obj->name, 2);                            \
  FIELD_RS (flag, 70)

#include "dwg.spec"

/* This was previously in encode, but since out_dxf needs it for r2013+ 3DSOLIDs
   and --disable-write is still an option, we need to move it here.
   A global acis_data_idx is needed, since encr_acis_data is split into blocks, but
   acis_data is a single stream, so we need to keep track of the current position.
 */
EXPORT char *
dwg_encrypt_SAT1 (BITCODE_BL blocksize, BITCODE_RC *restrict acis_data,
                  int *restrict acis_data_idx)
{
  char *encr_sat_data = (char*)calloc (blocksize, 1);
  int i = *acis_data_idx;
  int j;
  for (j = 0; j < (int)blocksize; j++)
    {
      if ((char)acis_data[j] <= 32)
        encr_sat_data[i++] = acis_data[j];
      else
        encr_sat_data[i++] = 159 - acis_data[j];
    }
  *acis_data_idx = i;
  return encr_sat_data;
}

static int
new_encr_sat_data_line (Dwg_Entity_3DSOLID *restrict _obj,Bit_Chain *dest,
                        unsigned int i)
{
  /*
  if (i + 1 >= _obj->num_blocks)
    {
      _obj->encr_sat_data = realloc (_obj->encr_sat_data, (i + 2) * sizeof (char*));
      _obj->block_size = realloc (_obj->block_size, (i + 2) * sizeof (BITCODE_BL));
      _obj->num_blocks = i + 1;
    }
  _obj->encr_sat_data[i] = calloc (dest->byte + 2, 1); // fresh, the dest buf is too large
  bit_write_TF (dest, (BITCODE_TF) "\n\000", 2); // ensure proper eol, dxf out relies on that.
  memcpy (_obj->encr_sat_data[i], dest->chain, dest->byte);
  _obj->block_size[i] = dest->byte - 1; // dont count the final 0
  bit_set_position (dest, 0);
  i++;
  */
  bit_write_TF (dest, (BITCODE_TF) "\n", 1); // ensure proper eol, dxf out relies on that
  return i;
}

// logical values are class-specific, and must be strings.
static const char*
SAT_boolean (const char *act_record, bool value)
{
  static int argc = 0;
  if (!strEQc (act_record, "varblendsplsur") &&
      !strEQc (act_record, "face") &&
      !strEQc (act_record, "bdy_geom"))
    argc = 0;

  if (strEQc (act_record, "sphere") ||
      strEQc (act_record, "plane") ||
      strEQc (act_record, "stripc") ||
      strEQc (act_record, "torus"))
    return !value ? "forward_v" : "reverse_v";
  else if (strEQc (act_record, "spline") ||
           strEQc (act_record, "edge") ||
           strEQc (act_record, "meshsurf") ||
           strEQc (act_record, "pcurve") ||
           strEQc (act_record, "intcurve"))
    return !value ? "forward" : "reversed";
  else if (strEQc (act_record, "surfcur") ||
           strEQc (act_record, "bldcur") ||
           strEQc (act_record, "parcur") ||
           strEQc (act_record, "projcur") ||
           strEQc (act_record, "perspsil"))
    return !value ? "surf2" : "surf1";
  else if (strEQc (act_record, "sweepsur"))
    return !value ? "normal" : "angled";
  else if (strEQc (act_record, "var_cross_section"))
    return value ? "radius" : "no_radius";
  else if (strEQc (act_record, "var_radius"))
    return value ? "uncalibrated" : "calibrated";
  else if (strEQc (act_record, "wire"))
    return value ? "in" : "out";
  else if (strEQc (act_record, "adv_var_blend"))
    return !value ? "sharp" : "smooth";
  else if (strEQc (act_record, "attrib_fhlhead"))
    return !value ? "invalid" : "valid";
  else if (strEQc (act_record, "attrib_fhlplist") ||
           strEQc (act_record, "attrib_fhl_slist"))
    return !value ? "invisible" : "visible";
  else if (strEQc (act_record, "bl_ent_ent") ||
           strEQc (act_record, "bl_inst"))
    return !value ? "unset" : "set";

  // TODO orthosur undocumented
  // now the few classes with mult. locical args
  else if (strEQc (act_record, "face"))
    {
      if (!argc)
        {
          argc++;
          return !value ? "forward" : "reversed";
        }
      else if (argc == 1)
        {
          argc++;
          return !value ? "single" : "double";
        }
      else
        {
          argc = 0;
          return !value ? "out" : "in";
        }
    }
  else if (strEQc (act_record, "varblendsplsur"))
    {
      if (!argc)
        {
          argc++;
          return !value ? "concave" : "convex";
        }
      else
        {
          argc = 0;
          return !value ? "rb_snapshot" : "rb_envelope";
        }
    }
  else if (strEQc (act_record, "attrib_var_blend"))
    {
      if (!argc)
        {
          argc++;
          return value ? "uncalibrated" : "calibrated";
        }
      else if (argc == 1)
        {
          argc++;
          return !value ? "one_radius" : "two_radii";
        }
      else
        {
          argc = 0;
          return !value ? "forward" : "reversed";
        }
    }
  else if (strEQc (act_record, "bdy_geom"))
    {
      if (!argc)
        {
          argc++;
          return value ? "non_cross" : "cross";
        }
      else
        {
          argc++;
          return !value ? "non_smooth" : "smooth";
        }
    }
  else
    return value ? "I" : "F";
}

/* Converts v2 SAB acis_data in-place to SAT v1 encr_sat_data[].
   Sets dxf_sab_converted to 1, denoting that encr_sat_data is NOT the
   encrypted acis_data anymore, rather the converted from SAB for DXF */
EXPORT int
dwg_convert_SAB_to_SAT1 (Dwg_Entity_3DSOLID *restrict _obj)
{
  Bit_Chain dest = { NULL, 0, 0, 0 };
  Bit_Chain src = { NULL, 0, 0, 0 };
  unsigned int i = 0, num_blocks = 2, size = 0;
  BITCODE_RC c;
  char *p = (char*)&_obj->acis_data[15];
  //char *end, *dest, *enddest;
  BITCODE_RL version, num_records, num_entities, has_history;
  //char *product_string, *acis_version, *date;
  BITCODE_RD num_mm_units, resabs, resnor;
  // Note that r2013+ has ASM data instead.
  // const char enddata[] = "\016\003End\016\002of\016\004ACIS\r\004data";
  // const char enddata1[] = "\016\003End\016\002of\016\003ASM\r\004data";
  int first = 1;
  int forward = 0;
  char act_record [80];

  if (_obj->num_blocks)
    num_blocks = _obj->num_blocks;
  if (!_obj->block_size)
    _obj->block_size = calloc (num_blocks, sizeof (BITCODE_BL));
  if (!_obj->encr_sat_data)
    _obj->encr_sat_data = calloc (num_blocks, sizeof (char *));

  _obj->_dxf_sab_converted = 1;
  if (!_obj->sab_size)
    _obj->sab_size = _obj->block_size[0];
  //end = &p[_obj->sab_size];

  if (!memBEGINc ((char*)_obj->acis_data, "ACIS BinaryFile"))
    {
      LOG_ERROR ("acis_data is not a SAB 2 'ACIS BinaryFile'");
      return 1;
    }
  //dest = &_obj->encr_sat_data[0][0];
  //enddest = &dest[size];
  bit_chain_alloc (&dest);
  src.chain = &_obj->acis_data[15];
  src.size = _obj->sab_size - 15;

// header only
#define SAB_RD(key)                                                     \
  c = bit_read_RC (&src); /* 6 */                                       \
  LOG_HANDLE (#key " [%d] ", c)                                         \
  key = bit_read_RD (&src);                                             \
  dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%g ", key);     \
  LOG_TRACE ("%g ", key)
// record variant
#define SAB_RD1()                                                       \
  {                                                                     \
    double f = bit_read_RD (&src);                                      \
    if (dest.byte + 16 >= dest.size)                                     \
      bit_chain_alloc (&dest);                                          \
    dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%g ", f);     \
    LOG_TRACE ("%g ", f);                                               \
  }
// key is ignored here. header only
#define SAB_T(key)                                                      \
  {                                                                     \
    int len;                                                            \
    c = bit_read_RC (&src);                                             \
    LOG_HANDLE (#key " [%d] ", c)                                       \
    len = bit_read_RC (&src);                                           \
    dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%d ", len);   \
    LOG_TRACE ("%d %.*s ", len, len, &src.chain[src.byte]);             \
    bit_write_TF (&dest, &src.chain[src.byte], len);                    \
    bit_write_TF (&dest, (BITCODE_TF) " ", 1);                          \
    src.byte += len;                                                    \
  }
#define SAB_TF(x)                                                       \
  bit_write_TF (&dest, (BITCODE_TF) x, sizeof (x) - 1);                 \
  bit_write_TF (&dest, (BITCODE_TF) " ", 1);                            \
  LOG_TRACE ("%s ", x)
#define SAB_TV(x)                                                       \
  bit_write_TF (&dest, (BITCODE_TF) x, strlen (x));                     \
  bit_write_TF (&dest, (BITCODE_TF) " ", 1);                            \
  LOG_TRACE ("%s ", x)

  // create the two vectors encr_sat_data[] and block_size[] on the fly from the SAB
  // http://paulbourke.net/dataformats/sat/sat.pdf
  /* ACIS BinaryFile [64 81 6x0[ [2 7x0] 
     "\a\020Autodesk AutoCAD\a\024ASM 223.0.1.1930 OSX\a\030Mon Jun 18 11:09:32 2018\006"
     6x0 16 63 "\006\215\355\265\240\367ư>" "\006\273\275\327\331\337|\333= "\r\tasmheader" \f\377\377\377\377\004\377\377\377\377\a\f223.0.1.1930\021 \r\004body \f\377\377\377\377\004\377\377\377\377\f\377\377\377\377\f\002"
   */
  version = bit_read_RL (&src);
  num_records = bit_read_RL (&src);  // if 0 until end marker. total
  num_entities = bit_read_RL (&src); // named top in the ACIS docs
  has_history = bit_read_RL (&src);  // named as flags in the ACIS docs
  dest.byte += sprintf ((char*)dest.chain, "%d %d %d %d ", version, num_records,
                        num_entities, has_history);
  LOG_TRACE ("%d %d %d %d \n", version, num_records, num_entities, has_history);
  i = new_encr_sat_data_line (_obj, &dest, i);

  SAB_T (product_string)
  SAB_T (acis_version)
  SAB_T (date)
  i = new_encr_sat_data_line (_obj, &dest, i);
  LOG_TRACE ("\n");

  SAB_RD (num_mm_units);
  SAB_RD (resabs);
  SAB_RD (resnor);
  i = new_encr_sat_data_line (_obj, &dest, i);
  LOG_TRACE ("\n");

  c = bit_read_RC (&src); // type tag
  while (src.byte < src.size)
    {
      LOG_HANDLE ("[%d] ", c)
      switch (c)
        {
        // check size, realloc encr_sat_data[i], set dest
        case 17:   //  # end of record
          first = 1;
          forward = 0;
          if (dest.byte + 2 >= dest.size)
            bit_chain_alloc (&dest);
          dest.byte += sprintf ((char*)&dest.chain[dest.byte], "#\n");
          LOG_TRACE ("#\n")
          //i = new_encr_sat_data_line (_obj, &dest, i);
          break;
        case 13:   // ident
          first = 1;
          _obj->encr_sat_data[i] = (char*)dest.chain;
          // fallthru
        case 7:  // char len
        case 14: // subident
          {
            int len = bit_read_RC (&src);
            if (dest.byte + len + 4 >= dest.size)
              bit_chain_alloc (&dest);
            if (c == 7 && i < 3)
              {
                dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%d ", len);
                LOG_TRACE ("%d ", len);
              }
            LOG_TRACE ("%.*s%s", len, &src.chain[src.byte], c == 14 ? "-" : " ")
            bit_write_TF (&dest, &src.chain[src.byte], len);
            if (c == 13 && len < 80)
              {
                memcpy (act_record, &src.chain[src.byte], len);
                act_record[len] = '\0'; // to find identifier-specific true/false strings
              }
            // TODO Begin-of-ACIS-History-Data => new line
            // TODO End-of-ACIS-History-Section => new line
            //if (has_history && c == 13 && len = 4 && memBEGINc (&src.chain[src.byte], "Data"))
            //  i = new_encr_sat_data_line (_obj, &dest, i);
            src.byte += len;
            if (c == 14)
              bit_write_TF (&dest, (BITCODE_TF)"-", 1);
            else
              bit_write_TF (&dest, (BITCODE_TF)" ", 1);
            break;
          }
        case 8:  // short len
          {
            int len = bit_read_RS (&src);
            LOG_TRACE ("%.*s%s", len, &src.chain[src.byte], " ")
            bit_write_TF (&dest, &src.chain[src.byte], len);
            src.byte += len;
            bit_write_TF (&dest, (BITCODE_TF)" ", 1);
            break;
          }
        case 9:  // long len
          {
            int len = bit_read_RL (&src);
            LOG_TRACE ("%.*s%s", len, &src.chain[src.byte], " ")
            bit_write_TF (&dest, &src.chain[src.byte], len);
            src.byte += len;
            bit_write_TF (&dest, (BITCODE_TF)" ", 1);
            break;
          }
        case 10: // 0 byte TRUE
          {
            const char *s = SAT_boolean (act_record, 1);
            SAB_TV (s);
          }
          break;
        case 11: // 0 byte FALSE
          {
            const char *s = SAT_boolean (act_record, 0);
            SAB_TV (s);
          }
          break;
        case 15: // 0 byte subtype start
          SAB_TF ("{");
          break;
        case 16: // 1 byte subtype end
          SAB_TF ("}");
          LOG_HANDLE ("[%c] ", src.chain[src.byte]);
          //src.byte++;
          break;
        case 2: // char constant
          {
            int8_t l = (int8_t)bit_read_RC (&src);
            if (dest.byte + 4 >= dest.size)
              bit_chain_alloc (&dest);
            dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%" PRId8 " ", l);
            LOG_TRACE ("%" PRId8 " ", l)
          }
          break;
        case 3: // short constant
          {
            int16_t l = (int16_t)bit_read_RS (&src);
            if (dest.byte + 8 >= dest.size)
              bit_chain_alloc (&dest);
            dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%" PRId16 " ", l);
            LOG_TRACE ("%" PRId16 " ", l)
          }
          break;
        case 4: // long constant
          {
            BITCODE_RLd l = (BITCODE_RLd)bit_read_RL (&src);
            if (dest.byte + 8 >= dest.size)
              bit_chain_alloc (&dest);
            dest.byte += sprintf ((char*)&dest.chain[dest.byte], "$%" PRId32 " ", l);
            LOG_TRACE ("$%" PRId32 " ", l)
          }
          break;
        case 5: // float constant
          {
            float f = bit_read_RL (&src);
            if (dest.byte + 16 >= dest.size)
              bit_chain_alloc (&dest);
            dest.byte += sprintf ((char*)&dest.chain[dest.byte], "%g ", (double)f);
            LOG_TRACE ("%g ", (double)f)
          }
          break;
        case 12: // 4 byte pointer index
          {
            BITCODE_RLd l = (BITCODE_RLd)bit_read_RL (&src);
            if (dest.byte + 8 >= dest.size)
              bit_chain_alloc (&dest);
            dest.byte += sprintf ((char*)&dest.chain[dest.byte], "$%" PRId32 " ", l);
            LOG_TRACE ("$%" PRId32 " ", l)
          }
          break;
        case 19: // 3x double-float position
        case 20: // 3x double-float vector
          SAB_RD1();
          SAB_RD1();
          // fallthru
        case 6:  // 8 byte double-float, e.g. in the 2nd header line
          SAB_RD1();
          break;
        //case 21:  // enum <identifier>
        //  break;
        default:
          LOG_ERROR ("Unknown SAB tag %d", c);
        }
      c = bit_read_RC (&src);
    }

  //if (c != 17) // last line didn't end with #, but End-of-ACIS-data or End-of-ASM-data
  //  i = new_encr_sat_data_line (_obj, &dest, i);
  num_blocks = _obj->num_blocks = 1;
  bit_write_TF (&dest, (BITCODE_TF)"\n", 1);
  _obj->encr_sat_data[i] = calloc (dest.byte, 1); // shrink it
  memcpy (_obj->encr_sat_data[i], dest.chain, dest.byte);
  _obj->block_size[i] = dest.byte;
  bit_chain_free (&dest);
  LOG_TRACE ("\n");
  _obj->acis_empty = 0;
  _obj->version = 1; // conversion complete

  if (i + 2 >= num_blocks)
    _obj->block_size = realloc (_obj->block_size, (i + 2) * sizeof (BITCODE_BL));
  _obj->block_size[i + 1] = 0;
  return 0;
}

static int
dxf_3dsolid (Bit_Chain *restrict dat, const Dwg_Object *restrict obj,
             Dwg_Entity_3DSOLID *restrict _obj)
{
  BITCODE_BL i;
  int error = 0;

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_B (acis_empty, 290);
  if (!FIELD_VALUE (acis_empty))
    {
      FIELD_B (unknown, 0);
      if (FIELD_VALUE (version) == 2)
        {
          BITCODE_RC *acis_data;
          LOG_TRACE ("Convert SAB ACIS BinaryFile v2 to encrypted SAT v1\n");
          error |= dwg_convert_SAB_to_SAT1 (_obj);

          for (i = 0; i < FIELD_VALUE (num_blocks); i++)
            {
              int idx = 0; // here idx is just local, always starting at 0. ignored
              char *ptr
                  = dwg_encrypt_SAT1 (_obj->block_size[i],
                                  (BITCODE_RC *)_obj->encr_sat_data[i], &idx);

              free (_obj->encr_sat_data[i]);
              _obj->encr_sat_data[i] = ptr;
            }
          _obj->version = 1; // conversion complete
        }
      FIELD_BS (version, 70); // always 1
      for (i = 0; i < FIELD_VALUE (num_blocks); i++)
        {
          char *s = FIELD_VALUE (encr_sat_data[i]);
          // FIXME
          //int len = _obj->_dxf_sab_converted ? FIELD_VALUE (block_size[i]) : strlen (s);
          int len = FIELD_VALUE (block_size[i]);
          // DXF 1 + 3 if >255
          while (len > 0)
            {
              char *n = strchr (s, '\n');
              int l = len > 255 ? 255 : len;
              if (n && (n - s < len))
                l = n - s;
              if (l)
                {
                  if (l < 255)
                    GROUP (1);
                  else
                    GROUP (3);
                  if (s[l - 1] == '\r')
                    fprintf (dat->fh, "%.*s\n", l, s);
                  else
                    fprintf (dat->fh, "%.*s\r\n", l, s);
                  l++;
                  len -= l;
                  s += l;
                }
              else
                {
                  len--;
                  s++;
                }
            }
        }
    }
  // the rest is done in COMMON_3DSOLID in the spec.
  return error;
}

/* returns 0 on success
 */
static int
dwg_dxf_variable_type (const Dwg_Data *restrict dwg, Bit_Chain *restrict dat,
                       Dwg_Object *restrict obj)
{
  int i;
  Dwg_Class *klass;
  int is_entity;

  i = obj->type - 500;
  if (i < 0 || i >= dwg->num_classes)
    return DWG_ERR_INVALIDTYPE;

  klass = &dwg->dwg_class[i];
  if (!klass || !klass->dxfname)
    return DWG_ERR_INTERNALERROR;
  is_entity = dwg_class_is_entity (klass);

  // if (!is_entity)
  //  fprintf(dat->fh, "  0\r\n%s\r\n", dxfname);

  // clang-format off
  #include "classes.inc"
  // clang-format on

  return DWG_ERR_UNHANDLEDCLASS;
}

/* process unsorted vertices until SEQEND */
#define decl_dxf_process_VERTEX(token)                                        \
  static int dxf_process_VERTEX_##token (Bit_Chain *restrict dat,             \
                                         const Dwg_Object *restrict obj,      \
                                         int *restrict i)                     \
  {                                                                           \
    int error = 0;                                                            \
    Dwg_Entity_POLYLINE_##token *_obj                                         \
        = obj->tio.entity->tio.POLYLINE_##token;                              \
                                                                              \
    VERSIONS (R_13, R_2000)                                                   \
    {                                                                         \
      Dwg_Object *last_vertex = _obj->last_vertex->obj;                       \
      Dwg_Object *o = _obj->first_vertex ? _obj->first_vertex->obj : NULL;    \
      if (!o)                                                                 \
        return DWG_ERR_INVALIDHANDLE;                                         \
      if (o->fixedtype == DWG_TYPE_VERTEX_##token)                            \
        error |= dwg_dxf_VERTEX_##token (dat, o);                             \
      *i = *i + 1;                                                            \
      do                                                                      \
        {                                                                     \
          o = dwg_next_object (o);                                            \
          if (!o)                                                             \
            return DWG_ERR_INVALIDHANDLE;                                     \
          if (strEQc (#token, "PFACE")                                        \
              && o->fixedtype == DWG_TYPE_VERTEX_PFACE_FACE)                  \
            {                                                                 \
              error |= dwg_dxf_VERTEX_PFACE_FACE (dat, o);                    \
            }                                                                 \
          else if (o->fixedtype == DWG_TYPE_VERTEX_##token)                   \
            {                                                                 \
              error |= dwg_dxf_VERTEX_##token (dat, o);                       \
            }                                                                 \
          *i = *i + 1;                                                        \
        }                                                                     \
      while (o->fixedtype != DWG_TYPE_SEQEND && o != last_vertex);            \
      o = _obj->seqend ? _obj->seqend->obj : NULL;                            \
      if (o && o->fixedtype == DWG_TYPE_SEQEND)                               \
        error |= dwg_dxf_SEQEND (dat, o);                                     \
      *i = *i + 1;                                                            \
    }                                                                         \
    SINCE (R_2004)                                                            \
    {                                                                         \
      Dwg_Object *o;                                                          \
      for (BITCODE_BL j = 0; j < _obj->num_owned; j++)                        \
        {                                                                     \
          o = _obj->vertex && _obj->vertex[j] ? _obj->vertex[j]->obj : NULL;  \
          if (strEQc (#token, "PFACE") && o                                   \
              && o->fixedtype == DWG_TYPE_VERTEX_PFACE_FACE)                  \
            {                                                                 \
              error |= dwg_dxf_VERTEX_PFACE_FACE (dat, o);                    \
            }                                                                 \
          else if (o && o->fixedtype == DWG_TYPE_VERTEX_##token)              \
            {                                                                 \
              error |= dwg_dxf_VERTEX_##token (dat, o);                       \
            }                                                                 \
        }                                                                     \
      o = _obj->seqend ? _obj->seqend->obj : NULL;                            \
      if (o && o->fixedtype == DWG_TYPE_SEQEND)                               \
        error |= dwg_dxf_SEQEND (dat, o);                                     \
      *i = *i + _obj->num_owned + 1;                                          \
    }                                                                         \
    return error;                                                             \
  }

// clang-format off
decl_dxf_process_VERTEX (2D)
decl_dxf_process_VERTEX (3D)
decl_dxf_process_VERTEX (MESH)
decl_dxf_process_VERTEX (PFACE)
// clang-format on

/* process if seqend before attribs */
#define decl_dxf_process_INSERT(token)                                        \
  static int dxf_process_##token (Bit_Chain *restrict dat,                    \
                                  const Dwg_Object *restrict obj,             \
                                  int *restrict i)                            \
  {                                                                           \
    int error = 0;                                                            \
    Dwg_Entity_##token *_obj = obj->tio.entity->tio.token;                    \
                                                                              \
    if (!_obj->has_attribs)                                                   \
        return 0;                                                             \
    VERSIONS (R_13, R_2000)                                                   \
    {                                                                         \
      Dwg_Object *last_attrib                                                 \
          = _obj->last_attrib ? _obj->last_attrib->obj : NULL;                \
      Dwg_Object *o = _obj->first_attrib ? _obj->first_attrib->obj : NULL;    \
      if (!o || !last_attrib)                                                 \
        return DWG_ERR_INVALIDHANDLE;                                         \
      if (o->fixedtype == DWG_TYPE_ATTRIB)                                    \
        error |= dwg_dxf_ATTRIB (dat, o);                                     \
      *i = *i + 1;                                                            \
      do                                                                      \
        {                                                                     \
          o = dwg_next_object (o);                                            \
          if (!o)                                                             \
            return DWG_ERR_INVALIDHANDLE;                                     \
          if (o->fixedtype == DWG_TYPE_ATTRIB)                                \
            error |= dwg_dxf_ATTRIB (dat, o);                                 \
          *i = *i + 1;                                                        \
        }                                                                     \
      while (o->fixedtype == DWG_TYPE_ATTRIB && o != last_attrib);            \
      o = _obj->seqend ? _obj->seqend->obj : NULL;                            \
      if (o && o->fixedtype == DWG_TYPE_SEQEND)                               \
        error |= dwg_dxf_SEQEND (dat, o);                                     \
      *i = *i + 1;                                                            \
    }                                                                         \
    SINCE (R_2004)                                                            \
    {                                                                         \
      Dwg_Object *o;                                                          \
      for (BITCODE_BL j = 0; j < _obj->num_owned; j++)                        \
        {                                                                     \
          o = _obj->attrib_handles && _obj->attrib_handles[j]                 \
                  ? _obj->attrib_handles[j]->obj                              \
                  : NULL;                                                     \
          if (o && o->fixedtype == DWG_TYPE_ATTRIB)                           \
            error |= dwg_dxf_ATTRIB (dat, o);                                 \
        }                                                                     \
      o = _obj->seqend ? _obj->seqend->obj : NULL;                            \
      if (o && o->fixedtype == DWG_TYPE_SEQEND)                               \
        error |= dwg_dxf_SEQEND (dat, o);                                     \
      *i = *i + _obj->num_owned + 1;                                          \
    }                                                                         \
    return error;                                                             \
  }

// clang-format off
decl_dxf_process_INSERT (INSERT)
decl_dxf_process_INSERT (MINSERT)
// clang-format on

static int dwg_dxf_object (Bit_Chain *restrict dat,
                           const Dwg_Object *restrict obj,
                           int *restrict i)
{
  int error = 0;
  int minimal;

  if (!obj || !obj->parent)
    return DWG_ERR_INTERNALERROR;
  minimal = obj->parent->opts & DWG_OPTS_MINIMAL;

  switch (obj->type)
    {
    case DWG_TYPE_TEXT:
      return dwg_dxf_TEXT (dat, obj);
    case DWG_TYPE_ATTDEF:
      return dwg_dxf_ATTDEF (dat, obj);
    case DWG_TYPE_BLOCK:
      return dwg_dxf_BLOCK (dat, obj);
    case DWG_TYPE_ENDBLK:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return 0; // dwg_dxf_ENDBLK(dat, obj);
    case DWG_TYPE_SEQEND:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return 0; // dwg_dxf_SEQEND(dat, obj);

    case DWG_TYPE_INSERT:
      error = dwg_dxf_INSERT (dat, obj);
      return error | dxf_process_INSERT (dat, obj, i);
    case DWG_TYPE_MINSERT:
      error = dwg_dxf_MINSERT (dat, obj);
      return error | dxf_process_MINSERT (dat, obj, i);
    case DWG_TYPE_POLYLINE_2D:
      error = dwg_dxf_POLYLINE_2D (dat, obj);
      return error | dxf_process_VERTEX_2D (dat, obj, i);
    case DWG_TYPE_POLYLINE_3D:
      error = dwg_dxf_POLYLINE_3D (dat, obj);
      return error | dxf_process_VERTEX_3D (dat, obj, i);
    case DWG_TYPE_POLYLINE_PFACE:
      error = dwg_dxf_POLYLINE_PFACE (dat, obj);
      return error | dxf_process_VERTEX_PFACE (dat, obj, i);
    case DWG_TYPE_POLYLINE_MESH:
      error = dwg_dxf_POLYLINE_MESH (dat, obj);
      return error | dxf_process_VERTEX_MESH (dat, obj, i);

    case DWG_TYPE_ATTRIB:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_ATTRIB (dat, obj);
    case DWG_TYPE_VERTEX_2D:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_VERTEX_2D (dat, obj);
    case DWG_TYPE_VERTEX_3D:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_VERTEX_3D (dat, obj);
    case DWG_TYPE_VERTEX_MESH:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_VERTEX_MESH (dat, obj);
    case DWG_TYPE_VERTEX_PFACE:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_VERTEX_PFACE (dat, obj);
    case DWG_TYPE_VERTEX_PFACE_FACE:
      LOG_WARN ("stale %s subentity", obj->dxfname);
      return dwg_dxf_VERTEX_PFACE_FACE (dat, obj);

    case DWG_TYPE_ARC:
      return dwg_dxf_ARC (dat, obj);
    case DWG_TYPE_CIRCLE:
      return dwg_dxf_CIRCLE (dat, obj);
    case DWG_TYPE_LINE:
      return dwg_dxf_LINE (dat, obj);
    case DWG_TYPE_DIMENSION_ORDINATE:
      return dwg_dxf_DIMENSION_ORDINATE (dat, obj);
    case DWG_TYPE_DIMENSION_LINEAR:
      return dwg_dxf_DIMENSION_LINEAR (dat, obj);
    case DWG_TYPE_DIMENSION_ALIGNED:
      return dwg_dxf_DIMENSION_ALIGNED (dat, obj);
    case DWG_TYPE_DIMENSION_ANG3PT:
      return dwg_dxf_DIMENSION_ANG3PT (dat, obj);
    case DWG_TYPE_DIMENSION_ANG2LN:
      return dwg_dxf_DIMENSION_ANG2LN (dat, obj);
    case DWG_TYPE_DIMENSION_RADIUS:
      return dwg_dxf_DIMENSION_RADIUS (dat, obj);
    case DWG_TYPE_DIMENSION_DIAMETER:
      return dwg_dxf_DIMENSION_DIAMETER (dat, obj);
    case DWG_TYPE_POINT:
      return dwg_dxf_POINT (dat, obj);
    case DWG_TYPE__3DFACE:
      return dwg_dxf__3DFACE (dat, obj);
    case DWG_TYPE_SOLID:
      return dwg_dxf_SOLID (dat, obj);
    case DWG_TYPE_TRACE:
      return dwg_dxf_TRACE (dat, obj);
    case DWG_TYPE_SHAPE:
      return dwg_dxf_SHAPE (dat, obj);
    case DWG_TYPE_VIEWPORT:
      return minimal ? 0 : dwg_dxf_VIEWPORT (dat, obj);
    case DWG_TYPE_ELLIPSE:
      return dwg_dxf_ELLIPSE (dat, obj);
    case DWG_TYPE_SPLINE:
      return dwg_dxf_SPLINE (dat, obj);
    case DWG_TYPE_REGION:
      return dwg_dxf_REGION (dat, obj);
    case DWG_TYPE__3DSOLID:
      return dwg_dxf__3DSOLID (dat, obj);
    case DWG_TYPE_BODY:
      return dwg_dxf_BODY (dat, obj);
    case DWG_TYPE_RAY:
      return dwg_dxf_RAY (dat, obj);
    case DWG_TYPE_XLINE:
      return dwg_dxf_XLINE (dat, obj);
    case DWG_TYPE_DICTIONARY:
      return minimal ? 0 : dwg_dxf_DICTIONARY (dat, obj);
    case DWG_TYPE_MTEXT:
      return dwg_dxf_MTEXT (dat, obj);
    case DWG_TYPE_LEADER:
      return dwg_dxf_LEADER (dat, obj);
    case DWG_TYPE_TOLERANCE:
      return dwg_dxf_TOLERANCE (dat, obj);
    case DWG_TYPE_MLINE:
#if 1 || defined DEBUG_CLASSES
      // TODO: looks good, but acad import crashes
      return dwg_dxf_MLINE (dat, obj);
#else
      LOG_WARN ("Unhandled Entity MLINE in out_dxf %u/%lX", obj->index,
                obj->handle.value)
      if (0) dwg_dxf_MLINE (dat, obj);
      return DWG_ERR_UNHANDLEDCLASS;
#endif
    case DWG_TYPE_BLOCK_CONTROL:
    case DWG_TYPE_BLOCK_HEADER:
    case DWG_TYPE_LAYER_CONTROL:
    case DWG_TYPE_LAYER:
    case DWG_TYPE_STYLE_CONTROL:
    case DWG_TYPE_STYLE:
    case DWG_TYPE_LTYPE_CONTROL:
    case DWG_TYPE_LTYPE:
    case DWG_TYPE_VIEW_CONTROL:
    case DWG_TYPE_VIEW:
    case DWG_TYPE_UCS_CONTROL:
    case DWG_TYPE_UCS:
    case DWG_TYPE_VPORT_CONTROL:
    case DWG_TYPE_VPORT:
    case DWG_TYPE_APPID_CONTROL:
    case DWG_TYPE_APPID:
    case DWG_TYPE_DIMSTYLE_CONTROL:
    case DWG_TYPE_DIMSTYLE:
    case DWG_TYPE_VPORT_ENTITY_CONTROL:
    case DWG_TYPE_VPORT_ENTITY_HEADER:
      break;
    case DWG_TYPE_GROUP:
      return dwg_dxf_GROUP (dat, obj);
    case DWG_TYPE_MLINESTYLE:
      return minimal ? 0 : dwg_dxf_MLINESTYLE (dat, obj);
    case DWG_TYPE_OLE2FRAME:
      return minimal ? 0 : dwg_dxf_OLE2FRAME (dat, obj);
    case DWG_TYPE_DUMMY:
      return 0;
    case DWG_TYPE_LONG_TRANSACTION:
      return minimal ? 0 : dwg_dxf_LONG_TRANSACTION (dat, obj);
    case DWG_TYPE_LWPOLYLINE:
      return dwg_dxf_LWPOLYLINE (dat, obj);
    case DWG_TYPE_HATCH:
      return dwg_dxf_HATCH (dat, obj);
    case DWG_TYPE_XRECORD:
      return minimal ? 0 : dwg_dxf_XRECORD (dat, obj);
    case DWG_TYPE_PLACEHOLDER:
      return minimal ? 0 : dwg_dxf_PLACEHOLDER (dat, obj);
    case DWG_TYPE_PROXY_ENTITY:
      // TODO dwg_dxf_PROXY_ENTITY(dat, obj);
      return DWG_ERR_UNHANDLEDCLASS;
    case DWG_TYPE_OLEFRAME:
      return minimal ? 0 : dwg_dxf_OLEFRAME (dat, obj);
    case DWG_TYPE_VBA_PROJECT:
      if (!minimal)
        {
          LOG_ERROR ("Unhandled Object VBA_PROJECT");
          // dwg_dxf_VBA_PROJECT(dat, obj);
          return DWG_ERR_UNHANDLEDCLASS;
        }
      return 0;
    case DWG_TYPE_LAYOUT:
      return minimal ? 0 : dwg_dxf_LAYOUT (dat, obj);
    default:
      if (obj->type == obj->parent->layout_type)
        {
          return minimal ? 0 : dwg_dxf_LAYOUT (dat, obj);
        }
      /* > 500 */
      else if ((error
                = dwg_dxf_variable_type (obj->parent, dat, (Dwg_Object *)obj))
               & DWG_ERR_UNHANDLEDCLASS)
        {
          Dwg_Data *dwg = obj->parent;
          int j = obj->type - 500;
          Dwg_Class *klass = NULL;

          if (j >= 0 && j < (int)dwg->num_classes)
            klass = &dwg->dwg_class[j];
          if (!klass)
            {
              LOG_WARN ("Unknown object, skipping eed/reactors/xdic");
              return DWG_ERR_INVALIDTYPE;
            }
          return error;
        }
    }
  return DWG_ERR_UNHANDLEDCLASS;
}

static int
dxf_common_entity_handle_data (Bit_Chain *restrict dat,
                               const Dwg_Object *restrict obj)
{
  const Dwg_Data *dwg = obj->parent;
  const Dwg_Object_Entity *ent = obj->tio.entity;
  const Dwg_Object_Entity *_obj = ent;
  int error = 0;
  BITCODE_BL vcount = 0;

  // clang-format off
  #include "common_entity_handle_data.spec"
  #include "common_entity_data.spec"
  // clang-format on

  return error;
}

RETURNS_NONNULL
const char *
dxf_format (int code)
{
  if (0 <= code && code < 5)
    return "%s";
  if (code == 5 || code == -5)
    return "%lX";
  if (5 < code && code < 10)
    return "%s";
  if (code < 60)
    return "%-16.14f";
  if (code < 80)
    return "%6i";
  if (80 <= code && code <= 99) // BL int32 lgtm [cpp/constant-comparison]
    return "%9li";
  if (code == 100)
    return "%s";
  if (code == 102)
    return "%s";
  if (code == 105)
    return "%lX";
  if (110 <= code && code <= 149)
    return "%-16.14f";
  if (160 <= code && code <= 169)
    return "%12li";
  if (170 <= code && code <= 179)
    return "%6i";
  if (210 <= code && code <= 239)
    return "%-16.14f";
  if (270 <= code && code <= 289)
    return "%6i";
  if (290 <= code && code <= 299)
    return "%6i"; // boolean
  if (300 <= code && code <= 319)
    return "%s";
  if (320 <= code && code <= 369)
    return "%lX";
  if (370 <= code && code <= 389)
    return "%6i";
  if (390 <= code && code <= 399)
    return "%lX";
  if (400 <= code && code <= 409)
    return "%6i";
  if (410 <= code && code <= 419)
    return "%s";
  if (420 <= code && code <= 429)
    return "%9li"; // int32_t
  if (430 <= code && code <= 439)
    return "%s";
  if (440 <= code && code <= 449)
    return "%9li"; // int32_t
  if (450 <= code && code <= 459)
    return "%12li"; // long
  if (460 <= code && code <= 469)
    return "%-16.14f";
  if (470 <= code && code <= 479)
    return "%s";
  if (480 <= code && code <= 481)
    return "%lX";
  if (code == 999)
    return "%s";
  if (1000 <= code && code <= 1009)
    return "%s";
  if (1010 <= code && code <= 1059)
    return "%-16.14f";
  if (1060 <= code && code <= 1070)
    return "%6i";
  if (code == 1071)
    return "%9li"; // int32_t
  if (code == 1002) // RC
    return "%6i";
  if (code == 1003) // RL layer
    return "%9li";
  if (code > 1000)
    return dxf_format (code - 1000);

  return "(unknown code)";
}

/* num => string. for the reverse see in_dxf.c:dxf_fixup_header()
   TODO: maybe use a table.
 */
RETURNS_NONNULL
const char *
dxf_codepage (int code, Dwg_Data *dwg)
{
  if (code == 30 || code == 0)
    return "ANSI_1252"; // WesternEurope Windows
  else if (code == 1)
    return "US_ASCII";
  else if (code == 2)
    return "ISO-8859-1"; // WesternEurope Latin-1
  else if (code == 3)
    return "ISO-8859-2"; // MiddleEurope Latin-2
  else if (code == 4)
    return "ISO-8859-3"; // SouthEurope Latin-3
  else if (code == 5)
    return "ISO-8859-4"; // NorthEurope Latin-4
  else if (code == 6)
    return "ISO-8859-5"; // Cyrillic
  else if (code == 7)
    return "ISO-8859-6"; // Arabic
  else if (code == 8)
    return "ISO-8859-7"; // Greek
  else if (code == 9)
    return "ISO-8859-8"; // Hebrew
  else if (code == 10)
    return "ISO-8859-9"; // Turkish Latin-5
  else if (code == 11)
    return "CP437";     // DOS-US, DOS Latin US
  else if (code == 12)
    return "CP850";     // WesternEurope DOS
  else if (code == 13)
    return "CP852";     // CentralEurope DOS
  else if (code == 14)
    return "CP855";     // Cyrillic DOS
  else if (code == 15)
    return "CP857";     // Turkish DOS
  else if (code == 16)
    return "CP860";     // Portuguese DOS
  else if (code == 17)
    return "CP861";     // Icelandic DOS
  else if (code == 18)
    return "CP863";     // French DOS
  else if (code == 19)
    return "CP864";     // Arabic DOS
  else if (code == 20)
    return "CP865";     // Nordic DOS
  else if (code == 21)
    return "CP869";     // Greek DOS
  else if (code == 22)
    return "CP932";     // Japanese Shift JIS DOS
  else if (code == 23)
    return "MACINTOSH";
  else if (code == 24)
    return "BIG5";      // Taiwan DOS
  else if (code == 25)
    return "CP949";     // Korean UnifiedHangulCode DOS
  else if (code == 26)
    return "JOHAB";     // Korean cp1361 DOS
  else if (code == 27)
    return "CP866";     // Russian DOS
  else if (code == 28)
    return "ANSI_1250"; // CentralEurope Windows
  else if (code == 29)
    return "ANSI_1251"; // Cyrillic Windows
  else if (code == 31)
    return "GB2312";    // SimplifiedChinese
  else if (code == 32)
    return "ANSI_1253"; // Greek Windows
  else if (code == 33)
    return "ANSI_1254"; // Turkish Windows
  else if (code == 34)
    return "ANSI_1255"; // Hebrew Windows
  else if (code == 35)
    return "ANSI_1256"; // Arabic Windows
  else if (code == 36)
    return "ANSI_1257"; // Baltic Windows
  else if (code == 37)
    return "ANSI_874"; // Thai Windows
  else if (code == 38)
    return "ANSI_932"; // Japanese Windows
  else if (code == 39)
    return "ANSI_936"; // gbk UnifiedChinese Windows
  else if (code == 40)
    return "ANSI_949"; // Korean Windows
  else if (code == 41)
    return "ANSI_950"; // TradChinese Windows
  else if (code == 42)
    return "ANSI_1361"; // Korean JOHAB Windows
  else if (code == 43)
    return "ANSI_1200"; // UTF-16 LE Microsoft
  else if (code == 44)
    return "ANSI_1258"; // Vietnamese Windows
  else if (dwg->header.version >= R_2007)
    return "UTF-8"; // dwg internally: UCS-16, for DXF: UTF-8
  else
    return "";
}

// see
// https://www.autodesk.com/techpubs/autocad/acad2000/dxf/header_section_group_codes_dxf_02.htm
GCC30_DIAG_IGNORE (-Wformat-nonliteral)
AFL_GCC_TOOBIG
static int
dxf_header_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  Dwg_Header_Variables *_obj = &dwg->header_vars;
  Dwg_Object *obj = NULL;
  double ms;
  const int minimal = dwg->opts & DWG_OPTS_MINIMAL;
  const char *codepage = dxf_codepage (dwg->header.codepage, dwg);

  if (!*codepage)
    {
      LOG_WARN ("Unknown codepage %d, assuming ANSI_1252",
                dwg->header.codepage);
    }

  // clang-format off
  #include "header_variables_dxf.spec"
  // clang-format on

  return 0;
}
AFL_GCC_POP

// only called since r2000. but not really needed, unless referenced
static int
dxf_classes_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  BITCODE_BS j;

  SECTION (CLASSES);
  LOG_TRACE ("num_classes: %u\n", dwg->num_classes);
  for (j = 0; j < dwg->num_classes; j++)
    {
      const char *dxfname = dwg->dwg_class[j].dxfname;
      if (!dxfname)
        continue;
      // some classes are now builtin
      if (dat->version >= R_2004
          && (strEQc (dxfname, "ACDBPLACEHOLDER")
              || strEQc (dxfname, "LAYOUT")))
        continue;
      RECORD (CLASS);
      VALUE_TV (dxfname, 1);
      VALUE_T (dwg->dwg_class[j].cppname, 2);
      VALUE_T (dwg->dwg_class[j].appname, 3);
      VALUE_RS (dwg->dwg_class[j].proxyflag, 90);
      SINCE (R_2004) { VALUE_RC (dwg->dwg_class[j].num_instances, 91); }
      VALUE_RC (dwg->dwg_class[j].is_zombie, 280);
      // Is-an-entity. 1f2 for entities, 1f3 for objects
      VALUE_RC (dwg->dwg_class[j].item_class_id == 0x1F2 ? 1 : 0, 281);
    }
  ENDSEC ();
  return 0;
}

static int
dxf_tables_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  int error = 0;
  unsigned int i;

  SECTION (TABLES);
  {
    Dwg_Object_VPORT_CONTROL *_ctrl = &dwg->vport_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_VPORT_CONTROL)
      {
        TABLE (VPORT);
        // add handle 5 here at first
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_VPORT_CONTROL (dat, ctrl);
        // TODO how far back can DXF read 1000?
        if (dat->version != dat->from_version && dat->from_version >= R_2000)
          {
            /* if saved from newer version, eg. AC1032: */
            VALUE_TV ("ACAD", 1001);
            VALUE_TV ("DbSaveVer", 1000);
            VALUE_RS ((dat->from_version * 3) + 15,
                      1071); // so that 69 is R_2018
          }
        for (i = 0; i < dwg->vport_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_VPORT)
              {
                // reordered in the DXF: 2,70,10,11,12,13,14,15,16,...
                // special-cased in the spec
                error |= dwg_dxf_VPORT (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_LTYPE_CONTROL *_ctrl = &dwg->ltype_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_LTYPE_CONTROL)
      {
        Dwg_Object *obj;
        TABLE (LTYPE);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_LTYPE_CONTROL (dat, ctrl);
        // first the 2 builtin ltypes: ByBlock, ByLayer
        if ((obj = dwg_ref_object (dwg, dwg->header_vars.LTYPE_BYBLOCK))
            && obj->type == DWG_TYPE_LTYPE)
          {
            error |= dwg_dxf_LTYPE (dat, obj);
          }
        if ((obj = dwg_ref_object (dwg, dwg->header_vars.LTYPE_BYLAYER))
            && obj->type == DWG_TYPE_LTYPE)
          {
            error |= dwg_dxf_LTYPE (dat, obj);
          }
        // here LTYPE_CONTINUOUS is already included
        for (i = 0; i < dwg->ltype_control.num_entries; i++)
          {
            obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_LTYPE)
              {
                error |= dwg_dxf_LTYPE (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_LAYER_CONTROL *_ctrl = &dwg->layer_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_LAYER_CONTROL)
      {
        TABLE (LAYER);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_LAYER_CONTROL (dat, ctrl);
        for (i = 0; i < dwg->layer_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_LAYER)
              error |= dwg_dxf_LAYER (dat, obj);
            // else if (obj && obj->type == DWG_TYPE_DICTIONARY)
            //  error |= dwg_dxf_DICTIONARY(dat, obj);
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_STYLE_CONTROL *_ctrl = &dwg->style_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_STYLE_CONTROL)
      {
        TABLE (STYLE);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_STYLE_CONTROL (dat, ctrl);
        for (i = 0; i < dwg->style_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_STYLE)
              {
                error |= dwg_dxf_STYLE (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_VIEW_CONTROL *_ctrl = &dwg->view_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_VIEW_CONTROL)
      {
        TABLE (VIEW);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_VIEW_CONTROL (dat, ctrl);
        for (i = 0; i < dwg->view_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            // FIXME implement the other two
            if (obj && obj->type == DWG_TYPE_VIEW)
              error |= dwg_dxf_VIEW (dat, obj);
            /*
              else if (obj && obj->fixedtype == DWG_TYPE_SECTIONVIEWSTYLE)
              error |= dwg_dxf_SECTIONVIEWSTYLE(dat, obj);
              if (obj && obj->fixedtype == DWG_TYPE_DETAILVIEWSTYLE) {
              error |= dwg_dxf_DETAILVIEWSTYLE(dat, obj);
            */
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_UCS_CONTROL *_ctrl = &dwg->ucs_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_UCS_CONTROL)
      {
        TABLE (UCS);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_UCS_CONTROL (dat, ctrl);
        for (i = 0; i < dwg->ucs_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_UCS)
              {
                error |= dwg_dxf_UCS (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  SINCE (R_13)
  {
    Dwg_Object_APPID_CONTROL *_ctrl = &dwg->appid_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_APPID_CONTROL)
      {
        TABLE (APPID);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_APPID_CONTROL (dat, ctrl);
        for (i = 0; i < dwg->appid_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_APPID)
              {
                error |= dwg_dxf_APPID (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  {
    Dwg_Object_DIMSTYLE_CONTROL *_ctrl = &dwg->dimstyle_control;
    Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
    if (ctrl && ctrl->fixedtype == DWG_TYPE_DIMSTYLE_CONTROL)
      {
        TABLE (DIMSTYLE);
        COMMON_TABLE_CONTROL_FLAGS;
        error |= dwg_dxf_DIMSTYLE_CONTROL (dat, ctrl);
        // ignoring morehandles
        for (i = 0; i < dwg->dimstyle_control.num_entries; i++)
          {
            Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
            if (obj && obj->type == DWG_TYPE_DIMSTYLE)
              {
                error |= dwg_dxf_DIMSTYLE (dat, obj);
              }
          }
        ENDTAB ();
      }
  }
  // fool the warnings. this table is nowhere to be found in the wild. maybe
  // pre-R_11
  if (0 && dwg->vport_entity_control.num_entries)
    {
      Dwg_Object_VPORT_ENTITY_CONTROL *_ctrl = &dwg->vport_entity_control;
      Dwg_Object *ctrl = &dwg->object[_ctrl->objid];
      if (ctrl && ctrl->fixedtype == DWG_TYPE_VPORT_ENTITY_CONTROL)
        {
          TABLE (VPORT_ENTITY);
          COMMON_TABLE_CONTROL_FLAGS;
          error |= dwg_dxf_VPORT_ENTITY_CONTROL (dat, ctrl);
          for (i = 0; i < dwg->vport_entity_control.num_entries; i++)
            {
              Dwg_Object *obj = dwg_ref_object (dwg, _ctrl->entries[i]);
              if (obj && obj->type == DWG_TYPE_VPORT_ENTITY_HEADER)
                {
                  error |= dwg_dxf_VPORT_ENTITY_HEADER (dat, obj);
                }
            }
          // avoid unused warnings
          dwg_dxf_PROXY_ENTITY (dat, &dwg->object[0]);
          ENDTAB ();
        }
    }
  SINCE (R_13)
  {
    Dwg_Object *ctrl;
    Dwg_Object_BLOCK_CONTROL *_ctrl = dwg_block_control (dwg);
    // Dwg_Object *obj = dwg_ref_object(dwg, _ctrl->model_space);
    // Dwg_Object *mspace = NULL, *pspace = NULL;
    if (!_ctrl)
      return DWG_ERR_INVALIDDWG;
    ctrl = &dwg->object[_ctrl->objid];
    if (!ctrl || ctrl->fixedtype != DWG_TYPE_BLOCK_CONTROL)
      return DWG_ERR_INVALIDDWG;

    TABLE (BLOCK_RECORD);
    COMMON_TABLE_CONTROL_FLAGS;
    error |= dwg_dxf_BLOCK_CONTROL (dat, ctrl);

#if 1
    for (i = 0; i < dwg->num_objects; i++)
      {
        Dwg_Object *hdr = &dwg->object[i];
        if (hdr && hdr->supertype == DWG_SUPERTYPE_OBJECT
            && hdr->type == DWG_TYPE_BLOCK_HEADER)
          {
            // not necessarily in the same order as DXF, but exhaustive
            RECORD (BLOCK_RECORD);
            error |= dwg_dxf_BLOCK_HEADER (dat, hdr);
          }
      }
#else
    if (obj && obj->type == DWG_TYPE_BLOCK_HEADER)
      {
        mspace = obj;
        RECORD (BLOCK_RECORD);
        error |= dwg_dxf_BLOCK_HEADER (dat, obj);
      }
    if (_ctrl->paper_space)
      {
        obj = dwg_ref_object (dwg, _ctrl->paper_space);
        if (obj && obj->type == DWG_TYPE_BLOCK_HEADER)
          {
            pspace = obj;
            RECORD (BLOCK_RECORD);
            error |= dwg_dxf_BLOCK_HEADER (dat, obj);
          }
      }
    for (i = 0; i < dwg->block_control.num_entries; i++)
      {
        obj = dwg_ref_object (dwg, dwg->block_control.block_headers[i]);
        if (obj && obj->type == DWG_TYPE_BLOCK_HEADER && obj != mspace
            && obj != pspace)
          {
            RECORD (BLOCK_RECORD);
            error |= dwg_dxf_BLOCK_HEADER (dat, obj);
          }
      }
#endif

    ENDTAB ();
  }
  ENDSEC ();
  return 0;
}

static void
dxf_ENDBLK_empty (Bit_Chain *restrict dat, const Dwg_Object *restrict hdr)
{
  // temp. only. not registered in dwg->object[]
  Dwg_Object *obj = (Dwg_Object *)calloc (1, sizeof (Dwg_Object));
  Dwg_Data *dwg = hdr->parent;
  // Dwg_Entity_ENDBLK *_obj;
  obj->parent = dwg;
  obj->index = dwg->num_objects;
  dwg_setup_ENDBLK (obj);
  obj->tio.entity->ownerhandle = (BITCODE_H)calloc (1, sizeof (Dwg_Object_Ref));
  obj->tio.entity->ownerhandle->obj = (Dwg_Object *)hdr;
  obj->tio.entity->ownerhandle->handleref = hdr->handle;
  obj->tio.entity->ownerhandle->absolute_ref = hdr->handle.value;
  //_obj = obj->tio.entity->tio.ENDBLK;
  dwg_dxf_ENDBLK (dat, obj);
  free (obj->tio.entity->tio.ENDBLK);
  free (obj->tio.entity->ownerhandle);
  free (obj->tio.entity);
  free (obj);
}

// a BLOCK_HEADER
static int
dxf_block_write (Bit_Chain *restrict dat, const Dwg_Object *restrict hdr,
                 const Dwg_Object *restrict mspace, int *restrict i)
{
  int error = 0;
  const Dwg_Object_BLOCK_HEADER *restrict _hdr
      = hdr->tio.object->tio.BLOCK_HEADER;
  Dwg_Object *restrict obj = get_first_owned_block (hdr); // BLOCK
  Dwg_Object *restrict endblk = NULL;
  unsigned long int mspace_ref = mspace->handle.value;

  if (obj)
    error |= dwg_dxf_object (dat, obj, i);
  else
    {
      SINCE (R_2004)
        {
          // first_owned_block
          SINCE (R_2007)
            {
              char *s = bit_convert_TU ((BITCODE_TU)_hdr->name);
              LOG_ERROR ("BLOCK_HEADER %s block_entity[0] missing", s);
              free (s);
            }
          else
            LOG_ERROR ("BLOCK_HEADER %s block_entity[0] missing", _hdr->name);
          return DWG_ERR_INVALIDDWG;
        }
      else
        LOG_WARN ("BLOCK_HEADER %s block_entity[0] missing", _hdr->name);
    }
  // Skip all *Model_Space entities, esp. new ones: UNDERLAY, MULTILEADER, ...
  // They are all under ENTITIES later. But WIPEOUT is here...
  // Note: the objects may vary (e.g. example_2000), but the index not
  if ((hdr == mspace) || (hdr->index == mspace->index))
    obj = NULL;
  else
    obj = get_first_owned_entity (hdr); // first_entity or entities[0]
  while (obj)
    {
      if (obj->supertype == DWG_SUPERTYPE_ENTITY
          && obj->fixedtype != DWG_TYPE_ENDBLK
          && (obj->tio.entity->entmode != 2 ||
              (obj->tio.entity->ownerhandle != NULL
               && obj->tio.entity->ownerhandle->absolute_ref != mspace_ref)))
        error |= dwg_dxf_object (dat, obj, i);
      obj = get_next_owned_block_entity (hdr, obj); // until last_entity
    }
  endblk = get_last_owned_block (hdr);
  if (endblk)
    {
      error |= dwg_dxf_ENDBLK (dat, endblk);
      LOG_INFO ("\n")
    }
  else
    {
      LOG_WARN ("Empty ENDBLK for \"%s\" %lX", _hdr->name,
                hdr ? hdr->handle.value : 0);
      dxf_ENDBLK_empty (dat, hdr);
      LOG_INFO ("\n")
    }
  return error;
}

static int
dxf_blocks_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  int error = 0;
  int i;
  Dwg_Object *mspace = dwg_model_space_object (dwg);

  if (!mspace)
    return DWG_ERR_UNHANDLEDCLASS;

  // If there's no *Model_Space block skip this BLOCKS section.
  // Or try handle 1F with r2000+, 17 with r14
  // obj = get_first_owned_block(hdr);
  // if (!obj)
  //  obj = dwg_resolve_handle(dwg, dwg->header.version >= R_2000 ? 0x1f :
  //  0x17);
  // if (!obj)
  //  return 1;

  SECTION (BLOCKS);
  /* There may be unconnected pspace blocks (not caught by above),
     such as pspace referred by a LAYOUT or DIMENSION, so for simplicity just
     scan all BLOCK_HEADER's and just skip *Model_Space. #81 BLOCK_HEADER -
     LAYOUT - BLOCK - ENDBLK
   */
  for (i = 0; (BITCODE_BL)i < dwg->num_objects; i++)
    {
      if (dwg->object[i].supertype == DWG_SUPERTYPE_OBJECT
          && dwg->object[i].type == DWG_TYPE_BLOCK_HEADER)
        {
          error |= dxf_block_write (dat, &dwg->object[i], mspace /* to be skipped*/, &i);
        }
  }

  ENDSEC ();
  return error;
}

static int
dxf_entities_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  int error = 0;
  Dwg_Object *hdr = dwg_model_space_object (dwg);
  Dwg_Object *obj;
  if (!hdr)
    return DWG_ERR_INVALIDDWG;

  SECTION (ENTITIES);
#if 1
  obj = get_first_owned_entity (hdr); // first_entity or entities[0]
  while (obj)
    {
      int i = obj->index;
      error |= dwg_dxf_object (dat, obj, &i);
      obj = get_next_owned_block_entity (hdr, obj); // until last_entity
    }
#else
  for (int i = 0; (BITCODE_BL)i < dwg->num_objects; i++)
    {
      Dwg_Object *obj = &dwg->object[i];
      if (obj->supertype == DWG_SUPERTYPE_ENTITY && obj->type != DWG_TYPE_BLOCK
          && obj->type != DWG_TYPE_ENDBLK)
        {
          Dwg_Object_Ref *owner = obj->tio.entity->ownerhandle;
          if (!owner || (owner && owner->obj == hdr))
            error |= dwg_dxf_object (dat, obj, &i);
        }
    }
#endif
  ENDSEC ();
  return error;
}

// check for valid ownerhandle. set to 0 if not
int
dxf_validate_DICTIONARY (Dwg_Object *obj)
{
  Dwg_Object_Ref *ownerhandle = obj->tio.object->ownerhandle;
  if (ownerhandle && !dwg_ref_object (obj->parent, ownerhandle))
    {
      LOG_INFO ("Wrong DICTIONARY.ownerhandle %lX\n", ownerhandle->absolute_ref);
      ownerhandle->absolute_ref = 0;
      return 0;
    }
  return 1;
}

static int
dxf_objects_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  int error = 0;
  int i;

  SECTION (OBJECTS);
  for (i = 0; (BITCODE_BL)i < dwg->num_objects; i++)
    {
      const Dwg_Object *restrict obj = &dwg->object[i];
      if (obj->supertype == DWG_SUPERTYPE_OBJECT
          && obj->type != DWG_TYPE_BLOCK_HEADER && !dwg_obj_is_control (obj))
        error |= dwg_dxf_object (dat, obj, &i);
    }
  ENDSEC ();
  return error;
}

// New ACDSDATA r2013+ section, with ACDSSCHEMA elements
static int
dxf_acds_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  //const char *section = "AcDsProtoype";
  Dwg_AcDs *_obj = &dwg->acds;
  if (0 && _obj->num_segidx)
    {
      SECTION (ACSDSDATA); // FIXME
      // 70
      // 71
      // 0 ACDSSCHEMA
      // TODO ...
      ENDSEC ();
    }
  return 0;
}

GCC30_DIAG_IGNORE (-Wformat-nonliteral)
// TODO: Beware, there's also a new ACDSDATA section, with ACDSSCHEMA elements
// and the Thumbnail_Data (per block?)
static int
dxf_thumbnail_write (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  Bit_Chain *pic = (Bit_Chain *)&dwg->thumbnail;
  if (pic->chain && pic->size && pic->size > 10)
    {
      SECTION (THUMBNAILIMAGE);
      VALUE_RL (pic->size, 90);
      VALUE_BINARY (pic->chain, pic->size, 310);
      ENDSEC ();
    }
  return 0;
}


AFL_GCC_TOOBIG
int
dwg_write_dxf (Bit_Chain *restrict dat, Dwg_Data *restrict dwg)
{
  const int minimal = dwg->opts & DWG_OPTS_MINIMAL;
  //struct Dwg_Header *obj = &dwg->header;

  loglevel = dwg->opts & DWG_OPTS_LOGLEVEL;
  if (dat->from_version == R_INVALID)
    dat->from_version = dat->version;
  if (dwg->header.version <= R_2000 && dwg->header.from_version > R_2000)
    dwg_fixup_BLOCKS_entities (dwg);

  setlocale (LC_NUMERIC, "C");

  VALUE_TV (PACKAGE_STRING, 999);

  // A minimal header requires only $ACADVER, $HANDSEED, and then ENTITIES
  // see https://pythonhosted.org/ezdxf/dxfinternals/filestructure.html
  dxf_header_write (dat, dwg);

  if (!minimal)
    {
      // if downgraded from r2000 to r14, but we still have classes, keep the
      // classes
      if ((dat->from_version >= R_2000 && dwg->num_classes)
          || dat->version >= R_2000)
        {
          if (dxf_classes_write (dat, dwg) >= DWG_ERR_CRITICAL)
            goto fail;
        }

      if (dxf_tables_write (dat, dwg) >= DWG_ERR_CRITICAL)
        goto fail;

      if (dxf_blocks_write (dat, dwg) >= DWG_ERR_CRITICAL)
        goto fail;
    }

  if (dxf_entities_write (dat, dwg) >= DWG_ERR_CRITICAL)
    goto fail;

  if (!minimal)
    {
      SINCE (R_13)
      {
        if (dxf_objects_write (dat, dwg) >= DWG_ERR_CRITICAL)
          goto fail;
      }
      SINCE (R_2013)
      {
        if (dxf_acds_write (dat, dwg) >= DWG_ERR_CRITICAL)
          goto fail;
      }
      SINCE (R_2000)
      {
        if (dxf_thumbnail_write (dat, dwg) >= DWG_ERR_CRITICAL)
          goto fail;
      }
    }
  RECORD (EOF);

  return 0;
fail:
  return 1;
}
AFL_GCC_POP

#undef IS_PRINT
#undef IS_DXF
