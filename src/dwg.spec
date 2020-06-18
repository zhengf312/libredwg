/* -*- c -*- */
/*****************************************************************************/
/*  LibreDWG - free implementation of the DWG file format                    */
/*                                                                           */
/*  Copyright (C) 2009-2010,2018-2020 Free Software Foundation, Inc.         */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

/*
 * dwg.spec: DWG entities and objects specification
 * written by Felipe Corrêa da Silva Sances
 * modified by Rodrigo Rodrigues da Silva
 * modified by Till Heuschmann
 * modified by Reini Urban
 * modified by Denis Pruchkovsky
 */

#include "spec.h"

/* (1/7) */
DWG_ENTITY (TEXT)

  DXF {
    //TODO can be skipped with DXF if STANDARD
    FIELD_HANDLE (style, 5, 7);
  }
  SUBCLASS (AcDbText)
  PRE (R_13) {
    FIELD_2RD (insertion_pt, 10);
    FIELD_RD (height, 40);
    FIELD_TV (text_value, 1);
    if (R11OPTS (1))
      FIELD_RD (rotation, 50);
    if (R11OPTS (2))
      FIELD_RD (width_factor, 41);
    if (R11OPTS (4))
      FIELD_RD (oblique_angle, 51);
    if (R11OPTS (8)) {
      DECODER { _ent->ltype_r11 = bit_read_RC (dat); }
      ENCODER { bit_write_RC (dat, _ent->ltype_r11); }
      PRINT   { LOG_TRACE ("ltype_r11: " FORMAT_RS "\n", _ent->ltype_r11); }
    }
    if (R11OPTS (16))
      FIELD_CAST (generation, RC, BS, 71);
    if (R11OPTS (32))
      FIELD_CAST (horiz_alignment, RC, BS, 72);
    if (R11OPTS (64))
      FIELD_2RD (alignment_pt, 11);
    if (R11OPTS (256))
      FIELD_CAST (vert_alignment, RC, BS, 73);
  }
  VERSIONS (R_13, R_14)
    {
      FIELD_BD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);
      FIELD_2RD (alignment_pt, 11);
      FIELD_3BD (extrusion, 210);
      FIELD_BD (thickness, 39);
      FIELD_BD (oblique_angle, 51);
      FIELD_BD (rotation, 50);
      FIELD_BD (height, 40);
      FIELD_BD (width_factor, 41);
      FIELD_TV (text_value, 1);
      FIELD_BS (generation, 71);
      FIELD_BS (horiz_alignment, 72);
      FIELD_BS (vert_alignment, 73);
    }

  IF_FREE_OR_SINCE (R_2000)
    {
      /* We assume that the user (the client application)
         is responsible for taking care of properly updating the dataflags field
         which indicates which fields in the data structures are valid and which are
         undefined */
      BITCODE_RC dataflags;
      FIELD_RC (dataflags, 0);
      dataflags = FIELD_VALUE (dataflags);

      if (!(dataflags & 0x01))
        FIELD_RD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);

      if (!(dataflags & 0x02))
        FIELD_2DD (alignment_pt, 10.0, 20.0, 11);

      FIELD_BE (extrusion, 210);
      FIELD_BT (thickness, 39);

      if (!(dataflags & 0x04))
        FIELD_RD (oblique_angle, 51);
      if (!(dataflags & 0x08))
        FIELD_RD (rotation, 50);

      FIELD_RD (height, 40);

      if (!(dataflags & 0x10))
        FIELD_RD (width_factor, 41);

      FIELD_T (text_value, 1);

      if (!(dataflags & 0x20))
        FIELD_BS (generation, 71);
      if (!(dataflags & 0x40))
        FIELD_BS (horiz_alignment, 72);
      if (!(dataflags & 0x80))
        FIELD_BS (vert_alignment, 73);
    }

  COMMON_ENTITY_HANDLE_DATA;
  SINCE (R_13)
    {
      IF_ENCODE_FROM_PRE_R13 {
        //FIXME: should really just lookup the style table; style is the index.
        FIELD_VALUE (style) = 0; //dwg_resolve_handle (dwg, obj->ltype_rs);
      }
#ifndef IS_DXF
      FIELD_HANDLE (style, 5, 7);
#endif
    }
  SUBCLASS (AcDbText)

DWG_ENTITY_END

/* (2/16) */
DWG_ENTITY (ATTRIB)

  DXF {
    //TODO can be skipped with DXF if STANDARD
    FIELD_HANDLE (style, 5, 7);
  }
  SUBCLASS (AcDbText)
  PRE (R_13)
    {
      LOG_ERROR ("TODO ATTRIB")
    }
  VERSIONS (R_13, R_14)
    {
      FIELD_BD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);
      FIELD_2RD (alignment_pt, 11);
      FIELD_3BD (extrusion, 210);
      FIELD_BD (thickness, 39);
      FIELD_BD (oblique_angle, 51);
      FIELD_BD (rotation, 50);
      FIELD_BD (height, 40);
      FIELD_BD (width_factor, 41);
      FIELD_TV (text_value, 1);
      FIELD_BS (generation, 71);
      FIELD_BS (horiz_alignment, 72);
      FIELD_BS (vert_alignment, 73);
    }

  IF_FREE_OR_SINCE (R_2000)
    {
      /* We assume that the user (the client application)
         is responsible for taking care of properly updating the dataflags field
         which indicates which fields in the data structures are valid and which are
         undefined */
      BITCODE_RC dataflags;
      FIELD_RC (dataflags, 0);
      dataflags = FIELD_VALUE (dataflags);

      if (!(dataflags & 0x01))
        FIELD_RD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);

      if (!(dataflags & 0x02))
        FIELD_2DD (alignment_pt, 10.0, 20.0, 11);

      FIELD_BE (extrusion, 210);
      FIELD_BT (thickness, 39);

      if (!(dataflags & 0x04))
        FIELD_RD (oblique_angle, 51);
      if (!(dataflags & 0x08))
        FIELD_RD (rotation, 50);

      FIELD_RD (height, 40);

      if (!(dataflags & 0x10))
        FIELD_RD (width_factor, 41);

      FIELD_T (text_value, 1);

      if (!(dataflags & 0x20))
        FIELD_BS (generation, 71);
      if (!(dataflags & 0x40))
        FIELD_BS (horiz_alignment, 72);
      if (!(dataflags & 0x80))
        FIELD_BS (vert_alignment, 74);
    }

  SUBCLASS (AcDbAttribute)
  SINCE (R_2010)
    {
      int dxf = dat->version == R_2010 ? 280: 0;
      FIELD_RC (class_version, dxf); // 0 = r2010
      VALUEOUTOFBOUNDS (class_version, 10)
    }
  SINCE (R_2018)
    {
      FIELD_RC (type, 70); // 1=single line, 2=multi line attrib, 4=multi line attdef

      if (FIELD_VALUE (type) > 1)
        {
          SUBCLASS (AcDbMText)
          LOG_WARN ("MTEXT fields")
          // TODO fields handles to MTEXT entities. how many?
          FIELD_HANDLE (mtext_handles, 0, 340); //TODO

          FIELD_BS (annotative_data_size, 70);
          if (FIELD_VALUE (annotative_data_size) > 1)
            {
              FIELD_RC (annotative_data_bytes, 0);
              FIELD_HANDLE (annotative_app, 0, 0); //TODO
              FIELD_BS (annotative_short, 0);
            }
        }
    }

  FIELD_T (tag, 2);
  FIELD_BS (field_length, 73);
  FIELD_RC (flags, 70); // 1 invisible, 2 constant, 4 verify, 8 preset

  SINCE (R_2007) {
    FIELD_B (lock_position_flag, 0); // 70
  }

  COMMON_ENTITY_HANDLE_DATA;

  FIELD_HANDLE (style, 5, 0); // unexpected here in DXF

DWG_ENTITY_END

/* (3/15) */
DWG_ENTITY (ATTDEF)

  DXF {
    //TODO can be skipped with DXF if STANDARD
    FIELD_HANDLE (style, 5, 7);
  }
  SUBCLASS (AcDbText)
  PRE (R_13)
    {
      LOG_ERROR ("TODO ATTDEF")
    }
  VERSIONS (R_13, R_14)
    {
      FIELD_BD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);
      FIELD_2RD (alignment_pt, 11);
      FIELD_3BD (extrusion, 210);
      FIELD_BD (thickness, 39);
      FIELD_BD (oblique_angle, 51);
      FIELD_BD (rotation, 50);
      FIELD_BD (height, 40);
      FIELD_BD (width_factor, 41);
      FIELD_T (default_value, 1);
      FIELD_BS (generation, 71);
      FIELD_BS (horiz_alignment, 72);
      FIELD_BS (vert_alignment, 74);
    }

  IF_FREE_OR_SINCE (R_2000)
    {
      /* We assume that the user (the client application)
         is responsible for taking care of properly updating the dataflags field
         which indicates which fields in the data structures are valid and which are
         undefined */
      BITCODE_RC dataflags;
      FIELD_RC (dataflags, 0);
      dataflags = FIELD_VALUE (dataflags);

      if (!(dataflags & 0x01))
        FIELD_RD (elevation, 30);
      FIELD_2RD (insertion_pt, 10);

      if (!(dataflags & 0x02))
        FIELD_2DD (alignment_pt, 10.0, 20.0, 11);

      FIELD_BE (extrusion, 210);
      FIELD_BT (thickness, 39);

      if (!(dataflags & 0x04))
        FIELD_RD (oblique_angle, 51);
      if (!(dataflags & 0x08))
        FIELD_RD (rotation, 50);

      FIELD_RD (height, 40);

      if (!(dataflags & 0x10))
        FIELD_RD (width_factor, 41);

      FIELD_T (default_value, 1);

      if (!(dataflags & 0x20))
        FIELD_BS (generation, 71);
      if (!(dataflags & 0x40))
        FIELD_BS (horiz_alignment, 72);
      if (!(dataflags & 0x80))
        FIELD_BS (vert_alignment, 74);
    }

  SUBCLASS (AcDbAttributeDefinition);
  SINCE (R_2010)
    {
      int dxf = dat->version == R_2010 ? 280: 0;
      FIELD_RC (class_version, dxf); // 0 = r2010
      VALUEOUTOFBOUNDS (class_version, 10)
    }
  DXF { FIELD_T (prompt, 3); }
  DXF { FIELD_T (tag, 2); }
  IF_FREE_OR_SINCE (R_2018)
    {
      FIELD_RC (type, 70); // 1=single line, 2=multi line attrib, 4=multi line attdef

      if (FIELD_VALUE (type) > 1)
        {
          SUBCLASS (AcDbMText)
          LOG_WARN ("MTEXT fields")
          // TODO fields handles to MTEXT entities. how many?
          FIELD_HANDLE (mtext_handles, 0, 340); //TODO

          FIELD_BS (annotative_data_size, 70);
          if (FIELD_VALUE (annotative_data_size) > 1)
            {
              FIELD_RC (annotative_data_bytes, 0);
              FIELD_HANDLE (annotative_app, 0, 0); //TODO
              FIELD_BS (annotative_short, 0);
            }
        }
    }

  FIELD_T (tag, 0);
  FIELD_BS (field_length, 0); //DXF 73, unused
  FIELD_RC (flags, 70); // 1 invisible, 2 constant, 4 verify, 8 preset

  SINCE (R_2007) {
    FIELD_B (lock_position_flag, 70);
  }

  // specific to ATTDEF
  SINCE (R_2010) {
    FIELD_RC (attdef_class_version, 280);
    VALUEOUTOFBOUNDS (attdef_class_version, 10)
  }
  FIELD_T (prompt, 0);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (style, 5, 0);

DWG_ENTITY_END

/* (4/12) */
DWG_ENTITY (BLOCK)

  SUBCLASS (AcDbBlockBegin)
  BLOCK_NAME (name, 2) //special pre-R13 naming rules

  COMMON_ENTITY_HANDLE_DATA;

#ifdef IS_DXF
  {
    Dwg_Object *o
        = _ent->ownerhandle && _ent->ownerhandle->obj
              ? _ent->ownerhandle->obj : NULL;
    VALUE_BL (0, 70);
    if (!o)
      o = dwg_ref_object (dwg, _ent->ownerhandle);
    if (!o || o->fixedtype != DWG_TYPE_BLOCK_HEADER)
      {
        Dwg_Bitcode_3RD nullpt = { 0.0, 0.0, 0.0 };
        VALUE_3BD (nullpt, 10);
      }
    else
      {
        Dwg_Object_BLOCK_HEADER *hdr = o->tio.object->tio.BLOCK_HEADER;
        VALUE_3BD (hdr->base_pt, 10);
      }
    BLOCK_NAME (name, 3); // special pre-R13 naming rules
    VALUE_TFF ("", 1);
  }
#endif

DWG_ENTITY_END

/* (5/13) */
DWG_ENTITY (ENDBLK)

  SUBCLASS (AcDbBlockEnd)
  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* (6) */
DWG_ENTITY (SEQEND)

  //SUBCLASS (AcDbSequenceEnd) //unused
  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* (7/14) */
DWG_ENTITY (INSERT)

  SUBCLASS (AcDbBlockReference)
#ifdef IS_DXF
    FIELD_HANDLE_NAME (block_header, 2, BLOCK_HEADER);
    if (FIELD_VALUE (has_attribs))
      FIELD_B (has_attribs, 66);
#endif
  PRE (R_13) {
    FIELD_2RD (ins_pt, 10);
  } else {
    FIELD_3DPOINT (ins_pt, 10);
  }

  VERSIONS (R_13, R_14)
    {
      FIELD_3BD_1 (scale, 41); // 42,43
    }

  SINCE (R_2000)
    {
      DXF_OR_PRINT {
        if (_obj->scale.x != 1.0 || _obj->scale.y != 1.0 || _obj->scale.z != 1.0)
          FIELD_3BD_1 (scale, 41);
      }
      DECODER
        {
          FIELD_BB (scale_flag, 0);
          if (FIELD_VALUE (scale_flag) == 3)
            {
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_VALUE (scale.y) = 1.0;
              FIELD_VALUE (scale.z) = 1.0;
            }
          else if (FIELD_VALUE (scale_flag) == 1)
            {
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_DD (scale.y, 1.0, 42);
              FIELD_DD (scale.z, 1.0, 43);
            }
          else if (FIELD_VALUE (scale_flag) == 2)
            {
              FIELD_RD (scale.x, 41);
              FIELD_VALUE (scale.y) = FIELD_VALUE (scale.x);
              FIELD_VALUE (scale.z) = FIELD_VALUE (scale.x);
            }
          else //if (FIELD_VALUE (scale_flag) == 0)
            {
              FIELD_RD (scale.x, 41);
              FIELD_DD (scale.y, FIELD_VALUE (scale.x), 42);
              FIELD_DD (scale.z, FIELD_VALUE (scale.x), 43);
            }
          FIELD_3PT_TRACE (scale, DD, 41);
        }

      ENCODER
        {
          if (FIELD_VALUE (scale.x) == 1.0 &&
              FIELD_VALUE (scale.y) == 1.0 &&
              FIELD_VALUE (scale.z) == 1.0)
            {
              FIELD_VALUE (scale_flag) = 3;
              FIELD_BB (scale_flag, 0);
            }
          else if (FIELD_VALUE (scale.x) == FIELD_VALUE (scale.y) &&
                   FIELD_VALUE (scale.x) == FIELD_VALUE (scale.z))
            {
              FIELD_VALUE (scale_flag) = 2;
              FIELD_BB (scale_flag, 0);
              FIELD_RD (scale.x, 41);
            }
          else if (FIELD_VALUE (scale.x) == 1.0)
            {
              FIELD_VALUE (scale_flag) = 1;
              FIELD_BB (scale_flag, 0);
              FIELD_RD (scale.x, 41);
              FIELD_DD (scale.y, 1.0, 42);
              FIELD_DD (scale.z, 1.0, 43);
            }
          else
            {
              FIELD_VALUE (scale_flag) = 0;
              FIELD_BB (scale_flag, 0);
              FIELD_RD (scale.x, 41);
              FIELD_DD (scale.y, FIELD_VALUE (scale.x), 42);
              FIELD_DD (scale.z, FIELD_VALUE (scale.x), 43);
            }
          FIELD_3PT_TRACE (scale, DD, 41);
        }
    }

  PRE (R_13) {
    FIELD_RD (rotation, 50);
  } else {
    FIELD_BD (rotation, 50);
    FIELD_3DPOINT (extrusion, 210);
    FIELD_B (has_attribs, 0); // 66 above
  }

  SINCE (R_2004)
    {
      if (FIELD_VALUE (has_attribs))
        FIELD_BL (num_owned, 0);
    }

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (block_header, 5, 0);
  //There is a typo in the spec. it says "R13-R200:".
  //I guess it means "R13-R2000:" (just like in MINSERT)
  VERSIONS (R_13, R_2000)
    {
      if (FIELD_VALUE (has_attribs))
        {
          FIELD_HANDLE (first_attrib, 4, 0);
          FIELD_HANDLE (last_attrib, 4, 0);
        }
    }

  //Spec typo? Spec says "2004:" but I think it should be "2004+:"
  // just like field num_owned (AND just like in MINSERT)
  IF_FREE_OR_SINCE (R_2004)
    {
      if (FIELD_VALUE (has_attribs))
        {
          HANDLE_VECTOR (attrib_handles, num_owned, 4, 0);
        }
    }

  if (FIELD_VALUE (has_attribs)) {
    FIELD_HANDLE (seqend, 3, 0);
  }

DWG_ENTITY_END

/* (8) 20.4.10*/
DWG_ENTITY (MINSERT)

  SUBCLASS (AcDbBlockReference)
#ifdef IS_DXF
    FIELD_HANDLE_NAME (block_header, 2, BLOCK_HEADER);
    if (FIELD_VALUE (has_attribs))
      FIELD_B (has_attribs, 66);
#endif
  FIELD_3DPOINT (ins_pt, 10);

  VERSIONS (R_13, R_14) {
    FIELD_3BD_1 (scale, 41);
  }

  SINCE (R_2000)
    {
      DXF_OR_PRINT {
        if (_obj->scale.x != 1.0 || _obj->scale.y != 1.0 || _obj->scale.z != 1.0)
          FIELD_3BD_1 (scale, 41);
      }
      DECODER
        {
          FIELD_BB (scale_flag, 0);
          if (FIELD_VALUE (scale_flag) == 3)
            {
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_VALUE (scale.y) = 1.0;
              FIELD_VALUE (scale.z) = 1.0;
            }
          else if (FIELD_VALUE (scale_flag) == 1)
            {
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_DD (scale.y, 1.0, 42);
              FIELD_DD (scale.z, 1.0, 43);
            }
          else if (FIELD_VALUE (scale_flag) == 2)
            {
              FIELD_RD (scale.x, 41);
              FIELD_VALUE (scale.y) = FIELD_VALUE (scale.x);
              FIELD_VALUE (scale.z) = FIELD_VALUE (scale.x);
            }
          else
            {
              assert (FIELD_VALUE (scale_flag) == 0);
              FIELD_RD (scale.x, 41);
              FIELD_DD (scale.y, FIELD_VALUE (scale.x), 42);
              FIELD_DD (scale.z, FIELD_VALUE (scale.x), 43);
            }
          FIELD_3PT_TRACE (scale, DD, 41);
        }

      ENCODER
        {
          if (FIELD_VALUE (scale.x) == 1.0 &&
              FIELD_VALUE (scale.y) == 1.0 &&
              FIELD_VALUE (scale.z) == 1.0)
            {
              FIELD_VALUE (scale_flag) = 3;
              FIELD_BB (scale_flag, 0);
            }
          else if (FIELD_VALUE (scale.x) == 1.0)
             {
              FIELD_VALUE (scale_flag) = 1;
              FIELD_BB (scale_flag, 0);
              FIELD_DD (scale.y, 1.0, 42);
              FIELD_DD (scale.z, 1.0, 43);
             }
          else if (FIELD_VALUE (scale.x) == FIELD_VALUE (scale.y) &&
                   FIELD_VALUE (scale.x) == FIELD_VALUE (scale.z))
            {
              FIELD_VALUE (scale_flag) = 2;
              FIELD_BB (scale_flag, 0);
              FIELD_RD (scale.x, 41);
            }
          else
            {
              FIELD_VALUE (scale_flag) = 0;
              FIELD_BB (scale_flag, 0);
              FIELD_RD (scale.x, 41);
              FIELD_DD (scale.y, FIELD_VALUE (scale.x), 42);
              FIELD_DD (scale.z, FIELD_VALUE (scale.x), 43);
            }
          FIELD_3PT_TRACE (scale, DD, 41);
        }
    }

  FIELD_BD (rotation, 50);
  FIELD_3BD (extrusion, 210);
  FIELD_B (has_attribs, 0);

  SINCE (R_2004)
    {
      if (FIELD_VALUE (has_attribs))
        FIELD_BL (num_owned, 0);
    }

  FIELD_BS (num_cols, 70);
  FIELD_BS (num_rows, 71);
  FIELD_BD (col_spacing, 44);
  FIELD_BD (row_spacing, 45);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (block_header, 5, 0);
  IF_FREE_OR_VERSIONS (R_13, R_2000)
  {
    if (FIELD_VALUE (has_attribs))
      {
        FIELD_HANDLE (first_attrib, 4, 0);
        FIELD_HANDLE (last_attrib, 4, 0);
      }
  }

  IF_FREE_OR_SINCE (R_2004)
    {
    if (FIELD_VALUE (has_attribs))
      {
        HANDLE_VECTOR (attrib_handles, num_owned, 4, 0);
      }
    }

  if (FIELD_VALUE (has_attribs))
    {
      FIELD_HANDLE (seqend, 3, 0);
    }

DWG_ENTITY_END

//(9) Unknown

/* (10/20) */
DWG_ENTITY (VERTEX_2D)

  SUBCLASS (AcDbVertex)
  SUBCLASS (AcDb2dVertex)
  PRE (R_13)
  {
    FIELD_2RD (point, 10);
    if (R11OPTS (1))
      FIELD_RD (start_width, 40);
    if (R11OPTS (2))
      FIELD_RD (end_width, 41);
    if (R11OPTS (4))
      FIELD_RD (tangent_dir, 50);
    if (R11OPTS (8))
      FIELD_RC (flag, 70);
  }
  SINCE (R_13)
  {
    FIELD_RC0 (flag, 70);
    FIELD_3BD (point, 10);

  /* Decoder and Encoder routines could be the same but then we
     wouldn't compress data when saving. So we explicitly implemented
     the encoder routine with the compression technique described in
     the spec. --Juca */
    DXF_OR_PRINT {
      if (FIELD_VALUE (flag) != 0) {
        FIELD_BD0 (start_width, 40);
        FIELD_BD0 (end_width, 41);
      }
    }
    DECODER
    {
      FIELD_BD (start_width, 40);
      if (FIELD_VALUE (start_width) < 0)
        {
          FIELD_VALUE (start_width) = -FIELD_VALUE (start_width);
          FIELD_VALUE (end_width) = FIELD_VALUE (start_width);
        }
      else
        {
          FIELD_BD (end_width, 41);
        }
    }

  ENCODER
    {
      if (FIELD_VALUE (start_width) && FIELD_VALUE (start_width) == FIELD_VALUE (end_width))
        {
          //TODO: This is ugly! We should have a better way of doing such things
          FIELD_VALUE (start_width) = -FIELD_VALUE (start_width);
          FIELD_BD (start_width, 40);
          FIELD_VALUE (start_width) = -FIELD_VALUE (start_width);
        }
      else
        {
          FIELD_BD (start_width, 40);
          FIELD_BD (end_width, 41);
        }
    }

    DXF {
      if (FIELD_VALUE (flag) != 0)
        FIELD_BD0 (bulge, 42);
    } else {
      FIELD_BD (bulge, 42);
    }
    SINCE (R_2010) {
      FIELD_BL (id, 91);
    }
    DXF {
      if (FIELD_VALUE (flag) != 0)
        FIELD_BD (tangent_dir, 50);
    } else {
      FIELD_BD (tangent_dir, 50);
    }
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(11)*/
DWG_ENTITY (VERTEX_3D)

  SUBCLASS (AcDbVertex)
  SUBCLASS (AcDb3dPolylineVertex) //SUBCLASS (AcDb3dVertex)?
  FIELD_RC (flag, 0);
  FIELD_3BD (point, 10);
  DXF { FIELD_RC (flag, 70); }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(12)*/
DWG_ENTITY (VERTEX_MESH)

  SUBCLASS (AcDbVertex)
  SUBCLASS (AcDbPolyFaceMeshVertex) //?
  FIELD_RC (flag, 0);
  FIELD_3BD (point, 10);
  DXF { FIELD_RC (flag, 70); }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(13)*/
DWG_ENTITY (VERTEX_PFACE)

  SUBCLASS (AcDbVertex)
  SUBCLASS (AcDbPolyFaceMeshVertex)
  FIELD_RC (flag, 0);
  FIELD_3BD (point, 10);
  DXF { FIELD_RC (flag, 70); }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(14)*/
DWG_ENTITY (VERTEX_PFACE_FACE)

  SUBCLASS (AcDbFaceRecord)
  DXF {
    BITCODE_3RD pt = { 0.0, 0.0, 0.0 };
    VALUE_3BD (pt, 10);
    VALUE_RC ((BITCODE_RC)128, 70);
    FIELD_BS (vertind[0], 71);
    if (FIELD_VALUE (vertind[1]))
      FIELD_BS (vertind[1], 72);
    if (FIELD_VALUE (vertind[2]))
      FIELD_BS (vertind[2], 73);
    if (FIELD_VALUE (vertind[3]))
      FIELD_BS (vertind[3], 74);
  } else {
    //FIELD_VALUE (pt) = { 0.0, 0.0, 0.0 };
    FIELD_VALUE (flag) = 128;
    FIELD_BS (vertind[0], 71);
    FIELD_BS (vertind[1], 72);
    FIELD_BS (vertind[2], 73);
    FIELD_BS (vertind[3], 74);
  }
  //TODO R13 has color_rs and ltype_rs for all vertices, not in DXF

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(15)*/
DWG_ENTITY (POLYLINE_2D)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDb2dPolyline)
  PRE (R_13)
  {
    if (R11OPTS (1))
      FIELD_CAST (flag, RC, RS, 70);
    if (R11OPTS (2))
      FIELD_RD (start_width, 40);
    //??
    if (R11OPTS (4))
      FIELD_RS (curve_type, 75);
    if (R11OPTS (8))
      FIELD_RD (end_width, 40);
  }
  SINCE (R_13)
  {
    DXF {
      FIELD_B (has_vertex, 66);
    }
    else {
      FIELD_VALUE (has_vertex) = 1;
    }
    FIELD_BS0 (flag, 70);
    FIELD_BS0 (curve_type, 75);
    DECODER_OR_ENCODER {
      FIELD_BD (start_width, 40);
      FIELD_BD (end_width, 41);
      FIELD_BT (thickness, 39);
      FIELD_BD (elevation, 30);
    }
    DXF {
      BITCODE_3RD pt = { 0.0, 0.0, 0.0 };
      pt.z = FIELD_VALUE (elevation);
      FIELD_BT0 (thickness, 39);
      KEY (elevation); VALUE_3BD (pt, 10);
      FIELD_BD (start_width, 40);
      FIELD_BD (end_width, 41);
    }
    FIELD_BE (extrusion, 210);

    SINCE (R_2004) {
      FIELD_BL (num_owned, 0);
    }
  }
  COMMON_ENTITY_HANDLE_DATA;

  IF_FREE_OR_VERSIONS (R_13, R_2000)
    {
      FIELD_HANDLE (first_vertex, 4, 0);
      FIELD_HANDLE (last_vertex, 4, 0);
    }

  IF_FREE_OR_SINCE (R_2004)
    {
      HANDLE_VECTOR (vertex, num_owned, 3, 0);
    }

  IF_FREE_OR_SINCE (R_13)
    {
      FIELD_HANDLE (seqend, 3, 0);
    }

DWG_ENTITY_END

/*(16)*/
DWG_ENTITY (POLYLINE_3D)

  SUBCLASS (AcDb3dPolyline)
  DXF {
    FIELD_B (has_vertex, 66);
  }
  else {
    FIELD_VALUE (has_vertex) = 1;
  }
  FIELD_RC (curve_type, 75);
  FIELD_RC (flag, 70);

  SINCE (R_2004) {
    FIELD_BL (num_owned, 0);
  }

  COMMON_ENTITY_HANDLE_DATA;
  IF_FREE_OR_VERSIONS (R_13, R_2000)
    {
      FIELD_HANDLE (first_vertex, 4, 0);
      FIELD_HANDLE (last_vertex, 4, 0);
    }
  IF_FREE_OR_SINCE (R_2004)
    {
      HANDLE_VECTOR (vertex, num_owned, 3, 0);
    }
  FIELD_HANDLE (seqend, 3, 0);

DWG_ENTITY_END

/* (17/8) */
DWG_ENTITY (ARC)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbCircle)
  PRE (R_13) {
    FIELD_2RD (center, 10);
    FIELD_RD (radius, 40);
    FIELD_RD (start_angle, 50);
    FIELD_RD (end_angle, 51);
    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (center.z, 30);
  }
  LATER_VERSIONS {
    FIELD_3BD (center, 10);
    FIELD_BD (radius, 40);
    FIELD_BT (thickness, 39);
    FIELD_BE (extrusion, 210);
    SUBCLASS (AcDbArc)
    FIELD_BD (start_angle, 50);
    FIELD_BD (end_angle, 51);
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* (18/3) */
DWG_ENTITY (CIRCLE)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbCircle)
  PRE (R_13) {
    FIELD_2RD (center, 10);
    FIELD_RD (radius, 40);
    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (center.z, 38);
  }
  LATER_VERSIONS {
    FIELD_3BD (center, 10);
    FIELD_BD (radius, 40);
    FIELD_BT (thickness, 39);
    FIELD_BE (extrusion, 210);
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* (19/1) */
DWG_ENTITY (LINE)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbLine)
  PRE (R_13) {
    if (R11FLAG (4))
      FIELD_3RD (start, 10)
    else
      FIELD_2RD (start, 10)

    if (R11FLAG (4))
      FIELD_3RD (end, 11)
    else
      FIELD_2RD (end, 11)

    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (thickness, 39);
  }
  VERSIONS (R_13, R_14)
    {
      FIELD_3BD (start, 10);
      FIELD_3BD (end, 11);
    }
  SINCE (R_2000)
    {
      ENCODER {
        FIELD_VALUE (z_is_zero) = (FIELD_VALUE (start.z) == 0.0 &&
                                   FIELD_VALUE (end.z) == 0.0);
      }
      DXF_OR_PRINT
        {
          JSON { FIELD_B (z_is_zero, 0); }
          FIELD_3DPOINT (start, 10);
          FIELD_3DPOINT (end, 11);
        }
      else
        {
          FIELD_B (z_is_zero, 0);
          FIELD_RD (start.x, 10);
          FIELD_DD (end.x, FIELD_VALUE (start.x), 11);
          FIELD_RD (start.y, 20);
          FIELD_DD (end.y, FIELD_VALUE (start.y), 21);

          if (FIELD_VALUE (z_is_zero))
            {
              FIELD_VALUE (start.z) = 0.0;
              FIELD_VALUE (end.z) = 0.0;
            }
          else
            {
              FIELD_RD (start.z, 30);
              FIELD_DD (end.z, FIELD_VALUE (start.z), 31);
            }
          FIELD_3PT_TRACE (start, DD, 10);
          FIELD_3PT_TRACE (end, DD, 11);
        }
    }

  SINCE (R_13) {
    FIELD_BT (thickness, 39);
    FIELD_BE (extrusion, 210);
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/**
 * DIMENSION_common declaration
 */
#ifndef COMMON_ENTITY_DIMENSION
#define COMMON_ENTITY_DIMENSION \
    SUBCLASS (AcDbDimension) \
    SINCE (R_2010) \
      { \
        FIELD_RC (class_version, 280); /* 0=r2010 */ \
        VALUEOUTOFBOUNDS (class_version, 10) \
      } \
    DXF { \
      FIELD_VALUE (blockname) = dwg_dim_blockname (dwg, obj); \
      FIELD_BE (extrusion, 210); \
      FIELD_T (blockname, 2); \
      FIELD_3BD (def_pt, 10); \
    } else { \
      FIELD_3BD (extrusion, 210); \
    } \
    FIELD_2RD (text_midpt, 11); \
    FIELD_BD (elevation, 31); \
    DXF { \
      FIELD_RC (flag, 70); \
    } else { \
      FIELD_RC (flag1, 0); \
    } \
    DECODER { \
      BITCODE_RC flag = FIELD_VALUE (flag1); \
      flag &= 0xE0; /* clear the upper flag bits, and fix them: */ \
      flag = (flag & 1) ? flag & 0x7F : flag | 0x80; /* bit 7 is inverse of bit 0 */ \
      flag = (flag & 2) ? flag | 0x20 : flag & 0xDF; /* set bit 5 to bit 1 */ \
      if      (_obj->flag == DWG_TYPE_DIMENSION_ALIGNED)  flag |= 1; \
      else if (_obj->flag == DWG_TYPE_DIMENSION_ANG2LN)   flag |= 2; \
      else if (_obj->flag == DWG_TYPE_DIMENSION_DIAMETER) flag |= 3; \
      else if (_obj->flag == DWG_TYPE_DIMENSION_RADIUS)   flag |= 4; \
      else if (_obj->flag == DWG_TYPE_DIMENSION_ANG3PT)   flag |= 5; \
      else if (_obj->flag == DWG_TYPE_DIMENSION_ORDINATE) flag |= 6; \
      FIELD_VALUE (flag) = flag; \
    } \
    DXF { \
      if (dat->from_version >= R_2007) { \
        FIELD_T (user_text, 1); \
      } else if (_obj->user_text && strlen (_obj->user_text)) { \
        FIELD_TV (user_text, 1); \
      } \
    } else { \
      FIELD_T (user_text, 1); \
    } \
    FIELD_BD0 (text_rotation, 53); \
    FIELD_BD0 (horiz_dir, 51); \
    FIELD_3BD_1 (ins_scale, 0); \
    FIELD_BD0 (ins_rotation, 54); \
    SINCE (R_2000) \
      { \
        FIELD_BS (attachment, 71); \
        FIELD_BS (lspace_style, 72); \
        FIELD_BD (lspace_factor, 41); \
        FIELD_BD (act_measurement, 42); \
      } \
    SINCE (R_2007) \
      { \
        FIELD_B (unknown, 73); \
        FIELD_B (flip_arrow1, 74); \
        FIELD_B (flip_arrow2, 75); \
      } \
    FIELD_2RD (clone_ins_pt, 12); \
    DXF { \
      FIELD_HANDLE (dimstyle, 5, 3); \
    }
#endif

/*(20)*/
DWG_ENTITY (DIMENSION_ORDINATE)

  COMMON_ENTITY_DIMENSION
  SUBCLASS (AcDbOrdinateDimension)
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10);
  }
  FIELD_3BD (feature_location_pt, 13);
  FIELD_3BD (leader_endpt, 14);
  FIELD_RC (flag2, 70);
  DECODER {
    BITCODE_RC flag = FIELD_VALUE (flag);
    flag = (FIELD_VALUE (flag2) & 1)
            ? flag | 0x80 : flag & 0xBF; /* set bit 6 */
    FIELD_VALUE (flag) = flag;
  }
  JSON { FIELD_RC (flag, 0); }

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/* (21/23) */
DWG_ENTITY (DIMENSION_LINEAR)

  // TODO PRE (R_R13)
  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDbAlignedDimension)
  FIELD_3BD (xline1_pt, 13);
  FIELD_3BD (xline2_pt, 14);
  FIELD_3BD (def_pt, 10);
  FIELD_BD0 (oblique_angle, 52);
  FIELD_BD0 (dim_rotation, 50);
  SUBCLASS (AcDbRotatedDimension)

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/*(22)*/
DWG_ENTITY (DIMENSION_ALIGNED)

  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDbAlignedDimension)
  UNTIL (R_9) {
    FIELD_2RD (xline1_pt, 13);
    FIELD_2RD (xline2_pt, 14);
  } LATER_VERSIONS {
    FIELD_3BD (xline1_pt, 13);
    FIELD_3BD (xline2_pt, 14);
  }
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10);
  }
  FIELD_BD0 (oblique_angle, 52);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/*(23)*/
DWG_ENTITY (DIMENSION_ANG3PT)

  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDb3PointAngularDimension)
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10);
  }
  FIELD_3BD (xline1_pt, 13);
  FIELD_3BD (xline2_pt, 14);
  FIELD_3BD (center_pt, 15);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/*(24)*/
DWG_ENTITY (DIMENSION_ANG2LN)

  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDb2LineAngularDimension)
  JSON { FIELD_3BD (def_pt, 10); }
  else { FIELD_2RD (def_pt, 10); }
  FIELD_3BD (xline1start_pt, 13);
  FIELD_3BD (xline1end_pt, 14);
  FIELD_3BD (xline2start_pt, 15);
  FIELD_3BD (xline2end_pt, 16);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/*(25)*/
DWG_ENTITY (DIMENSION_RADIUS)

  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDbRadialDimension)
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10);
  }
  FIELD_3BD (first_arc_pt, 15);
  FIELD_BD (leader_len, 40);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/*(26)*/
DWG_ENTITY (DIMENSION_DIAMETER)

  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDbDiametricDimension)
  FIELD_3BD (first_arc_pt, 15);
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10); // = far_chord_pt
  }
  FIELD_BD (leader_len, 40);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);

DWG_ENTITY_END

/* (27/2) */
DWG_ENTITY (POINT)

  SUBCLASS (AcDbPoint)
  //TODO PRE (R_13)
  FIELD_BD (x, 10);
  FIELD_BD (y, 20);
  FIELD_BD (z, 30);
  FIELD_BT (thickness, 39);
  FIELD_BE (extrusion, 210);
  FIELD_BD (x_ang, 50);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* (28/22) */
DWG_ENTITY (_3DFACE)

  SUBCLASS (AcDbFace)
  // TODO PRE (R_R13)
  VERSIONS (R_13, R_14)
    {
      FIELD_3BD (corner1, 10);
      FIELD_3BD (corner2, 11);
      FIELD_3BD (corner3, 12);
      FIELD_3BD (corner4, 13);
      FIELD_BS (invis_flags, 70);
    }

  SINCE (R_2000)
    {
      FIELD_B (has_no_flags, 0);

      DXF_OR_PRINT
        {
          JSON { FIELD_B (z_is_zero, 0); }
          FIELD_3DPOINT (corner1, 10);
        }
      DECODER
        {
          FIELD_B (z_is_zero, 0);
          FIELD_RD (corner1.x, 10);
          FIELD_RD (corner1.y, 20);
          if (FIELD_VALUE (z_is_zero))
            FIELD_VALUE (corner1.z) = 0;
          else
            FIELD_RD (corner1.z, 30);
        }

      ENCODER
        {
          FIELD_VALUE (z_is_zero) = (FIELD_VALUE (corner1.z) == 0);
          FIELD_B (z_is_zero, 0);
          FIELD_RD (corner1.x, 10);
          FIELD_RD (corner1.y, 20);
          if (!FIELD_VALUE (z_is_zero))
            FIELD_RD (corner1.z, 30);
        }

      FIELD_3DD (corner2, corner1, 11);
      FIELD_3DD (corner3, corner2, 12);
      FIELD_3DD (corner4, corner3, 13);
    }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(29)*/
DWG_ENTITY (POLYLINE_PFACE)

  SUBCLASS (AcDbPolyFaceMesh)
  DXF {
    BITCODE_3RD pt = { 0.0, 0.0, 0.0 };
    FIELD_B (has_vertex, 66);
    KEY (elevation); VALUE_3BD (pt, 10);
    KEY (flag); VALUE_BL (64, 70);
  }
  else {
    FIELD_VALUE (has_vertex) = 1;
  }
  FIELD_BS (numverts, 71);
  FIELD_BS (numfaces, 72);

  SINCE (R_2004) {
    FIELD_BL (num_owned, 0);
  }

  COMMON_ENTITY_HANDLE_DATA;
  IF_FREE_OR_VERSIONS (R_13, R_2000)
    {
      FIELD_HANDLE (first_vertex, 4, 0);
      FIELD_HANDLE (last_vertex, 4, 0);
    }
  IF_FREE_OR_SINCE (R_2004)
    {
      HANDLE_VECTOR (vertex, num_owned, 4, 0);
    }
  FIELD_HANDLE (seqend, 3, 0);

DWG_ENTITY_END

/*(30)*/
DWG_ENTITY (POLYLINE_MESH)

  SUBCLASS (AcDbPolygonMesh)
  FIELD_BS (flag, 70);
  FIELD_BS (curve_type, 75);
  FIELD_BS (num_m_verts, 71);
  FIELD_BS (num_n_verts, 72);
  FIELD_BS (m_density, 73);
  FIELD_BS (n_density, 74);

  SINCE (R_2004) {
    FIELD_BL (num_owned, 0);
  }

  COMMON_ENTITY_HANDLE_DATA;
  VERSIONS (R_13, R_2000)
    {
      FIELD_HANDLE (first_vertex, 4, 0);
      FIELD_HANDLE (last_vertex, 4, 0);
    }
  IF_FREE_OR_SINCE (R_2004)
    {
      VALUEOUTOFBOUNDS (num_owned, 100000)
      HANDLE_VECTOR (vertex, num_owned, 4, 0);
    }
  FIELD_HANDLE (seqend, 3, 0);

DWG_ENTITY_END

/* (31/11) */
DWG_ENTITY (SOLID)

  SUBCLASS (AcDbTrace)
  PRE (R_13) {
    FIELD_2RD (corner1, 10);
    FIELD_2RD (corner2, 11);
    FIELD_2RD (corner3, 12);
    FIELD_2RD (corner4, 13);
    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (elevation, 38);
  }
  LATER_VERSIONS {
    FIELD_BT (thickness, 39);
    FIELD_BD (elevation, 38);
    FIELD_2RD (corner1, 10);
    FIELD_2RD (corner2, 11);
    FIELD_2RD (corner3, 12);
    FIELD_2RD (corner4, 13);
    FIELD_BE (extrusion, 210);

    COMMON_ENTITY_HANDLE_DATA;
  }

DWG_ENTITY_END

/* (32/9) */
DWG_ENTITY (TRACE)

  SUBCLASS (AcDbTrace)
  PRE (R_13) {
    FIELD_2RD (corner1, 10);
    FIELD_2RD (corner2, 11);
    FIELD_2RD (corner3, 12);
    FIELD_2RD (corner4, 13);
    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (elevation, 38);
  }
  LATER_VERSIONS {
    FIELD_BT (thickness, 39);
    FIELD_BD (elevation, 38);
    FIELD_2RD (corner1, 10);
    FIELD_2RD (corner2, 11);
    FIELD_2RD (corner3, 12);
    FIELD_2RD (corner4, 13);
    FIELD_BE (extrusion, 210);

    COMMON_ENTITY_HANDLE_DATA;
  }

DWG_ENTITY_END

/* (33/4) */
DWG_ENTITY (SHAPE)

  DXF { FIELD_HANDLE (style, 5, 7); }
  SUBCLASS (AcDbShape)
  PRE (R_13) {
    FIELD_HANDLE (style, 5, 0);
    FIELD_2RD (ins_pt, 10);
    FIELD_RS (style_id, 0); // dxf: 2
    if (R11OPTS (1))
      FIELD_3RD (extrusion, 210);
    if (R11OPTS (2))
      FIELD_RD (ins_pt.z, 38);
  }
  LATER_VERSIONS {
    FIELD_3BD (ins_pt, 10);
    FIELD_BD (scale, 40);  // documented as size
    FIELD_BD (rotation, 50);
    FIELD_BD (width_factor, 41);
    FIELD_BD (oblique_angle, 51);
    FIELD_BD (thickness, 39);
#ifdef IS_DXF
    {
      Dwg_Object *style;
      if (_obj->style)
        style = dwg_resolve_handle (dwg, _obj->style->absolute_ref);
      else
        {
          Dwg_Object_Ref *ctrlref = dwg->header_vars.STYLE_CONTROL_OBJECT;
          Dwg_Object *ctrl
            = ctrlref ? dwg_resolve_handle (dwg, ctrlref->absolute_ref) : NULL;
          Dwg_Object_STYLE_CONTROL *_ctrl
            = ctrl ? ctrl->tio.object->tio.STYLE_CONTROL : NULL;
          Dwg_Object_Ref *styleref = _ctrl && _obj->style_id < _ctrl->num_entries
                                     ? _ctrl->entries[_obj->style_id] // index
                                     : NULL;
          style = styleref ? dwg_resolve_handle (dwg, styleref->absolute_ref) : NULL;
        }
      if (style && style->fixedtype == DWG_TYPE_STYLE)
        // dxf 2 for the name from SHAPE styles
        VALUE_T (style->tio.object->tio.STYLE->name, 2);
    }
#else
    FIELD_BS (style_id, 0); // STYLE index in dwg to SHAPEFILE
#endif
    FIELD_3BD (extrusion, 210);

    COMMON_ENTITY_HANDLE_DATA;
    FIELD_HANDLE (style, 5, 0);
  }

DWG_ENTITY_END

/* (34/24) */
DWG_ENTITY (VIEWPORT)

  SUBCLASS (AcDbViewport)
  PRE (R_13) {
    FIELD_3RD (center, 10);
    FIELD_RD (width, 40);
    FIELD_RD (height, 41);
    FIELD_RS (on_off, 68);
  }
  LATER_VERSIONS {
    FIELD_3BD (center, 10);
    FIELD_BD (width, 40);
    FIELD_BD (height, 41);
  }
  DXF {
    FIELD_VALUE (on_off) = 1;
    FIELD_VALUE (id) = 1;
    FIELD_RS (on_off, 68);
    FIELD_RS (id, 69);
  }

  SINCE (R_2000) {
    FIELD_3BD (view_target, 17);
    FIELD_3BD (VIEWDIR, 16);
    FIELD_BD (twist_angle, 51);
    FIELD_BD (VIEWSIZE, 45);
    FIELD_BD (lens_length, 42);
    FIELD_BD (front_clip_z, 43);
    FIELD_BD (back_clip_z, 44);
    if (dwg->header.dwg_version != 0x1a) { // AC1020/R_2006 only here
      FIELD_BD (SNAPANG, 50);
      FIELD_2RD (VIEWCTR, 12);
      FIELD_2RD (SNAPBASE, 13);
    } else {
      // on R_2006: no SNAPANG, SNAPBASE
      FIELD_2RD (VIEWCTR, 12);
    }
    FIELD_2RD (SNAPUNIT, 14);
    FIELD_2RD (GRIDUNIT, 15);
    FIELD_BS (circle_zoom, 72);
  }
  SINCE (R_2007) {
    FIELD_BS (grid_major, 61);
  }

  SINCE (R_2000) {
    FIELD_BL (num_frozen_layers, 0);
    FIELD_BL (status_flag, 90);
    FIELD_T (style_sheet, 1);
    FIELD_RC (render_mode, 281);
    FIELD_B (ucs_at_origin, 74);
    FIELD_B (UCSVP, 71);
    FIELD_3BD (ucsorg, 110);
    FIELD_3BD (ucsxdir, 111);
    FIELD_3BD (ucsydir, 112);
    FIELD_BD (ucs_elevation, 146);
    FIELD_BS (UCSORTHOVIEW, 79);
  }

  SINCE (R_2004) {
    FIELD_BS (shadeplot_mode, 170);
  }
  SINCE (R_2007) {
    FIELD_B (use_default_lights, 292);
    FIELD_RC (default_lighting_type, 282);
    FIELD_BD (brightness, 141);
    FIELD_BD (contrast, 142);
    FIELD_CMC (ambient_color, 63);
  }

  COMMON_ENTITY_HANDLE_DATA;
  VERSIONS (R_13, R_14) {
    FIELD_HANDLE (vport_entity_header, 5, 0);
  }
  VERSION (R_2000) {
    HANDLE_VECTOR (frozen_layers, num_frozen_layers, 5, 341);
    FIELD_HANDLE (clip_boundary, 5, 340);
  }
  SINCE (R_2004) {
    HANDLE_VECTOR (frozen_layers, num_frozen_layers, 4, 341);
    FIELD_HANDLE (clip_boundary, 5, 340);
  }
  VERSION (R_2000) {
    FIELD_HANDLE (vport_entity_header, 5, 0);
  }
  SINCE (R_2000) {
    FIELD_HANDLE (named_ucs, 5, 345);
    FIELD_HANDLE (base_ucs, 5, 346);
  }
  SINCE (R_2007) {
    FIELD_HANDLE (background, 4, 332);
    FIELD_HANDLE (visualstyle, 5, 348);
    FIELD_HANDLE (shadeplot, 4, 333);
    FIELD_HANDLE (sun, 3, 361);
  }

DWG_ENTITY_END

/*(35)*/
DWG_ENTITY (ELLIPSE)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbEllipse)
  FIELD_3BD (center, 10);
  FIELD_3BD (sm_axis, 11);
  FIELD_3BD (extrusion, 210);
  FIELD_BD (axis_ratio, 40);
  FIELD_BD (start_angle, 41);
  FIELD_BD (end_angle, 42);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(36)*/
DWG_ENTITY (SPLINE)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbSpline)
  FIELD_BL (scenario, 0);
  UNTIL (R_2013) {
    if (FIELD_VALUE (scenario) != 1 && FIELD_VALUE (scenario) != 2)
      LOG_ERROR ("unknown scenario %d", FIELD_VALUE (scenario));
    DECODER {
      if (FIELD_VALUE (scenario) == 1)
        FIELD_VALUE (splineflags1) = 8;
      else if (FIELD_VALUE (scenario) == 2)
        FIELD_VALUE (splineflags1) = 9;
    }
  }
  SINCE (R_2013) {
    FIELD_BL (splineflags1, 0);
    FIELD_BL (knotparam, 0);
    if (FIELD_VALUE (splineflags1) & 1)
      FIELD_VALUE (scenario) = 2;
    if (FIELD_VALUE (knotparam) == 15)
      FIELD_VALUE (scenario) = 1;
  }

  // extrusion on planar
  DXF { VALUE_RD (0.0, 210); VALUE_RD (0.0, 220); VALUE_RD (1.0, 230);
        FIELD_BL (flag, 70);
      }
  FIELD_BL (degree, 71);

  if (FIELD_VALUE (scenario) & 1) { // spline
    FIELD_B (rational, 0); // flag bit 2
    FIELD_B (closed_b, 0); // flag bit 0
    FIELD_B (periodic, 0); // flag bit 1
    FIELD_BD (knot_tol, 42); // def: 0.0000001
    FIELD_BD (ctrl_tol, 43); // def: 0.0000001
    FIELD_BL (num_knots, 72);
    FIELD_BL (num_ctrl_pts, 73);
    FIELD_B (weighted, 0);

    DECODER {
      // not 32
      FIELD_VALUE (flag) = 8 +          /* planar */
        FIELD_VALUE (closed_b) +        /* 1 */
        (FIELD_VALUE (periodic) << 1) + /* 2 */
        (FIELD_VALUE (rational) << 2) + /* 4 */
        (FIELD_VALUE (weighted) << 4);  /* 16 */
        // ignore method fit points and closed bits
        /*((FIELD_VALUE (splineflags1) & ~5) << 7)*/
      LOG_TRACE ("=> flag: %d [70]\n", FIELD_VALUE (flag));
    }
    FIELD_VECTOR (knots, BD, num_knots, 40);
    REPEAT (num_ctrl_pts, ctrl_pts, Dwg_SPLINE_control_point)
    REPEAT_BLOCK
        SUB_FIELD_3BD_inl (ctrl_pts[rcount1], xyz, 10);
        if (!FIELD_VALUE (weighted))
          FIELD_VALUE (ctrl_pts[rcount1].w) = 0; // skipped when encoding
        else
          SUB_FIELD_BD (ctrl_pts[rcount1], w, 41);
    END_REPEAT_BLOCK
    SET_PARENT_OBJ (ctrl_pts);
    END_REPEAT (ctrl_pts);
  }
  else { // bezier spline, scenario 2
    DECODER {
      // flag 32 in DXF
      FIELD_VALUE (flag) = 8 + 32 + // planar, not rational
        // ignore method fit points and closed bits
        ((FIELD_VALUE (splineflags1) & ~5) << 7);
      LOG_TRACE ("=> flag: %d [70]\n", FIELD_VALUE (flag));
    }
    FIELD_BD (fit_tol, 44); // def: 0.0000001
    FIELD_3BD (beg_tan_vec, 12);
    FIELD_3BD (end_tan_vec, 13);
    FIELD_BL (num_fit_pts, 74);
    FIELD_3DPOINT_VECTOR (fit_pts, num_fit_pts, 11);
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

// 37, 38 and 39 are ACIS entities
#define WIRESTRUCT_fields(name)                       \
  FIELD_RC (name.type, 0);                            \
  FIELD_BL (name.selection_marker, 0);                \
  PRE (R_2004) {                                      \
    FIELD_CAST (name.color, BS, BL, 0);               \
  } else {                                            \
    FIELD_BL (name.color, 0); }                       \
  FIELD_BL (name.acis_index, 0);                      \
  /* TODO: align num_points to 255 */                 \
  FIELD_BL (name.num_points, 0);                      \
  FIELD_3DPOINT_VECTOR (name.points, name.num_points, 0); \
  FIELD_B (name.transform_present, 0);                \
  if (FIELD_VALUE (name.transform_present))           \
    {                                                 \
      FIELD_3BD (name.axis_x, 0);                     \
      FIELD_3BD (name.axis_y, 0);                     \
      FIELD_3BD (name.axis_z, 0);                     \
      FIELD_3BD (name.translation, 0);                \
      FIELD_3BD (name.scale, 0);                      \
      FIELD_B (name.has_rotation, 0);                 \
      FIELD_B (name.has_reflection, 0);               \
      FIELD_B (name.has_shear, 0);                    \
    }

#if defined (IS_DECODER)

#define DECODE_3DSOLID decode_3dsolid (dat, hdl_dat, obj, (Dwg_Entity_3DSOLID *)_obj);

static int decode_3dsolid (Bit_Chain* dat, Bit_Chain* hdl_dat,
                           Dwg_Object *restrict obj,
                           Dwg_Entity_3DSOLID *restrict _obj)
{
  Dwg_Data* dwg = obj->parent;
  BITCODE_BL j;
  BITCODE_BL vcount;
  BITCODE_BL i = 0;
  BITCODE_BL total_size = 0;
  BITCODE_BL num_blocks = 0;
  int acis_data_idx;
  int error = 0;

  FIELD_B (acis_empty, 290);
  if (!FIELD_VALUE (acis_empty))
    {
      FIELD_B (unknown, 0);
      IF_ENCODE_FROM_EARLIER {
        FIELD_VALUE (version) = 1;
      }
      FIELD_BS (version, 70);
      // which is SAT format ACIS 4.0 (since r2000+)
      if (FIELD_VALUE (version) == 1)
        {
          do
            {
              FIELD_VALUE (encr_sat_data) = (char**)
                realloc (FIELD_VALUE (encr_sat_data), (i+1) * sizeof (char*));
              FIELD_VALUE (block_size) = (BITCODE_BL*)
                realloc (FIELD_VALUE (block_size), (i+1) * sizeof (BITCODE_BL));
              FIELD_BL (block_size[i], 0);
              if (FIELD_VALUE (block_size[i]) > 0
                  && AVAIL_BITS (dat) > 8 * FIELD_VALUE (block_size[i]))
                {
                  FIELD_TFv (encr_sat_data[i], FIELD_VALUE (block_size[i]), 1);
                  total_size += FIELD_VALUE (block_size[i]);
                }
              else
                {
                  _obj->encr_sat_data[i] = NULL;
                  _obj->block_size[i] = 0;
                }
            }
          while (FIELD_VALUE (block_size[i++]) > 0 && AVAIL_BITS (dat) >= 16); // crc RS

          // de-obfuscate SAT data
          FIELD_VALUE (acis_data) = (BITCODE_RC *)malloc (total_size + 1);
          num_blocks = i - 1;
          FIELD_VALUE (num_blocks) = num_blocks;
          LOG_TRACE ("num_blocks: " FORMAT_BL "\n", FIELD_VALUE (num_blocks));
          acis_data_idx = 0;
          for ( i = 0; i < num_blocks; i++)
            {
              for (j = 0; j < FIELD_VALUE (block_size[i]); j++)
                {
                  if (FIELD_VALUE (encr_sat_data[i][j]) <= 32)
                    {
                      FIELD_VALUE (acis_data)[acis_data_idx++]
                        = FIELD_VALUE (encr_sat_data[i][j]);
                    }
                  else
                    {
                      FIELD_VALUE (acis_data)[acis_data_idx++]
                        = 159 - FIELD_VALUE (encr_sat_data[i][j]);
                    }
                }
            }
          FIELD_VALUE (acis_data)[acis_data_idx] = '\0';
          // DXF 1 + 3 if >255
          LOG_TRACE ("acis_data:\n%s\n", FIELD_VALUE (acis_data));
        }
      else //if (FIELD_VALUE (version)==2)
        /* version 2, SAB: binary, unencrypted SAT format for ACIS 7.0/ShapeManager.
           ACIS versions:
           R14 release            106   (ACIS 1.6)
           R15 (2000) release     400   (ACIS 4.0)
           R18 (2004) release     20800 (ASM ShapeManager, forked from ACIS 7.0)
           R21 (2007) release     21200
           R24 (2010) release     21500
           R27 (2013) release     21800
           R?? (2018) release            223.0.1.1930
        */
        {
          FIELD_VALUE (block_size) = (BITCODE_BL*)calloc (2, sizeof (BITCODE_BL));
          FIELD_VALUE (encr_sat_data) = NULL;
          //TODO string in strhdl, even <r2007
          // either has_ds_data (r2013+) or the blob is here
          if (!obj->tio.entity->has_ds_data)
            {
              char *p;
              // Note that r2013+ has End-of-ASM-data (not ACIS anymore, but their fork)
              const char end[] = "\016\003End\016\002of\016\004ACIS\r\004data";
              const char end1[] = "\016\003End\016\002of\016\003ASM\r\004data";
              long pos = dat->byte;
              BITCODE_BL size = dat->size - dat->byte - 1;
              FIELD_VALUE (acis_data) = (unsigned char*)calloc (size, 1);
              // Binary SAB. unencrypted, documented format until "End-of-ACIS-data"
              // TODO There exist also SAB streams with a given number of records, but I
              // haven't seen them here. See dwg_convert_SAB_to_SAT1
              // Better read the first header line here, to check for num_records 0.
              // Or even parse the whole SAB format here, and store the SAB different
              // to the ASCII acis_data.
              FIELD_TFF (acis_data, size, 1); // SAB "ACIS BinaryFile"
              LOG_TRACE ("Unknown ACIS 2 SAB sab_size " FORMAT_BL " starting at %ld\n",
                         size, pos);
              if ((p = (char*)memmem (_obj->acis_data, size, end, strlen (end))))
                {
                  size = p - (char*)_obj->acis_data;
                  size += strlen (end);
                  dat->byte = pos + size;
                  _obj->sab_size = size;
                  LOG_TRACE ("Found End-of-ACIS-data. sab_size: " FORMAT_BL ", new pos: %lu\n",
                             size, dat->byte);
                }
              else if ((p = (char*)memmem (_obj->acis_data, size, end1, strlen (end1))))
                {
                  size = p - (char*)_obj->acis_data;
                  size += strlen (end1);
                  dat->byte = pos + size;
                  _obj->sab_size = size;
                  LOG_TRACE ("Found End-of-ASM-data. sab_size: " FORMAT_BL ", new pos: %lu\n",
                             size, dat->byte);
                }
              else
                LOG_TRACE ("No End-of-ACIS or ASM data marker found\n");
              _obj->sab_size = _obj->block_size[0] = size;
            }
          else
            LOG_WARN ("SAB from AcDs blob not yet implemented");
          //total_size = FIELD_VALUE (_obj->block_size[0]);
        }
    }
  return error;
}
#else
#define DECODE_3DSOLID {}
#define FREE_3DSOLID {}
#endif //#if IS_DECODER

#ifdef IS_ENCODER
#define ENCODE_3DSOLID encode_3dsolid(dat, hdl_dat, obj, (Dwg_Entity_3DSOLID *)_obj);
static int encode_3dsolid (Bit_Chain* dat, Bit_Chain* hdl_dat,
                           Dwg_Object *restrict obj,
                           Dwg_Entity_3DSOLID *restrict _obj)
{
  Dwg_Data* dwg = obj->parent;
  BITCODE_BL i = 0;
  BITCODE_BL num_blocks = FIELD_VALUE (num_blocks);
  int acis_data_idx = 0;
  int error = 0;

  FIELD_B (acis_empty, 290);
  if (!FIELD_VALUE (acis_empty))
    {
      FIELD_B (unknown, 0);
      FIELD_BS (version, 70);
      // which is SAT format ACIS 4.0 (since r2000+)
      if (FIELD_VALUE (version) == 1)
        {
          // from decode and indxf we already have all fields.
          // from other importers we have acis_data, but maybe not
          // encr_sat_data.
          if (!num_blocks)
            num_blocks = 100; // max
          if (!FIELD_VALUE (block_size))
            {
              if (!FIELD_VALUE (acis_data))
                {
                  VALUE_RL (0, 0);
                  return error;
                }
              FIELD_VALUE (block_size) = (BITCODE_BL*)calloc (2, sizeof (BITCODE_BL));
              FIELD_VALUE (block_size[0]) = strlen ((char*)FIELD_VALUE (acis_data));
              FIELD_VALUE (block_size[1]) = 0;
              LOG_TRACE ("default block_size[0] = %d\n", (int)FIELD_VALUE (block_size[0]));
              num_blocks = 1;
            }
          LOG_TRACE ("acis_data:\n%s\n", FIELD_VALUE (acis_data));
          for (i = 0; FIELD_VALUE (block_size[i]) && i < num_blocks; i++)
            {
              if (!FIELD_VALUE (encr_sat_data[i]))
                {
                  if (!FIELD_VALUE (acis_data))
                    {
                      VALUE_RL (0, 0);
                      return error;
                    }
                  // global acis_data_idx is need for the global acis_data
                  FIELD_VALUE (encr_sat_data[i])
                    = dwg_encrypt_SAT1 (FIELD_VALUE (block_size[i]),
                                    FIELD_VALUE (acis_data), &acis_data_idx);
                  LOG_TRACE ("dwg_encrypt_SAT1 %d\n", i);
                }
              FIELD_BL (block_size[i], 0);
              FIELD_TF (encr_sat_data[i], FIELD_VALUE (block_size[i]), 1);
            }
          FIELD_BL (block_size[num_blocks], 0);
        }
      else //if (FIELD_VALUE (version)==2)
        {
          if (_obj->acis_data && _obj->sab_size)
            {
              LOG_TRACE ("acis_data [TF %u 1]:\n%.*s\n", (unsigned)FIELD_VALUE (sab_size),
                         15, FIELD_VALUE (acis_data));
              // Binary SAB, unencrypted
              if (obj->tio.entity->has_ds_data)
                {
                  LOG_WARN ("Disable SAB from AcDs blob"); // TODO AcDs support
                  obj->tio.entity->has_ds_data = 0;
                }
              bit_write_TF (dat, _obj->acis_data, _obj->sab_size);
              LOG_TRACE_TF (&_obj->acis_data[15], (int)(_obj->sab_size - 15));
            }
        }
    }
  return error;
}
#else
#define ENCODE_3DSOLID {}
#define FREE_3DSOLID {}
#endif //#if IS_ENCODER

#ifdef IS_FREE
#undef FREE_3DSOLID
#define FREE_3DSOLID {} free_3dsolid (obj, (Dwg_Entity_3DSOLID *)_obj);
static int free_3dsolid (Dwg_Object *restrict obj, Dwg_Entity_3DSOLID *restrict _obj)
{
  int error = 0;
  Bit_Chain *dat = &pdat;

  if (!FIELD_VALUE (acis_empty))
    {
      if (FIELD_VALUE (encr_sat_data))
        {
          for (BITCODE_BL i = 0; i <= FIELD_VALUE (num_blocks); i++)
            {
              if (FIELD_VALUE (encr_sat_data[i]) != NULL)
                FIELD_TF (encr_sat_data[i], block_size[i], 0);
            }
        }
      FREE_IF (FIELD_VALUE (encr_sat_data));
      FREE_IF (FIELD_VALUE (block_size));
    }
  FREE_IF (FIELD_VALUE (acis_data));
  return error;
}
#else
#define FREE_3DSOLID {}
#endif

#define COMMON_3DSOLID                                                                             \
  FIELD_B (wireframe_data_present, 0);                                                             \
  if (FIELD_VALUE (wireframe_data_present))                                                        \
    {                                                                                              \
      FIELD_B (point_present, 0);                                                                  \
      if (FIELD_VALUE (point_present))                                                             \
        {                                                                                          \
          FIELD_3BD (point, 0);                                                                    \
        }                                                                                          \
      else                                                                                         \
        {                                                                                          \
          FIELD_VALUE (point.x) = 0;                                                               \
          FIELD_VALUE (point.y) = 0;                                                               \
          FIELD_VALUE (point.z) = 0;                                                               \
        }                                                                                          \
      FIELD_BL (isolines, 0);                                                                      \
      FIELD_B (isoline_present, 0);                                                                \
      if (FIELD_VALUE (isoline_present))                                                           \
        {                                                                                          \
          FIELD_BL (num_wires, 0);                                                                 \
          REPEAT (num_wires, wires, Dwg_3DSOLID_wire)                                              \
          REPEAT_BLOCK                                                                             \
              WIRESTRUCT_fields (wires[rcount1])                                                   \
          END_REPEAT_BLOCK                                                                         \
          SET_PARENT (wires, (Dwg_Entity__3DSOLID*)_obj)                                           \
          END_REPEAT (wires);                                                                      \
          FIELD_BL (num_silhouettes, 0);                                                           \
          REPEAT (num_silhouettes, silhouettes, Dwg_3DSOLID_silhouette)                            \
          REPEAT_BLOCK                                                                             \
              SUB_FIELD_BL (silhouettes[rcount1], vp_id, 0);                                       \
              SUB_FIELD_3BD (silhouettes[rcount1], vp_target, 0);   /* ?? */                       \
              SUB_FIELD_3BD (silhouettes[rcount1], vp_dir_from_target, 0);                         \
              SUB_FIELD_3BD (silhouettes[rcount1], vp_up_dir, 0);                                  \
              SUB_FIELD_B (silhouettes[rcount1], vp_perspective, 0);                               \
              SUB_FIELD_B (silhouettes[rcount1], has_wires, 0);                                    \
              if (_obj->silhouettes[rcount1].has_wires)                                            \
                {                                                                                  \
                  SUB_FIELD_BL (silhouettes[rcount1], num_wires, 0);                               \
                  REPEAT2 (silhouettes[rcount1].num_wires, silhouettes[rcount1].wires, Dwg_3DSOLID_wire) \
                  REPEAT_BLOCK                                                                     \
                      WIRESTRUCT_fields (silhouettes[rcount1].wires[rcount2])                      \
                  END_REPEAT_BLOCK                                                                 \
                  SET_PARENT (silhouettes[rcount1].wires, (Dwg_Entity__3DSOLID*)_obj)              \
                  END_REPEAT (silhouettes[rcount1].wires);                                         \
                }                                                                                  \
          END_REPEAT_BLOCK                                                                         \
          SET_PARENT (silhouettes, (Dwg_Entity__3DSOLID*)_obj)                                     \
          END_REPEAT (silhouettes);                                                                \
        }                                                                                          \
      }                                                                                            \
                                                                                                   \
    FIELD_B (acis_empty_bit, 0); /* ?? */                                                          \
    if (FIELD_VALUE (version) > 1) {                                                               \
      SINCE (R_2007) {                                                                             \
        FIELD_BL (num_materials, 0);                                                               \
        REPEAT (num_materials, materials, Dwg_3DSOLID_material)                                    \
        REPEAT_BLOCK                                                                               \
            SUB_FIELD_BL (materials[rcount1], array_index, 0);                                     \
            SUB_FIELD_BL (materials[rcount1], mat_absref, 0);   /* ?? */                           \
            SUB_FIELD_HANDLE (materials[rcount1], material_handle, 5, 0);                          \
        END_REPEAT_BLOCK                                                                           \
        SET_PARENT (materials, (Dwg_Entity__3DSOLID*)_obj)                                         \
        END_REPEAT (materials);                                                                    \
      }                                                                                            \
    }                                                                                              \
    SINCE (R_2013) {                                                                               \
      FIELD_B (has_revision_guid, 0);                                                              \
      DXF {                                                                                        \
        FIELD_TFF (revision_guid, 38, 2);                                                          \
      }                                                                                            \
      else {                                                                                       \
        FIELD_BL (revision_major, 0);                                                              \
        FIELD_BS (revision_minor1, 0);                                                             \
        FIELD_BS (revision_minor2, 0);                                                             \
        FIELD_TFFx (revision_bytes, 8, 0);                                                         \
        DECODER {                                                                                  \
          dxf_3dsolid_revisionguid ((Dwg_Entity_3DSOLID*)_obj);                                    \
        }                                                                                          \
      }                                                                                            \
      FIELD_BL (end_marker, 0);                                                                    \
    }                                                                                              \
                                                                                                   \
    COMMON_ENTITY_HANDLE_DATA;                                                                     \
    if (FIELD_VALUE (version) > 1) {                                                               \
      SUBCLASS (AcDb3dSolid);                                                                      \
      SINCE (R_2007) {                                                                             \
        FIELD_HANDLE (history_id, 4, 350);                                                         \
      }                                                                                            \
    }

#define ACTION_3DSOLID \
  SUBCLASS (AcDbModelerGeometry); \
  DXF_OR_PRINT { \
    DXF_3DSOLID \
  } \
  DECODER { \
    DECODE_3DSOLID \
  } \
  ENCODER { \
    ENCODE_3DSOLID \
  } \
  JSON { \
    JSON_3DSOLID \
  } \
  FREE_3DSOLID \
  COMMON_3DSOLID

/*(37)*/
DWG_ENTITY (REGION)
  ACTION_3DSOLID;
DWG_ENTITY_END

/*(38)*/
DWG_ENTITY (_3DSOLID)
  ACTION_3DSOLID;
DWG_ENTITY_END

/*(39)*/
DWG_ENTITY (BODY)
  ACTION_3DSOLID;
DWG_ENTITY_END

/*(40) r13+ only */
DWG_ENTITY (RAY)
  SUBCLASS (AcDbRay)
  FIELD_3BD (point, 10);
  FIELD_3BD (vector, 11);
  COMMON_ENTITY_HANDLE_DATA;
DWG_ENTITY_END

/*(41) r13+ only*/
DWG_ENTITY (XLINE)
  SUBCLASS (AcDbXline)
  FIELD_3BD (point, 10);
  FIELD_3BD (vector, 11);
  COMMON_ENTITY_HANDLE_DATA;
DWG_ENTITY_END

/*(42)*/
DWG_OBJECT (DICTIONARY)

#ifdef IS_DXF
  SUBCLASS (AcDbDictionary)
  SINCE (R_13c3)
    FIELD_RC0 (hard_owner, 280);
  SINCE (R_2000)
    FIELD_BS0 (cloning, 281);
#else
  FIELD_BL (numitems, 0);
  SINCE (R_13c3) {
    SINCE (R_2000)
      {
        IF_ENCODE_FROM_EARLIER {
          FIELD_VALUE (cloning) = FIELD_VALUE (hard_owner) & 0xffff;
        }
        FIELD_BS (cloning, 281);
      }
    if (dat->version != R_13c3 || dwg->header.maint_version > 4)
      FIELD_RC (hard_owner, 280);
  }
  VALUEOUTOFBOUNDS (numitems, 10000)
#endif

#ifdef IS_DXF
  if (FIELD_VALUE (itemhandles) && FIELD_VALUE (texts)) {
     REPEAT (numitems, texts, T)
      {
        int dxf = FIELD_VALUE (hard_owner) & 1 ? 360 : 350;
        // ACAD_SORTENTS, ACAD_FILTER and SPATIAL are always hard 360
        if (dxf == 350 && dat->from_version >= R_2007)
          {
            char *text = FIELD_VALUE (texts[rcount1]);
#ifdef HAVE_NATIVE_WCHAR2
            const wchar_t *wstr1 = L"ACAD_SORTENTS";
            const wchar_t *wstr2 = L"ACAD_FILTER";
            const wchar_t *wstr3 = L"SPATIAL";
#else
            const uint8_t wstr1[]
                = { 'A', 0, 'C', 0, 'A', 0, 'D', 0, '_', 0, 'S', 0,
                    'O', 0, 'R', 0, 'T', 0, 'E', 0, 'N', 0, 'T', 0,  'S',
                     0,  0,  0 };
            const uint8_t wstr2[]
                = { 'A', 0, 'C', 0, 'A', 0, 'D', 0, '_', 0, 'F', 0,
                    'I', 0, 'L', 0, 'T', 0, 'E', 0, 'R', 0,  0,  0 };
            const uint8_t wstr3[] = { 'S', 0, 'P', 0, 'A', 0, 'T', 0,
                                      'I', 0, 'A', 0, 'L', 0,  0,  0 };
#endif
            if (bit_eq_TU (text, (BITCODE_TU)wstr1) ||
                bit_eq_TU (text, (BITCODE_TU)wstr2) ||
                bit_eq_TU (text, (BITCODE_TU)wstr3))
              dxf = 360;
          }
        else if (dxf == 350)
          {
            char *text = FIELD_VALUE (texts[rcount1]);
            if (strEQc (text, "ACAD_SORTENTS") ||
                strEQc (text, "ACAD_FILTER") ||
                strEQc (text, "SPATIAL"))
              dxf = 360;
          }
        FIELD_T (texts[rcount1], 3);
        VALUE_HANDLE (_obj->itemhandles[rcount1], itemhandles, 2, dxf);
      }
      END_REPEAT (texts)
    }
#elif defined (IS_JSON)
  // use a simple map: "items": { "text": [ handle ], ... }
  // the texts are all unique
  RECORD (items);
  if (FIELD_VALUE (itemhandles) && FIELD_VALUE (texts)) {
    for (rcount1 = 0; rcount1 < _obj->numitems; rcount1++)
      {
        FIRSTPREFIX
        VALUE_T (_obj->texts[rcount1]);
        fprintf (dat->fh, ": ");
        VALUE_HANDLE (_obj->itemhandles[rcount1], itemhandles, 2, 350);
      }
  }
  ENDRECORD()
#else
  FIELD_VECTOR_T (texts, T, numitems, 3);
#endif

  START_OBJECT_HANDLE_STREAM;
#if !defined(IS_DXF) && !defined (IS_JSON)
  // or DXF 360 if hard_owner
  HANDLE_VECTOR_N (itemhandles, FIELD_VALUE (numitems), 2, 350);
#endif

DWG_OBJECT_END

// DXF as ACDBDICTIONARYWDFLT
DWG_OBJECT (DICTIONARYWDFLT)

#ifdef IS_DXF
  SUBCLASS (AcDbDictionary)
  SINCE (R_2000)
  {
    if (FIELD_VALUE (hard_owner))
      FIELD_RC (hard_owner, 280);
    FIELD_BS (cloning, 281);
  }
#else
  FIELD_BL (numitems, 0);
  VERSION (R_14)
    FIELD_RL (cloning_r14, 0); // always 0
  SINCE (R_2000)
    {
      IF_ENCODE_FROM_EARLIER {
        FIELD_VALUE (cloning) = FIELD_VALUE (cloning_r14) & 0xffff;
      }
      FIELD_BS (cloning, 281);
      FIELD_RC (hard_owner, 0);
    }
#endif
  VALUEOUTOFBOUNDS (numitems, 10000)
#ifdef IS_DXF
    if (FIELD_VALUE (itemhandles) && FIELD_VALUE (texts)) {
      REPEAT (numitems, texts, T)
      {
        int dxf = FIELD_VALUE (hard_owner) & 1 ? 360 : 350;
        FIELD_T (texts[rcount1], 3);
        VALUE_HANDLE (_obj->itemhandles[rcount1], itemhandles, 2, dxf);
      }
      END_REPEAT (texts)
    }
#elif defined (IS_JSON)
  // use a simple map: "items": { "text": [ handle ], ... }
  // the texts are all unique
  RECORD (items);
  if (FIELD_VALUE (itemhandles) && FIELD_VALUE (texts)) {
    for (rcount1 = 0; rcount1 < _obj->numitems; rcount1++)
      {
        FIRSTPREFIX
        VALUE_T (_obj->texts[rcount1]);
        fprintf (dat->fh, ": ");
        VALUE_HANDLE (_obj->itemhandles[rcount1], itemhandles, 2, 350);
      }
  }
  ENDRECORD()
#else
  FIELD_VECTOR_T (texts, T, numitems, 3);
#endif

  START_OBJECT_HANDLE_STREAM;
#if !defined(IS_DXF) && !defined (IS_JSON)
  IF_FREE_OR_SINCE (R_2000)
    {
      HANDLE_VECTOR_N (itemhandles, FIELD_VALUE (numitems), 2, 350);
    }
#endif
  SUBCLASS (AcDbDictionaryWithDefault)
  FIELD_HANDLE (defaultid, 5, 340);

DWG_OBJECT_END

/*(43) pre-R13c4 OLE 1 only.
 converted on opening to OLE2FRAME on demand
 */
DWG_ENTITY (OLEFRAME)

  //SUBCLASS (AcDbFrame)
  //SUBCLASS (AcDbOleFrame)
  FIELD_BS (flag, 70);
  SINCE (R_2000) {
    FIELD_BS (mode, 0);
  }

  ENCODER {
    if (FIELD_VALUE (data_size) && !FIELD_VALUE (data))
      FIELD_VALUE (data_size) = 0;
  }
#ifndef IS_JSON
  FIELD_BL (data_size, 90);
#endif
  FIELD_BINARY (data, FIELD_VALUE (data_size), 310);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/*(44)*/
DWG_ENTITY (MTEXT)

  DXF { UNTIL (R_2007) {
    FIELD_HANDLE (style, 5, 7);
  } }
  SUBCLASS (AcDbMText)
  FIELD_3BD (insertion_pt, 10);
  FIELD_3BD (extrusion, 210);
  FIELD_3BD (x_axis_dir, 11);

  FIELD_BD (rect_width, 41);
  SINCE (R_2007) {
    FIELD_BD (rect_height, 46);
  }

  FIELD_BD (text_height, 40);
  FIELD_BS (attachment, 71);
  FIELD_BS (drawing_dir, 72);
  FIELD_BD (extents_height, 42);
  FIELD_BD (extents_width, 43); // nan's!
  FIELD_T (text, 1); // or 3 if >250
  /* doc error:
  UNTIL (R_2007) {
    FIELD_HANDLE (style, 5, 0);
  }
  */

  SINCE (R_2000)
    {
      FIELD_BS (linespace_style, 73);
      FIELD_BD (linespace_factor, 44);
      FIELD_B (unknown_bit, 0); //annotative?
    }

  SINCE (R_2004)
    {
      FIELD_BL (bg_fill_flag, 90);
      if (FIELD_VALUE (bg_fill_flag) & (dat->version <= R_2018 ? 1 : 0x10))
        {
          FIELD_BL (bg_fill_scale, 45); // def: 1.5
          FIELD_CMC (bg_fill_color, 63);
          FIELD_BL (bg_fill_trans, 441);
        }
    }
  SINCE (R_2018)
  {
    FIELD_B (annotative, 0);
    FIELD_BS (class_version, 0); // def: 0
    VALUEOUTOFBOUNDS (class_version, 10)
    FIELD_B (default_flag, 0);   // def: 1
    // redundant fields
    FIELD_BL (attachment, 71);
    FIELD_3BD (x_axis_dir, 11);
    FIELD_3BD (insertion_pt, 10);
    FIELD_BD (rect_width, 41);
    FIELD_BD (rect_height, 0);
    FIELD_BD (extents_width, 42);
    FIELD_BD (extents_height, 43);
    // end redundant fields

    DECODE_UNKNOWN_BITS
    FIELD_BL (column_type, 75);
    if (FIELD_VALUE (column_type)) //DEBUGGING
      {
        FIELD_BL (num_column_heights, 76);
        FIELD_BD (column_width, 48);
        FIELD_BD (gutter, 49);
        FIELD_B (auto_height, 79);
        FIELD_B (flow_reversed, 74);
        if (!FIELD_VALUE (auto_height) && FIELD_VALUE (column_type) == 2)
          {
            FIELD_VECTOR (column_heights, BD, num_column_heights, 50);
          }
      }
  }

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (style, 5, 0);
  SINCE (R_2018)
    FIELD_HANDLE (appid, 5, 0);

DWG_ENTITY_END

/* (45) unstable */
DWG_ENTITY (LEADER)

  //SUBCLASS (AcDbCurve)
  SUBCLASS (AcDbLeader)
  FIELD_B (unknown_bit_1, 0);
  FIELD_BS (path_type, 72);
  FIELD_BS (annot_type, 73); //0: text, 1: tol, 2: insert, 3 (def): none
  FIELD_BL (num_points, 76);
  FIELD_3DPOINT_VECTOR (points, num_points, 10);
  FIELD_3DPOINT (origin, 0);
  FIELD_3DPOINT (extrusion, 210);
  FIELD_3DPOINT (x_direction, 211);
  FIELD_3DPOINT (inspt_offset, 212);

  VERSIONS (R_14, R_2007) {
    FIELD_3DPOINT (endptproj, 0);
  }
  VERSIONS (R_13, R_14) {
    FIELD_BD (dimgap, 0);
  }

  FIELD_BD (box_height, 40);
  FIELD_BD (box_width , 41);
  FIELD_B (hookline_dir, 74);
  FIELD_B (arrowhead_on, 71);
  FIELD_BS (arrowhead_type, 0);

  VERSIONS (R_13, R_14)
    {
      FIELD_BD (dimasz, 0);
      FIELD_B (unknown_bit_2, 0);
      FIELD_B (unknown_bit_3, 0);
      FIELD_BS (unknown_short_1, 0);
      FIELD_BS (byblock_color, 77);
      FIELD_B (hookline_on, 75);
      FIELD_B (unknown_bit_5, 0);
    }

  SINCE (R_2000)
    {
      FIELD_B (hookline_on, 75);
      FIELD_B (unknown_bit_5, 0);
    }

  COMMON_ENTITY_HANDLE_DATA;
  SINCE (R_13) {
    FIELD_HANDLE (associated_annotation, 2, 340);
  }
  FIELD_HANDLE (dimstyle, 5, 3); // ODA bug, DXF documented as 2

DWG_ENTITY_END

/*(46)*/
DWG_ENTITY (TOLERANCE)

  SUBCLASS (AcDbFcf)   // for Feature Control Frames
  DXF { FIELD_HANDLE (dimstyle, 5, 3); }
  VERSIONS (R_13, R_14)
    {
      FIELD_BS (unknown_short, 0); //spec-typo? Spec says S instead of BS.
      FIELD_BD (height, 0);
      FIELD_BD (dimgap, 0);
    }

  FIELD_3DPOINT (ins_pt, 10);
  FIELD_3DPOINT (x_direction, 11);
  DXF  { FIELD_BE (extrusion, 210); }
  else { FIELD_3DPOINT (extrusion, 210); }
  FIELD_T (text_value, 1);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);

DWG_ENTITY_END

/*(47)*/
DWG_ENTITY (MLINE)

  SUBCLASS (AcDbMline)
  DXF { FIELD_HANDLE (mlinestyle, 5, 340); }
  FIELD_BD (scale, 40);
  FIELD_RC (justification, 70); /* spec-typo? Spec says EC instead of RC */
  FIELD_3DPOINT (base_point, 10);
  FIELD_3DPOINT (extrusion, 210);
  FIELD_BS (flags, 71);
  FIELD_RCu (num_lines, 73); //aka linesinstyle
  FIELD_BS (num_verts, 72);
  VALUEOUTOFBOUNDS (num_verts, 5000)
  VALUEOUTOFBOUNDS (num_lines, 1000)

  REPEAT (num_verts, verts, Dwg_MLINE_vertex)
  REPEAT_BLOCK
      SUB_FIELD_3DPOINT (verts[rcount1], vertex, 11);
      SUB_FIELD_3DPOINT (verts[rcount1], vertex_direction, 12);
      SUB_FIELD_3DPOINT (verts[rcount1], miter_direction, 13);
      FIELD_VALUE (verts[rcount1].num_lines) = FIELD_VALUE (num_lines);

      REPEAT2 (num_lines, verts[rcount1].lines, Dwg_MLINE_line)
      REPEAT_BLOCK
          SUB_FIELD_BS (verts[rcount1].lines[rcount2], num_segparms, 74);
          VALUEOUTOFBOUNDS (verts[rcount1].lines[rcount2].num_segparms, 5000)
          FIELD_VECTOR (verts[rcount1].lines[rcount2].segparms, BD, verts[rcount1].lines[rcount2].num_segparms, 41)

          SUB_FIELD_BS (verts[rcount1].lines[rcount2], num_areafillparms, 75);
          VALUEOUTOFBOUNDS (verts[rcount1].lines[rcount2].num_areafillparms, 5000)
          FIELD_VECTOR (verts[rcount1].lines[rcount2].areafillparms, BD, verts[rcount1].lines[rcount2].num_areafillparms, 42)
      END_REPEAT_BLOCK
      SET_PARENT (verts[rcount1].lines, &_obj->verts[rcount1])
      END_REPEAT (verts[rcount1].lines);
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (verts)
  END_REPEAT (verts);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (mlinestyle, 5, 0);

DWG_ENTITY_END

/*(48)*/
DWG_OBJECT (BLOCK_CONTROL)

  DXF {
    // plus MSPACE and PSPACE
    VALUE_RL (FIELD_VALUE (num_entries) +
              (dwg->header_vars.BLOCK_RECORD_PSPACE ? 2 : 1), 70);
  } else {
    FIELD_BL (num_entries, 70);
  }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);
  FIELD_HANDLE (model_space, 3, 0);
  FIELD_HANDLE (paper_space, 3, 0);

DWG_OBJECT_END

/* (49/1) */
DWG_OBJECT (BLOCK_HEADER)

  //DXF: the name must be from the block_entity!
  COMMON_TABLE_FLAGS (Block)
  DXF {
    // not allowed to be skipped, can be 0
    VALUE_HANDLE (_obj->layout, layout, 5, 340);
    // The DXF TABLE.BLOCK_RECORD only has this. More later in the BLOCKS section.
    return 0;
  }

  PRE (R_13)
  {
    FIELD_RD (base_pt.z, 30);
    FIELD_2RD (base_pt, 10);
    FIELD_RC (block_scaling, 0);
    FIELD_CAST (num_owned, RS, BL, 0);
    FIELD_RC (flag2, 0);
    FIELD_CAST (num_inserts, RS, RL, 0);
    FIELD_RS (flag3, 0);

    FIELD_VALUE (anonymous)    = FIELD_VALUE (flag) & 1;
    FIELD_VALUE (hasattrs)     = FIELD_VALUE (flag) & 2;
    FIELD_VALUE (blkisxref)    = FIELD_VALUE (flag) & 4;
    FIELD_VALUE (xrefoverlaid) = FIELD_VALUE (flag) & 8;
  }
  SINCE (R_13) {
    FIELD_B (anonymous, 0); // bit 1
    FIELD_B (hasattrs, 0);  // bit 2
    FIELD_B (blkisxref, 0); // bit 4
    FIELD_B (xrefoverlaid, 0); // bit 8
  }
  SINCE (R_2000) {
    FIELD_B (loaded_bit, 0); // bit 32
  }
  SINCE (R_13) {
    FIELD_VALUE (flag) |= FIELD_VALUE (anonymous) |
                          FIELD_VALUE (hasattrs) << 1 |
                          FIELD_VALUE (blkisxref) << 2 |
                          FIELD_VALUE (xrefoverlaid) << 3;
  }
  SINCE (R_2004) { // but not in 2007
    FIELD_BL (num_owned, 0);
    if (FIELD_VALUE (num_owned) > 0xf00000)
      {
        LOG_WARN ("Unreasonable high num_owned value")
      }
  }

  SINCE (R_13) {
    FIELD_3DPOINT (base_pt, 10);
    FIELD_T (xref_pname, 1); // and 3
  }

  IF_FREE_OR_SINCE (R_2000)
    {
      FIELD_NUM_INSERTS (num_inserts, RL, 0);
      FIELD_T (description, 4);

#ifndef IS_JSON
      FIELD_BL (preview_size, 0);
#endif
      VALUEOUTOFBOUNDS (preview_size, 0xa00000)
      else
        {
          FIELD_BINARY (preview, FIELD_VALUE (preview_size), 310);
        }
    }

  SINCE (R_2007)
    {
      FIELD_BS (insert_units, 70);
      FIELD_B (explodable, 280);
      FIELD_RC (block_scaling, 281);
    }

  SINCE (R_13) {
    START_OBJECT_HANDLE_STREAM;
    FIELD_HANDLE (block_entity, 3, 0);
  }

  VERSIONS (R_13, R_2000)
    {
      if (!FIELD_VALUE (blkisxref) && !FIELD_VALUE (xrefoverlaid))
        {
          FIELD_HANDLE (first_entity, 4, 0);
          FIELD_HANDLE (last_entity, 4, 0);
        }
    }
  IF_FREE_OR_SINCE (R_2004)
    {
      if (FIELD_VALUE (num_owned) < 0xf00000) {
        HANDLE_VECTOR (entities, num_owned, 4, 0);
      }
    }
  SINCE (R_13) {
    FIELD_HANDLE (endblk_entity, 3, 0);
  }
  IF_FREE_OR_SINCE (R_2000)
    {
      if (FIELD_VALUE (num_inserts) && FIELD_VALUE (num_inserts) < 0xf00000) {
        HANDLE_VECTOR (inserts, num_inserts, 4, 0);
      }
      FIELD_HANDLE (layout, 5, 340);
    }

DWG_OBJECT_END

/*(50)*/
DWG_OBJECT (LAYER_CONTROL)

  DXF {
    // minus 0
    VALUE_RL (FIELD_VALUE (num_entries) - 1, 70);
  } else {
    FIELD_BL (num_entries, 70);
  }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* (51/2) */
DWG_OBJECT (LAYER)

  COMMON_TABLE_FLAGS (Layer);
  PRE (R_13)
  {
    FIELD_RS (color_rs, 62);  // color
    FIELD_RS (ltype_rs, 7);   // style

    DECODER {
      FIELD_VALUE (on)            = FIELD_VALUE (color_rs) >= 0;
      FIELD_VALUE (frozen)        = FIELD_VALUE (flag) & 1;
      FIELD_VALUE (frozen_in_new) = FIELD_VALUE (flag) & 2;
      FIELD_VALUE (locked)        = FIELD_VALUE (flag) & 4;
    }
  }
  VERSIONS (R_13, R_14)
  {
    FIELD_B (frozen, 0); // bit 1
    FIELD_B (on, 0);     // really: negate the color
    FIELD_B (frozen_in_new, 0);
    FIELD_B (locked, 0);
  }
  SINCE (R_2000) {
    int flag = FIELD_VALUE (flag);
    FIELD_BSx (flag, 0); // 70,290,370
    flag = FIELD_VALUE (flag);
    // contains frozen (1 bit), on (2 bit), frozen by default in new viewports (4 bit),
    // locked (8 bit), plotting flag (16 bit), and linewt (mask with 0x03E0)
    //FIELD_VALUE (flag) = (BITCODE_RC)FIELD_VALUE (flag_s) & 0xff;
    FIELD_VALUE (frozen) = flag & 1;
    FIELD_VALUE (on) = !(flag & 2);
    FIELD_VALUE (frozen_in_new) = flag & 4;
    FIELD_VALUE (locked) = flag & 8;
    FIELD_VALUE (plotflag) = flag & (1<<15) ? 1 : 0;
    FIELD_VALUE (linewt) = (flag & 0x03E0) >> 5;
    DXF_OR_PRINT {
      int lw = dxf_cvt_lweight (FIELD_VALUE (linewt));
      FIELD_B (plotflag, 290);
      JSON {
        FIELD_RC (linewt, 370);
      } else {
        KEY (linewt); VALUE_RC ((signed char)lw, 370);
      }
    }
  }
  FIELD_CMC (color, 62);
  VERSIONS (R_13, R_14)
  {
    DECODER { FIELD_VALUE (on) = FIELD_VALUE (color.index) >= 0; }
    FIELD_VALUE (flag) |= FIELD_VALUE (frozen) |
      (FIELD_VALUE (frozen_in_new) << 1) |
      (FIELD_VALUE (locked) << 2) |
      (FIELD_VALUE (color.index) < 0 ? 32 : 0);
  }

  START_OBJECT_HANDLE_STREAM;
  SINCE (R_2000) {
    FIELD_HANDLE (plotstyle, 5, 390);
  }
  SINCE (R_2007) {
    FIELD_HANDLE (material, 5, 347);
  }
  FIELD_HANDLE (ltype, 5, 6);
  //TODO handle: DXF 370
  SINCE (R_2013) {
    FIELD_HANDLE (visualstyle, 5, 348);
  }
DWG_OBJECT_END

/* STYLE table (52) */
DWG_OBJECT (STYLE_CONTROL)

  DXF {
    // minus Standard
    VALUE_RL (FIELD_VALUE (num_entries) - 1, 70);
  } else {
    FIELD_BL (num_entries, 70); //RC?
  }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* (53/3) preR13+DXF: STYLE, documented as SHAPEFILE */
DWG_OBJECT (STYLE)

  COMMON_TABLE_FLAGS (TextStyle)

  SINCE (R_13)
  {
    FIELD_B (is_shape, 0);        //wrong oda doc
    FIELD_B (is_vertical, 0);     //
    FIELD_VALUE (flag) |= (FIELD_VALUE (is_vertical) ? 4 : 0) +
                          (FIELD_VALUE (is_shape) ? 1 : 0);
  }
  PRE (R_13)
  {
    FIELD_RD (text_size, 40);
    FIELD_RD (width_factor, 41);
    FIELD_RD (oblique_angle, 50);
    FIELD_RC (generation, 71);
    FIELD_RD (last_height, 42);
    FIELD_TFv (font_file, 64, 3);
    FIELD_TFv (bigfont_file, 64, 4);
    FIELD_VALUE (is_shape)    = FIELD_VALUE (flag) & 4;
    FIELD_VALUE (is_vertical) = FIELD_VALUE (flag) & 1;
  }
  LATER_VERSIONS
  {
    FIELD_BD (text_size, 40);
    FIELD_BD (width_factor, 41); // xScale
    FIELD_BD (oblique_angle, 50);
    FIELD_RC (generation, 71);
    FIELD_BD (last_height, 42);
    FIELD_T (font_file, 3);
    FIELD_T (bigfont_file, 4);
    //1001 1000 1071 mandatory r2007+ if .ttf
    //long truetype font’s pitch and family, charset, and italic and bold flags
    DXF {
      char _buf[256];
      char *s;
      if (FIELD_VALUE (font_file))
        {
          SINCE (R_2007) {
            s = bit_convert_TU ((BITCODE_TU)FIELD_VALUE (font_file));
            strncpy (_buf, s, 255);
            free (s);
          }
          else {
            strncpy (_buf, FIELD_VALUE (font_file), 255);
          }
          _buf[255] = '\0';
          if ((s = strstr (_buf, ".ttf")) ||
              (s = strstr (_buf, ".TTF")))
            {
              *s = 0;
              VALUE_TFF ("ACAD", 1001);
              VALUE_TFF (_buf, 1000); // typeface
              VALUE_RL (34, 1071); // ttf_flags
            }
        }
    }

    START_OBJECT_HANDLE_STREAM;
  }

DWG_OBJECT_END

//(54): Unknown
//(55): Unknown

/*(56)*/
DWG_OBJECT (LTYPE_CONTROL)

  // DXF minus ByLayer/ByBlock/Continuous ?
  FIELD_BS (num_entries, 70);

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);
  FIELD_HANDLE (byblock, 3, 0);
  FIELD_HANDLE (bylayer, 3, 0);

DWG_OBJECT_END

/* (57/5) 
 * Unstable, ACAD import errors
 */
DWG_OBJECT (LTYPE)

  COMMON_TABLE_FLAGS (Linetype)

  PRE (R_13) {
    FIELD_TFv (description, 48, 3);
  }
  LATER_VERSIONS {
    FIELD_T (description, 3);
    FIELD_BD (pattern_len, 0); // total length
  }
  FIELD_RC (alignment, 72);
  FIELD_RCu (num_dashes, 73);
  DXF { FIELD_BD (pattern_len, 40); }
  REPEAT (num_dashes, dashes, Dwg_LTYPE_dash)
  REPEAT_BLOCK
      SUB_FIELD_BD (dashes[rcount1],length, 49);
      DXF {
        SUB_FIELD_BS (dashes[rcount1],shape_flag, 74);
        if (_obj->dashes[rcount1].shape_flag) // eg BATTING
          {
            SUB_FIELD_BS (dashes[rcount1],complex_shapecode, 75);
            SUB_FIELD_HANDLE (dashes[rcount1],style, 5, 340);
            SUB_FIELD_BD (dashes[rcount1],scale, 46);
            SUB_FIELD_BD (dashes[rcount1],rotation, 50); // absolute or relative
            SUB_FIELD_RD (dashes[rcount1],x_offset, 44);
            SUB_FIELD_RD (dashes[rcount1],y_offset, 45);
            if (_obj->dashes[rcount1].shape_flag & 2) // 10
              {
                SUB_FIELD_T (dashes[rcount1],text, 9);
              }
          }
      } else {
        SUB_FIELD_BS (dashes[rcount1],complex_shapecode, 75);
        SUB_FIELD_HANDLE (dashes[rcount1],style, 5, 340);
        SUB_FIELD_RD (dashes[rcount1],x_offset, 44);
        SUB_FIELD_RD (dashes[rcount1],y_offset, 45);
        SUB_FIELD_BD (dashes[rcount1],scale, 46);
        SUB_FIELD_BD (dashes[rcount1],rotation, 50);
        SUB_FIELD_BS (dashes[rcount1],shape_flag, 74);
      }
      DECODER {
        if (FIELD_VALUE (dashes[rcount1].shape_flag) & 2)
          FIELD_VALUE (has_strings_area) = 1;
        PRE (R_13) {
          FIELD_VALUE (pattern_len) += FIELD_VALUE (dashes[rcount1].length);
        }
      }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (dashes)
  END_REPEAT (dashes);

  UNTIL (R_2004) {
    JSON {
      if (FIELD_VALUE (has_strings_area))
        FIELD_BINARY (strings_area, 256, 0);
    }
    else {
      FIELD_BINARY (strings_area, 256, 0);
      DECODER {
        for (rcount1 = 0; rcount1 < _obj->num_dashes; rcount1++)
          {
            if (_obj->dashes[rcount1].shape_flag & 2)
              {
                static int dash_i = 0;
                _obj->dashes[rcount1].text = (char*)&_obj->strings_area[dash_i];
                dash_i += strlen (_obj->dashes[rcount1].text) + 1;
              }
          }
      }
    }
  }
  LATER_VERSIONS {
    if (FIELD_VALUE (has_strings_area)) {
      FIELD_BINARY (strings_area, 512, 0);
      DECODER {
        for (rcount1 = 0; rcount1 < _obj->num_dashes; rcount1++)
          {
            if (_obj->dashes[rcount1].shape_flag & 2)
              {
                static int dash_i = 0;
                _obj->dashes[rcount1].text = (char*)&_obj->strings_area[dash_i];
                dash_i += bit_wcs2len ((BITCODE_TU)_obj->dashes[rcount1].text) + 2;
              }
          }
      }
    }
  }

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

//(58): Unknown
//(59): Unknown

/*(60)*/
DWG_OBJECT (VIEW_CONTROL)

  DXF {
    // minus ?
    VALUE_RL (FIELD_VALUE (num_entries) - 1, 70);
  } else {
    FIELD_BL (num_entries, 70);
  }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* (61/6) */
DWG_OBJECT (VIEW)

  COMMON_TABLE_FLAGS (View)

  // subclass AbstractViewTableRecord:
  PRE (R_13)
  {
    FIELD_RD (VIEWSIZE, 40);
    FIELD_2RD (VIEWCTR, 10);
    FIELD_RD (view_width, 41);
    DXF {
      FIELD_3RD (VIEWDIR, 11);
    }
    SINCE (R_10) {
      FIELD_3RD (view_target, 12);
      FIELD_3RD (VIEWDIR, 0);
      FIELD_CAST (VIEWMODE, RS, 4BITS, 0);
      FIELD_RD (lens_length, 42); // defaults to 50.0
      FIELD_RD (front_clip_z, 43);
      FIELD_RD (back_clip_z, 44);
      FIELD_RD (twist_angle, 50);
      DXF {
        FIELD_CAST (VIEWMODE, RS, 4BITS, 71);
      }
    }
  }
  LATER_VERSIONS
  {
    FIELD_BD (VIEWSIZE, 40); // i.e view height
    FIELD_BD (view_width, 0);
    DECODER {
      FIELD_VALUE (aspect_ratio) = FIELD_VALUE (VIEWSIZE) == 0.0
        ? 0.0
        : FIELD_VALUE (view_width) / FIELD_VALUE (VIEWSIZE);
      LOG_TRACE ("aspect_ratio: %f (calc)\n", FIELD_VALUE (aspect_ratio))
    }
    JSON {
      FIELD_BD (aspect_ratio, 0);
    }
    // subclass ViInfo (shared with VPORT, but different DXF codes)
    FIELD_2RD (VIEWCTR, 10);
    DXF {
      FIELD_BD (view_width, 41);
      FIELD_3BD (VIEWDIR, 11);
    }
    FIELD_3BD (view_target, 12);
    FIELD_3BD (VIEWDIR, 0);
    FIELD_BD (twist_angle, 50);
    FIELD_BD (lens_length, 42);
    FIELD_BD (front_clip_z, 43);
    FIELD_BD (back_clip_z, 44);
    FIELD_4BITS (VIEWMODE, 71);
  }
  SINCE (R_2000) {
    FIELD_RC (render_mode, 281);
  }
  SINCE (R_2007) {
    IF_ENCODE_FROM_EARLIER {
      FIELD_VALUE (use_default_lights) = 1;
      FIELD_VALUE (default_lightning_type) = 1;
      FIELD_VALUE (ambient_color.index) = 250;
      //TODO FIELD_VALUE (ambient_color.rgb) = ?;
    }
    FIELD_HANDLE0 (background, 4, 332);
    FIELD_HANDLE0 (visualstyle, 5, 348);
    FIELD_B (use_default_lights, 292);
    FIELD_RC (default_lightning_type, 282);
    FIELD_BD (brightness, 141);
    FIELD_BD (contrast, 142);
    FIELD_CMC (ambient_color, 63);
    FIELD_HANDLE0 (sun, 3, 361);
  }
  // end of ViInfo

  // subclass ViewTableRecord:
  SINCE (R_13) {
    FIELD_B (is_pspace, 0);
    FIELD_VALUE (flag) |= FIELD_VALUE (is_pspace);
  }
  SINCE (R_2000) {
    FIELD_B (associated_ucs, 72);
    if (FIELD_VALUE (associated_ucs)) {
      FIELD_3BD (ucsorg, 110);
      FIELD_3BD (ucsxdir, 111);
      FIELD_3BD (ucsydir, 112);
      FIELD_BD (ucs_elevation, 146);
      FIELD_BS (UCSORTHOVIEW, 79);
      FIELD_HANDLE (base_ucs, 5, 346);
      FIELD_HANDLE0 (named_ucs, 5, 345);
    }
  }

  SINCE (R_2007) {
    FIELD_B (is_camera_plottable, 73);
  }
  START_OBJECT_HANDLE_STREAM;
  SINCE (R_2007) {
    FIELD_HANDLE0 (livesection, 4, 334); // a SECTIONOBJECT?
  }

DWG_OBJECT_END

/*(62)*/
DWG_OBJECT (UCS_CONTROL)

  FIELD_BS (num_entries, 70); //BS or BL?

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* (63/7) */
DWG_OBJECT (UCS)

  COMMON_TABLE_FLAGS (Ucs)
  PRE (R_13)
  {
    FIELD_3RD (ucsorg, 10);
    FIELD_3RD (ucsxdir, 11);
    FIELD_3RD (ucsydir, 12);
  }
  LATER_VERSIONS
  {
    FIELD_3BD (ucsorg, 10);
    FIELD_3BD (ucsxdir, 11);
    FIELD_3BD (ucsydir, 12);
  }
  SINCE (R_2000)
  {
    FIELD_BD0 (ucs_elevation, 146);
    FIELD_BS (UCSORTHOVIEW, 79);
    FIELD_HANDLE0 (base_ucs, DWG_HDL_HARDPTR, 346);
    FIELD_HANDLE (named_ucs, DWG_HDL_HARDPTR, 0);

    FIELD_BS (num_orthopts, 0);
    REPEAT (num_orthopts, orthopts, Dwg_UCS_orthopts)
    REPEAT_BLOCK
      SUB_FIELD_BS (orthopts[rcount1],type, 71);
      SUB_FIELD_3BD (orthopts[rcount1],pt, 13);
    END_REPEAT_BLOCK
    SET_PARENT_OBJ (orthopts)
    END_REPEAT (orthopts);
  }
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/* (0x40/64) */
DWG_OBJECT (VPORT_CONTROL)

  DXF {
    // minus Standard
    VALUE_RL (FIELD_VALUE (num_entries) - 1, 70);
  } else {
    FIELD_BS (num_entries, 70);
  }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* 0x41/65 /8 */
DWG_OBJECT (VPORT)

  COMMON_TABLE_FLAGS (Viewport)

 DXF { // has a different order of fields

  FIELD_2RD (lower_left, 10);
  FIELD_2RD (upper_right, 11);
  FIELD_2RD (VIEWCTR, 12);
  FIELD_2RD (SNAPBASE, 13);
  FIELD_2RD (SNAPUNIT, 14);
  FIELD_2RD (GRIDUNIT, 15);
  FIELD_3RD (VIEWDIR, 16);
  FIELD_3RD (view_target, 17);
  FIELD_RD (VIEWSIZE, 40);
  FIELD_RD (aspect_ratio, 41); // = view_width / VIEWSIZE
  FIELD_RD (lens_length, 42);
  FIELD_RD (front_clip_z, 43);
  FIELD_RD (back_clip_z, 44);
  FIELD_RD (SNAPANG, 50);
  FIELD_RD (view_twist, 51);
  PRE (R_13) {
    FIELD_RC (UCSFOLLOW, 71);
  }
  else {
    FIELD_VALUE (VIEWMODE) |= ((FIELD_VALUE (UCSFOLLOW) << 2) | FIELD_VALUE (UCSVP));
    FIELD_4BITS (VIEWMODE, 71); // UCSFOLLOW is bit 3 of 71, UCSVP bit 0, ucs_at_origin bit 1
  }
  FIELD_RS (circle_zoom, 72);
  FIELD_RC (FASTZOOM, 73);
  FIELD_RC (UCSICON, 74);
  FIELD_RS (SNAPMODE, 75);
  FIELD_RC (GRIDMODE, 76);
  FIELD_RC (SNAPSTYLE, 77);
  FIELD_RS (SNAPISOPAIR, 78);

  SINCE (R_2000) {
    FIELD_RC (render_mode, 281);
    FIELD_B (UCSVP, 71); // bit 0 of 71
    FIELD_3BD (ucsorg, 110);
    FIELD_3BD (ucsxdir, 111);
    FIELD_3BD (ucsydir, 112);
    FIELD_HANDLE0 (named_ucs, 5, 345);
    if (FIELD_VALUE (UCSORTHOVIEW))
      FIELD_HANDLE (base_ucs, 5, 346);
    FIELD_BS (UCSORTHOVIEW, 79);
    FIELD_BD (ucs_elevation, 146);
  }
  SINCE (R_2007) {
    FIELD_HANDLE0 (background, 4, 332);
    FIELD_HANDLE0 (visualstyle, 5, 348);
    FIELD_BS (grid_flags, 60);
    FIELD_BS (grid_major, 61);
    FIELD_B (use_default_lights, 292);
    FIELD_RC (default_lightning_type, 282);
    FIELD_BD (brightness, 141);
    FIELD_BD (contrast, 142);
    FIELD_CMC (ambient_color, 63);
    FIELD_HANDLE0 (sun, 5, 361);
  }

  //TODO convert back 1001 1070 xdata
  REACTORS (4);
  XDICOBJHANDLE (3);

  }
  /* end of DXF: now DWG */
  else {

  PRE (R_13)
  { // TODO verify
    FIELD_RD (VIEWSIZE, 40);
    FIELD_RD (aspect_ratio, 41);
    DECODER {
      FIELD_VALUE (view_width) = FIELD_VALUE (aspect_ratio) * FIELD_VALUE (VIEWSIZE);
      LOG_TRACE ("view_width: %f (calc)\n", FIELD_VALUE (view_width))
    }
    FIELD_2RD (VIEWCTR, 12);
    FIELD_3RD (view_target, 17);
    FIELD_3RD (VIEWDIR, 16);
    FIELD_RD (view_twist, 51);
    FIELD_RD (lens_length, 42);
    FIELD_RD (front_clip_z, 43);
    FIELD_RD (back_clip_z, 44);
    FIELD_CAST (VIEWMODE, RS, 4BITS, 71);

    FIELD_2RD (lower_left, 10);
    FIELD_2RD (upper_right, 11);
    FIELD_RC (UCSFOLLOW, 71);
    FIELD_RS (circle_zoom, 72); //circle sides
    FIELD_RC (FASTZOOM, 73);
    FIELD_RC (UCSICON, 74);
    FIELD_RC (GRIDMODE, 76);
    FIELD_2RD (GRIDUNIT, 15);
    FIELD_CAST (SNAPMODE, RS, B, 75);
    FIELD_RC (SNAPSTYLE, 77);
    FIELD_RS (SNAPISOPAIR, 78);
    FIELD_RD (SNAPANG, 50);
    FIELD_2RD (SNAPBASE, 13);
    FIELD_2RD (SNAPUNIT, 14);
  }
  else
  {
    FIELD_BD (VIEWSIZE, 40);  // i.e view height
    FIELD_BD (view_width, 0); // -nan in example_2000
    DECODER {
      FIELD_VALUE (aspect_ratio) = FIELD_VALUE (VIEWSIZE) == 0.0
        ? 0.0
        : FIELD_VALUE (view_width) / FIELD_VALUE (VIEWSIZE);
      LOG_TRACE ("aspect_ratio: %f (calc)\n", FIELD_VALUE (aspect_ratio))
    }
    JSON {
      FIELD_BD (aspect_ratio, 0);
    }
    // subclass ViInfo (shared with VIEW, but different DXF codes)
    FIELD_2RD (VIEWCTR, 12);
    FIELD_3BD (view_target, 17);
    FIELD_3BD (VIEWDIR, 16);
    FIELD_BD (view_twist, 51);
    FIELD_BD (lens_length, 42);
    FIELD_BD (front_clip_z, 43);
    FIELD_BD (back_clip_z, 44);
    FIELD_4BITS (VIEWMODE, 71);
    SINCE (R_2000) {
      FIELD_RC (render_mode, 281);
    }
    SINCE (R_2007) {
      IF_ENCODE_FROM_EARLIER {
        FIELD_VALUE (use_default_lights) = 1;
        FIELD_VALUE (default_lightning_type) = 1;
        FIELD_VALUE (ambient_color.index) = 250;
        //TODO FIELD_VALUE (ambient_color.rgb) = ?;
        //TODO FIELD_VALUE (ambient_color.byte) = ?; //+ name, book_name
      }
      VERSIONS (R_13, R_2004) {
        FIELD_HANDLE (sun, 3, 361);
      }
      SINCE (R_2007) {
        FIELD_HANDLE (background, 4, 332); //soft ptr
        FIELD_HANDLE (visualstyle, 5, 348); //hard ptr
        FIELD_HANDLE (sun, 3, 361); //hard owner
      }
      FIELD_B (use_default_lights, 292);
      FIELD_RC (default_lightning_type, 282);
      FIELD_BD (brightness, 141);
      FIELD_BD (contrast, 142);
      FIELD_CMC (ambient_color, 63); // +421, 431
    }

    FIELD_2RD (lower_left, 10);
    FIELD_2RD (upper_right, 11);
    FIELD_B (UCSFOLLOW, 0); // bit 3 of 71
    FIELD_BS (circle_zoom, 72);
    FIELD_B (FASTZOOM, 73);
    FIELD_BB (UCSICON, 74); // bits 0 and 1 of 71: uscicon_on, ucsicon_at_origin
    FIELD_B (GRIDMODE, 76);
    FIELD_2RD (GRIDUNIT, 15);
    FIELD_B (SNAPMODE, 75);
    FIELD_B (SNAPSTYLE, 77);
    FIELD_BS (SNAPISOPAIR, 78);
    if (dwg->header.dwg_version != 0x1a) { // AC1020/R_2006 only here
      FIELD_BD (SNAPANG, 50);
      FIELD_2RD (SNAPBASE, 13);
    }
    FIELD_2RD (SNAPUNIT, 14);

    SINCE (R_2000) {
      FIELD_B (ucs_at_origin, 0);
      FIELD_B (UCSVP, 71);
      FIELD_3BD (ucsorg, 110);
      FIELD_3BD (ucsxdir, 111);
      FIELD_3BD (ucsydir, 112);
      FIELD_BD (ucs_elevation, 146);
      FIELD_BS (UCSORTHOVIEW, 79);
    }

    SINCE (R_2007) {
      FIELD_BS (grid_flags, 60);
      FIELD_BS (grid_major, 61);
    }
  }

  START_OBJECT_HANDLE_STREAM;
  SINCE (R_2000) {
    FIELD_HANDLE0 (named_ucs, 5, 345);
    FIELD_HANDLE0 (base_ucs, 5, 346);
  }
 }

DWG_OBJECT_END

/*(66)*/
DWG_OBJECT (APPID_CONTROL)

  FIELD_BS (num_entries, 70);

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);

DWG_OBJECT_END

/* (67/9) Registered Apps */
DWG_OBJECT (APPID)

  COMMON_TABLE_FLAGS (RegApp)
  SINCE (R_13) {
    FIELD_RC0 (unknown, 71); // in DXF only with ADE_PROJECTION
  }
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/*(68)*/
DWG_OBJECT (DIMSTYLE_CONTROL)

  FIELD_BS (num_entries, 70);
  SUBCLASS (AcDbDimStyleTable)
  SINCE (R_2000)
    { /* number of additional hard handles, undocumented */
      FIELD_RCu (num_morehandles, 71);
    }

  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 2, 0);
  HANDLE_VECTOR (morehandles, num_morehandles, 5, 340);

DWG_OBJECT_END

/* (69/10) */
DWG_OBJECT (DIMSTYLE)

  DXF {
    FIELD_VALUE (flag) = FIELD_VALUE (flag0);
  }
  COMMON_TABLE_FLAGS (DimStyle)

  PRE (R_13)
    {
      FIELD_RC (DIMTOL, 71);
      FIELD_RC (DIMLIM, 72);
      FIELD_RC (DIMTIH, 73);
      FIELD_RC (DIMTOH, 74);
      FIELD_RC (DIMSE1, 75);
      FIELD_RC (DIMSE2, 76);
      FIELD_RC (DIMALT, 170);
      FIELD_RC (DIMTOFL, 172);
      FIELD_RC (DIMSAH, 173);
      FIELD_RC (DIMTIX, 174);
      FIELD_RC (DIMSOXD, 175);
      FIELD_CAST (DIMALTD, RC, BS, 171);
      FIELD_CAST (DIMZIN, RC, BS, 78);
      FIELD_RC (DIMSD1, 281);
      FIELD_RC (DIMSD2, 282);
      FIELD_CAST (DIMTOLJ, RC, BS, 283);
      FIELD_CAST (DIMJUST, RC, BS, 280);
      FIELD_CAST (DIMFIT, RC, BS, 287);
      FIELD_RC (DIMUPT, 288);
      FIELD_CAST (DIMTZIN, RC, BS, 284);
      FIELD_CAST (DIMMALTZ, RC, BS, 285);
      FIELD_CAST (DIMMALTTZ, RC, BS, 286);
      FIELD_CAST (DIMTAD, RC, BS, 77);
      FIELD_RS (DIMUNIT, 270);
      FIELD_RS (DIMAUNIT, 275);
      FIELD_RS (DIMDEC, 271);
      FIELD_RS (DIMTDEC, 272);
      FIELD_RS (DIMALTU, 273);
      FIELD_RS (DIMALTTD, 274);
      FIELD_RD (DIMSCALE, 40);
      FIELD_RD (DIMASZ, 41);
      FIELD_RD (DIMEXO, 42);
      FIELD_RD (DIMDLI, 43);
      FIELD_RD (DIMEXE, 44);
      FIELD_RD (DIMRND, 45);
      FIELD_RD (DIMDLE, 46);
      FIELD_RD (DIMTP, 47);
      FIELD_RD (DIMTM, 48);
      FIELD_RD (DIMTXT, 140);
      FIELD_RD (DIMCEN, 141);
      FIELD_RD (DIMTSZ, 142);
      FIELD_RD (DIMALTF, 143);
      FIELD_RD (DIMLFAC, 144);
      FIELD_RD (DIMTVP, 145);
      FIELD_RD (DIMTFAC, 146);
      FIELD_RD (DIMGAP, 147);
      FIELD_TV (DIMPOST, 3);
      FIELD_TV (DIMAPOST, 4); //??
      FIELD_TV (DIMBLK_T, 5);
      FIELD_TV (DIMBLK1_T, 6);
      FIELD_TV (DIMBLK2_T, 7);
      FIELD_CAST (DIMCLRD_N, RC, RS, 176);
      FIELD_CAST (DIMCLRE_N, RC, RS, 177);
      FIELD_CAST (DIMCLRT_N, RC, RS, 178);
    }
  VERSIONS (R_13, R_14)
    {
      FIELD_B (DIMTOL, 71);
      FIELD_B (DIMLIM, 72);
      FIELD_B (DIMTIH, 73);
      FIELD_B (DIMTOH, 74);
      FIELD_B (DIMSE1, 75);
      FIELD_B (DIMSE2, 76);
      FIELD_B (DIMALT, 170);
      FIELD_B (DIMTOFL, 172);
      FIELD_B (DIMSAH, 173);
      FIELD_B (DIMTIX, 174);
      FIELD_B (DIMSOXD, 175);
      FIELD_CAST (DIMALTD, RC, BS, 171);
      FIELD_CAST (DIMZIN, RC, BS, 78);
      FIELD_B (DIMSD1, 281);
      FIELD_B (DIMSD2, 282);
      FIELD_CAST (DIMTOLJ, RC, BS, 283);
      FIELD_CAST (DIMJUST, RC, BS, 280);
      FIELD_CAST (DIMFIT, RC, BS, 287);
      FIELD_B (DIMUPT, 288);
      FIELD_CAST (DIMTZIN, RC, BS, 284);
      FIELD_CAST (DIMMALTZ, RC, BS, 285);
      FIELD_CAST (DIMMALTTZ, RC, BS, 286);
      FIELD_CAST (DIMTAD, RC, BS, 77);
      FIELD_BS (DIMUNIT, 270);
      FIELD_BS (DIMAUNIT, 275);
      FIELD_BS (DIMDEC, 271);
      FIELD_BS (DIMTDEC, 272);
      FIELD_BS (DIMALTU, 273);
      FIELD_BS (DIMALTTD, 274);
      FIELD_BD (DIMSCALE, 40);
      FIELD_BD (DIMASZ, 41);
      FIELD_BD (DIMEXO, 42);
      FIELD_BD (DIMDLI, 43);
      FIELD_BD (DIMEXE, 44);
      FIELD_BD (DIMRND, 45);
      FIELD_BD (DIMDLE, 46);
      FIELD_BD (DIMTP, 47);
      FIELD_BD (DIMTM, 48);
      FIELD_BD (DIMTXT, 140);
      FIELD_BD (DIMCEN, 141);
      FIELD_BD (DIMTSZ, 142);
      FIELD_BD (DIMALTF, 143);
      FIELD_BD (DIMLFAC, 144);
      FIELD_BD (DIMTVP, 145);
      FIELD_BD (DIMTFAC, 146);
      FIELD_BD (DIMGAP, 147);
      FIELD_TV (DIMPOST, 3);
      FIELD_TV (DIMAPOST, 4);
      FIELD_TV (DIMBLK_T, 5);
      FIELD_TV (DIMBLK1_T, 6);
      FIELD_TV (DIMBLK2_T, 7);
      FIELD_CMC (DIMCLRD, 176);
      FIELD_CMC (DIMCLRE, 177);
      FIELD_CMC (DIMCLRT, 178);
    }
  else FREE {
      FIELD_TV (DIMBLK_T, 5);
      FIELD_TV (DIMBLK1_T, 6);
      FIELD_TV (DIMBLK2_T, 7);
  }
  IF_FREE_OR_SINCE (R_2000)
    {
      FIELD_T (DIMPOST, 3);
      FIELD_T (DIMAPOST, 4);
      FIELD_BD (DIMSCALE, 40);
      FIELD_BD (DIMASZ, 41);
      FIELD_BD (DIMEXO, 42);
      FIELD_BD (DIMDLI, 43);
      FIELD_BD (DIMEXE, 44);
      FIELD_BD (DIMRND, 45);
      FIELD_BD (DIMDLE, 46);
      FIELD_BD (DIMTP, 47);
      FIELD_BD (DIMTM, 48);
    }

  SINCE (R_2007)
    {
      FIELD_BD (DIMFXL, 49);
      FIELD_BD (DIMJOGANG, 50);
      FIELD_BS (DIMTFILL, 69);
      FIELD_CMC (DIMTFILLCLR, 70);
    }

  SINCE (R_2000)
    {
      FIELD_B (DIMTOL, 71);
      FIELD_B (DIMLIM, 72);
      FIELD_B (DIMTIH, 73);
      FIELD_B (DIMTOH, 74);
      FIELD_B (DIMSE1, 75);
      FIELD_B (DIMSE2, 76);
      FIELD_BS (DIMTAD, 77);
      FIELD_BS (DIMZIN, 78);
      FIELD_BS (DIMAZIN, 79);
    }

  SINCE (R_2007)
    {
      FIELD_BS (DIMARCSYM, 90);
    }

  IF_FREE_OR_SINCE (R_2000)
    {
      FIELD_BD (DIMTXT, 140);
      FIELD_BD (DIMCEN, 141);
      FIELD_BD (DIMTSZ, 142);
      FIELD_BD (DIMALTF, 143);
      FIELD_BD (DIMLFAC, 144);
      FIELD_BD (DIMTVP, 145);
      FIELD_BD (DIMTFAC, 146);
      FIELD_BD (DIMGAP, 147);
      FIELD_BD (DIMALTRND, 148);
      FIELD_B (DIMALT, 170);
      FIELD_BS (DIMALTD, 171);
      FIELD_B (DIMTOFL, 172);
      FIELD_B (DIMSAH, 173);
      FIELD_B (DIMTIX, 174);
      FIELD_B (DIMSOXD, 175);
      FIELD_CMC (DIMCLRD, 176);
      FIELD_CMC (DIMCLRE, 177);
      FIELD_CMC (DIMCLRT, 178);
      FIELD_BS (DIMADEC, 179);
      FIELD_BS (DIMDEC, 271);
      FIELD_BS (DIMTDEC, 272);
      FIELD_BS (DIMALTU, 273);
      FIELD_BS (DIMALTTD, 274);
      FIELD_BS (DIMAUNIT, 275);
      FIELD_BS (DIMFRAC, 276);
      FIELD_BS (DIMLUNIT, 277);
      FIELD_BS (DIMDSEP, 278);
      FIELD_BS (DIMTMOVE, 279);
      FIELD_BS (DIMJUST, 280);
      FIELD_B (DIMSD1, 281);
      FIELD_B (DIMSD2, 282);
      FIELD_BS (DIMTOLJ, 283);
      FIELD_BS (DIMTZIN, 284);
      FIELD_BS (DIMALTZ, 285);
      FIELD_BS (DIMALTTZ, 286);
      FIELD_B (DIMUPT, 288);
      FIELD_BS (DIMFIT, 289);
    }

  SINCE (R_2007)
    {
      FIELD_B (DIMFXLON, 290);
    }

  IF_FREE_OR_SINCE (R_2010)
    {
      FIELD_B (DIMTXTDIRECTION, 295);
      FIELD_BD (DIMALTMZF, 0); // undocumented
      FIELD_T (DIMALTMZS, 0); // undocumented
      FIELD_BD (DIMMZF, 0); // undocumented
      FIELD_T (DIMMZS, 0); // undocumented
    }

  SINCE (R_2000)
    {
      FIELD_BSd (DIMLWD, 371);
      FIELD_BSd (DIMLWE, 372);
    }

  SINCE (R_13)
  {
    FIELD_B (flag0, 0); // Bit 0 of 70
    FIELD_VALUE (flag) |= FIELD_VALUE (flag0);

    START_OBJECT_HANDLE_STREAM;
    FIELD_HANDLE (DIMTXSTY, 5, 340); /* Text style (DIMTXSTY) */
  }
  IF_FREE_OR_SINCE (R_2000)
    {
      FIELD_HANDLE (DIMLDRBLK, 5, 341); /* Leader arrow (DIMLDRBLK)*/
      FIELD_HANDLE (DIMBLK, 5, 342);  /* Arrow */
      FIELD_HANDLE (DIMBLK1, 5, 343); /* Arrow 1 */
      FIELD_HANDLE (DIMBLK2, 5, 344); /* Arrow 2 */
    }
  IF_FREE_OR_SINCE (R_2007)
    {
      FIELD_HANDLE (DIMLTYPE, 5, 345);
      FIELD_HANDLE (DIMLTEX1, 5, 346);
      FIELD_HANDLE (DIMLTEX2, 5, 347);
    }

DWG_OBJECT_END

/* VIEWPORT (VX) ENTITY CONTROL (70) */
DWG_OBJECT (VPORT_ENTITY_CONTROL)

  FIELD_BS (num_entries, 70);
  SUBCLASS (AcDbVXTable)
  CONTROL_HANDLE_STREAM;
  HANDLE_VECTOR (entries, num_entries, 4, 0);

DWG_OBJECT_END

/* VIEWPORT (VX) ENTITY HEADER (71/11) */
DWG_OBJECT (VPORT_ENTITY_HEADER)

  COMMON_TABLE_FLAGS (VX)
  FIELD_B (is_on, 290); // bit 1 of 70
  FIELD_VALUE (flag) |= FIELD_VALUE (is_on) << 1;

  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (viewport, 4, 338);
  FIELD_HANDLE (prev_entry, 5, 340);
DWG_OBJECT_END

/*(72)*/
DWG_OBJECT (GROUP)

  SUBCLASS (AcDbGroup)
  FIELD_T (name, 300);
  FIELD_BS (unnamed, 70);
  FIELD_BS (selectable, 71);
  FIELD_BL (num_groups, 0);
  VALUEOUTOFBOUNDS (num_groups, 10000)

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (groups, num_groups, 5, 340);

DWG_OBJECT_END

/* (73) */
DWG_OBJECT (MLINESTYLE)

  SUBCLASS (AcDbMlineStyle)
  FIELD_T (name, 2);
  FIELD_T (description, 0);
  FIELD_BS (flag, 70);  /*!< 1 = Fill on,
                             2 = Display miters,
                             16 = Start square end (line) cap,
                             32 = Start inner arcs cap,
                             64 = Start round (outer arcs) cap,
                             256 = End square (line) cap,
                             512 = End inner arcs cap,
                             1024 = End round (outer arcs) cap */
  DXF { FIELD_T (description, 3); }
  FIELD_CMC (fill_color, 62); /*!< default 256 */
#ifdef IS_DXF
  // 0 - 90
  FIELD_VALUE (start_angle) = rad2deg (FIELD_VALUE (start_angle));
  FIELD_VALUE (end_angle)   = rad2deg (FIELD_VALUE (end_angle));
  while (FIELD_VALUE (start_angle) > 90.0) FIELD_VALUE (start_angle) -= 90.0;
  while (FIELD_VALUE (end_angle)   > 90.0) FIELD_VALUE (end_angle)   -= 90.0;
  VALUE (FIELD_VALUE (start_angle), RD, 51)
  VALUE (FIELD_VALUE (end_angle), RD, 52)
#else
  FIELD_BD (start_angle, 51); /*!< default 90 deg */
  FIELD_BD (end_angle, 52);   /*!< default 90 deg */
#endif
  FIELD_RCu (num_lines, 71);
  REPEAT (num_lines, lines, Dwg_MLINESTYLE_line)
  REPEAT_BLOCK
      SUB_FIELD_BD (lines[rcount1], offset, 49);
      SUB_FIELD_CMC (lines[rcount1], color, 62); /*!< default: 0 */
      PRE (R_2018)
      {
#if defined (IS_DXF) && !defined (IS_ENCODER)
        switch (FIELD_VALUE (lines[rcount1].lt_index)) {
        case 32767: VALUE_TFF ("BYLAYER", 6); break; /* default (SHRT_MAX) */
        case 32766: VALUE_TFF ("BYBLOCK", 6); break;
        case 0:  VALUE_TFF ("CONTINUOUS", 6); break;
        //TODO else lookup name on LTYPE_CONTROL list
        default: /*FIELD_HANDLE_NAME (lt.ltype, 5, 6);*/
                 VALUE_TFF ("", 6); break;
        }
#else
        SUB_FIELD_BSd (lines[rcount1], lt_index, 6);
#endif
      }
      LATER_VERSIONS {
        SUB_FIELD_HANDLE (lines[rcount1], lt_ltype, 5, 6);
      }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (lines)
  END_REPEAT (lines);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

//pg.135
DWG_OBJECT (DICTIONARYVAR)

  SUBCLASS (DictionaryVariables)
  FIELD_RC (intval, 280);
  FIELD_T (str, 1);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

#ifndef IS_INDXF
int DWG_FUNC_N (ACTION,_HATCH_gradientfill)(
                        Bit_Chain *restrict dat,
                        Bit_Chain *restrict str_dat,
                        const Dwg_Object *restrict obj,
                        Dwg_Entity_HATCH *restrict _obj);

int DWG_FUNC_N (ACTION,_HATCH_gradientfill)(
                        Bit_Chain *restrict dat,
                        Bit_Chain *restrict str_dat,
                        const Dwg_Object *restrict obj,
                        Dwg_Entity_HATCH *restrict _obj)
{
  BITCODE_BL vcount, rcount3, rcount4;
  int error = 0;
  //Dwg_Data* dwg = obj->parent;

  FIELD_BL (is_gradient_fill, 450);
  FIELD_BL (reserved, 451);
  FIELD_BD (gradient_angle, 460);
  FIELD_BD (gradient_shift, 461);
  FIELD_BL (single_color_gradient, 452); //bool
  FIELD_BD (gradient_tint, 462);
  FIELD_BL (num_colors, 453); //default: 2
  if (FIELD_VALUE (is_gradient_fill) != 0 && FIELD_VALUE (num_colors) > 1000)
    {
      LOG_ERROR ("Invalid gradient fill HATCH.num_colors " FORMAT_BL,
                _obj->num_colors);
      _obj->num_colors = 0;
      return DWG_ERR_VALUEOUTOFBOUNDS;
    }
  REPEAT (num_colors, colors, Dwg_HATCH_Color)
  REPEAT_BLOCK
      SUB_FIELD_BD (colors[rcount1], shift_value, 463);
      SUB_FIELD_CMC (colors[rcount1], color, 63);
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (colors)
  END_REPEAT (colors);
  FIELD_T (gradient_name, 470);
  return error;
}
#endif

#ifdef IS_JSON
#  define JSON_END_REPEAT(f)  ENDHASH
#else
#  define JSON_END_REPEAT(f)  END_REPEAT (f)
#endif

//(78 + varies) pg.136
DWG_ENTITY (HATCH)

  SUBCLASS (AcDbHatch)
#if !defined (IS_DXF) && !defined (IS_INDXF)
  SINCE (R_2004)
    {
      error |= DWG_FUNC_N (ACTION,_HATCH_gradientfill)(dat,str_dat,obj,_obj);
    }
#endif
#ifdef IS_FREE
  if (dat->from_version >= R_2004)
    {
      error |= DWG_FUNC_N (ACTION,_HATCH_gradientfill)(dat,str_dat,obj,_obj);
    }
#endif
  DXF {
    BITCODE_3RD pt = { 0.0, 0.0, 0.0 };
    pt.z = FIELD_VALUE (elevation);
    KEY (elevation); VALUE_3BD (pt, 10);
  } else {
    FIELD_BD (elevation, 30);
  }
  ENCODER { normalize_BE (FIELD_VALUE (extrusion)); }
  FIELD_3BD (extrusion, 210);
  DECODER { normalize_BE (FIELD_VALUE (extrusion)); }
  FIELD_T (name, 2); //default: SOLID
  FIELD_B (is_solid_fill, 70); //default: 1, pattern_fill: 0
  FIELD_B (is_associative, 71);
  FIELD_BL (num_paths, 91);
  VALUEOUTOFBOUNDS (num_paths, 10000)
  REPEAT (num_paths, paths, Dwg_HATCH_Path)
  REPEAT_BLOCK
      SUB_FIELD_BL (paths[rcount1], flag, 92);
      if (!(FIELD_VALUE (paths[rcount1].flag) & 2))
        {
          SUB_FIELD_BL (paths[rcount1], num_segs_or_paths, 93);
          if (FIELD_VALUE (paths[rcount1].num_segs_or_paths > 10000))
            {
              LOG_ERROR ("Invalid HATCH.num_segs_or_paths " FORMAT_BL,
                        _obj->paths[rcount1].num_segs_or_paths);
              _obj->paths[rcount1].num_segs_or_paths = 0;
              JSON_END_REPEAT (paths);
              return DWG_ERR_VALUEOUTOFBOUNDS;
            }
#define segs paths[rcount1].segs
          REPEAT2 (paths[rcount1].num_segs_or_paths, segs, Dwg_HATCH_PathSeg)
          REPEAT_BLOCK
              SUB_FIELD_RC (segs[rcount2],curve_type, 72); // 1-4
              switch (FIELD_VALUE (segs[rcount2].curve_type))
                {
                    case 1: /* LINE */
                      SUB_FIELD_2RD (segs[rcount2],first_endpoint, 10);
                      SUB_FIELD_2RD (segs[rcount2],second_endpoint, 11);
                      break;
                    case 2: /* CIRCULAR ARC */
                      SUB_FIELD_2RD (segs[rcount2], center, 10);
                      SUB_FIELD_BD (segs[rcount2], radius, 40);
                      SUB_FIELD_BD (segs[rcount2], start_angle, 50);
                      SUB_FIELD_BD (segs[rcount2], end_angle, 51);
                      SUB_FIELD_B (segs[rcount2], is_ccw, 73);
                      break;
                    case 3: /* ELLIPTICAL ARC */
                      SUB_FIELD_2RD (segs[rcount2], center, 10);
                      SUB_FIELD_2RD (segs[rcount2], endpoint, 11);
                      SUB_FIELD_BD (segs[rcount2], minor_major_ratio, 40);
                      SUB_FIELD_BD (segs[rcount2], start_angle, 50);
                      SUB_FIELD_BD (segs[rcount2], end_angle, 51);
                      SUB_FIELD_B (segs[rcount2], is_ccw, 73);
                      break;
                    case 4: /* SPLINE */
                      SUB_FIELD_BL (segs[rcount2], degree, 94);
                      SUB_FIELD_B (segs[rcount2], is_rational, 73);
                      SUB_FIELD_B (segs[rcount2], is_periodic, 74);
                      SUB_FIELD_BL (segs[rcount2], num_knots, 95);
                      SUB_FIELD_BL (segs[rcount2], num_control_points, 96);
                      if (FIELD_VALUE (segs[rcount2].num_knots > 10000))
                        {
                          LOG_ERROR ("Invalid HATCH.paths.segs.num_knots " FORMAT_BL,
                                    _obj->segs[rcount2].num_knots);
                          _obj->segs[rcount2].num_knots = 0;
                          JSON_END_REPEAT (segs);
                          JSON_END_REPEAT (paths);
                          return DWG_ERR_VALUEOUTOFBOUNDS;
                        }
                      FIELD_VECTOR (segs[rcount2].knots, BD,
                                    segs[rcount2].num_knots, 40);
                      if (FIELD_VALUE (segs[rcount2].num_control_points > 10000))
                        {
                          LOG_ERROR ("Invalid HATCH.paths.segs.num_control_points " FORMAT_BL,
                                    _obj->segs[rcount2].num_control_points);
                          _obj->segs[rcount2].num_control_points = 0;
                          JSON_END_REPEAT (segs);
                          JSON_END_REPEAT (paths);
                          return DWG_ERR_VALUEOUTOFBOUNDS;
                        }
#define control_points segs[rcount2].control_points
                      REPEAT3 (segs[rcount2].num_control_points, control_points, Dwg_HATCH_ControlPoint)
                      REPEAT_BLOCK
                          SUB_FIELD_2RD (control_points[rcount3], point, 10);
                          if (FIELD_VALUE (segs[rcount2].is_rational))
                            SUB_FIELD_BD (control_points[rcount3], weight, 40)
                      END_REPEAT_BLOCK
                      SET_PARENT (control_points,
                                 &_obj->segs[rcount2])
                      END_REPEAT (control_points);
#undef control_points
                      SINCE (R_2013) // r2014 really
                        {
#define seg segs[rcount2]
                          SUB_FIELD_BL (seg, num_fitpts, 97);
                          FIELD_2RD_VECTOR (seg.fitpts, seg.num_fitpts, 11);
#undef seg
                        }
                      break;
                    default:
                      LOG_ERROR ("Invalid HATCH.curve_type %d\n",
                                FIELD_VALUE (segs[rcount2].curve_type));
                      DEBUG_HERE_OBJ
                      _obj->segs[rcount2].curve_type = 0;
                      JSON_END_REPEAT (segs);
                      JSON_END_REPEAT (paths);
                      return DWG_ERR_VALUEOUTOFBOUNDS;
                }
          END_REPEAT_BLOCK
          SET_PARENT (segs, &_obj->paths[rcount1])
          END_REPEAT (segs);
#undef segs
        }
      else
        { /* POLYLINE PATH */
          SUB_FIELD_B (paths[rcount1],bulges_present, 72);
          SUB_FIELD_B (paths[rcount1],closed, 73);
          SUB_FIELD_BL (paths[rcount1],num_segs_or_paths, 93);
#define polyline_paths paths[rcount1].polyline_paths
          REPEAT2 (paths[rcount1].num_segs_or_paths, polyline_paths, Dwg_HATCH_PolylinePath)
          REPEAT_BLOCK
              SUB_FIELD_2RD (polyline_paths[rcount2],point, 10);
              if (FIELD_VALUE (paths[rcount1].bulges_present))
                {
                  SUB_FIELD_BD (polyline_paths[rcount2],bulge, 42);
                }
          END_REPEAT_BLOCK
          SET_PARENT (polyline_paths, &_obj->paths[rcount1])
          END_REPEAT (polyline_paths);
#undef polyline_paths
        }
      SUB_FIELD_BL (paths[rcount1],num_boundary_handles, 97);
#if defined (IS_DXF) && !defined (IS_ENCODER)
      DXF {
        if (_obj->boundary_handles && rcount1 < _obj->num_boundary_handles) {
          FIELD_HANDLE (boundary_handles[rcount1], 0, 330)
        } else {
          LOG_WARN ("HATCH.num_path < num_boundary_handles or empty boundary_handles")
          VALUE_HANDLE ((BITCODE_H)NULL, boundary_handles, 0, 330)
        }
      }
#endif
      DECODER {
        FIELD_VALUE (num_boundary_handles) += FIELD_VALUE (paths[rcount1].num_boundary_handles);
        FIELD_VALUE (has_derived) =
          FIELD_VALUE (has_derived) || (FIELD_VALUE (paths[rcount1].flag) & 0x4);
      }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (paths)
  END_REPEAT (paths);
#ifdef IS_DXF
  SINCE (R_2004)
    {
      error |= DWG_FUNC_N (ACTION,_HATCH_gradientfill)(dat,str_dat,obj,_obj);
    }
#endif
  FIELD_BS (style, 75); // 0=normal (odd parity); 1=outer; 2=whole
  FIELD_BS (pattern_type, 76); // 0=user; 1=predefined; 2=custom
  if (!FIELD_VALUE (is_solid_fill))
    {
      FIELD_BD (angle, 52);
      FIELD_BD (scale_spacing, 41); //default 1.0
      FIELD_B (double_flag, 77);
      FIELD_BS (num_deflines, 78);
      REPEAT (num_deflines, deflines, Dwg_HATCH_DefLine)
      REPEAT_BLOCK
          SUB_FIELD_BD (deflines[rcount1], angle, 53);
          SUB_FIELD_2BD_1 (deflines[rcount1], pt0, 43);
          SUB_FIELD_2BD_1 (deflines[rcount1], offset, 45);
          SUB_FIELD_BS (deflines[rcount1], num_dashes, 79);
          FIELD_VECTOR (deflines[rcount1].dashes, BD, deflines[rcount1].num_dashes, 49)
      END_REPEAT_BLOCK
      SET_PARENT_OBJ (deflines)
      END_REPEAT (deflines);
    }

  if (FIELD_VALUE (has_derived))
    FIELD_BD (pixel_size, 47);
  FIELD_BL (num_seeds, 98);
  VALUEOUTOFBOUNDS (num_seeds, 10000)
  FIELD_2RD_VECTOR (seeds, num_seeds, 10);
  VALUEOUTOFBOUNDS (num_boundary_handles, 10000)

  COMMON_ENTITY_HANDLE_DATA;
  HANDLE_VECTOR (boundary_handles, num_boundary_handles, 4, 0); /* DXF: inlined above */

DWG_OBJECT_END

#if defined (DEBUG_CLASSES) || defined (IS_FREE)

// Hatched closed polygon
// debugging
DWG_ENTITY (MPOLYGON)

  SUBCLASS (AcDbMPolygon)

  FIELD_BS (style, 75); // 0=normal (odd parity); 1=outer; 2=whole //??
#if !defined (IS_DXF) && !defined (IS_INDXF)
  SINCE (R_2004)
    {
      error |= DWG_FUNC_N (ACTION,_HATCH_gradientfill)(dat,str_dat,obj,(Dwg_Entity_HATCH *)_obj);
    }
#endif

  DXF {
    BITCODE_3RD pt = { 0.0, 0.0, 0.0 };
    pt.z = FIELD_VALUE (elevation);
    KEY (elevation); VALUE_3BD (pt, 10);
  } else {
    FIELD_BD (elevation, 30);
  }
  ENCODER { normalize_BE (FIELD_VALUE (extrusion)); }
  FIELD_3BD (extrusion, 210);
  DECODER { normalize_BE (FIELD_VALUE (extrusion)); }
  FIELD_T (name, 2);

  //??
  FIELD_BS (is_solid_fill, 70); //default: 1, pattern_fill: 0
  FIELD_B (is_associative, 71);

  FIELD_BL (num_paths, 91);
  VALUEOUTOFBOUNDS (num_paths, 10000)
  REPEAT (num_paths, paths, Dwg_HATCH_Path)
  REPEAT_BLOCK
      SUB_FIELD_BL (paths[rcount1], flag, 92);
      if (!(FIELD_VALUE (paths[rcount1].flag) & 2))
        {
          SUB_FIELD_BL (paths[rcount1], num_segs_or_paths, 93);
          if (FIELD_VALUE (paths[rcount1].num_segs_or_paths > 10000))
            {
              LOG_ERROR ("Invalid HATCH.num_segs_or_paths " FORMAT_BL,
                        _obj->paths[rcount1].num_segs_or_paths);
              _obj->paths[rcount1].num_segs_or_paths = 0;
              JSON_END_REPEAT (paths);
              return DWG_ERR_VALUEOUTOFBOUNDS;
            }
#define segs paths[rcount1].segs
          REPEAT2 (paths[rcount1].num_segs_or_paths, segs, Dwg_HATCH_PathSeg)
          REPEAT_BLOCK
              SUB_FIELD_RC (segs[rcount2],curve_type, 72); // 1-4
              switch (FIELD_VALUE (segs[rcount2].curve_type))
                {
                    case 1: /* LINE */
                      SUB_FIELD_2RD (segs[rcount2],first_endpoint, 10);
                      SUB_FIELD_2RD (segs[rcount2],second_endpoint, 11);
                      break;
                    case 2: /* CIRCULAR ARC */
                      SUB_FIELD_2RD (segs[rcount2], center, 10);
                      SUB_FIELD_BD (segs[rcount2], radius, 40);
                      SUB_FIELD_BD (segs[rcount2], start_angle, 50);
                      SUB_FIELD_BD (segs[rcount2], end_angle, 51);
                      SUB_FIELD_B (segs[rcount2], is_ccw, 73);
                      break;
                    case 3: /* ELLIPTICAL ARC */
                      SUB_FIELD_2RD (segs[rcount2], center, 10);
                      SUB_FIELD_2RD (segs[rcount2], endpoint, 11);
                      SUB_FIELD_BD (segs[rcount2], minor_major_ratio, 40);
                      SUB_FIELD_BD (segs[rcount2], start_angle, 50);
                      SUB_FIELD_BD (segs[rcount2], end_angle, 51);
                      SUB_FIELD_B (segs[rcount2], is_ccw, 73);
                      break;
                    case 4: /* SPLINE */
                      SUB_FIELD_BL (segs[rcount2], degree, 94);
                      SUB_FIELD_B (segs[rcount2], is_rational, 73);
                      SUB_FIELD_B (segs[rcount2], is_periodic, 74);
                      SUB_FIELD_BL (segs[rcount2], num_knots, 95);
                      SUB_FIELD_BL (segs[rcount2], num_control_points, 96);
                      if (FIELD_VALUE (segs[rcount2].num_knots > 10000))
                        {
                          LOG_ERROR ("Invalid HATCH.paths.segs.num_knots " FORMAT_BL,
                                    _obj->segs[rcount2].num_knots);
                          _obj->segs[rcount2].num_knots = 0;
                          JSON_END_REPEAT (segs);
                          JSON_END_REPEAT (paths);
                          return DWG_ERR_VALUEOUTOFBOUNDS;
                        }
                      FIELD_VECTOR (segs[rcount2].knots, BD,
                                    segs[rcount2].num_knots, 40);
                      if (FIELD_VALUE (segs[rcount2].num_control_points > 10000))
                        {
                          LOG_ERROR ("Invalid HATCH.paths.segs.num_control_points " FORMAT_BL,
                                    _obj->segs[rcount2].num_control_points);
                          _obj->segs[rcount2].num_control_points = 0;
                          JSON_END_REPEAT (segs);
                          JSON_END_REPEAT (paths);
                          return DWG_ERR_VALUEOUTOFBOUNDS;
                        }
#define control_points segs[rcount2].control_points
                      REPEAT3 (segs[rcount2].num_control_points, control_points, Dwg_HATCH_ControlPoint)
                      REPEAT_BLOCK
                          SUB_FIELD_2RD (control_points[rcount3], point, 10);
                          if (FIELD_VALUE (segs[rcount2].is_rational))
                            SUB_FIELD_BD (control_points[rcount3], weight, 40)
                      END_REPEAT_BLOCK
                      SET_PARENT (control_points,
                                 &_obj->segs[rcount2])
                      END_REPEAT (control_points);
#undef control_points
                      SINCE (R_2013) // r2014 really
                        {
#define seg segs[rcount2]
                          SUB_FIELD_BL (seg, num_fitpts, 97);
                          FIELD_2RD_VECTOR (seg.fitpts, seg.num_fitpts, 11);
#undef seg
                        }
                      break;
                    default:
                      LOG_ERROR ("Invalid HATCH.curve_type %d\n",
                                FIELD_VALUE (segs[rcount2].curve_type));
                      DEBUG_HERE_OBJ
                      _obj->segs[rcount2].curve_type = 0;
                      JSON_END_REPEAT (segs);
                      JSON_END_REPEAT (paths);
                      return DWG_ERR_VALUEOUTOFBOUNDS;
                }
          END_REPEAT_BLOCK
          SET_PARENT (segs, &_obj->paths[rcount1])
          END_REPEAT (segs);
#undef segs
        }
      else
        { /* POLYLINE PATH */
          SUB_FIELD_B (paths[rcount1],bulges_present, 72);
          SUB_FIELD_B (paths[rcount1],closed, 73);
          SUB_FIELD_BL (paths[rcount1],num_segs_or_paths, 93);
#define polyline_paths paths[rcount1].polyline_paths
          REPEAT2 (paths[rcount1].num_segs_or_paths, polyline_paths, Dwg_HATCH_PolylinePath)
          REPEAT_BLOCK
              SUB_FIELD_2RD (polyline_paths[rcount2],point, 10);
              if (FIELD_VALUE (paths[rcount1].bulges_present))
                {
                  SUB_FIELD_BD (polyline_paths[rcount2],bulge, 42);
                }
          END_REPEAT_BLOCK
          SET_PARENT (polyline_paths, &_obj->paths[rcount1])
          END_REPEAT (polyline_paths);
#undef polyline_paths
        }
      SUB_FIELD_BL (paths[rcount1],num_boundary_handles, 97);
#if defined (IS_DXF) && !defined (IS_ENCODER)
      DXF {
        if (_obj->boundary_handles && rcount1 < _obj->num_boundary_handles) {
          FIELD_HANDLE (boundary_handles[rcount1], 0, 330)
        } else {
          LOG_WARN ("HATCH.num_path < num_boundary_handles or empty boundary_handles")
          VALUE_HANDLE ((BITCODE_H)NULL, boundary_handles, 0, 330)
        }
      }
#endif
  END_REPEAT_BLOCK
  SET_PARENT (paths, (Dwg_Entity_HATCH*)_obj)
  END_REPEAT (paths);
#ifdef IS_DXF
  SINCE (R_2004)
    {
      error |= DWG_FUNC_N (ACTION,_HATCH_gradientfill)(dat,str_dat,obj,(Dwg_Entity_HATCH *)_obj);
    }
#endif

  DXF {
    FIELD_CMC (color, 62);
    FIELD_2RD (x_dir, 11);
    FIELD_BL (num_boundary_handles, 99);
  }

  SINCE (R_2013) {
    //FIELD_BS (pattern_type, 76); // 0=user; 1=predefined; 2=custom
    FIELD_BL (is_solid_fill, 0);
    FIELD_BD (angle, 52);
    FIELD_BD (scale_spacing, 41); //default 1.0
    FIELD_B (double_flag, 77);
    FIELD_BL (num_deflines, 78);
    REPEAT (num_deflines, deflines, Dwg_HATCH_DefLine)
    REPEAT_BLOCK
        SUB_FIELD_BD (deflines[rcount1], angle, 53);
        SUB_FIELD_2BD_1 (deflines[rcount1], pt0, 43);
        SUB_FIELD_2BD_1 (deflines[rcount1], offset, 45);
        SUB_FIELD_BS (deflines[rcount1], num_dashes, 79);
        FIELD_VECTOR (deflines[rcount1].dashes, BD, deflines[rcount1].num_dashes, 49)
    END_REPEAT_BLOCK
    SET_PARENT (deflines, (Dwg_Entity_HATCH*)_obj)
    END_REPEAT (deflines);
  }

  // not DXF
  FIELD_CMC (color, 0);
  FIELD_2RD (x_dir, 0);
  FIELD_BL (num_boundary_handles, 0);

  COMMON_ENTITY_HANDLE_DATA;
  HANDLE_VECTOR (boundary_handles, num_boundary_handles, 4, 0); /* DXF: inlined above */

DWG_OBJECT_END

#endif

//pg.139
DWG_OBJECT (IDBUFFER)

  SUBCLASS (AcDbIdBuffer)
  FIELD_RC (unknown, 0);
  FIELD_BL (num_obj_ids, 0);
  VALUEOUTOFBOUNDS (num_obj_ids, 10000)

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (obj_ids, num_obj_ids, 4, 330);

DWG_OBJECT_END

//pg.204 20.4.80
DWG_ENTITY (IMAGE)

  SUBCLASS (AcDbRasterImage)
  FIELD_BL (class_version, 90);
  if (FIELD_VALUE (class_version) > 10)
    return DWG_ERR_VALUEOUTOFBOUNDS;
  FIELD_3DPOINT (pt0, 10);
  FIELD_3DPOINT (uvec, 11);
  FIELD_3DPOINT (vvec, 12);
  FIELD_2RD (size, 13);
  FIELD_HANDLE (imagedef, 5, 340); // hard pointer
  FIELD_BS (display_props, 70);
  FIELD_B (clipping, 280);
  FIELD_RC (brightness, 281);
  FIELD_RC (contrast, 282);
  FIELD_RC (fade, 283);
  FIELD_HANDLE (imagedefreactor, 3, 360); // hard owner
  SINCE (R_2010) {
    FIELD_B (clip_mode, 0);
  }
  FIELD_BS (clip_boundary_type, 71); // 1 rect, 2 polygon
  if (FIELD_VALUE (clip_boundary_type) == 1)
    FIELD_VALUE (num_clip_verts) = 2;
  else
    FIELD_BL (num_clip_verts, 91);
  FIELD_2RD_VECTOR (clip_verts, num_clip_verts, 14);

  DXF { SINCE (R_2010) {
    FIELD_B (clip_mode, 290);
  }}
  COMMON_ENTITY_HANDLE_DATA;
DWG_ENTITY_END

//pg.142 test-data/*/Leader_*.dwg
DWG_OBJECT (IMAGEDEF)
  SUBCLASS (AcDbRasterImageDef)
  FIELD_BL (class_version, 90);
  if (FIELD_VALUE (class_version) > 10)
    return DWG_ERR_VALUEOUTOFBOUNDS;
  FIELD_2RD (image_size, 10);
  FIELD_T (file_path, 1);
  FIELD_B (is_loaded, 280);
  FIELD_RC (resunits, 281);
  FIELD_2RD (pixel_size, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

//PG.143
DWG_OBJECT (IMAGEDEF_REACTOR)
  SUBCLASS (AcDbRasterImageDefReactor)
  FIELD_BL (class_version, 90);
  if (FIELD_VALUE (class_version) > 10)
    return DWG_ERR_VALUEOUTOFBOUNDS;

  START_OBJECT_HANDLE_STREAM;
  DXF { VALUE_HANDLE (obj->tio.object->ownerhandle, ownerhandle, 3, 330); }
DWG_OBJECT_END

//pg.144
DWG_OBJECT (LAYER_INDEX)
  SUBCLASS (AcDbIndex)
  FIELD_TIMEBLL (last_updated, 40);
  SUBCLASS (AcDbLayerIndex)
  FIELD_BL (num_entries, 0);
  VALUEOUTOFBOUNDS (num_entries, 20000)
  DXF { VALUE_BL (0, 90); }
  REPEAT (num_entries, entries, Dwg_LAYER_entry)
  REPEAT_BLOCK
      SUB_FIELD_BL (entries[rcount1], numlayers, 0);
      SUB_FIELD_T (entries[rcount1], name, 8);
      SUB_FIELD_HANDLE (entries[rcount1], handle, 5, 360);
      DXF { SUB_FIELD_BL (entries[rcount1], numlayers, 90); }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (entries)
  END_REPEAT (entries)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// (varies)
DWG_OBJECT (PLOTSETTINGS)
  // See also LAYOUT
  SUBCLASS (AcDbPlotSettings)
  FIELD_T (printer_cfg_file, 1);
  FIELD_T (paper_size, 2);
  FIELD_BSx (plot_flags, 0);
  FIELD_BD (left_margin, 40);
  FIELD_BD (bottom_margin, 41);
  FIELD_BD (right_margin, 42);
  FIELD_BD (top_margin, 43);
  FIELD_BD (paper_width, 44);
  FIELD_BD (paper_height, 45);
  FIELD_T (canonical_media_name, 4);
  FIELD_2BD_1 (plot_origin, 46);
  FIELD_BS (plot_paper_unit, 0);
  FIELD_BS (plot_rotation_mode, 0);
  FIELD_BS (plot_type, 0);
  FIELD_2BD_1 (plot_window_ll, 48);
  FIELD_2BD_1 (plot_window_ur, 140);
  UNTIL (R_2000) {
    ENCODER {
      if (_obj->plotview && !_obj->plotview_name)
        _obj->plotview_name = dwg_handle_name (dwg, "VIEW", _obj->plotview);
    }
    FIELD_T (plotview_name, 6);
    DECODER {
      _obj->plotview = dwg_find_tablehandle (dwg, _obj->plotview_name, "VIEW");
    }
  }
  LATER_VERSIONS {
    DECODER {
      if (!_obj->plotview && _obj->plotview_name)
        _obj->plotview = dwg_find_tablehandle (dwg, _obj->plotview_name, "VIEW");
    }
    DXF {
      FIELD_T (plotview_name, 6);
    } else {
      FIELD_HANDLE (plotview, 4, 6);
    }
    DECODER {
      if (!_obj->plotview_name)
        _obj->plotview_name = dwg_handle_name (dwg, "VIEW", _obj->plotview);
    }
  }
  FREE { FIELD_TV (plotview_name, 6); FIELD_HANDLE (plotview, 5, 6); }
  FIELD_BD (paper_units, 142);
  FIELD_BD (drawing_units, 143);
  DXF {
    FIELD_BS (plot_flags, 70);
    FIELD_BS (plot_paper_unit, 72);
    FIELD_BS (plot_rotation_mode, 73);
    FIELD_BS (plot_type, 74);
  }
  FIELD_T (stylesheet, 7);
  FIELD_BS (std_scale_type, 75);
  FIELD_BD (std_scale_factor, 147);
  FIELD_2BD_1 (paper_image_origin, 148);
  SINCE (R_2004)
    {
      FIELD_BS (shadeplot_type, 76);
      FIELD_BS (shadeplot_reslevel, 77);
      FIELD_BS (shadeplot_customdpi, 78);
    }
  SINCE (R_2007) {
    FIELD_HANDLE (shadeplot, 4, 333);
  }
DWG_OBJECT_END

//pg.145
DWG_OBJECT (LAYOUT)

  SUBCLASS (AcDbPlotSettings)
  FIELD_T (plotsettings.printer_cfg_file, 1);
  FIELD_T (plotsettings.paper_size, 2);
  FIELD_BSx (plotsettings.plot_flags, 0);
  FIELD_BD (plotsettings.left_margin, 40);
  FIELD_BD (plotsettings.bottom_margin, 41);
  FIELD_BD (plotsettings.right_margin, 42);
  FIELD_BD (plotsettings.top_margin, 43);
  FIELD_BD (plotsettings.paper_width, 44);
  FIELD_BD (plotsettings.paper_height, 45);
  FIELD_T (plotsettings.canonical_media_name, 4);
  FIELD_2BD_1 (plotsettings.plot_origin, 46);
  FIELD_BS (plotsettings.plot_paper_unit, 0);
  FIELD_BS (plotsettings.plot_rotation_mode, 0);
  FIELD_BS (plotsettings.plot_type, 0);
  FIELD_2BD_1 (plotsettings.plot_window_ll, 48);
  FIELD_2BD_1 (plotsettings.plot_window_ur, 140);
  UNTIL (R_2000) {
    ENCODER {
      if (_obj->plotsettings.plotview && !_obj->plotsettings.plotview_name)
        _obj->plotsettings.plotview_name = dwg_handle_name (dwg, "VIEW",
                                             _obj->plotsettings.plotview);
    }
    FIELD_T (plotsettings.plotview_name, 6);
    DECODER {
      _obj->plotsettings.plotview = dwg_find_tablehandle (dwg,
                                      _obj->plotsettings.plotview_name, "VIEW");
    }
  }
  LATER_VERSIONS {
    DECODER {
      if (!_obj->plotsettings.plotview && _obj->plotsettings.plotview_name)
        _obj->plotsettings.plotview = dwg_find_tablehandle (dwg,
                 _obj->plotsettings.plotview_name, "VIEW");
    }
    DXF {
      FIELD_T (plotsettings.plotview_name, 6);
    } else {
      FIELD_HANDLE (plotsettings.plotview, 4, 6);
    }
    DECODER {
      if (!_obj->plotsettings.plotview_name)
        _obj->plotsettings.plotview_name = dwg_handle_name (dwg, "VIEW",
                                              _obj->plotsettings.plotview);
    }
  }
  FREE { FIELD_TV (plotsettings.plotview_name, 6); FIELD_HANDLE (plotsettings.plotview, 5, 6); }
  FIELD_BD (plotsettings.paper_units, 142);
  FIELD_BD (plotsettings.drawing_units, 143);
  DXF {
    FIELD_BS (plotsettings.plot_flags, 70);
    FIELD_BS (plotsettings.plot_paper_unit, 72);
    FIELD_BS (plotsettings.plot_rotation_mode, 73);
    FIELD_BS (plotsettings.plot_type, 74);
  }
  FIELD_T (plotsettings.stylesheet, 7);
  FIELD_BS (plotsettings.std_scale_type, 75);
  FIELD_BD (plotsettings.std_scale_factor, 147);
  FIELD_2BD_1 (plotsettings.paper_image_origin, 148);
  SINCE (R_2004)
    {
      FIELD_BS (plotsettings.shadeplot_type, 76);
      FIELD_BS (plotsettings.shadeplot_reslevel, 77);
      FIELD_BS (plotsettings.shadeplot_customdpi, 78);
    }
  SINCE (R_2007) {
    FIELD_HANDLE (plotsettings.shadeplot, 4, 333);
  }

  SUBCLASS (AcDbLayout)
  FIELD_T (layout_name, 1);
  DXF {
    FIELD_BS (layout_flags, 70);
  }
  FIELD_BS (tab_order, 71);
  FIELD_BSx (layout_flags, 0);
  FIELD_3DPOINT (INSBASE, 0);
  FIELD_2RD (LIMMIN, 10);
  FIELD_2RD (LIMMAX, 11);
  DXF {
    FIELD_3DPOINT (INSBASE, 12);
    FIELD_3DPOINT (EXTMIN, 14);
    FIELD_3DPOINT (EXTMAX, 15);
    FIELD_BD (ucs_elevation, 146);
  }
  FIELD_3DPOINT (UCSORG, 13);
  FIELD_3DPOINT (UCSXDIR, 16);
  FIELD_3DPOINT (UCSYDIR, 17);
  FIELD_BD (ucs_elevation, 0);
  FIELD_BS (UCSORTHOVIEW, 76);
  FIELD_3DPOINT (EXTMIN, 0);
  FIELD_3DPOINT (EXTMAX, 0);

  SINCE (R_2004) {
    FIELD_BL (num_viewports, 0);
    VALUEOUTOFBOUNDS (num_viewports, 10000)
  }

  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (block_header, 4, 330); // => pspace or mspace (owner)
  FIELD_HANDLE0 (active_viewport, 4, 331);
  FIELD_HANDLE0 (base_ucs, 5, 346);
  FIELD_HANDLE0 (named_ucs, 5, 345);

  SINCE (R_2004) {
    HANDLE_VECTOR (viewports, num_viewports, 4, 0);
  }

DWG_OBJECT_END

//20.4.85 p.211
DWG_ENTITY (LWPOLYLINE)

  SUBCLASS (AcDbPolyline)
#ifdef IS_DXF
  FIELD_BL (num_points, 90);
  //1 closed, 128 plinegen
  VALUE_BS ((FIELD_VALUE (flag) & 128) + (FIELD_VALUE (flag) & 512 ? 1 : 0), 70);
#else
  FIELD_BS (flag, 70); // 512 closed, 128 plinegen, 4 constwidth, 8 elevation, 2 thickness
                       // 1 extrusion, 16 num_bulges, 1024 vertexidcount, 32 numwidths
#endif

  if (FIELD_VALUE (flag) & 4)
    FIELD_BD (const_width, 43);
  if (FIELD_VALUE (flag) & 8)
    FIELD_BD (elevation, 38);
  if (FIELD_VALUE (flag) & 2)
    FIELD_BD (thickness, 39);
  if (FIELD_VALUE (flag) & 1) //clashes with the dxf closed bit flag 512
    FIELD_3BD (extrusion, 210);

#ifndef IS_DXF
  FIELD_BL (num_points, 90);
  VALUEOUTOFBOUNDS (num_points, 20000)
#endif

  if (FIELD_VALUE (flag) & 16)
    FIELD_BL (num_bulges, 0);
  SINCE (R_2010) {
    if (FIELD_VALUE (flag) & 1024)
      FIELD_BL (num_vertexids, 0); //always same as num_points
  }
  if (FIELD_VALUE (flag) & 32)
    FIELD_BL (num_widths, 0);

#ifdef IS_DXF
    REPEAT (num_points, points, BITCODE_2RD)
      {
        FIELD_2RD (points[rcount1], 10);
        if (FIELD_VALUE (num_widths) && FIELD_VALUE (widths) &&
            FIELD_VALUE (num_bulges) == FIELD_VALUE (num_points) &&
            (FIELD_VALUE (widths[rcount1].start) != 0.0 ||
             FIELD_VALUE (widths[rcount1].end) != 0.0))
          {
            FIELD_BD (widths[rcount1].start, 40);
            FIELD_BD (widths[rcount1].end, 41);
          }
        if (FIELD_VALUE (num_bulges) && FIELD_VALUE (bulges) &&
            FIELD_VALUE (num_bulges) == FIELD_VALUE (num_points))
          FIELD_BD (bulges[rcount1], 42);
        SINCE (R_2010) {
          if (FIELD_VALUE (num_vertexids) && FIELD_VALUE (vertexids) &&
              FIELD_VALUE (num_vertexids) == FIELD_VALUE (num_points))
            FIELD_BL (vertexids[rcount1], 91);
        }
      }
    END_REPEAT (points)
#else
#  ifndef IS_RELEASE
    if (FIELD_VALUE (num_points) > 20000) {
      LOG_ERROR ("Invalid LWPOLYLINE.num_points %ld", (long)FIELD_VALUE (num_points));
      _obj->num_points = 0;
      DEBUG_HERE_OBJ
      return DWG_ERR_VALUEOUTOFBOUNDS;
    }
#  endif
    VERSIONS (R_13, R_14) {
      FIELD_2RD_VECTOR (points, num_points, 10);
    }
    IF_FREE_OR_SINCE (R_2000) {
      FIELD_2DD_VECTOR (points, num_points, 10);
    }

    FIELD_VECTOR (bulges, BD, num_bulges, 42);
    SINCE (R_2010) {
      FIELD_VECTOR (vertexids, BL, num_vertexids, 91);
    }
    REPEAT (num_widths, widths, Dwg_LWPOLYLINE_width)
    REPEAT_BLOCK
        SUB_FIELD_BD (widths[rcount1],start, 40);
        SUB_FIELD_BD (widths[rcount1],end, 41);
    END_REPEAT_BLOCK
    END_REPEAT (widths)
#endif

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

//(74+varies) pg.149
DWG_ENTITY (OLE2FRAME)

  SUBCLASS (AcDbOle2Frame)
#ifdef IS_DXF
  // via dwg_decode_ole2() from the first 0x80 bytes in data
  FIELD_BS (oleversion, 70); //  always 2
  FIELD_TF (oleclient, strlen (_obj->oleclient), 3);
  FIELD_3BD (pt1, 10);  // upper left
  FIELD_3BD (pt2, 11);  // lower right
#endif
  FIELD_BS (type, 71); // 1: Link, 2: Embedded, 3: Static
  SINCE (R_2000) {
    FIELD_BS (mode, 72); // tile_mode, 0: mspace, 1: pspace
    DXF { FIELD_RC (lock_aspect, 73); }
  }
  ENCODER {
    if (FIELD_VALUE (data_size) && !FIELD_VALUE (data))
      FIELD_VALUE (data_size) = 0;
  }
#ifndef IS_JSON
  FIELD_BL (data_size, 90);
#endif
  FIELD_BINARY (data, FIELD_VALUE (data_size), 310);
#ifdef IS_DECODER
  dwg_decode_ole2 (_obj);
#endif
#ifdef IS_DXF
  VALUE_TFF ("OLE", 1);
#endif

  SINCE (R_2000) {
    FIELD_RC (lock_aspect, 0);
  }

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

//pg.276
#if 0 /* no proxy subtypes yet. seems to be the same as LWPOLYLINE */
DWG_ENTITY (PROXY_LWPOLYLINE)

  DECODE_UNKNOWN_BITS
  FIELD_RL (size);
  FIELD_BS (flag, 70);

  if (FIELD_VALUE (flag) & 4)
    FIELD_BD (const_width, 43);
  if (FIELD_VALUE (flag) & 8)
    FIELD_BD (elevation, 38);
  if (FIELD_VALUE (flag) & 2)
    FIELD_BD (thickness, 39);
  if (FIELD_VALUE (flag) & 1)
    FIELD_3BD (extrusion, 210);

  FIELD_BL (num_points, 90);
  VALUEOUTOFBOUNDS (num_points, 20000)

  if (FIELD_VALUE (flag) & 16)
    FIELD_BL (num_bulges, 0);
  if (FIELD_VALUE (flag) & 32)
    FIELD_BL (num_widths, 0);

  VERSIONS (R_13, R_14) {
    FIELD_2RD_VECTOR (points, num_points);
  }
  IF_FREE_OR_SINCE (R_2000) {
    FIELD_2DD_VECTOR (points, num_points);
  }

  FIELD_VECTOR (bulges, BD, num_bulges);
  REPEAT (num_widths, widths, Dwg_LWPOLYLINE_width)
  REPEAT_BLOCK
      SUB_FIELD_BD (widths[rcount1].start);
      SUB_FIELD_BD (widths[rcount1].end);
  END_REPEAT_BLOCK
  END_REPEAT (widths)

  FIELD_RC (unknown_1);
  FIELD_RC (unknown_2);
  FIELD_RC (unknown_3);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END
#endif /* no proxy subtypes yet */

//(498) pg.149 r2000+
DWG_ENTITY (PROXY_ENTITY)

  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbProxyEntity)
  UNTIL (R_14) {
    FIELD_BL (class_id, 90);
  }
  LATER_VERSIONS {
    FIELD_BL (class_id, 91);
  }
  PRE (R_2018)
  {
    int dxf = dat->version <= R_14 ? 91: 95;
    FIELD_BL (version, dxf); // i.e. version << 8 + maint_version
  }
  SINCE (R_2018)
  { // if encode from earlier: maint_version = version<<16 + acad version
    FIELD_BL (version, 71);
    FIELD_BL (maint_version, 97);
  }
  SINCE (R_2000)
  {
    FIELD_B (from_dxf, 70); // Original Data Format: 0 dwg, 1 dxf
  }

  DECODER {
    unsigned char opts = dat->opts;
    _obj->data_numbits = (dat->size * 8) - bit_position (dat);
    _obj->data_size = dat->size - dat->byte;
    if (dat->size > obj->size)
      {
        LOG_TRACE ("dat not restricted, dat->size %lu > obj->size %u\n",
                   dat->size, obj->size);
        _obj->data_numbits = ((obj->address * 8) + obj->bitsize) - bit_position (dat);
        _obj->data_size = _obj->data_numbits % 8;
        if (_obj->data_numbits) _obj->data_size++;
      }
    LOG_TRACE ("data_numbits: " FORMAT_BL "\n", _obj->data_numbits);
    LOG_TRACE ("data_size: " FORMAT_BL "\n", _obj->data_size);
    dat->opts &= 0xf0;
    FIELD_TF (data, _obj->data_size, 310);
    dat->opts = opts;
  }
  ENCODER {
    // write is always aligned
    if ((dwg->opts & DWG_OPTS_INDXF) && !_obj->data_numbits)
      _obj->data_numbits = 8 * _obj->data_size;
    LOG_TRACE ("data_numbits: " FORMAT_BL "\n", _obj->data_numbits);
    LOG_TRACE ("data_size: " FORMAT_BL "\n", _obj->data_size);
  }
  JSON {
    FIELD_BL (data_numbits, 0);
  }
  DXF_OR_PRINT {
    // preview 92/310 is also proxy data
    FIELD_BL (data_size, 93);
  }
#ifndef IS_DECODER
  FIELD_BINARY (data, FIELD_VALUE (data_size), 310);
#endif
#if defined IS_DECODER || defined IS_ENCODER
  {
    int bits = _obj->data_numbits - (_obj->data_size * 8);
    if (!(bits > -8 && bits <= 0))
      LOG_ERROR ("Invalid data_numbits %u - (_obj->data_size %u * 8): %d",
                 _obj->data_numbits, _obj->data_size, bits);
    assert (bits > -8 && bits <= 0);
    if (bits < 0)
      // back off a few bits, we wrote too much
      bit_advance_position (dat, bits);
  }
#endif

  COMMON_ENTITY_HANDLE_DATA;
#ifdef IS_DECODER
  {
    unsigned long pos = bit_position (hdl_dat);
    unsigned char opts = dat->opts;
    dat->opts &= 0xf0;
    _obj->num_objids = 0;
    while (hdl_dat->byte < hdl_dat->size)
      {
        Dwg_Handle hdl;
        if (bit_read_H (hdl_dat, &hdl))
          break;
        else
          _obj->num_objids++;
      }
    dat->opts = opts;
    bit_set_position (hdl_dat, pos);
  }
#endif
  HANDLE_VECTOR (objids, num_objids, ANYCODE, 340); // code 3 or 4

DWG_ENTITY_END

//(499) pg.149 r2000+
DWG_OBJECT (PROXY_OBJECT)

  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbProxyObject)
  FIELD_BL (class_id, 91);
  PRE (R_2018)
  {
    FIELD_BL (version, 95);
  }
  SINCE (R_2018)
  { // if encode from earlier: maint_version = version<<16 + acad version
    FIELD_BL (version, 71);
    FIELD_BL (maint_version, 97);
  }
  SINCE (R_2000)
  {
    FIELD_B (from_dxf, 70); // Original Data Format: 0 dwg, 1 dxf
  }

  DECODER {
    unsigned char opts = dat->opts;
    _obj->data_numbits = (dat->size * 8) - bit_position (dat);
    _obj->data_size = dat->size - dat->byte;
    if (dat->size > obj->size)
      {
        LOG_TRACE ("dat not restricted, dat->size %lu > obj->size %u\n",
                   dat->size, obj->size);
        _obj->data_numbits
            = ((obj->address * 8) + obj->bitsize) - bit_position (dat);
        _obj->data_size = _obj->data_numbits % 8;
        if (_obj->data_numbits) _obj->data_size++;
      }
    LOG_TRACE ("data_numbits: " FORMAT_BL "\n", _obj->data_numbits);
    LOG_TRACE ("data_size: " FORMAT_BL "\n", _obj->data_size);
    dat->opts &= 0xf0;
    FIELD_TF (data, _obj->data_size, 310);
    dat->opts = opts;
  }
  ENCODER {
    // write is always aligned
    if ((dwg->opts & DWG_OPTS_INDXF) && !_obj->data_numbits)
      _obj->data_numbits = 8 * _obj->data_size;
    LOG_TRACE ("data_numbits: " FORMAT_BL "\n", _obj->data_numbits);
    LOG_TRACE ("data_size: " FORMAT_BL "\n", _obj->data_size);
  }
  JSON {
    FIELD_BL (data_numbits, 0);
  }
  DXF_OR_PRINT {
    // preview 92/310 is also proxy data
    FIELD_BL (data_size, 93);
  }
#ifndef IS_DECODER
  FIELD_BINARY (data, FIELD_VALUE (data_size), 310);
#endif
#if defined IS_DECODER || defined IS_ENCODER
  {
    int bits = _obj->data_numbits - (_obj->data_size * 8);
    if (!(bits > -8 && bits <= 0))
      LOG_ERROR ("Invalid data_numbits %u - (_obj->data_size %u * 8): %d",
                 _obj->data_numbits, _obj->data_size, bits);
    assert (bits > -8 && bits <= 0);
    if (bits < 0)
      // back off a few bits, we wrote too much
      bit_advance_position (dat, bits);
  }
#endif

  START_OBJECT_HANDLE_STREAM;
#ifdef IS_DECODER
  {
    unsigned long pos = bit_position (hdl_dat);
    unsigned char opts = dat->opts;
    dat->opts &= 0xf0;
    _obj->num_objids = 0;
    while (hdl_dat->byte < hdl_dat->size)
      {
        Dwg_Handle hdl;
        if (bit_read_H (hdl_dat, &hdl))
          break;
        else
          _obj->num_objids++;
      }
    dat->opts = opts;
    bit_set_position (hdl_dat, pos);
  }
#endif
  HANDLE_VECTOR (objids, num_objids, ANYCODE, 340); // code 3 or 4

DWG_OBJECT_END

// 20.4.99 Value, page 241. for FIELD and TABLE
#define TABLE_value_fields(value)                                             \
  PRE (R_2007) { FIELD_VALUE (value.data_type) &= ~0x200; }                   \
  LATER_VERSIONS { FIELD_BL (value.format_flags, 93); }                       \
  FIELD_BL (value.data_type, 90);                                             \
  if (!(dat->version >= R_2007 && FIELD_VALUE (value.format_flags) & 1))      \
    {                                                                         \
      switch (FIELD_VALUE (value.data_type))                                  \
        {                                                                     \
        case 0: /* kUnknown */                                                \
          FIELD_BL (value.data_long, 91);                                     \
          break;                                                              \
        case 1: /* kLong */                                                   \
          FIELD_BL (value.data_long, 91);                                     \
          break;                                                              \
        case 2: /* kDouble */                                                 \
          FIELD_BD (value.data_double, 140);                                  \
          break;                                                              \
        case 4:                           /* kString */                       \
          FIELD_T (value.data_string, 1); /* and 2. TODO multiple lines */    \
          break;                                                              \
        case 8: /* kDate */                                                   \
          FIELD_BL (value.data_size, 92);                                     \
          FIELD_BINARY (value.data_date, FIELD_VALUE (value.data_size), 310); \
          break;                                                              \
        case 16: /* kPoint */                                                 \
          FIELD_2RD (value.data_point, 11);                                   \
          break;                                                              \
        case 32: /* k3dPoint */                                               \
          FIELD_3RD (value.data_3dpoint, 11);                                 \
          break;                                                              \
        case 64: /* kObjectId */                                              \
          FIELD_HANDLE (value.data_handle, -1, 330);                          \
          break;                                                              \
        case 128: /* kBuffer */                                               \
          LOG_ERROR ("Unknown data type in TABLE entity: \"kBuffer\".\n")     \
          break;                                                              \
        case 256: /* kResBuf */                                               \
          LOG_ERROR ("Unknown data type in TABLE entity: \"kResBuf\".\n")     \
          break;                                                              \
        case 512: /* kGeneral since r2007*/                                   \
          SINCE (R_2007) { FIELD_BL (value.data_size, 0); }                   \
          else                                                                \
          {                                                                   \
            LOG_ERROR (                                                       \
                "Unknown data type in TABLE entity: \"kGeneral before "       \
                "R_2007\".\n")                                                \
          }                                                                   \
          break;                                                              \
        default:                                                              \
          LOG_ERROR ("Invalid data type in TABLE entity\n")                   \
          DEBUG_HERE_OBJ                                                      \
          error |= DWG_ERR_INVALIDTYPE;                                       \
          break;                                                              \
          /*return DWG_ERR_INVALIDTYPE; */                                    \
        }                                                                     \
    }                                                                         \
  SINCE (R_2007)                                                              \
  {                                                                           \
    FIELD_BL (value.unit_type, 94);                                           \
    FIELD_T (value.format_string, 300);                                       \
    FIELD_T (value.value_string, 302);                                        \
  }

DWG_OBJECT (FIELD)

  SUBCLASS (AcDbField)
  FIELD_T (id, 1);
  FIELD_T (code, 2); // and code 3 for subsequent >255 chunks
  // DXF { }
  FIELD_BL (num_childs, 90);
  VALUEOUTOFBOUNDS (num_childs, 20000)
  FIELD_BL (num_objects, 97);
  VALUEOUTOFBOUNDS (num_objects, 20000)
  PRE (R_2007) {
    FIELD_TV (format, 4);
  }
  FIELD_BL (evaluation_option, 91);
  FIELD_BL (filing_option, 92);
  FIELD_BL (field_state, 94);
  FIELD_BL (evaluation_status, 95);
  FIELD_BL (evaluation_error_code, 96);
  //DEBUG_HERE_OBJ
  FIELD_T (evaluation_error_msg, 300);
  TABLE_value_fields (value)
  if (error & DWG_ERR_INVALIDTYPE)
    return error;

  FIELD_T (value_string, 301); // and 9 for subsequent >255 chunks
  FIELD_BL (value_string_length, 98); //ODA bug TV

  FIELD_BL (num_childval, 93);
  VALUEOUTOFBOUNDS (num_childval, 20000)
  REPEAT (num_childval, childval, Dwg_FIELD_ChildValue)
  REPEAT_BLOCK
      SUB_FIELD_T (childval[rcount1],key, 6);
      TABLE_value_fields (childval[rcount1].value)
      if (error & DWG_ERR_INVALIDTYPE)
        {
          JSON_END_REPEAT (childval);
          return error;
        }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (childval)
  END_REPEAT (childval)

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (childs, num_childs, 3, 360);
  HANDLE_VECTOR (objects, num_objects, 5, 331);

DWG_OBJECT_END

DWG_OBJECT (FIELDLIST)

  SUBCLASS (AcDbIdSet)
  FIELD_BL (num_fields, 90);
  VALUEOUTOFBOUNDS (num_fields, 20000)
  FIELD_B (unknown, 0); // has handles?

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (fields, num_fields, 0, 330); // 2 or 4, or 3.0.0
  SUBCLASS (AcDbFieldList)

DWG_OBJECT_END

// only one v2 testcase yet, but decodes fine
DWG_OBJECT (GEODATA)

  SUBCLASS (AcDbGeoData)
  UNTIL (R_2007) // r2009, class_version 1 really
    {
      // 1 for r2009, 2 for r2010 (default), 3 for r2013 (same as r2010)
      ENCODER {
        _obj->class_version = 1;
        _obj->scale_vec.x = _obj->scale_vec.y = _obj->scale_vec.z = 1.0;
      }
      FIELD_BL (class_version, 90);
      DXF { FIELD_BS (coord_type, 70); }
      FIELD_HANDLE (host_block, 4, 330);
      FIELD_BS (coord_type, 0); // 0 unknown, 1 local grid, 2 projected grid,
                                // 3 geographic (defined by latitude/longitude) (default)
      FIELD_3BD (ref_pt, 11);   // wrong in ODA docs
      FIELD_BL (units_value_horiz, 91); // 0-12, hor_units
      FIELD_3BD (design_pt, 10);
      FIELD_3BD (obs_pt, 0);    // always 0,0,0
      FIELD_3BD (up_dir, 210);
      // TODO compute if downgrading
      FIELD_BD (north_dir_angle_deg, 52);
      FIELD_3BD_1 (scale_vec, 43); // always 1,1,1

      FIELD_T (coord_system_def, 301); // & 303
      FIELD_T (geo_rss_tag, 302);
      FIELD_BD (unit_scale_horiz, 46); // hor_unit_scale
      FIELD_T (coord_system_datum, 303); //obsolete, ""
      FIELD_T (coord_system_wkt, 304);   //obsolete, ""
    }
  else // r2010+
    {
      IF_ENCODE_FROM_EARLIER {
        _obj->class_version = dat->version >= R_2013 ? 3 : 2;
      }
      FIELD_BL (class_version, 90); // TODO set by dwgversion 2 or 3
      FIELD_HANDLE (host_block, 4, 330);
      FIELD_BS (coord_type, 70); // 0 unknown, 1 local grid, 2 projected grid,
                                 // 3 geographic (defined by latitude/longitude) (default)
      FIELD_3BD (design_pt, 10);
      FIELD_3BD (ref_pt, 11);
      FIELD_BD (unit_scale_horiz, 40);
      FIELD_BL (units_value_horiz, 91); // hor_units
      FIELD_BD (unit_scale_vert, 41);   // 0xffffffff
      FIELD_BL (units_value_vert, 92);  // vert_units
      FIELD_3BD (up_dir, 210);
      // TODO compute if upgrading
      FIELD_2RD (north_dir, 12); // obsolete: 1,1,1
      // Civil3D fields:
      FIELD_BL (scale_est, 95); // None = 1 (default: ScaleEstMethodUnity),
                                // User defined = 2, Grid scale at reference point = 3,
                                // Prismodial = 4
      FIELD_BD (user_scale_factor, 141);
      FIELD_B (do_sea_level_corr, 294);
      FIELD_BD (sea_level_elev, 142);
      FIELD_BD (coord_proj_radius, 143);
      FIELD_T (coord_system_def, 301); // and 303 if longer
      FIELD_T (geo_rss_tag, 302);
    }
  if (FIELD_VALUE (class_version) > 10)
    return DWG_ERR_VALUEOUTOFBOUNDS;
  FIELD_T (observation_from_tag, 305);
  FIELD_T (observation_to_tag, 306);
  FIELD_T (observation_coverage_tag, 0);
  FIELD_BL (num_geomesh_pts, 93);
  VALUEOUTOFBOUNDS (num_geomesh_pts, 50000)
  REPEAT_N (FIELD_VALUE (num_geomesh_pts), geomesh_pts, Dwg_GEODATA_meshpt)
  REPEAT_BLOCK
      SUB_FIELD_2RD (geomesh_pts[rcount1],source_pt, 13);
      SUB_FIELD_2RD (geomesh_pts[rcount1],dest_pt, 14);
  END_REPEAT_BLOCK
  END_REPEAT (geomesh_pts);
  FIELD_BL (num_geomesh_faces, 96);
  VALUEOUTOFBOUNDS (num_geomesh_faces, 50000)
  REPEAT_N (FIELD_VALUE (num_geomesh_faces), geomesh_faces, Dwg_GEODATA_meshface)
  REPEAT_BLOCK
      SUB_FIELD_BL (geomesh_faces[rcount1],face1, 97);
      SUB_FIELD_BL (geomesh_faces[rcount1],face2, 98);
      SUB_FIELD_BL (geomesh_faces[rcount1],face3, 99);
  END_REPEAT_BLOCK
  END_REPEAT (geomesh_faces);

  UNTIL (R_2007) // r2009, class_version 1
    {
      ENCODER {
        _obj->ref_pt2d.x = _obj->ref_pt.y; _obj->ref_pt2d.y = _obj->ref_pt.x;
      }
      FIELD_B (has_civil_data, 0); // 1
      FIELD_B (obsolete_false, 0); // 0
      FIELD_2RD (ref_pt2d, 0);     // (y, x)
      FIELD_2RD (ref_pt2d, 0);
      FIELD_BL (unknown1, 0); // 0
      FIELD_BL (unknown2, 0); // 0
      FIELD_2RD (zero1, 0);   // origin (0,0)
      FIELD_2RD (zero2, 0);
      FIELD_B (unknown_b, 0); // 0
      FIELD_BD (north_dir_angle_deg, 0);
      FIELD_BD (north_dir_angle_rad, 0);
      FIELD_BL (scale_est, 0);
      FIELD_BD (user_scale_factor, 0);
      FIELD_B (do_sea_level_corr, 0);
      FIELD_BD (sea_level_elev, 0);
      FIELD_BD (coord_proj_radius, 0);
    }
  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

//pg.220, 20.4.91
DWG_OBJECT (RASTERVARIABLES)
  SUBCLASS (AcDbRasterVariables)
  FIELD_BL (class_version, 90);
  if (FIELD_VALUE (class_version) > 10)
    return DWG_ERR_VALUEOUTOFBOUNDS;
  FIELD_BS (image_frame, 70);
  FIELD_BS (image_quality, 71);
  FIELD_BS (units, 72);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// 20.4.93 page 221
DWG_OBJECT (SORTENTSTABLE)

  SUBCLASS (AcDbSortentsTable)
  FIELD_BL (num_ents, 0);
  VALUEOUTOFBOUNDS (num_ents, 50000)
  // read these code 0 handles from the normal stream
  str_dat = hdl_dat; hdl_dat = dat;
  HANDLE_VECTOR (sort_ents, num_ents, 0, 0);
  hdl_dat = str_dat;

  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (block_owner, 4, 0); // mspace or pspace
  HANDLE_VECTOR_N (ents, FIELD_VALUE (num_ents), 4, 0);

  DXF {
    for (vcount = 0; vcount < _obj->num_ents; vcount++)
      {
        FIELD_HANDLE (ents[vcount], 4, 331);
        FIELD_HANDLE (sort_ents[vcount], 0, 5);
      }
  }

DWG_OBJECT_END

//pg.222, 20.4.94 to clip external references
DWG_OBJECT (SPATIAL_FILTER)

  SUBCLASS (AcDbFilter)
  SUBCLASS (AcDbSpatialFilter)
  FIELD_BS (num_clip_verts, 70);
  VALUEOUTOFBOUNDS (num_clip_verts, 10000)
  FIELD_2RD_VECTOR (clip_verts, num_clip_verts, 10);
  FIELD_3BD (extrusion, 210);
  FIELD_3BD (origin, 10);
  FIELD_BS (display_boundary_on, 71);
  FIELD_BS (front_clip_on, 72);
  if (FIELD_VALUE (front_clip_on))
    FIELD_BD (front_clip_z, 40);

  FIELD_BS (back_clip_on, 73);
  if (FIELD_VALUE (back_clip_on))
    FIELD_BD (back_clip_z, 41);

  FIELD_VECTOR_N (inverse_transform, BD, 12, 40);
  FIELD_VECTOR_N (transform, BD, 12, 40);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

//pg.153, unstable, no coverage
DWG_OBJECT (SPATIAL_INDEX)

  SUBCLASS (AcDbIndex)
  FIELD_TIMEBLL (last_updated, 40);
  SUBCLASS (AcDbSpatialIndex)
  FIELD_BD (num1, 40);
  FIELD_BD (num2, 40);
  FIELD_BD (num3, 40);
  FIELD_BD (num4, 40);
  FIELD_BD (num5, 40);
  FIELD_BD (num6, 40);
  FIELD_BL (num_hdls, 90);
  HANDLE_VECTOR (hdls, num_hdls, 5, 330);
  FIELD_BL (bindata_size, 90);
  FIELD_BINARY (bindata, FIELD_VALUE (bindata_size), 310);
  DXF { VALUE_TFF ("END ACDBSPATIALINDEX BINARY DATA", 1); }

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// 20.4.101.3 Content format for TABLECONTENT and CellStyle_Field
#define ContentFormat_fields(fmt)                 \
  DXF { VALUE_TFF ("CONTENTFORMAT", 300) }        \
  DXF { VALUE_TFF ("CONTENTFORMAT_BEGIN", 1) }    \
  FIELD_BLx (fmt.property_override_flags, 90);    \
  FIELD_BLx (fmt.property_flags, 91);             \
  FIELD_BLx (fmt.value_data_type, 92);            \
  FIELD_BLx (fmt.value_unit_type, 93);            \
  FIELD_T (fmt.value_format_string, 300);         \
  FIELD_BD (fmt.rotation, 40);                    \
  FIELD_BD (fmt.block_scale, 140);                \
  FIELD_BL (fmt.cell_alignment, 94);              \
  FIELD_CMTC (fmt.content_color, 62);             \
  FIELD_HANDLE (fmt.text_style, 3, 340);          \
  FIELD_BD (fmt.text_height, 144);                \
  DXF { VALUE_TFF ("CONTENTFORMAT_END", 309) }

// Cell style 20.4.101.4 for TABLE, TABLECONTENT, TABLESTYLE, and CELLSTYLEMAP
#define CellStyle_fields(sty)						\
  DXF { VALUE_TFF ("TABLEFORMAT_BEGIN", 1) }				\
  FIELD_BL (sty.type, 90);						\
  FIELD_BSx (sty.data_flags, 170);					\
  if (FIELD_VALUE (sty.data_flags))					\
    {									\
      FIELD_BLx (sty.property_override_flags, 91);			\
      FIELD_BLx (sty.merge_flags, 92);					\
      FIELD_CMTC (sty.bg_color, 62);					\
      FIELD_BL (sty.content_layout, 93);				\
      ContentFormat_fields (sty.content_format);			\
      FIELD_BSx (sty.margin_override_flags, 171);			\
      if (FIELD_VALUE (sty.margin_override_flags))			\
	{								\
	  DXF { VALUE_TFF ("MARGIN", 301) }				\
	  DXF { VALUE_TFF ("CELLMARGIN_BEGIN", 1) }			\
	  FIELD_BD (sty.vert_margin, 40);				\
	  FIELD_BD (sty.horiz_margin, 40);				\
	  FIELD_BD (sty.bottom_margin, 40);				\
	  FIELD_BD (sty.right_margin, 40);				\
	  FIELD_BD (sty.margin_horiz_spacing, 40);			\
	  FIELD_BD (sty.margin_vert_spacing, 40);			\
	  DXF { VALUE_TFF ("CELLMARGIN_END", 309) }			\
	}								\
      FIELD_BL (sty.num_borders, 94); /* 0-6 */			\
      VALUEOUTOFBOUNDS (sty.num_borders, 6);				\
      REPEAT2 (sty.num_borders, sty.borders, Dwg_GridFormat)		\
      REPEAT_BLOCK							\
	DXF {								\
	  if (FIELD_VALUE (sty.borders[rcount2].index_mask))		\
	    {								\
	      SUB_FIELD_BL (sty.borders[rcount2],index_mask, 95);	\
	      VALUE_TFF ("GRIDFORMAT", 302);				\
	      VALUE_TFF ("GRIDFORMAT_BEGIN", 1);			\
	    }								\
	}								\
	SUB_FIELD_BLx (sty.borders[rcount2],index_mask, 0);		\
	if (FIELD_VALUE (sty.borders[rcount2].index_mask))		\
	  {								\
	    SUB_FIELD_BL (sty.borders[rcount2],border_overrides, 90);	\
	    SUB_FIELD_BL (sty.borders[rcount2],border_type, 91);	\
	    SUB_FIELD_CMTC (sty.borders[rcount2],color, 62);		\
	    SUB_FIELD_BLd (sty.borders[rcount2],linewt, 92);		\
	    SUB_FIELD_HANDLE (sty.borders[rcount2],ltype, 3, 340);	\
	    SUB_FIELD_BL (sty.borders[rcount2],visible, 93);		\
	    SUB_FIELD_BD (sty.borders[rcount2],double_line_spacing, 40);\
	  }								\
	DXF { VALUE_TFF ("GRIDFORMAT_END", 309) }			\
      END_REPEAT_BLOCK							\
      END_REPEAT (sty.borders);						\
    }									\
  DXF { VALUE_TFF ("TABLEFORMAT_END", 309) }

#if defined (DEBUG_CLASSES) || defined (IS_FREE)

// clang-format off
#define row tdata.rows[rcount1]
#define cell row.cells[rcount2]
#define content cell.cell_contents[rcount3]
#define geom cell.geometry[0]
#define attr content.attrs[rcount4]
#define merged fdata.merged_cells[rcount1]

// pg.237 20.4.97 for TABLE (2010+) and TABLECONTENT
#define TABLECONTENT_fields					\
  SUBCLASS (AcDbLinkedData)                                     \
  FIELD_T (ldata.name, 1);					\
  FIELD_T (ldata.description, 300);				\
  SUBCLASS (AcDbLinkedTableData)                                \
  FIELD_BL (tdata.num_cols, 90);				\
  REPEAT (tdata.num_cols, tdata.cols, Dwg_TableDataColumn)	\
  REPEAT_BLOCK							\
      SUB_FIELD_T (tdata.cols[rcount1],name, 300);		\
      DXF { VALUE_TFF ("LINKEDTABLEDATACOLUMN_BEGIN", 1) }      \
      SUB_FIELD_BL (tdata.cols[rcount1],custom_data, 91);	\
      DXF { VALUE_TFF ("DATAMAP_BEGIN", 1) }                    \
      CellStyle_fields (tdata.cols[rcount1].cellstyle);		\
      DXF { VALUE_TFF ("DATAMAP_END", 309) }                    \
      DXF { VALUE_TFF ("LINKEDTABLEDATACOLUMN_END", 309) }      \
  END_REPEAT_BLOCK						\
  SET_PARENT (tdata.cols, &_obj->tdata)				\
  END_REPEAT (tdata.cols);					\
  FIELD_BL (tdata.num_rows, 90);				\
  REPEAT (tdata.num_rows, tdata.rows, Dwg_TableRow)		\
  REPEAT_BLOCK							\
      FIELD_BL (row.num_cells, 90);				\
      REPEAT2 (row.num_cells, row.cells, Dwg_TableCell)		\
      REPEAT_BLOCK						\
          SUB_FIELD_BL (cell,flag, 90);				\
          SUB_FIELD_T (cell,tooltip, 300);			\
          SUB_FIELD_BL (cell,customdata, 91);			\
          SUB_FIELD_BL (cell,num_customdata_items, 90);		\
          REPEAT3 (cell.num_customdata_items, cell.customdata_items, Dwg_TABLE_CustomDataItem) \
          REPEAT_BLOCK						\
              SUB_FIELD_T (cell.customdata_items[rcount3],name, 300);	 \
              TABLE_value_fields (cell.customdata_items[rcount3].value); \
              if (error & DWG_ERR_INVALIDTYPE)			\
                {						\
                  JSON_END_REPEAT (cell.customdata_items);	\
                  JSON_END_REPEAT (row.cells);			\
                  JSON_END_REPEAT (tdata.rows);			\
                  return error;					\
                }						\
          END_REPEAT_BLOCK					\
          SET_PARENT_FIELD (cell.customdata_items, cell_parent, &_obj->cell)	\
          END_REPEAT (cell.customdata_items);			\
          SUB_FIELD_BL (cell,has_linked_data, 92);		\
          if (FIELD_VALUE (cell.has_linked_data))		\
            {							\
              SUB_FIELD_HANDLE (cell,data_link, 5, 340);	\
              SUB_FIELD_BL (cell,num_rows, 93);			\
              SUB_FIELD_BL (cell,num_cols, 94);			\
              SUB_FIELD_BL (cell,unknown, 96);			\
            }							\
          SUB_FIELD_BL (cell,num_cell_contents, 95);		\
          DXF { VALUE_TFF ("CONTENT", 302) }                    \
          DXF { VALUE_TFF ("CELLCONTENT_BEGIN", 1) }            \
          REPEAT3 (cell.num_cell_contents, cell.cell_contents, Dwg_TableCellContent) \
          REPEAT_BLOCK						\
              SUB_FIELD_BL (content,type, 90);			\
              if (FIELD_VALUE (content.type) == 1)		\
                {						\
                  DXF { VALUE_TFF ("VALUE", 300) }              \
                  /* 20.4.99 Value, page 241 */         	\
                  TABLE_value_fields (content.value)		\
                  if (error & DWG_ERR_INVALIDTYPE)		\
                    {						\
                      JSON_END_REPEAT (cell.cell_contents);	\
                      JSON_END_REPEAT (row.cells);		\
                      JSON_END_REPEAT (tdata.rows);		\
                      return error;				\
                    }						\
                }						\
              else if (FIELD_VALUE (content.type) == 2) { /* Field */	\
                SUB_FIELD_HANDLE (content,handle, 3, 340);	\
              }							\
              else if (FIELD_VALUE (content.type) == 4) { /* Block */	\
                SUB_FIELD_HANDLE (content,handle, 3, 340);	\
              }							\
              SUB_FIELD_BL (content,num_attrs, 91);		\
              REPEAT4 (content.num_attrs, content.attrs, Dwg_TableCellContent_Attr)	\
              REPEAT_BLOCK					\
                  SUB_FIELD_HANDLE (attr,attdef, 5, 330);	\
                  SUB_FIELD_T (attr,value, 301);		\
                  SUB_FIELD_BL (attr,index, 92);		\
              END_REPEAT_BLOCK					\
              SET_PARENT (content.attrs, &_obj->content)	\
              END_REPEAT (content.attrs);			\
              DXF { VALUE_TFF ("CELLCONTENT_END", 309) }        \
              DXF { VALUE_TFF ("FORMATTEDCELLCONTENT_BEGIN", 1) }  \
              FIELD_BS (content.has_content_format_overrides, 170) \
              if (FIELD_VALUE (content.has_content_format_overrides))	\
                {						\
                  ContentFormat_fields (content.content_format);\
                }						\
              DXF { VALUE_TFF ("FORMATTEDCELLCONTENT_END", 309) } \
          END_REPEAT_BLOCK					\
          SET_PARENT (cell.cell_contents, &_obj->cell)		\
          END_REPEAT (cell.cell_contents);			\
          SUB_FIELD_BL (cell, style_id, 90);			\
          SUB_FIELD_BL (cell, has_geom_data, 91);		\
          if (FIELD_VALUE (cell.has_geom_data))			\
            {							\
              SUB_FIELD_BL (cell,geom_data_flag, 91);		\
              SUB_FIELD_BD (cell,width_w_gap, 40);		\
              SUB_FIELD_BD (cell,height_w_gap, 41);		\
              SUB_FIELD_BL (cell,num_geometry, 94);		\
              SUB_FIELD_HANDLE (cell,tablegeometry, 4, 330);	\
              REPEAT (cell.num_geometry, cell.geometry, Dwg_CellContentGeometry) \
              REPEAT_BLOCK					\
                  SUB_FIELD_3BD (geom,dist_top_left, 10);	\
                  SUB_FIELD_3BD (geom,dist_center, 11);		\
                  SUB_FIELD_BD (geom,content_width, 43);	\
                  SUB_FIELD_BD (geom,content_height, 44);	\
                  SUB_FIELD_BD (geom,width, 45);		\
                  SUB_FIELD_BD (geom,height, 46);		\
                  SUB_FIELD_BL (geom,unknown, 95);		\
              END_REPEAT_BLOCK					\
              SET_PARENT_FIELD (cell.geometry, cell_parent, &_obj->cell) \
              END_REPEAT (cell.geometry);			\
            }							\
      END_REPEAT_BLOCK						\
      SET_PARENT_FIELD (row.cells, row_parent, &_obj->row)	\
      END_REPEAT (row.cells);					\
      SUB_FIELD_BL (row,custom_data, 91);			\
      SUB_FIELD_BL (row,num_customdata_items, 90);		\
      REPEAT3 (row.num_customdata_items, row.customdata_items, Dwg_TABLE_CustomDataItem) \
      REPEAT_BLOCK						\
          SUB_FIELD_T (row.customdata_items[rcount3],name, 300);	\
          TABLE_value_fields (row.customdata_items[rcount3].value);	\
          if (error & DWG_ERR_INVALIDTYPE)			\
            {							\
              JSON_END_REPEAT (row.customdata_items);		\
              JSON_END_REPEAT (tdata.rows);			\
              return error;					\
            }							\
      END_REPEAT_BLOCK						\
      SET_PARENT_FIELD (row.customdata_items, row_parent, &_obj->row)	\
      END_REPEAT (row.customdata_items);			\
      {								\
        CellStyle_fields (row.cellstyle);			\
        SUB_FIELD_BL (row,style_id, 90);			\
        SUB_FIELD_BL (row,height, 40);				\
      }								\
  END_REPEAT_BLOCK						\
  SET_PARENT (tdata.rows, &_obj->tdata)				\
  END_REPEAT (tdata.rows);					\
  FIELD_BL (tdata.num_field_refs, 0);				\
  HANDLE_VECTOR (tdata.field_refs, tdata.num_field_refs, 3, 0);	\
  FIELD_BL (fdata.num_merged_cells, 90);			\
  REPEAT (fdata.num_merged_cells, fdata.merged_cells, Dwg_FormattedTableMerged)	\
  REPEAT_BLOCK							\
      SUB_FIELD_BL (merged,top_row, 91);			\
      SUB_FIELD_BL (merged,left_col, 92);			\
      SUB_FIELD_BL (merged,bottom_row, 93);			\
      SUB_FIELD_BL (merged,right_col, 94);			\
  END_REPEAT_BLOCK						\
  SET_PARENT (fdata.merged_cells, &_obj->fdata)			\
  END_REPEAT (fdata.merged_cells)

// clang-format on

DWG_OBJECT (TABLECONTENT)
  DECODE_UNKNOWN_BITS
  TABLECONTENT_fields;

  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (tablestyle, 3, 340);
DWG_OBJECT_END

// pg.229 20.4.96, as ACAD_TABLE (varies)
// works ok for the pre-2010 variant, deriving from INSERT
// r2010+ it is TABLECONTENT
DWG_ENTITY (TABLE)

  DECODE_UNKNOWN_BITS
  SINCE (R_2010) //AC1024
    {
      FIELD_RC (unknown_rc, 0);
      FIELD_HANDLE (tablestyle, 5, 342);
      //FIELD_HANDLE (unknown_h, 5, 0);
      FIELD_BL (unknown_bl, 0);
      VERSION (R_2010)
        FIELD_B (unknown_b, 0); // default 1
      VERSION (R_2013)
        FIELD_BL (unknown_bl1, 0);
      // i.e. TABLECONTENT: 20.4.96.2 AcDbTableContent subclass: 20.4.97
      TABLECONTENT_fields;

#undef row
#undef cell
#undef content
#undef geom
#undef attr
#undef merged

    }
  else {
    SUBCLASS (AcDbBlockReference)
    FIELD_3BD (insertion_pt, 10);
    VERSIONS (R_13, R_14) {
      FIELD_3BD_1 (scale, 41);
    }
    SINCE (R_2000)
      {
        FIELD_BB (data_flags, 0);
        switch (FIELD_VALUE (data_flags))
          {
            case 0:
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_DD (scale.y, FIELD_VALUE (scale.x), 42);
              FIELD_DD (scale.z, FIELD_VALUE (scale.x), 43);
              break;
            case 1:
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_DD (scale.y, 1.0, 42);
              FIELD_DD (scale.z, 1.0, 43);
              break;
            case 2:
              FIELD_RD (scale.x, 41);
              FIELD_VALUE (scale.y) = FIELD_VALUE (scale.x);
              FIELD_VALUE (scale.z) = FIELD_VALUE (scale.x);
              break;
            case 3:
              FIELD_VALUE (scale.x) = 1.0;
              FIELD_VALUE (scale.y) = 1.0;
              FIELD_VALUE (scale.z) = 1.0;
              break;
            default:
              LOG_ERROR ("Invalid data_flags in TABLE entity %d\n",
                        (int)FIELD_VALUE (data_flags))
              _obj->data_flags = 0;
              DEBUG_HERE_OBJ
              return DWG_ERR_INVALIDTYPE;
              //break;
          }
  #ifndef IS_FREE
        FIELD_3PT_TRACE (scale, DD, 41);
  #endif
      }
  
    FIELD_BD (rotation, 50);
    FIELD_3BD (extrusion, 210);
    FIELD_B (has_attribs, 66);
  
    SINCE (R_2004) {
      FIELD_BL (num_owned, 0);
      VALUEOUTOFBOUNDS (num_owned, 10000)
    }
    FIELD_HANDLE (block_header, 5, 2);
    VERSIONS (R_13, R_2000)
      {
        if (FIELD_VALUE (has_attribs))
          {
            FIELD_HANDLE (first_attrib, 4, 0);
            FIELD_HANDLE (last_attrib, 4, 0);
          }
      }
  
    SINCE (R_2004)
      {
  #if defined (IS_JSON) || defined (IS_DXF)
        if (!_obj->attrib_handles && _obj->num_owned)
          _obj->num_owned = 0;
  #endif
        HANDLE_VECTOR (attrib_handles, num_owned, 4, 0)
      }
    if (FIELD_VALUE (has_attribs)) {
      FIELD_HANDLE (seqend, 3, 0);
    }
  
    SUBCLASS (AcDbTable)
    FIELD_HANDLE (tablestyle, 5, 342);
    FIELD_BS (flag_for_table_value, 90);
    FIELD_3BD (horiz_direction, 11);
    FIELD_BL (num_cols, 92);
    VALUEOUTOFBOUNDS (num_cols, 5000)
    FIELD_BL (num_rows, 91);
    VALUEOUTOFBOUNDS (num_rows, 5000)
    FIELD_VECTOR (col_widths, BD, num_cols, 142);
    FIELD_VECTOR (row_heights, BD, num_rows, 141);
    FIELD_VALUE (num_cells) = FIELD_VALUE (num_rows) * FIELD_VALUE (num_cols);
    #define cell cells[rcount1]
    REPEAT (num_cells, cells, Dwg_TABLE_Cell)
    REPEAT_BLOCK
        //SUBCLASS (AcDbDataCell)
        SUB_FIELD_BS (cell,type, 171);
        SUB_FIELD_RC (cell,flags, 172);
        SUB_FIELD_B (cell,is_merged_value, 173);
        SUB_FIELD_B (cell,is_autofit_flag, 174);
        SUB_FIELD_BL (cell,merged_width_flag, 175);
        SUB_FIELD_BL (cell,merged_height_flag, 176);
        DXF {
          PRE (R_2007) {
            SUB_FIELD_CAST (cell,cell_flag_override, BS, BL, 177);
          } LATER_VERSIONS {
            SUB_FIELD_BL (cell,cell_flag_override, 91);
          }
          SUB_FIELD_BS (cell,virtual_edge_flag, 178);
        }
        SUB_FIELD_BD (cell,rotation, 145);

        if (FIELD_VALUE (cell.type) == 1)
          { /* text cell */
            SUB_FIELD_HANDLE0 (cell,text_style, 3, 344);
            // TODO: <r2007 and empty style and shorter than 250, single dxf 1 line
            // else split into mult. text lines
            SUB_FIELD_T (cell,text_value, 1);
            SUB_FIELD_B (cell,additional_data_flag, 0);
          }
        if (FIELD_VALUE (cell.type) == 2)
          { /* block cell */
            SUB_FIELD_HANDLE0 (cell,block_handle, 3, 340);
            SUB_FIELD_BD (cell,block_scale, 144);
            SUB_FIELD_B (cell,additional_data_flag, 0);
            if (FIELD_VALUE (cell.additional_data_flag))
              {
                #define attr cell.attr_defs[rcount2]
                REPEAT2 (cell.num_attr_defs, cell.attr_defs, Dwg_TABLE_AttrDef)
                REPEAT_BLOCK
                    SUB_FIELD_HANDLE (cell.attr_defs[rcount2],attdef, 4, 331);
                    SUB_FIELD_BS (cell.attr_defs[rcount2],index, 179);
                    SUB_FIELD_T (cell.attr_defs[rcount2],text, 300); // dxf?
                END_REPEAT_BLOCK
                END_REPEAT (cell.attr_defs);
                //total_num_attr_defs += FIELD_VALUE (cell.num_attr_defs);
                #undef attr
              }
          }
        if (FIELD_VALUE (cells) &&
            (FIELD_VALUE (cell.type) == 1 ||
             FIELD_VALUE (cell.type) == 2))
          { /* common to both text and block cells */
            if (FIELD_VALUE (cell.additional_data_flag) == 1)
              {
                BITCODE_BL cell_flag;
                SUB_FIELD_BL (cell,cell_flag_override, 0);
                cell_flag = FIELD_VALUE (cell.cell_flag_override);
                SUB_FIELD_RC (cell,virtual_edge_flag, 0);
  
                if (cell_flag & 0x01)
                  SUB_FIELD_RS (cell,cell_alignment, 170);
                if (cell_flag & 0x02)
                  SUB_FIELD_B (cell,bg_fill_none, 283);
                if (cell_flag & 0x04)
                  SUB_FIELD_CMTC (cell,bg_color, 63);
                if (cell_flag & 0x08)
                  {
                    SUB_FIELD_CMTC (cell,content_color, 64);
                    SUB_FIELD_HANDLE (cell,text_style, 3, 7); //?
                  }
                if (cell_flag & 0x10) {
                  SUB_FIELD_HANDLE (cell,text_style, 3, 7);
                }
                if (cell_flag & 0x20)
                  SUB_FIELD_BD (cell,text_height, 140);
                if (cell_flag & 0x00040)
                  SUB_FIELD_CMTC (cell,top_grid_color, 69);
                if (cell_flag & 0x00400)
                  SUB_FIELD_BS (cell,top_grid_linewt, 279);
                if (cell_flag & 0x04000)
                  SUB_FIELD_BS (cell,top_visibility, 289);
                if (cell_flag & 0x00080)
                  SUB_FIELD_CMTC (cell,right_grid_color, 65);
                if (cell_flag & 0x00800)
                  SUB_FIELD_BS (cell,right_grid_linewt, 275);
                if (cell_flag & 0x08000)
                  SUB_FIELD_BS (cell,right_visibility, 285);
                if (cell_flag & 0x00100)
                  SUB_FIELD_CMTC (cell,bottom_grid_color, 66);
                if (cell_flag & 0x01000)
                  SUB_FIELD_BS (cell,bottom_grid_linewt, 276);
                if (cell_flag & 0x10000)
                  SUB_FIELD_BS (cell,bottom_visibility, 286);
                if (cell_flag & 0x00200)
                  SUB_FIELD_CMTC (cell,left_grid_color, 68);
                if (cell_flag & 0x02000)
                  SUB_FIELD_BS (cell,left_grid_linewt, 278);
                if (cell_flag & 0x20000)
                  SUB_FIELD_BS (cell,left_visibility, 288);
  
                SUB_FIELD_BL (cell,unknown, 0);
  
                // 20.4.99 Value, page 241
                TABLE_value_fields (cell.value)
                if (error & DWG_ERR_INVALIDTYPE)
                  {
                    JSON_END_REPEAT (cells);
                    return error;
                  }
              }
          }
    END_REPEAT_BLOCK
    SET_PARENT_OBJ (cells)
    END_REPEAT (cells);
    #undef cell
    /* End Cell Data (remaining data applies to entire table)*/
  
    /* COMMON: */
    FIELD_B (has_table_overrides, 0);
    if (FIELD_VALUE (has_table_overrides))
      {
        BITCODE_BL table_flag;
        FIELD_BL (table_flag_override, 93);
        table_flag = FIELD_VALUE (table_flag_override);
        if (table_flag & 0x0001)
          FIELD_B (title_suppressed, 280);
        FIELD_B (header_suppressed, 281); // yes, unchecked. always true
        if (table_flag & 0x0004)
          FIELD_BS (flow_direction, 70);
        if (table_flag & 0x0008)
          FIELD_BD (horiz_cell_margin, 40);
        if (table_flag & 0x0010)
          FIELD_BD (vert_cell_margin, 41);
        if (table_flag & 0x0020)
          FIELD_CMTC (title_row_color, 64); // CMTC?
        if (table_flag & 0x0040)
          FIELD_CMTC (header_row_color, 64); // CMTC?
        if (table_flag & 0x0080)
          FIELD_CMTC (data_row_color, 64);
        if (table_flag & 0x0100)
          FIELD_B (title_row_fill_none, 283);
        if (table_flag & 0x0200)
          FIELD_B (header_row_fill_none, 283);
        if (table_flag & 0x0400)
          FIELD_B (data_row_fill_none, 283);
        if (table_flag & 0x0800)
          FIELD_CMTC (title_row_fill_color, 63); // CMTC?
        if (table_flag & 0x1000)
          FIELD_CMTC (header_row_fill_color, 63); // CMTC?
        if (table_flag & 0x2000)
          {
            FIELD_CMTC (data_row_fill_color, 63); // CMTC?
            FIELD_HANDLE (title_row_style_override, ANYCODE, 7);
          }
        if (table_flag & 0x4000)
          FIELD_BS (title_row_alignment, 170);
        if (table_flag & 0x8000)
          FIELD_BS (header_row_alignment, 170);
        if (table_flag & 0x10000)
          FIELD_BS (data_row_alignment, 170);
        if (table_flag & 0x20000)
          FIELD_HANDLE (title_text_style, 5, 7);
        if (table_flag & 0x40000)
          {
            FIELD_HANDLE (header_text_style, 5, 7);
            //FIELD_HANDLE (header_row_style_override, ANYCODE, 7); ??
          }
        if (table_flag & 0x80000)
          FIELD_HANDLE (data_text_style, 5, 7);
        if (table_flag & 0x100000)
          FIELD_BD (title_row_height, 140);
        if (table_flag & 0x200000)
          FIELD_BD (header_row_height, 140);
        if (table_flag & 0x400000)
          FIELD_BD (data_row_height, 140);
      }
  
    FIELD_B (has_border_color_overrides, 0);
    if (FIELD_VALUE (has_border_color_overrides))
      {
        BITCODE_BL border_color;
        FIELD_BL (border_color_overrides_flag, 94);
        border_color = FIELD_VALUE (border_color_overrides_flag);
        if (border_color & 0x0001)
          FIELD_CMTC (title_horiz_top_color, 64);
        if (border_color & 0x0002)
          FIELD_CMTC (title_horiz_ins_color, 65);
        if (border_color & 0x0004)
          FIELD_CMTC (title_horiz_bottom_color, 66);
        if (border_color & 0x0008)
          FIELD_CMTC (title_vert_left_color, 63);
        if (border_color & 0x0010)
          FIELD_CMTC (title_vert_ins_color, 68);
        if (border_color & 0x0020)
          FIELD_CMTC (title_vert_right_color, 69);
        if (border_color & 0x0040)
          FIELD_CMTC (header_horiz_top_color, 64);
        if (border_color & 0x0080)
          FIELD_CMTC (header_horiz_ins_color, 65);
        if (border_color & 0x0100)
          FIELD_CMTC (header_horiz_bottom_color, 66);
        if (border_color & 0x0200)
          FIELD_CMTC (header_vert_left_color, 63);
        if (border_color & 0x0400)
          FIELD_CMTC (header_vert_ins_color, 68);
        if (border_color & 0x0800)
          FIELD_CMTC (header_vert_right_color, 69);
        if (border_color & 0x1000)
          FIELD_CMTC (data_horiz_top_color, 64);
        if (border_color & 0x2000)
          FIELD_CMTC (data_horiz_ins_color, 65);
        if (border_color & 0x4000)
          FIELD_CMTC (data_horiz_bottom_color, 66);
        if (border_color & 0x8000)
          FIELD_CMTC (data_vert_left_color, 63);
        if (border_color & 0x10000)
          FIELD_CMTC (data_vert_ins_color, 68);
        if (border_color & 0x20000)
          FIELD_CMTC (data_vert_right_color, 69);
      }
  
    FIELD_B (has_border_lineweight_overrides, 0);
    if (FIELD_VALUE (has_border_lineweight_overrides))
      {
        BITCODE_BL border_linewt;
        FIELD_BL (border_lineweight_overrides_flag, 95);
        border_linewt = FIELD_VALUE (border_lineweight_overrides_flag);
        if (border_linewt & 0x0001)
          FIELD_BS (title_horiz_top_linewt, 0);
        if (border_linewt & 0x0002)
          FIELD_BS (title_horiz_ins_linewt, 0);
        if (border_linewt & 0x0004)
          FIELD_BS (title_horiz_bottom_linewt, 0);
        if (border_linewt & 0x0008)
          FIELD_BS (title_vert_left_linewt, 0);
        if (border_linewt & 0x0010)
          FIELD_BS (title_vert_ins_linewt, 0);
        if (border_linewt & 0x0020)
          FIELD_BS (title_vert_right_linewt, 0);
        if (border_linewt & 0x0040)
          FIELD_BS (header_horiz_top_linewt, 0);
        if (border_linewt & 0x0080)
          FIELD_BS (header_horiz_ins_linewt, 0);
        if (border_linewt & 0x0100)
          FIELD_BS (header_horiz_bottom_linewt, 0);
        if (border_linewt & 0x0200)
          FIELD_BS (header_vert_left_linewt, 0);
        if (border_linewt & 0x0400)
          FIELD_BS (header_vert_ins_linewt, 0);
        if (border_linewt & 0x0800)
          FIELD_BS (header_vert_right_linewt, 0);
        if (border_linewt & 0x1000)
          FIELD_BS (data_horiz_top_linewt, 0);
        if (border_linewt & 0x2000)
          FIELD_BS (data_horiz_ins_linewt, 0);
        if (border_linewt & 0x4000)
          FIELD_BS (data_horiz_bottom_linewt, 0);
        if (border_linewt & 0x8000)
          FIELD_BS (data_vert_left_linewt, 0);
        if (border_linewt & 0x10000)
          FIELD_BS (data_vert_ins_linewt, 0);
        if (border_linewt & 0x20000)
          FIELD_BS (data_vert_right_linewt, 0);
      }
  
    FIELD_B (has_border_visibility_overrides, 0);
    if (FIELD_VALUE (has_border_visibility_overrides))
      {
        BITCODE_BL border_visibility;
        FIELD_BL (border_visibility_overrides_flag, 96);
        border_visibility = FIELD_VALUE (border_visibility_overrides_flag);
        if (border_visibility & 0x0001)
          FIELD_BS (title_horiz_top_visibility, 0);
        if (border_visibility & 0x0002)
          FIELD_BS (title_horiz_ins_visibility, 0);
        if (border_visibility & 0x0004)
          FIELD_BS (title_horiz_bottom_visibility, 0);
        if (border_visibility & 0x0008)
          FIELD_BS (title_vert_left_visibility, 0);
        if (border_visibility & 0x0010)
          FIELD_BS (title_vert_ins_visibility, 0);
        if (border_visibility & 0x0020)
          FIELD_BS (title_vert_right_visibility, 0);
        if (border_visibility & 0x0040)
          FIELD_BS (header_horiz_top_visibility, 0);
        if (border_visibility & 0x0080)
          FIELD_BS (header_horiz_ins_visibility, 0);
        if (border_visibility & 0x0100)
          FIELD_BS (header_horiz_bottom_visibility, 0);
        if (border_visibility & 0x0200)
          FIELD_BS (header_vert_left_visibility, 0);
        if (border_visibility & 0x0400)
          FIELD_BS (header_vert_ins_visibility, 0);
        if (border_visibility & 0x0800)
          FIELD_BS (header_vert_right_visibility, 0);
        if (border_visibility & 0x1000)
          FIELD_BS (data_horiz_top_visibility, 0);
        if (border_visibility & 0x2000)
          FIELD_BS (data_horiz_ins_visibility, 0);
        if (border_visibility & 0x4000)
          FIELD_BS (data_horiz_bottom_visibility, 0);
        if (border_visibility & 0x8000)
          FIELD_BS (data_vert_left_visibility, 0);
        if (border_visibility & 0x10000)
          FIELD_BS (data_vert_ins_visibility, 0);
        if (border_visibility & 0x20000)
          FIELD_BS (data_vert_right_visibility, 0);
      }
  
    COMMON_ENTITY_HANDLE_DATA;
  }
  SINCE (R_2010)
  {
    //... p237
    LOG_WARN ("TODO TABLE r2010+")
  
    FIELD_BS (unknown_bs, 0); //default 38
    FIELD_3BD (hor_dir, 11);
    FIELD_BL (has_break_data, 0); //BL or B?
    if (FIELD_VALUE (has_break_data))
      {
        FIELD_BL (break_flag, 0);
        FIELD_BL (break_flow_direction, 0);
        FIELD_BD (break_spacing, 0);
        FIELD_BL (break_unknown1, 0);
        FIELD_BL (break_unknown2, 0);
        FIELD_BL (num_break_heights, 0);
        VALUEOUTOFBOUNDS (num_break_heights, 5000)
        REPEAT (num_break_heights, break_heights, Dwg_TABLE_BreakHeight)
        REPEAT_BLOCK
            SUB_FIELD_3BD (break_heights[rcount1],position, 0);
            SUB_FIELD_BD (break_heights[rcount1],height, 0);
            SUB_FIELD_BL (break_heights[rcount1],flag, 0); // default: 2
        END_REPEAT_BLOCK
        SET_PARENT_OBJ (break_heights)
        END_REPEAT (break_heights);
      }
    FIELD_BL (num_break_rows, 0);
    VALUEOUTOFBOUNDS (num_break_rows, 5000)
    REPEAT (num_break_rows, break_rows, Dwg_TABLE_BreakRow)
    REPEAT_BLOCK
        SUB_FIELD_3BD (break_rows[rcount1],position, 0);
        SUB_FIELD_BL (break_rows[rcount1],start, 0);
        SUB_FIELD_BL (break_rows[rcount1],end, 0);
    END_REPEAT_BLOCK
    SET_PARENT_OBJ (break_rows)
    END_REPEAT (break_rows);

    COMMON_ENTITY_HANDLE_DATA;
    FIELD_HANDLE (tablestyle, 5, 342);
  }

DWG_ENTITY_END

#undef row
#undef cell
#undef content
#undef geom
#undef attr
#undef merged

#endif /* DEBUG_CLASSES */

// pg.246 20.4.102 and TABLE
// added with r2008, backcompat with r2007
// The cellstyle map can contain custom cell styles, whereas the TABLESTYLE
// only contains the Table (R24), _Title, _Header and _Data cell style.
DWG_OBJECT (CELLSTYLEMAP)
  SUBCLASS (AcDbCellStyleMap)
  FIELD_BL (num_cells, 90);
  REPEAT (num_cells, cells, Dwg_TABLESTYLE_cellstyle)
  REPEAT_BLOCK
      DXF { VALUE_TFF ("CELLSTYLE", 300); }
      CellStyle_fields (cells[rcount1].cellstyle);
      DXF { VALUE_TFF ("CELLSTYLE_BEGIN", 1) }
      SUB_FIELD_BL (cells[rcount1],id, 90);
      SUB_FIELD_BL (cells[rcount1],type, 91);
      SUB_FIELD_T (cells[rcount1],name, 300);
      DXF { VALUE_TFF ("CELLSTYLE_END", 309) }
  END_REPEAT_BLOCK
  SET_PARENT_FIELD (cells, parent, (Dwg_Object_TABLESTYLE*)_obj)
  END_REPEAT (cells);

DWG_OBJECT_END

//pg.246 20.4.103
// stable
DWG_OBJECT (TABLEGEOMETRY)

  SUBCLASS (AcDbTableGeometry)
  FIELD_BL (num_rows, 90);
  VALUEOUTOFBOUNDS (num_rows, 5000)
  FIELD_BL (num_cols, 91);
  VALUEOUTOFBOUNDS (num_cols, 5000)
  FIELD_BL (num_cells, 92);
  VALUEOUTOFBOUNDS (num_cells, 10000)
  REPEAT (num_cells, cells, Dwg_TABLEGEOMETRY_Cell)
  REPEAT_BLOCK
      #define cell cells[rcount1]
      SUB_FIELD_BL (cell,geom_data_flag, 93);
      SUB_FIELD_BD (cell,width_w_gap, 40);
      SUB_FIELD_BD (cell,height_w_gap, 41);
      SUB_FIELD_HANDLE (cell,tablegeometry, 4, 330);
      SUB_FIELD_BL (cell,num_geometry, 94);
      VALUEOUTOFBOUNDS (cell.num_geometry, 10000)
      REPEAT2 (cell.num_geometry, cell.geometry, Dwg_CellContentGeometry)
      REPEAT_BLOCK
          #define geom cell.geometry[rcount2]
          SUB_FIELD_3BD (geom,dist_top_left, 10);
          SUB_FIELD_3BD (geom,dist_center, 11);
          SUB_FIELD_BD (geom,content_width, 43);
          SUB_FIELD_BD (geom,content_height, 44);
          SUB_FIELD_BD (geom,width, 45);
          SUB_FIELD_BD (geom,height, 46);
          SUB_FIELD_BL (geom,unknown, 95);
          #undef geom
      END_REPEAT_BLOCK
      SET_PARENT_FIELD (cell.geometry, geom_parent, &_obj->cell)
      END_REPEAT (cell.geometry);
      #undef cell
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (cells)
  END_REPEAT (cells);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/* top, horizontal inside, bottom, left, vertical inside, right */
#define TABLESTYLE_rowstyle_border(nam, bord, rcount2)                  \
  JSON { RECORDs (bord); }                                              \
  SUB_FIELD_BSd (nam##_rowstyle.bord,linewt, 274+rcount2);              \
  SUB_FIELD_B (nam##_rowstyle.bord,visible, 284+rcount2);               \
  SUB_FIELD_CMC (nam##_rowstyle.bord,color, 64+rcount2);                \
  DECODER { _obj->nam##_rowstyle.bord.parent = &_obj->nam##_rowstyle; } \
  JSON { ENDRECORD (); }

/* data, title, header */
#define TABLESTYLE_rowstyle(nam)                                        \
  JSON { RECORDs (nam##_rowstyle); }                                    \
  SUB_FIELD_HANDLE (nam##_rowstyle,text_style, 5, 7); /* DXF by name */ \
  SUB_FIELD_BD (nam##_rowstyle,text_height, 140);                       \
  SUB_FIELD_BS (nam##_rowstyle,text_alignment, 170);                    \
  SUB_FIELD_CMC (nam##_rowstyle,text_color, 62);                        \
  SUB_FIELD_CMC (nam##_rowstyle,fill_color, 63);                        \
  SUB_FIELD_B (nam##_rowstyle,has_bgcolor, 283);                        \
  TABLESTYLE_rowstyle_border (nam, top_border, 0);                      \
  TABLESTYLE_rowstyle_border (nam, hor_border, 1);                      \
  TABLESTYLE_rowstyle_border (nam, bot_border, 2);                      \
  TABLESTYLE_rowstyle_border (nam, left_border, 3);                     \
  TABLESTYLE_rowstyle_border (nam, vert_border, 4);                     \
  TABLESTYLE_rowstyle_border (nam, right_border, 5);                    \
  SINCE (R_2007) {                                                      \
    SUB_FIELD_BL (nam##_rowstyle,data_type, 90);                        \
    SUB_FIELD_BL (nam##_rowstyle,unit_type, 91);                        \
    SUB_FIELD_TU (nam##_rowstyle,format_string, 1);                     \
  }                                                                     \
  DECODER { _obj->nam##_rowstyle.parent = _obj; }                       \
  JSON { ENDRECORD (); }

// See TABLE and p20.4.101
// Added with r2005
// TABLESTYLE only contains the Table (R24), _Title, _Header and _Data cell style.
DWG_OBJECT (TABLESTYLE)
  SUBCLASS (AcDbTableStyle)
  UNTIL (R_2007) {
    FIELD_T (name, 3);
    FIELD_BS (flow_direction, 70);
    FIELD_BS (flags, 71);
    FIELD_BD (horiz_cell_margin, 40);
    FIELD_BD (vert_cell_margin, 41);
    FIELD_B (is_title_suppressed, 280);
    FIELD_B (is_header_suppressed, 281);
  }
  LATER_VERSIONS { // r2010+
    FIELD_RC (unknown_rc, 70);
    FIELD_T (name, 3);
    FIELD_BL (unknown_bl1, 0);
    FIELD_BL (unknown_bl2, 0);
    FIELD_HANDLE (cellstyle_handle, DWG_HDL_HARDOWN, 0);
    CellStyle_fields (sty.cellstyle);
    DXF { VALUE_TFF ("CELLSTYLE_BEGIN", 1) }
    FIELD_BL0 (sty.id, 90);
    FIELD_BL0 (sty.type, 91);
    FIELD_T0 (sty.name, 300);
    DXF { VALUE_TFF ("CELLSTYLE_END", 309) }

    DECODER { FIELD_VALUE (flow_direction) = _obj->sty.cellstyle.property_override_flags & 0x10000; }
    FIELD_BL (numoverrides, 0);
    // FIXME style overrides for 0-6
    if (FIELD_VALUE (numoverrides))
      {
        FIELD_BL (unknown_bl3, 0);
        CellStyle_fields (ovr.cellstyle);
        DXF { VALUE_TFF ("CELLSTYLE_BEGIN", 1) }
        FIELD_BL0 (ovr.id, 90);
        FIELD_BL0 (ovr.type, 91);
        FIELD_T0 (ovr.name, 300);
        DXF { VALUE_TFF ("CELLSTYLE_END", 309) }
        LOG_WARN ("TODO TABLESTYLE r2010+ missing fields")
      }
  }

  TABLESTYLE_rowstyle (data);
  TABLESTYLE_rowstyle (title);
  TABLESTYLE_rowstyle (header);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

//(79 + varies) pg.247 20.4.104
DWG_OBJECT (XRECORD)

  DXF {
    SUBCLASS (AcDbXrecord)
    SINCE (R_2000) {
      FIELD_BS0 (cloning, 280);
    }
  }
  ENCODER {
    unsigned long pos = bit_position (dat);
    unsigned xdata_size = _obj->xdata_size;
    FIELD_BL (xdata_size, 0);
    FIELD_XDATA (xdata, xdata_size);
    if (xdata_size != _obj->xdata_size)
      { // easiest is to write both again.
        // else do BL patching with very unlikely bitwise memmove
        bit_set_position (dat, pos);
        FIELD_BL (xdata_size, 0);
        FIELD_XDATA (xdata, xdata_size);
      }
  } else {
    FIELD_BL (xdata_size, 0);
    FIELD_XDATA (xdata, xdata_size);
  }
#ifndef IS_DXF
  SINCE (R_2000) {
    FIELD_BS (cloning, 280);
  }
#endif

  START_OBJECT_HANDLE_STREAM;
  DECODER {
      for (vcount=0; bit_position (hdl_dat) < obj->handlestream_size; vcount++)
        {
          FIELD_VALUE (objid_handles) = vcount
            ? (BITCODE_H*)realloc (FIELD_VALUE (objid_handles),
                                   (vcount+1) * sizeof (Dwg_Object_Ref))
            : (BITCODE_H*)malloc (sizeof (Dwg_Object_Ref));
          FIELD_HANDLE_N (objid_handles[vcount], vcount, ANYCODE, 0);
          if (!FIELD_VALUE (objid_handles[vcount]))
            {
              if (!vcount)
                free (FIELD_VALUE (objid_handles));
              break;
            }
        }
      FIELD_VALUE (num_objid_handles) = vcount;
    }
  VALUEOUTOFBOUNDS (num_objid_handles, 10000)
#ifndef IS_FREE
  FIELD_TRACE (num_objid_handles, BL);
#endif
#ifndef IS_DECODER
  HANDLE_VECTOR (objid_handles, num_objid_handles, 4, 0);
#endif
#ifdef IS_DXF
  if (FIELD_VALUE (objid_handles)) {
    REPEAT (num_objid_handles, objid_handles, T)
        VALUE_H (_obj->objid_handles[rcount1], 340);
    END_REPEAT (objid_handles)
  }
#endif

DWG_OBJECT_END

//(80 + varies)
/// DXF as ACDBPLACEHOLDER
DWG_OBJECT (PLACEHOLDER)
  // no own data members
  // no SUBCLASS marker
DWG_OBJECT_END

// SCALE (varies)
// 20.4.92 page 221
DWG_OBJECT (SCALE)
  SUBCLASS (AcDbScale)
  FIELD_BS (flag, 70); // always 0
  FIELD_T (name, 300);
  FIELD_BD (paper_units, 140);
  FIELD_BD (drawing_units, 141);
  FIELD_B (is_unit_scale, 290);
DWG_OBJECT_END

// VBA_PROJECT (81 + varies), a blob
DWG_OBJECT (VBA_PROJECT)

  SINCE (R_2000) {
    SUBCLASS (AcDbVbaProject)
#ifndef IS_JSON
    FIELD_BL (data_size, 90);
#endif
    FIELD_BINARY (data, FIELD_VALUE (data_size), 310);

    START_OBJECT_HANDLE_STREAM;
  }
DWG_OBJECT_END

/* pg. 157, 20.4.48 (varies)
   AcDbMLeader
 */
DWG_ENTITY (MULTILEADER)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbMLeader)
  SINCE (R_2010) {
    FIELD_BS (class_version, 270); // default 2. 1 <= r2004
    VALUEOUTOFBOUNDS (class_version, 10)
  }
  DXF_OR_PRINT { VALUE_TFF ("CONTEXT_DATA{", 300); } //AcDbObjectContextData
  FIELD_BL (ctx.num_leaders, 0);
  VALUEOUTOFBOUNDS (ctx.num_leaders, 5000) // MAX_LEADER_NUMBER
  DXF_OR_PRINT { VALUE_TFF ("LEADER{", 302); }
  REPEAT (ctx.num_leaders, ctx.leaders, Dwg_LEADER_Node)
  REPEAT_BLOCK
      #define lnode ctx.leaders[rcount1]
      SUB_FIELD_B (lnode, has_lastleaderlinepoint, 290);
      SUB_FIELD_B (lnode, has_dogleg, 291);
      if (FIELD_VALUE (lnode.has_lastleaderlinepoint))
        SUB_FIELD_3BD (lnode, lastleaderlinepoint, 10);
      if (FIELD_VALUE (lnode.has_dogleg))
        SUB_FIELD_3BD (lnode, dogleg_vector, 11);
      SUB_FIELD_BL (lnode, num_breaks, 0);
      VALUEOUTOFBOUNDS (lnode.num_breaks, 5000)
      REPEAT2 (lnode.num_breaks, lnode.breaks, Dwg_LEADER_Break)
      REPEAT_BLOCK
          SUB_FIELD_3BD (lnode.breaks[rcount2], start, 11);
          SUB_FIELD_3BD (lnode.breaks[rcount2], end, 12);
      END_REPEAT_BLOCK
      SET_PARENT (lnode.breaks, (struct _dwg_LEADER_Line *)&_obj->lnode);
      END_REPEAT (lnode.breaks);

      SUB_FIELD_BL (lnode, branch_index, 90);
      SUB_FIELD_BD (lnode, dogleg_length, 40);
      DXF_OR_PRINT { VALUE_TFF ("LEADER_LINE{", 304); }
      SUB_FIELD_BL (lnode, num_lines, 0);
      VALUEOUTOFBOUNDS (lnode.num_lines, 5000)
      REPEAT2 (lnode.num_lines, lnode.lines, Dwg_LEADER_Line)
      REPEAT_BLOCK
          #define lline lnode.lines[rcount2]
          SUB_FIELD_BL (lline, num_points, 0);
          FIELD_3DPOINT_VECTOR (lline.points, lline.num_points, 10);
          SUB_FIELD_BL (lline, num_breaks, 0);
          VALUEOUTOFBOUNDS (lline.num_breaks, 5000)
          REPEAT3 (lline.num_breaks, lline.breaks, Dwg_LEADER_Break)
          REPEAT_BLOCK
              SUB_FIELD_3BD (lline.breaks[rcount3], start, 11);
              SUB_FIELD_3BD (lline.breaks[rcount3], end, 12);
          END_REPEAT_BLOCK
          SET_PARENT (lline.breaks, &_obj->lline);
          END_REPEAT (lline.breaks);
          SUB_FIELD_BL (lline, line_index, 91);

          SINCE (R_2010)
            {
              SUB_FIELD_BS (lline, type, 170);
              SUB_FIELD_CMC (lline, color, 92);
              SUB_FIELD_HANDLE (lline, ltype, 5, 340);
              SUB_FIELD_BLd (lline, linewt, 171);
              SUB_FIELD_BD (lline, arrow_size, 40);
              SUB_FIELD_HANDLE (lline, arrow_handle, 5, 341);
              SUB_FIELD_BL (lline, flags, 93);
            }
            #undef lline
      END_REPEAT_BLOCK
      SET_PARENT (lnode.lines, &_obj->lnode);
      END_REPEAT (lnode.lines)
      SINCE (R_2010)
        SUB_FIELD_BS (lnode, attach_dir, 271);
      DXF_OR_PRINT { VALUE_TFF ("}", 305); }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (ctx.leaders)
  END_REPEAT (ctx.leaders)
  DXF_OR_PRINT { VALUE_TFF ("}", 303); }

  FIELD_BD (ctx.scale_factor, 40);
  FIELD_3BD (ctx.content_base, 10);
  FIELD_BD (ctx.text_height, 41);
  FIELD_BD (ctx.arrow_size, 140);
  FIELD_BD (ctx.landing_gap, 145);
  FIELD_BS (ctx.text_left, 174);
  FIELD_BS (ctx.text_right, 175);
  FIELD_BS (ctx.text_angletype, 176);
  FIELD_BS (ctx.text_alignment, 177);

  FIELD_B (ctx.has_content_txt, 290);
  if (FIELD_VALUE (ctx.has_content_txt))
    {
      DECODER { FIELD_VALUE (ctx.content.txt.type) = 2; }
      FIELD_T (ctx.content.txt.default_text, 304);
      FIELD_3BD (ctx.content.txt.normal, 11);
      FIELD_HANDLE (ctx.content.txt.style, 5, 340);
      FIELD_3BD (ctx.content.txt.location, 12);
      FIELD_3BD (ctx.content.txt.direction, 13);
      FIELD_BD (ctx.content.txt.rotation, 42);
      FIELD_BD (ctx.content.txt.width, 43);
      FIELD_BD (ctx.content.txt.height, 44);
      FIELD_BD (ctx.content.txt.line_spacing_factor, 45);
      FIELD_BS (ctx.content.txt.line_spacing_style, 170);
      FIELD_CMC (ctx.content.txt.color, 90); // CMTC?
      FIELD_BS (ctx.content.txt.alignment, 171);
      FIELD_BS (ctx.content.txt.flow, 172);
      FIELD_CMC (ctx.content.txt.bg_color, 91); // CMTC?
      FIELD_BD (ctx.content.txt.bg_scale, 141);
      FIELD_BL (ctx.content.txt.bg_transparency, 92);
      FIELD_B (ctx.content.txt.is_bg_fill, 291);
      FIELD_B (ctx.content.txt.is_bg_mask_fill, 292);
      FIELD_BS (ctx.content.txt.col_type, 173);
      FIELD_B (ctx.content.txt.is_height_auto, 293);
      FIELD_BD (ctx.content.txt.col_width, 142);
      FIELD_BD (ctx.content.txt.col_gutter, 143);
      FIELD_B (ctx.content.txt.is_col_flow_reversed, 294);
      FIELD_BL (ctx.content.txt.num_col_sizes, 0);
      //VALUEOUTOFBOUNDS (ctx.content.txt.num_col_sizes, 5000)
      FIELD_VECTOR (ctx.content.txt.col_sizes, BD, ctx.content.txt.num_col_sizes, 144);
      FIELD_B (ctx.content.txt.word_break, 295);
      FIELD_B (ctx.content.txt.unknown, 0);
    }
  else // a union. either txt or blk
    {
      FIELD_B (ctx.has_content_blk, 296);
      if (FIELD_VALUE (ctx.has_content_blk))
        {
          DECODER { FIELD_VALUE (ctx.content.txt.type) = 1; }
          FIELD_HANDLE (ctx.content.blk.block_table, 4, 341);
          FIELD_3BD (ctx.content.blk.normal, 14);
          FIELD_3BD (ctx.content.blk.location, 15);
          FIELD_3BD (ctx.content.blk.scale, 16);
          FIELD_BD (ctx.content.blk.rotation, 46);
          FIELD_CMC (ctx.content.blk.color, 93); // CMTC?
          FIELD_VECTOR_N (ctx.content.blk.transform, BD, 16, 47);
        }
    }

  FIELD_3BD (ctx.base, 110);
  FIELD_3BD (ctx.base_dir, 111);  // dxf only 2d?
  FIELD_3BD (ctx.base_vert, 112); // dxf only 2d
  FIELD_B (ctx.is_normal_reversed, 297);

  SINCE (R_2010)
    {
      FIELD_BS (ctx.text_top, 273);
      FIELD_BS (ctx.text_bottom, 272);
    }
  DXF_OR_PRINT { VALUE_TFF ("}", 301); } //end CONTEXT_DATA
  // END MLEADER_AnnotContext

  FIELD_HANDLE (mleaderstyle, 5, 340);
  FIELD_BLx (flags, 90); // override flags
  FIELD_BS (type, 170);
  FIELD_CMC (color, 91);
  FIELD_HANDLE (ltype, 5, 341);
  FIELD_BLd (linewt, 171);
  FIELD_B (has_landing, 290);
  FIELD_B (has_dogleg, 291);
  FIELD_BD (landing_dist, 41);
  DECODER {
    if (bit_isnan (FIELD_VALUE (landing_dist)))
      {
        FIELD_VALUE (landing_dist) = 0.0;
        return DWG_ERR_VALUEOUTOFBOUNDS;
      }
  }
  FIELD_HANDLE0 (arrow_handle, 5, 342);
  FIELD_BD0 (arrow_size, 42);
  FIELD_BS (style_content, 172);
  FIELD_HANDLE (text_style, 5, 343);
  FIELD_BS (text_left, 173);
  FIELD_BS (text_right, 95);
  FIELD_BS (text_angletype, 174);
  FIELD_BS (text_alignment, 175); // unknown at ODA
  FIELD_CMC (text_color, 92);
  FIELD_B (has_text_frame, 292);
  FIELD_HANDLE0 (block_style, 5, 344);
  FIELD_CMC (block_color, 93);
  FIELD_3BD (block_scale, 10);
  FIELD_BD (block_rotation, 43);
  FIELD_BS (style_attachment, 176);
  FIELD_B (is_annotative, 293);

  VERSIONS (R_2000, R_2007)
    {
      FIELD_BL (num_arrowheads, 0);
      VALUEOUTOFBOUNDS (num_arrowheads, 5000)
      REPEAT (num_arrowheads, arrowheads, Dwg_LEADER_ArrowHead)
      REPEAT_BLOCK
          SUB_FIELD_B (arrowheads[rcount1],is_default, 94);
          SUB_FIELD_HANDLE (arrowheads[rcount1],arrowhead, 5, 345);
      END_REPEAT_BLOCK
      SET_PARENT_OBJ (arrowheads)
      END_REPEAT (arrowheads);

      FIELD_BL (num_blocklabels, 0);
      VALUEOUTOFBOUNDS (num_blocklabels, 5000)
      REPEAT (num_blocklabels, blocklabels, Dwg_LEADER_BlockLabel)
      REPEAT_BLOCK
          SUB_FIELD_HANDLE (blocklabels[rcount1],attdef, 4, 330);
          SUB_FIELD_T (blocklabels[rcount1],label_text, 302);
          SUB_FIELD_BS (blocklabels[rcount1],ui_index, 177);
          SUB_FIELD_BD (blocklabels[rcount1],width, 44);
      END_REPEAT_BLOCK
      SET_PARENT_OBJ (blocklabels)
      END_REPEAT (blocklabels)
      FIELD_B (is_neg_textdir, 294);
      FIELD_BS (ipe_alignment, 178);
      FIELD_BS (justification, 179);
      FIELD_BD (scale_factor, 45);
    }

  SINCE (R_2010)
    {
      FIELD_BS (attach_dir, 271);
      FIELD_BS (attach_top, 273);
      FIELD_BS (attach_bottom, 272);
    }
  SINCE (R_2013)
    FIELD_B (is_text_extended, 295);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

/* par 20.4.87 (varies) */
DWG_OBJECT (MLEADERSTYLE)

  SUBCLASS (AcDbMLeaderStyle)
  SINCE (R_2010) {
    IF_ENCODE_FROM_EARLIER {
      FIELD_VALUE (class_version) = 2;
    }
    // is also set on EED for APPID “ACAD_MLEADERVER”
    FIELD_BS (class_version, 179);
    VALUEOUTOFBOUNDS (class_version, 10)
  }
  else {
    JSON { FIELD_BS (class_version, 0); }
  }

  FIELD_BS (content_type, 170);
  FIELD_BS (mleader_order, 171);
  FIELD_BS (leader_order, 172);
  FIELD_BL (max_points, 90);
  FIELD_BD (first_seg_angle, 40);
  FIELD_BD (second_seg_angle, 41);
  FIELD_BS (type, 173);
  FIELD_CMC (line_color, 91);
  FIELD_HANDLE (line_type, 5, 340);
  FIELD_BLd (linewt, 92);
  FIELD_B (has_landing, 290);
  FIELD_BD (landing_gap, 42);
  FIELD_B (has_dogleg, 291);
  FIELD_BD (landing_dist, 43);
  FIELD_T (description, 3);
  FIELD_HANDLE (arrow_head, 5, 341);
  FIELD_BD (arrow_head_size, 44);
  FIELD_T (text_default, 300);
  FIELD_HANDLE (text_style, 5, 342);
  FIELD_BS (attach_left, 174);
  FIELD_BS (attach_right, 178);
//if (FIELD_VALUE (class_version) >= 2) {
    FIELD_BS (text_angle_type, 175);
//}
  FIELD_BS (text_align_type, 176);
  FIELD_CMC (text_color, 93); // as RGB only
  FIELD_BD (text_height, 45);
  FIELD_B (has_text_frame, 292);
  if (FIELD_VALUE (class_version) >= 2) {
    FIELD_B (text_always_left, 297); // in DXF always
  }
  FIELD_BD (align_space, 46);
  FIELD_HANDLE (block, 5, 343);
  FIELD_CMC (block_color, 94);
  JSON {
    FIELD_3BD (block_scale, 0)
  } else {
    FIELD_BD (block_scale.x, 47);
    FIELD_BD (block_scale.y, 49);
    FIELD_BD (block_scale.z, 140);
  }
  FIELD_B (use_block_scale, 293);
  FIELD_BD (block_rotation, 141);
  FIELD_B (use_block_rotation, 294);
  FIELD_BS (block_connection, 177);
  FIELD_BD (scale, 142);
  FIELD_B (is_changed, 295);
  FIELD_B (is_annotative, 296);
  FIELD_BD (break_size, 143);

  SINCE (R_2010)
    {
      FIELD_BS (attach_dir, 271);
      FIELD_BS (attach_top, 273);
      FIELD_BS (attach_bottom, 272);
    }
  SINCE (R_2013) {
    FIELD_B (text_extended, 298);
  }
DWG_OBJECT_END

////////////////////
// These variable objects are not described in the spec:
//

DWG_OBJECT (WIPEOUTVARIABLES)

  SUBCLASS (AcDbWipeoutVariables)
  //DXF { VALUE_BL (0, 90); } /* class_version */
  FIELD_BS (display_frame, 70);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// R2000+ picture. undocumented (varies)
DWG_ENTITY (WIPEOUT)

  //SUBCLASS (AcDbImage)
  //SUBCLASS (AcDbRasterImage)
  SUBCLASS (AcDbWipeout)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)
  FIELD_3DPOINT (pt0, 10);
  FIELD_3DPOINT (uvec, 11);
  FIELD_3DPOINT (vvec, 12);
  FIELD_2RD (size, 13);
  FIELD_BS (display_props, 70);
  FIELD_B (clipping, 280);
  FIELD_RC (brightness, 281);
  FIELD_RC (contrast, 282);
  FIELD_RC (fade, 283);

  SINCE (R_2010) {
    FIELD_B (clip_mode, 290);
  }
  FIELD_BS (clip_boundary_type, 71); // 1 rect, 2 polygon
  if (FIELD_VALUE (clip_boundary_type) == 1)
    FIELD_VALUE (num_clip_verts) = 2;
  else
    FIELD_BL (num_clip_verts, 91);
  VALUEOUTOFBOUNDS (num_clip_verts, 5000)
  FIELD_2RD_VECTOR (clip_verts, num_clip_verts, 14);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (imagedef, 5, 340);
  FIELD_HANDLE (imagedefreactor, 3, 360);

DWG_ENTITY_END

// (varies)
// in DXF as {PDF,DWF,DGN}DEFINITION
// no DWF, DGN coverage yet
DWG_OBJECT (UNDERLAYDEFINITION)

  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbUnderlayDefinition)
  FIELD_T (filename, 1);
  FIELD_T (name, 2);
  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// (varies)
// in DXF as 0 DGNUNDERLAY DWFUNDERLAY PDFUNDERLAY
// looks perfect, but no DWF, DGN coverage yet
DWG_ENTITY (UNDERLAY)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbUnderlayReference)
  FIELD_3BD (extrusion, 210);
  FIELD_3DPOINT (insertion_pt, 10);
  FIELD_BD (angle, 50);
  FIELD_3BD_1 (scale, 41);
  FIELD_RC (flag, 280);
  FIELD_RCd (contrast, 281); // 20-100. def: 100
  FIELD_RCd (fade, 282);  // 0-80

  FIELD_BL (num_clip_verts, 0);
  VALUEOUTOFBOUNDS (num_clip_verts, 5000)
  FIELD_2RD_VECTOR (clip_verts, num_clip_verts, 11);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (underlay_layer, 5, 0);
  FIELD_HANDLE (definition_id, 5, 340);
DWG_ENTITY_END

DWG_ENTITY (CAMERA) // i.e. a named view, not persistent in a DWG. CAMERADISPLAY=1
  //DECODE_UNKNOWN_BITS
  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (view, 5, 0);
DWG_ENTITY_END

// sectionplane, r2007+
DWG_ENTITY (SECTIONOBJECT)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbSection)
  FIELD_BL (state, 90);
  FIELD_BL (flags, 91);
  FIELD_T (name, 1);
  FIELD_3BD (vert_dir, 10);
  FIELD_BD (top_height, 40);
  FIELD_BD (bottom_height, 41);
  FIELD_BS (indicator_alpha, 70);
  FIELD_CMTC (indicator_color, 62); //dxf doc bug: 63, 411
  FIELD_BL (num_verts, 92);
  FIELD_3DPOINT_VECTOR (verts, num_verts, 11);
  FIELD_BL (num_blverts, 93);
  FIELD_3DPOINT_VECTOR (blverts, num_blverts, 12);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (section_settings, 5, 360);
DWG_ENTITY_END

DWG_OBJECT (SECTION_MANAGER)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbSectionManager)
  FIELD_B (is_live, 70);
  FIELD_BS (num_sections, 90);
  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (sections, num_sections, 5, 330);
DWG_OBJECT_END

// Unstable
DWG_OBJECT (SECTION_SETTINGS)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbSectionSettings)
  FIELD_BL (curr_type, 90);
  FIELD_BL (num_types, 91);
  VALUEOUTOFBOUNDS (num_types, 4) // max 4 types: live on/off, 2d, 3d
  REPEAT (num_types, types, Dwg_SECTION_typesettings)
  REPEAT_BLOCK
      DXF { VALUE_TFF ("SectionTypeSettings", 1); }
      SUB_FIELD_BL (types[rcount1], type, 90);
      SUB_FIELD_BL (types[rcount1], generation, 91);
      SUB_FIELD_BL (types[rcount1], num_sources, 92);
      SUB_HANDLE_VECTOR (types[rcount1], sources, num_sources, 5, 330);
      SUB_FIELD_HANDLE (types[rcount1], destblock, 4, 331);
      SUB_FIELD_T (types[rcount1], destfile, 1);
      SUB_FIELD_BL (types[rcount1], num_geom, 93);
      REPEAT2 (types[rcount1].num_geom, types[rcount1].geom, Dwg_SECTION_geometrysettings)
      REPEAT_BLOCK
          DXF { VALUE_TFF ("SectionGeometrySettings", 2); }
          SUB_FIELD_BL (types[rcount1].geom[rcount2], num_geoms, 90);
          SUB_FIELD_BL (types[rcount1].geom[rcount2], hexindex, 91);
          SUB_FIELD_BL (types[rcount1].geom[rcount2], flags, 92);
          SUB_FIELD_CMC (types[rcount1].geom[rcount2], color, 62);
          SUB_FIELD_T (types[rcount1].geom[rcount2], layer, 8);
          SUB_FIELD_T (types[rcount1].geom[rcount2], ltype, 6);
          SUB_FIELD_BD (types[rcount1].geom[rcount2], ltype_scale, 40);
          SUB_FIELD_T (types[rcount1].geom[rcount2], plotstyle, 1);
          SINCE (R_2000)
            SUB_FIELD_BLd (types[rcount1].geom[rcount2], linewt, 370);
          SUB_FIELD_BS (types[rcount1].geom[rcount2], face_transparency, 70);
          SUB_FIELD_BS (types[rcount1].geom[rcount2], edge_transparency, 71);
          SUB_FIELD_BS (types[rcount1].geom[rcount2], hatch_type, 72);
          ENCODER {
            if (bit_empty_T (dat, _obj->types[rcount1].geom[rcount2].hatch_pattern))
              _obj->types[rcount1].geom[rcount2].hatch_pattern = bit_set_T (dat, "SOLID");
          }
          SUB_FIELD_T (types[rcount1].geom[rcount2], hatch_pattern, 2);
          DECODER {
            if (bit_empty_T (dat, _obj->types[rcount1].geom[rcount2].hatch_pattern))
              {
                free (_obj->types[rcount1].geom[rcount2].hatch_pattern);
                _obj->types[rcount1].geom[rcount2].hatch_pattern = bit_set_T (dat, "SOLID");
              }
          }
          SUB_FIELD_BD (types[rcount1].geom[rcount2], hatch_angle, 41);
          SUB_FIELD_BD (types[rcount1].geom[rcount2], hatch_spacing, 42);
          SUB_FIELD_BD (types[rcount1].geom[rcount2], hatch_scale, 43);
          DXF { VALUE_TFF ("SectionGeometrySettingsEnd", 3); }
      END_REPEAT_BLOCK
      //SET_PARENT (types[rcount1].geom, &_obj->types[rcount1]);
      END_REPEAT (types[rcount1].geom)
      DXF { VALUE_TFF ("SectionTypeSettingsEnd", 3); }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (types);
  END_REPEAT (types)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

#ifndef IS_DXF

/* UNKNOWN (varies)
   container to hold a unknown class entity, see classes.inc
   every DEBUGGING class holds a bits array, an prefix offset and a bitsize.
   It starts after the common_entity|object_data until and goes until the end
   of final padding, to the CRC.
   (obj->address+obj->common_size/8 .. obj->address+obj->size)
 */
DWG_ENTITY (UNKNOWN_ENT)
  DECODE_UNKNOWN_BITS
  //COMMON_ENTITY_HANDLE_DATA; // including this
DWG_ENTITY_END

/* container to hold a raw class object (varies) */
DWG_OBJECT (UNKNOWN_OBJ)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

// just a dummy dwg filer, ignored for dxf.
// for now we use it as empty PROXY_OBJECT
DWG_OBJECT (DUMMY)
DWG_OBJECT_END

#endif /* IS_DXF */

DWG_OBJECT (LONG_TRANSACTION)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbLongTransaction)
  LOG_INFO ("TODO LONG_TRANSACTION\n");
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// (varies) UNSTABLE
DWG_OBJECT (OBJECT_PTR) //empty? only xdata. CAseDLPNTableRecord
  DECODE_UNKNOWN_BITS
  DEBUG_HERE_OBJ
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/* In work area:
   The following entities/objects are all stored with partial fields,
   plus as raw bits for examples/unknown.
   Coverage might be missing for some cases, or field names may change.
 */

#define AcDbAssocDependency_fields                         \
  SUBCLASS (AcDbAssocDependency);                          \
  FIELD_BS (assocdep.class_version, 90); /* 2 */           \
  VALUEOUTOFBOUNDS (assocdep.class_version, 3);            \
  FIELD_BL (assocdep.status, 90);                          \
  FIELD_B (assocdep.is_read_dep, 290);                     \
  FIELD_B (assocdep.is_write_dep, 290);                    \
  FIELD_B (assocdep.is_attached_to_object, 290);           \
  FIELD_B (assocdep.is_delegating_to_owning_action, 290);  \
  FIELD_BLd (assocdep.order, 90); /* -1 or 0 */            \
  FIELD_HANDLE (assocdep.dep_on, 3, 330);                  \
  FIELD_B (assocdep.has_name, 290);                        \
  if (FIELD_VALUE (assocdep.has_name)) {                   \
    FIELD_B (assocdep.name, 1);                            \
  }                                                        \
  FIELD_HANDLE (assocdep.readdep, 4, 330);                 \
  FIELD_HANDLE (assocdep.node, 3, 330);                    \
  FIELD_HANDLE (assocdep.dep_body, 4, 360);                \
  FIELD_BLd (assocdep.depbodyid, 90)

// (varies) UNSTABLE
// works ok on all Surface_20* but this coverage seems limited.
// field names may change.
// See AcDbAssocDependency.h
DWG_OBJECT (ASSOCDEPENDENCY)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocDependency);
  FIELD_BS (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 3);
  FIELD_BL (status, 90);
  FIELD_B (is_read_dep, 290);
  FIELD_B (is_write_dep, 290);
  FIELD_B (is_attached_to_object, 290);
  FIELD_B (is_delegating_to_owning_action, 290);
  FIELD_BLd (order, 90); /* -1 or 0 */
  FIELD_HANDLE (dep_on, 3, 330);
  FIELD_B (has_name, 290);
  if (FIELD_VALUE (has_name)) {
    FIELD_T (name, 1);
  }
  FIELD_HANDLE (readdep, 4, 330);
  FIELD_HANDLE (node, 3, 330);
  FIELD_HANDLE (dep_body, 4, 360);
  FIELD_BLd (depbodyid, 90);
  START_OBJECT_HANDLE_STREAM;
  DWG_OBJECT_END

#define AcDbAssocActionParam_fields \
  SUBCLASS (AcDbAssocActionParam)   \
  FIELD_BL (is_r2013, 90);          \
  if (_obj->is_r2013) {             \
    VALUE_BL (0, 90);               \
  }                                 \
  FIELD_T (name, 1)

#define AcDbAssocParamBasedActionBody_fields \
  SUBCLASS (AcDbAssocActionBody) \
  FIELD_BL (aab_version, 90); \
  SUBCLASS (AcDbAssocParamBasedActionBody) \
  FIELD_BL (pab_status, 90); \
  FIELD_BL (pab_l2, 90); \
  FIELD_BL (num_deps, 90); \
  FIELD_BL (pab_l4, 90); \
  FIELD_BL (pab_l5, 90)

#define AcDbAssocPathBasedSurfaceActionBody_fields \
  AcDbAssocParamBasedActionBody_fields; \
  SUBCLASS (AcDbAssocSurfaceActionBody)	\
  FIELD_BL (sab_status, 90); \
  FIELD_B (sab_b1, 290); \
  FIELD_BL (sab_l2, 90); \
  FIELD_B (sab_b2, 290); \
  FIELD_BS (sab_s1, 70); \
  SUBCLASS (AcDbAssocPathBasedSurfaceActionBody) \
  FIELD_BL (pbsab_status, 90)

// (varies) UNSTABLE
// works ok on all Surface_20* but this coverage seems limited.
// field names may change.
// See AcDbAssocActionBody.h
// summary: 78/98=79.59%
DWG_OBJECT (ASSOCPLANESURFACEACTIONBODY)
  DECODE_UNKNOWN_BITS
  AcDbAssocPathBasedSurfaceActionBody_fields;
  SUBCLASS (AcDbAssocPlaneSurfaceActionBody)
  FIELD_BL (psab_status, 90);

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (writedeps, num_deps, 0, 360);
  HANDLE_VECTOR (readdeps, num_deps, 0, 360);
  FIELD_VECTOR_T (descriptions, T, num_deps, 1);
DWG_OBJECT_END

// (varies) UNSTABLE
// 1-4 references, see associativity bits 1-8.
DWG_OBJECT (DIMASSOC)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbDimAssoc)
  FIELD_BLx (associativity, 90);
  FIELD_B (trans_space_flag, 70);
  FIELD_RC (rotated_type, 71);
  FIELD_HANDLE (dimensionobj, 4, 330);
  REPEAT_CN (4, ref, Dwg_DIMASSOC_Ref) // i.e. AcDbOsnapPointRef
  REPEAT_BLOCK
      // TODO: there could be much more blocks, up to 5.
      // 0 1 2 3 => 1 2 4 8. skip unset bits
      if (!(FIELD_VALUE (associativity) & (1<<rcount1)))
        {
#ifdef IS_JSON
          ENDHASH;
#endif
          continue;
        }
      LOG_HANDLE ("DIMASSOC_Ref.rcount1: %d\n", rcount1);
      // DXF: 1, 72, 10, ??, 75
      SUB_FIELD_T  (ref[rcount1], classname, 1); // "AcDbOsnapPointRef"
      SUB_FIELD_RC (ref[rcount1], osnap_type, 72); // 0-13
      // idpaths:
      SUB_FIELD_BL0 (ref[rcount1], num_intsectobj, 74);
      SUB_HANDLE_VECTOR (ref[rcount1], intsectobj, num_intsectobj, 5, 332);

      SUB_FIELD_BD (ref[rcount1], osnap_dist, 40);
      SUB_FIELD_3BD (ref[rcount1], osnap_pt, 10);

      // XrefFullSubentPath
      SUB_FIELD_BL (ref[rcount1], num_xrefs, 0); // 1 or 2
      SUB_VALUEOUTOFBOUNDS (ref[rcount1], num_xrefs, 100)
      SUB_HANDLE_VECTOR (ref[rcount1], xrefs, num_xrefs, 4, 331);

// restrict only when writing, not when reading?
//if (FIELD_VALUE (ref[rcount1].osnap_type) == 6 || FIELD_VALUE (ref[rcount1].osnap_type) == 11)
//  {
      SUB_FIELD_BL0 (ref[rcount1], main_subent_type, 73);
      SUB_FIELD_BL (ref[rcount1], main_gsmarker, 91);
      SUB_FIELD_BL (ref[rcount1], num_xrefpaths, 0);
      FIELD_VECTOR_T (ref[rcount1].xrefpaths, T, ref[rcount1].num_xrefpaths, 301)
//  }
      SUB_FIELD_B  (ref[rcount1], has_lastpt_ref, 75);
      if (FIELD_VALUE (ref[rcount1].has_lastpt_ref))
        {
          SUB_FIELD_3BD (ref[rcount1], lastpt_ref, 0);
        }
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (ref)
  END_REPEAT (ref)

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/*
TvVisualStyle:
  FIELD_T (name, 0);
  FIELD_B (is_default, 0);
 */

// r2007+ STABLE
// dbvisualstyle.h
DWG_OBJECT (VISUALSTYLE)
  SUBCLASS (AcDbVisualStyle)

  UNTIL (R_2007) {
    DECODER { // unstable might exit, use sane defaults
      FIELD_VALUE (edge_crease_angle) = 1.0;
      FIELD_VALUE (edge_opacity) = 1.0;
      FIELD_VALUE (edge_width) = 1;
      FIELD_VALUE (edge_silhouette_width) = 3; // or 5
      FIELD_VALUE (edge_overhang) = 6;
      FIELD_VALUE (edge_jitter) = 2;
      FIELD_VALUE (display_settings) = 1;
      SINCE (R_2010) {
        FIELD_VALUE (internal_only) = 1;
        FIELD_VALUE (edge_crease_angle_int) = 1;
        FIELD_VALUE (edge_color_int) = 1;
        FIELD_VALUE (edge_opacity_int) = 1;
        FIELD_VALUE (edge_width_int) = 1;
        FIELD_VALUE (edge_overhang_int) = 1;
        FIELD_VALUE (edge_jitter_int) = 1;
        FIELD_VALUE (edge_silhouette_color_int) = 1;
        FIELD_VALUE (edge_silhouette_width_int) = 1;
      }
    }
  }

  FIELD_T (description, 2);
  FIELD_BL (style_type, 70);
  PRE (R_2010) {
    FIELD_BL (face_lighting_model, 71);
    FIELD_BL (face_lighting_quality, 72);
    FIELD_BL (face_color_mode, 73);
    DXF { FIELD_BL (face_modifier, 90); }
    FIELD_BD (face_opacity, 40);
    FIELD_BD (face_specular, 41);
    DXF { VALUE_BL (5, 62); } // color
    FIELD_CMC (face_mono_color, 63);
    FIELD_BL (face_modifier, 0);

    FIELD_BL (edge_model, 74);
    FIELD_BL (edge_style, 91);
    FIELD_CMC (edge_intersection_color, 64);
    FIELD_CMC (edge_obscured_color, 65);
    FIELD_BLd (edge_obscured_ltype, 75);
    DXF { FIELD_BL (edge_intersection_ltype, 175); }
    FIELD_BD (edge_crease_angle, 42);
    if (_obj->edge_crease_angle < -360.0 || _obj->edge_crease_angle > 360.0)
    {
      LOG_ERROR ("Invalid edge_crease_angle %f, skipping", _obj->edge_crease_angle);
      _obj->edge_crease_angle = 0.0;
      return DWG_ERR_VALUEOUTOFBOUNDS;
    }

    FIELD_BL (edge_modifier, 92);
    FIELD_CMC (edge_color, 66);
    FIELD_BD (edge_opacity, 43);
    FIELD_CAST (edge_width, BS, BL, 76); // 1
    FIELD_CAST (edge_overhang, BS, BL, 77); // 6
    FIELD_BL (edge_jitter, 78); // 2 documented as BS
    FIELD_CMC (edge_silhouette_color, 67);
    FIELD_CAST (edge_silhouette_width, BS, BL, 79); // 3 or 5
    FIELD_CAST (edge_halo_gap, RC, BL, 170); // 0
    FIELD_CAST (edge_isolines, BS, BL, 171);
    VALUEOUTOFBOUNDS (edge_isolines, 5000)
    FIELD_B (edge_do_hide_precision, 290);
    FIELD_CAST (edge_style_apply, BS, BL, 174);
    FIELD_CAST (edge_intersection_ltype, BS, BL, 0); // DXF above
    FIELD_BL (display_settings, 93); // 1
    FIELD_BLd (display_brightness_bl, 44); // 0
    DECODER {
      FIELD_VALUE (display_brightness) = (double)FIELD_VALUE (display_brightness_bl);
    }
    FIELD_BL (display_shadow_type, 173); // 0
    DXF { FIELD_B (internal_only, 291); }
    SINCE (R_2007) {
      FIELD_BD (bd2007_45, 45);  // 0.0
    }
    FIELD_B (internal_only, 0);
  }
  SINCE (R_2010) {
    ENCODER { _obj->ext_lighting_model = 2; }
    FIELD_BS (ext_lighting_model, 177);
    FIELD_B (internal_only, 291);

    FIELD_BL (face_lighting_model, 71);       FIELD_BS (face_lighting_model_int, 176);
    FIELD_BL (face_lighting_quality, 72);     FIELD_BS (face_lighting_quality_int, 176);
    FIELD_BL (face_color_mode, 73);           FIELD_BS (face_color_mode_int, 176);
    FIELD_BS (face_modifier, 90);             FIELD_BS (face_modifier_int, 0);
    FIELD_BD (face_opacity, 40);              FIELD_BS (face_opacity_int, 176);
    FIELD_BD (face_specular, 41);             FIELD_BS (face_specular_int, 176);
    FIELD_CMC (face_mono_color, 63);          FIELD_BS (face_mono_color_int, 176);
    FIELD_BL (edge_model, 74);                FIELD_BS (edge_model_int, 176);
    FIELD_BL (edge_style, 91);                FIELD_BS (edge_style_int, 176);
    FIELD_CMC (edge_intersection_color, 64);  FIELD_BS (edge_intersection_color_int, 176);
    FIELD_CMC (edge_obscured_color, 65);      FIELD_BS (edge_obscured_color_int, 176);
    FIELD_BL (edge_obscured_ltype, 75);       FIELD_BS (edge_obscured_ltype_int, 176);
    FIELD_BL (edge_intersection_ltype, 175);  FIELD_BS (edge_intersection_ltype_int, 176);
    FIELD_BD (edge_crease_angle, 42);         FIELD_BS (edge_crease_angle_int, 176);
    FIELD_BL (edge_modifier, 92);             FIELD_BS (edge_modifier_int, 176); // this may be 0,1, or 2
    FIELD_CMC (edge_color, 66);               FIELD_BS (edge_color_int, 176);
    FIELD_BD (edge_opacity, 43);              FIELD_BS (edge_opacity_int, 176);
    FIELD_BL (edge_width, 76);                FIELD_BS (edge_width_int, 176);
    FIELD_BL (edge_overhang, 77);             FIELD_BS (edge_overhang_int, 176);
    FIELD_BL (edge_jitter, 78);               FIELD_BS (edge_jitter_int, 176);
    FIELD_CMC (edge_silhouette_color, 67);    FIELD_BS (edge_silhouette_color_int, 176);
    FIELD_BL (edge_silhouette_width, 79);     FIELD_BS (edge_silhouette_width_int, 176);
    FIELD_BL (edge_halo_gap, 170);            FIELD_BS (edge_halo_gap_int, 176);
    FIELD_BL (edge_isolines, 171);
    VALUEOUTOFBOUNDS (edge_isolines, 5000)    FIELD_BS (edge_isolines_int, 176);
    FIELD_B (edge_do_hide_precision, 290);    FIELD_BS (edge_do_hide_precision_int, 176);

    FIELD_BL (display_settings, 93);          FIELD_BS (display_settings_int, 176);
    FIELD_BD (display_brightness, 44);        FIELD_BS (display_brightness_int, 176);
    DECODER {
      if (FIELD_VALUE (display_brightness) >= -INT32_MAX && FIELD_VALUE (display_brightness) < INT32_MAX)
        FIELD_VALUE (display_brightness_bl) = (BITCODE_BLd)FIELD_VALUE (display_brightness);
    }
    FIELD_BL (display_shadow_type, 173);      FIELD_BS (display_shadow_type_int, 176);

    SINCE (R_2013) {
      DXF { FIELD_BS (num_props, 70); }
      else { FIELD_VALUE (num_props) = 58; }
      FIELD_B (b_prop1c, 290);                FIELD_BS (b_prop1c_int, 176);
      FIELD_B (b_prop1d, 290);                FIELD_BS (b_prop1d_int, 176);
      FIELD_B (b_prop1e, 290);                FIELD_BS (b_prop1e_int, 176);
      FIELD_B (b_prop1f, 90);                 FIELD_BS (b_prop1f_int, 176);
      FIELD_B (b_prop20, 290);                FIELD_BS (b_prop20_int, 176);
      FIELD_B (b_prop21, 90);                 FIELD_BS (b_prop21_int, 176);
      FIELD_B (b_prop22, 290);                FIELD_BS (b_prop22_int, 176);
      FIELD_B (b_prop23, 290);                FIELD_BS (b_prop23_int, 176);
      FIELD_B (b_prop24, 290);                FIELD_BS (b_prop24_int, 176);
      FIELD_BL (bl_prop25, 90);               FIELD_BS (bl_prop25_int, 176);
      FIELD_BD (bd_prop26, 40);               FIELD_BS (bd_prop26_int, 176);
      FIELD_BD (bd_prop27, 40);               FIELD_BS (bd_prop27_int, 176);
      FIELD_BL (bl_prop28, 90);               FIELD_BS (bl_prop28_int, 176);
      FIELD_CMC (c_prop29, 62);               FIELD_BS (c_prop29_int, 176);
      FIELD_BL (bl_prop2a, 90);               FIELD_BS (bl_prop2a_int, 176);
      FIELD_BL (bl_prop2b, 90);               FIELD_BS (bl_prop2b_int, 176);
      FIELD_CMC (c_prop2c, 62);               FIELD_BS (c_prop2c_int, 176);
      FIELD_B (b_prop2d, 0);                  FIELD_BS (b_prop2d_int, 176);
      FIELD_BL (bl_prop2e, 290);              FIELD_BS (bl_prop2e_int, 176);
      FIELD_BL (bl_prop2f, 90);               FIELD_BS (bl_prop2f_int, 176);
      FIELD_BL (bl_prop30, 90);               FIELD_BS (bl_prop30_int, 176);
      FIELD_B (b_prop31, 290);                FIELD_BS (b_prop31_int, 176);
      FIELD_BL (bl_prop32, 90);               FIELD_BS (bl_prop32_int, 176);
      FIELD_CMC (c_prop33, 62);               FIELD_BS (c_prop33_int, 176);
      FIELD_BD (bd_prop34, 40);               FIELD_BS (bd_prop34_int, 176);
      FIELD_BL (edge_wiggle, 90);             FIELD_BS (edge_wiggle_int, 176);  // prop 0x35
      FIELD_T (strokes, 1);                   FIELD_BS (strokes_int, 176);      // prop 0x36
      FIELD_B (b_prop37, 290);                FIELD_BS (b_prop37_int, 176);
      FIELD_BD (bd_prop38, 40);               FIELD_BS (bd_prop38_int, 176);
      FIELD_BD (bd_prop39, 40);               FIELD_BS (bd_prop39_int, 176);
    }
  }
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/* LIGHT: SpotLight, PointLight, DistantLight. dbLight.h
 */
DWG_ENTITY (LIGHT)

  SUBCLASS (AcDbLight);
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)
  FIELD_T (name, 1);
  FIELD_BL (type, 70);
  FIELD_B (status, 290);
#ifdef IS_DXF
  UNTIL (R_2000) {
    FIELD_BL (color.rgb, 90);
  } else {
    FIELD_CMC (color, 63);
  }
#else
  FIELD_CMC (color, 63);
#endif
  FIELD_B (plot_glyph, 291); /* if it's plottable */
  FIELD_BD (intensity, 40);
  FIELD_3BD (position, 10);
  FIELD_3BD (target, 11);
  FIELD_BL (attenuation_type, 72);
  FIELD_B (use_attenuation_limits, 292);
  FIELD_BD (attenuation_start_limit, 41);
  FIELD_BD (attenuation_end_limit, 42);
  FIELD_BD (hotspot_angle, 50);
  FIELD_BD (falloff_angle, 51);
  FIELD_B (cast_shadows, 293);
  FIELD_BL (shadow_type, 73);
  FIELD_BS (shadow_map_size, 91);
  FIELD_RCd (shadow_map_softness, 280);

  DECODER {
    // LIGHTINGUNITS is a member of the AcDbVariableDictionary
    // NOD => DICTIONARY => DICTIONARYVAR
    // may not be cached
    char *value = dwg_variable_dict (dwg, "LIGHTINGUNITS");
    LOG_TRACE ("vardict.LIGHTINGUNITS: %s\n", value);
    if (value && strEQ (value, "2")) /* PHOTOMETRIC */
      FIELD_VALUE (is_photometric) = 1;
  }
  LOG_TRACE ("is_photometric: %d\n", FIELD_VALUE (is_photometric));
  if (FIELD_VALUE (is_photometric))
  {
    FIELD_B (has_photometric_data, 1);
    // IES light model
    if (FIELD_VALUE (has_photometric_data))
      {
        DXF { VALUE_B (0, 295); }
        FIELD_B (has_webfile, 290);
        FIELD_T (webfile, 300);
        FIELD_BS (physical_intensity_method, 70);
        FIELD_BD (physical_intensity, 40);
        FIELD_BD (illuminance_dist, 41);
        FIELD_BS (lamp_color_type, 71); //0: temp. in kelvin, 1: as preset
        FIELD_BD (lamp_color_temp, 42);
        FIELD_BS (lamp_color_preset, 72);
        FIELD_3BD_1 (web_rotation, 43);
        // ExtendedLigthShape
        FIELD_BS (extlight_shape, 73);
        FIELD_BD (extlight_length, 46);
        FIELD_BD (extlight_width, 47);
        FIELD_BD (extlight_radius, 48);
        FIELD_BS (webfile_type, 74);
        FIELD_BS (web_symetry, 75);
        FIELD_BS (has_target_grip, 76); //bool
        FIELD_BD (web_flux, 49);
        FIELD_BD (web_angle1, 50);
        FIELD_BD (web_angle2, 51);
        FIELD_BD (web_angle3, 52);
        FIELD_BD (web_angle4, 53);
        FIELD_BD (web_angle5, 54);
        FIELD_BS (glyph_display_type, 77);
      }
  }
  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

// (varies)
// ENHANCEDBLOCK => AcDbDynamicBlockRoundTripPurgePreventer
DWG_OBJECT (DYNAMICBLOCKPURGEPREVENTER)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbDynamicBlockPurgePreventer)
  FIELD_BS (flag, 70); //1 class_version would be 90
  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (block, 5, 0)
DWG_OBJECT_END

// UNSTABLE
DWG_OBJECT (DBCOLOR)
  SUBCLASS (AcDbColor)
  FIELD_CMC (color, 62);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// (varies) UNSTABLE
// dbhelix.h
DWG_ENTITY (HELIX)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbSpline)
  FIELD_BL (scenario, 0);
  UNTIL (R_2013) {
    if (FIELD_VALUE (scenario) != 1 && FIELD_VALUE (scenario) != 2)
      LOG_ERROR ("unknown scenario %d", FIELD_VALUE (scenario));
  }
  SINCE (R_2013) {
    FIELD_BL (splineflags1, 0);
    FIELD_BL (knotparam, 0);
    if (FIELD_VALUE (splineflags1) & 1)
      FIELD_VALUE (scenario) = 2;
    if (FIELD_VALUE (knotparam) == 15)
      FIELD_VALUE (scenario) = 1;
  }

  DXF {
    // extrusion on planar
    VALUE_RD (0.0, 210); VALUE_RD (0.0, 220); VALUE_RD (1.0, 230);
    FIELD_BL (flag, 70);
  }
  FIELD_BL (degree, 71);

  if (FIELD_VALUE (scenario) & 2) // bezier spline
    {
      FIELD_VALUE (flag) = 8 + 32 + //planar, not rational
        // ignore method fit points and closed bits
        ((FIELD_VALUE (splineflags1) & ~5) << 7);
      FIELD_BD (fit_tol, 44); // def: 0.0000001
      FIELD_3BD (beg_tan_vec, 12);
      FIELD_3BD (end_tan_vec, 13);
      FIELD_BL (num_fit_pts, 74);
      VALUEOUTOFBOUNDS (num_fit_pts, 5000)
    }
  if (FIELD_VALUE (scenario) & 1) // spline
    {
      FIELD_B (rational, 0); // flag bit 2
      FIELD_B (closed_b, 0); // flag bit 0
      FIELD_B (periodic, 0); // flag bit 1
      FIELD_BD (knot_tol, 42); // def: 0.0000001
      FIELD_BD (ctrl_tol, 43); // def: 0.0000001
      FIELD_BL (num_knots, 72);
      VALUEOUTOFBOUNDS (num_knots, 10000)
      FIELD_BL (num_ctrl_pts, 73);
      VALUEOUTOFBOUNDS (num_ctrl_pts, 10000)
      FIELD_B (weighted, 0);

      FIELD_VALUE (flag) = 8 + //planar
        FIELD_VALUE (closed_b) +
        (FIELD_VALUE (periodic) << 1) +
        (FIELD_VALUE (rational) << 2) +
        (FIELD_VALUE (weighted) << 3);
    }

  if (FIELD_VALUE (scenario) & 1) {
    FIELD_VECTOR (knots, BD, num_knots, 40)
    REPEAT (num_ctrl_pts, ctrl_pts, Dwg_SPLINE_control_point)
    REPEAT_BLOCK
        SUB_FIELD_3BD_inl (ctrl_pts[rcount1], xyz, 10);
        if (!FIELD_VALUE (weighted))
          FIELD_VALUE (ctrl_pts[rcount1].w) = 0; // skipped when encoding
        else
          SUB_FIELD_BD (ctrl_pts[rcount1], w, 41);
    END_REPEAT_BLOCK
    SET_PARENT (ctrl_pts, (Dwg_Entity_SPLINE*)_obj);
    END_REPEAT (ctrl_pts);
  }
  if (FIELD_VALUE (scenario) & 2) {
    FIELD_3DPOINT_VECTOR (fit_pts, num_fit_pts, 11)
  }

  SUBCLASS (AcDbHelix)
  FIELD_BS (major_version, 90);
  FIELD_BS (maint_version, 91);
  FIELD_3BD (axis_base_pt, 10);
  FIELD_3BD_1 (start_pt, 11);
  FIELD_3BD_1 (axis_vector, 12);
  FIELD_BD (radius, 40);
  FIELD_BD (num_turns, 41);
  FIELD_BD (turn_height, 43);
  FIELD_B (handedness, 290); //0 left, 1 right (twist)
  FIELD_BS (constraint_type, 280); //0 constrain turn height, 1 turns, 2 height

DWG_ENTITY_END

// unstable
// See AcDbAssocActionBody.h and AcDbAssocDimDependencyBody.h
DWG_OBJECT (ASSOCALIGNEDDIMACTIONBODY)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocActionBody)
  FIELD_BL (aab_version, 90);
  SUBCLASS (AcDbAssocParamBasedActionBody)
  FIELD_BL (pab_status, 90);
  FIELD_BL (pab_l2, 90);
  FIELD_BL (pab_l3, 90);
  //FIELD_HANDLE (writedep, 0, 360);
  FIELD_BL (pab_l4, 90);
  FIELD_BL (pab_l5, 90);
  //FIELD_BL (pab_l6, 90);
  SUBCLASS (ACDBASSOCALIGNEDDIMACTIONBODY)
  FIELD_BL (dcm_status, 90); //has d_node or r_node

  //TODO: DXF has a different order
  START_OBJECT_HANDLE_STREAM;
  VERSION (R_2013) {
    FIELD_HANDLE (readdep, 4, 330);
    FIELD_HANDLE (writedep, 3, 360);
    FIELD_HANDLE (r_node, 4, 330);
    FIELD_HANDLE (d_node, 4, 330);
  } else {
    FIELD_HANDLE (writedep, 3, 360);
    FIELD_HANDLE (readdep, 4, 330);
    FIELD_HANDLE (d_node, 3, 330);
    FIELD_HANDLE (r_node, 4, 330);
  }
DWG_OBJECT_END

// undocumented fields, unstable, but looks stable.
// types: Sphere|Cylinder|Cone|Torus|Box|Wedge|Pyramid
DWG_ENTITY (MESH)
  SUBCLASS (AcDbSubDMesh)
  FIELD_BS (dlevel, 71);       // 2
  FIELD_B (is_watertight, 72); // 0
  FIELD_BL (num_subdiv_vertex, 91); //0
  FIELD_3DPOINT_VECTOR (subdiv_vertex, num_subdiv_vertex, 10);
  FIELD_BL (num_vertex, 92); //14 @14
  FIELD_3DPOINT_VECTOR (vertex, num_vertex, 10);
  FIELD_BL (num_faces, 93); // 30
  FIELD_VECTOR (faces, BL, num_faces, 90);

  FIELD_BL (num_edges, 94); // 19
  REPEAT (num_edges, edges, Dwg_MESH_edge)
  REPEAT_BLOCK
      SUB_FIELD_BL (edges[rcount1], idxfrom, 90);
      SUB_FIELD_BL (edges[rcount1], idxto, 90);
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (edges);
  END_REPEAT (edges);
  //FIELD_VECTOR (edges, Dwg_MESH_edge, num_edges * 2, 90);
  FIELD_BL (num_crease, 95); // 19
  FIELD_VECTOR (crease, BD, num_crease, 140);
  COMMON_ENTITY_HANDLE_DATA;
DWG_ENTITY_END

DWG_OBJECT (LIGHTLIST)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbLightList)
  FIELD_BL (class_version, 90);
  FIELD_BL (num_lights, 90);
  REPEAT (num_lights, lights, Dwg_LIGHTLIST_light)
  REPEAT_BLOCK
      SUB_FIELD_HANDLE (lights[rcount1],handle, 5, 5)
      SUB_FIELD_T (lights[rcount1],name, 1)
  END_REPEAT_BLOCK
  END_REPEAT (lights)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// hard-owned child of AcDbViewportTableRecord or AcDbViewport 361
// DXF docs put that as Entity, wrong!
DWG_OBJECT (SUN)
  SUBCLASS (AcDbSun)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)
  FIELD_B (is_on, 290);       // status, isOn
  FIELD_CMC (color, 63);
  FIELD_BD (intensity, 40);   //
  FIELD_B (has_shadow, 291);  // shadow on/off
  FIELD_BL (julian_day, 91);
  FIELD_BL (msecs, 92);
  FIELD_B (is_dst, 292);      // isDayLightSavingsOn
  FIELD_BL (shadow_type, 70); // 0 raytraced, 1 shadow maps
  FIELD_BS (shadow_mapsize, 71); // max 3968
  FIELD_RCd (shadow_softness, 280);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

#define AcDbRenderSettings_fields                                             \
    SUBCLASS (AcDbRenderSettings)                                             \
    VERSION (R_2013) { /* version 0x1f */                                     \
      VALUE_BL (_obj->class_version + 1, 90)                                  \
    } else {                                                                  \
      FIELD_BL (class_version, 90);                                           \
    }                                                                         \
    FIELD_T (name, 1);                                                        \
    FIELD_B (fog_enabled, 290);                                               \
    FIELD_B (fog_background_enabled, 290);                                    \
    FIELD_B (backfaces_enabled, 290);                                         \
    FIELD_B (environ_image_enabled, 290);                                     \
    FIELD_T (environ_image_filename, 1);                                      \
    FIELD_T (description, 1);                                                 \
    FIELD_BL (display_index, 90);                                             \
    VERSION (R_2013) {                                                        \
      FIELD_B (has_predefined, 290);                                          \
    }

DWG_OBJECT (RENDERSETTINGS)
  AcDbRenderSettings_fields;
DWG_OBJECT_END

DWG_OBJECT (MENTALRAYRENDERSETTINGS)
  AcDbRenderSettings_fields;
  SUBCLASS (AcDbMentalRayRenderSettings);
  FIELD_BL (mr_version, 90); /* = 2 */
  FIELD_BL (sampling1, 90);
  FIELD_BL (sampling2, 90);
  FIELD_BS (sampling_mr_filter, 70);
  FIELD_BD (sampling_filter1, 40);
  FIELD_BD (sampling_filter2, 40);
  FIELD_BD (sampling_contrast_color1, 40);
  FIELD_BD (sampling_contrast_color2, 40);
  FIELD_BD (sampling_contrast_color3, 40);
  FIELD_BD (sampling_contrast_color4, 40);
  FIELD_BS (shadow_mode, 70);
  FIELD_B  (shadow_maps_enabled, 290);
  FIELD_B  (ray_tracing_enabled, 290);
  FIELD_BL (ray_trace_depth1, 90);
  FIELD_BL (ray_trace_depth2, 90);
  FIELD_BL (ray_trace_depth3, 90);
  FIELD_B  (global_illumination_enabled, 290);
  FIELD_BL (gi_sample_count, 90);
  FIELD_B  (gi_sample_radius_enabled, 290);
  FIELD_BD (gi_sample_radius, 40);
  FIELD_BL (gi_photons_per_light, 90);
  FIELD_BL (photon_trace_depth1, 90);
  FIELD_BL (photon_trace_depth2, 90);
  FIELD_BL (photon_trace_depth3, 90);
  FIELD_B  (final_gathering_enabled, 290);
  FIELD_BL (fg_ray_count, 90);
  FIELD_B  (fg_sample_radius_state1, 290);
  FIELD_B  (fg_sample_radius_state2, 290);
  FIELD_B  (fg_sample_radius_state3, 290);
  FIELD_BD (fg_sample_radius1, 40);
  FIELD_BD (fg_sample_radius2, 40);
  FIELD_BD (light_luminance_scale, 40);
  FIELD_BS (diagnostics_mode, 70);
  FIELD_BS (diagnostics_grid_mode, 70);
  FIELD_BD (diagnostics_grid_float, 40);
  FIELD_BS (diagnostics_photon_mode, 70);
  FIELD_BS (diagnostics_bsp_mode, 70);
  FIELD_B  (export_mi_enabled, 290);
  FIELD_T  (mr_description, 1);
  FIELD_BL (tile_size, 90);
  FIELD_BS (tile_order, 70);
  FIELD_BL (memory_limit, 90);
  FIELD_B  (diagnostics_samples_mode, 290);
  FIELD_BD (energy_multiplier, 40);
  //START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (RAPIDRTRENDERSETTINGS)
  AcDbRenderSettings_fields;
  SUBCLASS (AcDbRapidRTRenderSettings)
  FIELD_BL (rapidrt_version, 90);
  FIELD_BL (render_target, 70);
  FIELD_BL (render_level, 90);
  FIELD_BL (render_time, 90);
  FIELD_BL (lighting_model, 70);
  FIELD_BL (filter_type, 70);
  FIELD_BD (filter_width, 40);
  FIELD_BD (filter_height, 40);
  VERSION (R_2013)
    {}
  else
    FIELD_B (has_predefined, 290); // when RENDERSETTINGS does not handle it
DWG_OBJECT_END

/* MATERIAL classes */

// each color writes RC flag, BD factor, BL rgb if flag=1
#define MAT_COLOR(color, dxf1, dxf2, dxf3)                                    \
  {                                                                           \
    FIELD_RC (color.flag, dxf1);     /* 0 Use current color, 1 Override */    \
    FIELD_BD (color.factor, dxf2);   /* 0.0 - 1.0 */                          \
    if (_obj->color.flag == 1)                                                \
      {                                                                       \
        FIELD_BLx (color.rgb, dxf3);                                           \
      }                                                                       \
  }

// We need to declare it first, because it's recursive. Only here
DWG_SUBCLASS_DECL (MATERIAL, Texture_diffusemap);

/* if source == 2 */
#define MAT_TEXTURE(map, value)                                               \
  {                                                                           \
    FIELD_BS (map.texturemode, 277);                                          \
    if (FIELD_VALUE (map.texturemode) == 0)                                   \
      {                                                                       \
        /* woodtexture */                                                     \
        MAT_COLOR (map.color1, 278, 460, 95);                                 \
        MAT_COLOR (map.color2, 279, 461, 96);                                 \
      }                                                                       \
    else if (FIELD_VALUE (map.texturemode) == 1)                              \
      {                                                                       \
        /* marbletexture */                                                   \
        MAT_COLOR (map.color1, 280, 465, 97);                                 \
        MAT_COLOR (map.color2, 281, 466, 98);                                 \
      }                                                                       \
    else if (FIELD_VALUE (map.texturemode) == 2)                              \
      {                                                                       \
        /* generic texture variant */                                         \
        FIELD_BS (genproctype, 0);                                            \
        switch (_obj->genproctype) {                                          \
        case 1:                                                               \
          FIELD_B (genprocvalbool, 291); break;                               \
        case 2:                                                               \
          FIELD_BS (genprocvalint, 271); break;                               \
        case 3:                                                               \
          FIELD_BD (genprocvalreal, 469); break;                              \
        case 4:                                                               \
          FIELD_CMC (genprocvalcolor, 62); break;                             \
        case 5:                                                               \
          FIELD_T (genprocvaltext, 301); break;                               \
        case 6:                                                               \
          FIELD_BS (num_gentextures, 0);                                      \
          REPEAT (num_gentextures, gentextures, Dwg_MATERIAL_gentexture)      \
          REPEAT_BLOCK                                                        \
            _obj->gentextures[rcount1].material = _obj;                       \
            SUB_FIELD_T (gentextures[rcount1], genprocname, 300);             \
            LOG_WARN ("recursive MATERIAL.gentextures")                       \
            CALL_SUBCLASS (_obj->gentextures[rcount1].material, MATERIAL,     \
                           Texture_diffusemap);                               \
          END_REPEAT_BLOCK                                                    \
          SET_PARENT_OBJ (gentextures);                                       \
          END_REPEAT (gentextures)                                            \
          FIELD_B (genproctableend, 292);                                     \
        default:                                                              \
          break;                                                              \
         }                                                                    \
      }                                                                       \
  }

#define MAT_MAPPER(map, dxf4, dxf5, dxf6, dxf7)                               \
  {                                                                           \
    /* 0 Inherit, 1 Planar (def), 2 Box, 3 Cylinder, 4 Sphere */              \
    FIELD_RC (map.projection, dxf4);                                          \
    /* 0 Inherit, 1 Tile (def), 2 Crop, 3 Clamp, 4 Mirror */                  \
    FIELD_RC (map.tiling, dxf5);                                              \
    /* 1 no, 2: scale to curr ent, 4: w/ current block transform */           \
    FIELD_RC (map.autotransform, dxf6);                                       \
    FIELD_VECTOR_N (map.transmatrix, BD, 16, dxf7);                           \
  }

#define MAT_MAP(map, dxf1, dxf2, dxf3, dxf4, dxf5, dxf6, dxf7)                \
    FIELD_BD (map.blendfactor, dxf1);                                         \
    MAT_MAPPER (map, dxf4, dxf5, dxf6, dxf7);                                 \
    FIELD_RC (map.source, dxf2); /* 0 scene, 1 file (def), 2 procedural */    \
    if (FIELD_VALUE (map.source) == 1)                                        \
      {                                                                       \
        FIELD_T (map.filename, dxf3); /* if NULL no map */                    \
      }                                                                       \
    else if (FIELD_VALUE (map.source) == 2)                                   \
      MAT_MAPPER (map, dxf4, dxf5, dxf6, dxf7)

#define Texture_diffusemap_fields MAT_TEXTURE (diffusemap, 0)
DWG_SUBCLASS (MATERIAL, Texture_diffusemap);

// (varies)
DWG_OBJECT (MATERIAL)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbMaterial)
  FIELD_T (name, 1);
  FIELD_T (description, 2);
  MAT_COLOR (ambient_color, 70, 40, 90);
  MAT_COLOR (diffuse_color, 71, 41, 91);

  MAT_MAP (diffusemap, 42, 72, 3, 73, 74, 75, 43);
  DXF {
    SINCE (R_2007)
      CALL_SUBCLASS (_obj, MATERIAL, Texture_diffusemap);
      /* MAT_TEXTURE (diffusemap, 0) */
    //DXF { VALUE_B (1, 292); } /* genproctableend  */
    //DXF { VALUE_BS (value, 277); } /* ?? */
  }
  MAT_COLOR (specular_color, 76, 45, 92);
  DXF { FIELD_BD (specular_gloss_factor, 44); }
  MAT_MAP (specularmap, 46, 77, 4, 78, 79, 170, 47);
  FIELD_BD (specular_gloss_factor, 0); // def: 0.5
  MAT_MAP (reflectionmap, 48, 171, 6, 172, 173, 174, 49);
  FIELD_BD (opacity_percent, 140);      // def: 1.0
  MAT_MAP (opacitymap, 141, 175, 7, 176, 177, 178, 142);
  MAT_MAP (bumpmap, 143, 179, 8, 270, 271, 272, 144);
  FIELD_BD (refraction_index, 145);     // def: 1.0
  MAT_MAP (refractionmap, 146, 273, 9, 274, 275, 276, 147);

  SINCE (R_2007) {
    // no DXF if 0
    FIELD_BD0 (translucence, 148);
    FIELD_BD0 (self_illumination, 149);
    FIELD_BD0 (reflectivity, 468);
    FIELD_BL0 (illumination_model, 93);
    FIELD_BL0 (channel_flags, 94);
    FIELD_BL0 (mode, 282);
  }

#if 0
  // missing:
  FIELD_BD (indirect_bump_scale, 461);
  FIELD_BD (reflectance_scale, 462);
  FIELD_BD (transmittance_scale, 463);
  FIELD_B (two_sided_material, 290);
  FIELD_BD (luminance, 464);
  FIELD_BS (luminance_mode, 270);
  FIELD_BS (normalmap_method, 271);
  FIELD_BD (normalmap_strength, 465); //def: 1.0
  MAT_MAP (normalmap, 42, 72, 3, 73, 74, 75, 43);
  FIELD_B (is_anonymous, 293);
  FIELD_BS (global_illumination, 272); // 0 none, 1 cast, 2 receive, 3 cast&receive
  FIELD_BS (final_gather, 273);        // 0 none, 1 cast, 2 receive, 3 cast&receive
  FIELD_BD (color_bleed_scale, 460);

  // saveas: ADVMATERIAL into xdic
  //FIELD_B (genproctableend, 292); // always 1
  //78
  //172
  //176
  //270
  //274
#endif
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_ENTITY (ARC_DIMENSION)

  DECODE_UNKNOWN_BITS
  COMMON_ENTITY_DIMENSION
  JSON { FIELD_RC (flag, 0); }
  SUBCLASS (AcDbArcDimension)
  DECODER_OR_ENCODER {
    FIELD_3BD (def_pt, 10);
  }
  FIELD_3BD (xline1_pt, 13);
  FIELD_3BD (xline2_pt, 14);
  FIELD_3BD (center_pt, 15);
  FIELD_B (is_partial, 70);
  FIELD_BD (arc_start_param, 41);
  FIELD_BD (arc_end_param, 42);
  FIELD_B (has_leader, 71);
  FIELD_3BD (leader1_pt, 16);
  FIELD_3BD (leader2_pt, 17);

  COMMON_ENTITY_HANDLE_DATA;
  FIELD_HANDLE (dimstyle, 5, 0);
  FIELD_HANDLE (block, 5, 0);
DWG_ENTITY_END

// as ACAD_LAYERFILTERS in the NOD
DWG_OBJECT (LAYERFILTER)
  SUBCLASS (AcDbLayerFilter)
  FIELD_BL (num_names, 0);
  FIELD_VECTOR_T (names, T, num_names, 8);
DWG_OBJECT_END

// abstract subclass. requires evalexpr
#define AcDbEvalExpr_fields                                                   \
  SUBCLASS (AcDbEvalExpr)                                                     \
  DXF { FIELD_BL (evalexpr.nodeid, 90); }                                     \
  FIELD_BLd (evalexpr.parentid, 0);                                           \
  FIELD_BL (evalexpr.major, 98);                                              \
  FIELD_BL (evalexpr.minor, 99);                                              \
  if (IF_IS_DXF && FIELD_VALUE (evalexpr.value_type) == -9999)                \
    {                                                                         \
      ; /* 70 -9999 not in DXF */                                             \
    }                                                                         \
  else                                                                        \
    {                                                                         \
      DXF { VALUE_TFF ("", 1); }                                              \
      FIELD_BSd (evalexpr.value_type, 70);                                    \
      /* TODO not a union yet */                                              \
      switch (_obj->evalexpr.value_type)                                      \
        {                                                                     \
        case 40:                                                              \
          FIELD_BD (evalexpr.value.num40, 40);                                \
          break;                                                              \
        case 10:                                                              \
          FIELD_2RD (evalexpr.value.pt2d, 10);                                \
          break;                                                              \
        case 11:                                                              \
          FIELD_2RD (evalexpr.value.pt3d, 11);                                \
          break;                                                              \
        case 1:                                                               \
          FIELD_T (evalexpr.value.text1, 1);                                  \
          break;                                                              \
        case 90:                                                              \
          FIELD_BL (evalexpr.value.long90, 90);                               \
          break;                                                              \
        case 91:                                                              \
          FIELD_HANDLE (evalexpr.value.handle91, 5, 91);                      \
          break;                                                              \
        case 70:                                                              \
          FIELD_BS (evalexpr.value.short70, 70);                              \
          break;                                                              \
        case -9999:                                                           \
        default:                                                              \
          break;                                                              \
        }                                                                     \
    }                                                                         \
  FIELD_BL (evalexpr.nodeid, 0)

// abstract subclass. as field value
#define AcDbEvalVariant_fields                                          \
  FIELD_BSd (value_type, 70);                                           \
  switch (_obj->value_type)                                             \
    {                                                                   \
    case 1:                                                             \
      SUB_FIELD_BD (value,bd, 40);                                      \
      break;                                                            \
    case 2:                                                             \
      SUB_FIELD_BL (value,bl, 90);                                      \
      break;                                                            \
    case 3:                                                             \
      SUB_FIELD_BS (value,bs, 70);                                      \
      break;                                                            \
    case 5:                                                             \
      SUB_FIELD_T (value,text, 1);                                      \
      break;                                                            \
    case 11:                                                            \
      SUB_FIELD_HANDLE (value,handle, 5, 91);                           \
      break;                                                            \
    /* more: 9 id, 12 pt3d, 14 pt2d */                                  \
    default:                                                            \
      break;                                                            \
    }

#define AcDbShHistoryNode_fields                                              \
    SUBCLASS (AcDbShHistoryNode)                                              \
    FIELD_BL (history_node.major, 90);                                        \
    FIELD_BL (history_node.minor, 91);                                        \
    FIELD_VECTOR_N1 (history_node.trans, BD, 16, 40);                         \
    FIELD_CMC (history_node.color, 62);                                       \
    FIELD_BL (history_node.step_id, 92);                                      \
    FIELD_HANDLE (history_node.material, 5, 347)

// Stable
// same as Wedge
DWG_OBJECT (ACSH_BOX_CLASS)
  //DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShBox)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_BD (length, 40);
  FIELD_BD (width, 41);
  FIELD_BD (height, 42);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// Stable
DWG_OBJECT (ACSH_WEDGE_CLASS)
  //DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShWedge)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_BD (length, 40);
  FIELD_BD (width, 41);
  FIELD_BD (height, 42);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// Stable
DWG_OBJECT (ACSH_SPHERE_CLASS)
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShSpere)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_BD (radius, 40);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// Stable
DWG_OBJECT (ACSH_CYLINDER_CLASS)
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShCylinder)
  FIELD_BL (major, 90);
  FIELD_BL (minor, 91);
  FIELD_BD (height, 40);
  FIELD_BD (major_radius, 41);
  FIELD_BD (minor_radius, 42);
  FIELD_BD (x_radius, 43);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// Unstable
DWG_OBJECT (ACSH_CONE_CLASS)
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShCone)
  FIELD_BL (major, 90);
  FIELD_BL (minor, 91);
  FIELD_BD (base_radius, 40);
  FIELD_BD (top_major_radius, 41);
  FIELD_BD (top_minor_radius, 42);
  FIELD_BD (top_x_radius, 43);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END


DWG_OBJECT (ACSH_PYRAMID_CLASS)
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShPyramid)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_BD (height, 40);
  FIELD_BL (sides, 92);
  FIELD_BD (radius, 41);
  FIELD_BD (topradius, 42);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_FILLET_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShFillet)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //1
  FIELD_BL (bl92, 92);
  FIELD_BL (num_edges, 93);
  FIELD_VECTOR (edges, BL, num_edges, 94)
  FIELD_BL (num_radiuses, 95);
  FIELD_VECTOR (radiuses, BD, num_radiuses, 41)
  FIELD_BL (num_startsetbacks, 96);
  FIELD_BL (num_endsetbacks, 97);
  FIELD_VECTOR (endsetbacks, BD, num_endsetbacks, 43)
  FIELD_VECTOR (startsetbacks, BD, num_startsetbacks, 42)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_CHAMFER_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShChamfer)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //1
  FIELD_BL (bl92, 92);
  FIELD_BD (base_dist, 41);
  FIELD_BD (other_dist, 42);
  FIELD_BL (num_edges, 93);
  FIELD_VECTOR (edges, BL, num_edges, 94)
  FIELD_BL (bl95, 95);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_TORUS_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShTorus)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //1
  FIELD_BD (major_radius, 40);
  FIELD_BD (minor_radius, 41);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_BREP_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShBrep)
  FIELD_BL (major, 90); // also in DWG?
  FIELD_BL (minor, 91);
  ACTION_3DSOLID;
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_BOOLEAN_CLASS)
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShBoolean)
  FIELD_BL (major, 90);
  FIELD_BL (minor, 91);
  FIELD_RCd (operation, 280);
  FIELD_BL (operand1, 92);
  FIELD_BL (operand2, 93);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

/*=============================================================================*/

/* In work area:
   The following entities/objects are only stored as raw UNKNOWN_ENT/OBJ,
   unless enabled via --enable-debug/-DDEBUG_CLASSES */

#if defined (DEBUG_CLASSES) || defined (IS_FREE)

DWG_OBJECT (OBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbObjectContextData)
  SINCE (R_2010) {
    IF_ENCODE_FROM_EARLIER {
      FIELD_VALUE (class_version) = 3;
    }
    FIELD_BS (class_version, 70);
    if (FIELD_VALUE (class_version) > 10)
      return DWG_ERR_VALUEOUTOFBOUNDS;
  }
  FIELD_B (is_default, 0);
  FIELD_B (in_dwg, 290);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (CONTEXTDATAMANAGER)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbContextDataManager)
  FIELD_HANDLE (objectcontext, 5, 0);
  FIELD_BL (num_submgrs, 0);
  REPEAT (num_submgrs, submgrs, Dwg_CONTEXTDATA_submgr)
  REPEAT_BLOCK
      SUB_FIELD_HANDLE (submgrs[rcount1],handle, 5, 0);
      SUB_FIELD_BL (submgrs[rcount1],num_entries, 90);
      REPEAT2 (submgrs[rcount1].num_entries, submgrs[rcount1].entries, Dwg_CONTEXTDATA_dict)
      REPEAT_BLOCK
          SUB_FIELD_HANDLE (submgrs[rcount1].entries[rcount2],itemhandle, 5, 350);
          SUB_FIELD_T (submgrs[rcount1].entries[rcount2],text, 3);
      END_REPEAT_BLOCK
      END_REPEAT (submgrs[rcount1].entries)
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (submgrs)
  END_REPEAT (submgrs)

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// (varies) DEBUGGING
// See AcDbAssocActionBody.h and ASSOCPLANESURFACEACTIONBODY
DWG_OBJECT (ASSOCEXTRUDEDSURFACEACTIONBODY)
  DECODE_UNKNOWN_BITS
  AcDbAssocPathBasedSurfaceActionBody_fields;
  SUBCLASS (AcDbAssocExtrudedSurfaceActionBody)
  FIELD_BL (esab_status, 90);

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (writedeps, num_deps, 0, 360);
  HANDLE_VECTOR (readdeps, num_deps, 0, 360);
  FIELD_VECTOR_T (descriptions, T, num_deps, 1);
DWG_OBJECT_END

// See AcDbAssocActionBody.h and ASSOCPLANESURFACEACTIONBODY
DWG_OBJECT (ASSOCLOFTEDSURFACEACTIONBODY)
  DECODE_UNKNOWN_BITS
  AcDbAssocPathBasedSurfaceActionBody_fields;
  SUBCLASS (AcDbAssocLoftedSurfaceActionBody)
  FIELD_BL (lsab_status, 90);

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (writedeps, num_deps, 0, 360);
  HANDLE_VECTOR (readdeps, num_deps, 0, 360);
  FIELD_VECTOR_T (descriptions, T, num_deps, 1);
DWG_OBJECT_END

// See AcDbAssocActionBody.h and ASSOCPLANESURFACEACTIONBODY
DWG_OBJECT (ASSOCREVOLVEDSURFACEACTIONBODY)
  DECODE_UNKNOWN_BITS
  AcDbAssocPathBasedSurfaceActionBody_fields;
  SUBCLASS (AcDbAssocRevolvedSurfaceActionBody)
  FIELD_BL (rsab_status, 90);

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (writedeps, num_deps, 0, 360);
  HANDLE_VECTOR (readdeps, num_deps, 0, 360);
  FIELD_VECTOR_T (descriptions, T, num_deps, 1);
DWG_OBJECT_END

// See AcDbAssocActionBody.h and ASSOCPLANESURFACEACTIONBODY
DWG_OBJECT (ASSOCSWEPTSURFACEACTIONBODY)
  DECODE_UNKNOWN_BITS
  AcDbAssocPathBasedSurfaceActionBody_fields;
  SUBCLASS (AcDbAssocSweptSurfaceActionBody)
  FIELD_BL (ssab_status, 90);

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (writedeps, num_deps, 0, 360);
  HANDLE_VECTOR (readdeps, num_deps, 0, 360);
  FIELD_VECTOR_T (descriptions, T, num_deps, 1);
DWG_OBJECT_END

// DEBUGGING
DWG_OBJECT (EVALUATION_GRAPH)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbEvalGraph)
  FIELD_BL (has_graph, 96);        // 1
  FIELD_BL (unknown1, 97);         // 1
  FIELD_BL (unknown2, 0);          // 1
  FIELD_BL (nodeid, 91);           // 0
  if (FIELD_VALUE (has_graph))
    {
      FIELD_BL (edge_flags, 93);   // 32
      FIELD_BL (num_evalexpr, 95); // 1
      // maybe REPEAT num_evalexpr: edge1-4, evalexpr
      FIELD_BLd (node_edge1, 92);   // -1
      FIELD_BLd (node_edge2, 92);   // -1
      FIELD_BLd (node_edge3, 92);   // -1
      FIELD_BLd (node_edge4, 92);   // -1
      VALUEOUTOFBOUNDS (num_evalexpr, 20)
    }

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (evalexpr, num_evalexpr, 5, 360);
DWG_OBJECT_END

#undef ASSOCACTION_fields
/* dof: 2 remaining degree of freedom */
#define ASSOCACTION_fields                                 \
  SUBCLASS (AcDbAssocAction)                               \
  /* until r2010: 1, 2013+: 2 */                           \
  FIELD_BS (class_version, 90);                            \
  /* 0 WellDefined, 1 UnderConstrained, 2 OverConstrained, \
     3 Inconsistent, 4 NotEvaluated, 5 NotAvailable,       \
     6 RejectedByClient */                                 \
  FIELD_BL (geometry_status, 90); /* 0 */                  \
  FIELD_HANDLE (owningnetwork, 5, 330);                    \
  FIELD_HANDLE (actionbody, 5, 360);                       \
  FIELD_BL (action_index, 90); /* 1 */                     \
  FIELD_BL (max_assoc_dep_index, 90)

// subclass of AcDbAssocAction DEBUGGING
// Object1 --ReadDep--> Action1 --WriteDep1--> Object2 --ReadDep--> Action2 ...
DWG_OBJECT (ASSOCNETWORK)
  DECODE_UNKNOWN_BITS
  ASSOCACTION_fields;

  SUBCLASS (AcDbAssocNetwork)
  FIELD_BL (unknown_n1, 90);
  FIELD_BL (unknown_n2, 90);
  FIELD_BL (num_actions, 90);
  VALUEOUTOFBOUNDS (num_actions, 100)

  START_OBJECT_HANDLE_STREAM;
  HANDLE_VECTOR (actions, num_actions, 5, 330);
DWG_OBJECT_END

// (varies) DEBUGGING
DWG_OBJECT (SUNSTUDY)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbSunStudy)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)
  FIELD_T (setup_name, 1);
  FIELD_T (description, 2);
  FIELD_BL (output_type, 70);
  if (FIELD_VALUE (output_type) == 0) // Sheet_Set
    {
      FIELD_B (use_subset, 290);
      FIELD_T (sheet_set_name, 3);
      FIELD_T (sheet_subset_name, 4);
    }
  FIELD_B (select_dates_from_calendar, 291);
  FIELD_BL (num_dates, 91);
  VALUEOUTOFBOUNDS (num_dates, 10000)
  REPEAT (num_dates, dates, Dwg_SUNSTUDY_Dates)
  REPEAT_BLOCK
      SUB_FIELD_BL (dates[rcount1], julian_day, 90);
      SUB_FIELD_BL (dates[rcount1], msecs, 90);
  END_REPEAT_BLOCK
  END_REPEAT (dates);
  FIELD_B (select_range_of_dates, 292);
  if (FIELD_VALUE (select_range_of_dates))
    {
       FIELD_BL (start_time, 93);
       FIELD_BL (end_time, 94);
       FIELD_BL (interval, 95);
    }
  FIELD_BL (num_hours, 91);
  VALUEOUTOFBOUNDS (num_hours, 10000)
  FIELD_VECTOR (hours, B, num_hours, 290);

  FIELD_BL (shade_plot_type, 74);
  FIELD_BL (numvports, 75);
  FIELD_BL (numrows, 76);
  FIELD_BL (numcols, 77);
  FIELD_BD (spacing, 40);
  FIELD_B (lock_viewports, 293);
  FIELD_B (label_viewports, 294);

  START_OBJECT_HANDLE_STREAM;
  FIELD_HANDLE (page_setup_wizard, 5, 340);
  FIELD_HANDLE (view, 5, 341);
  FIELD_HANDLE (visualstyle, 2, 342);
  FIELD_HANDLE (text_style, 2, 343);

DWG_OBJECT_END

// (varies) UNSTABLE
// in DXF as POSITIONMARKER (rename?, no), command: GEOMARKPOSITION, GEOMARKPOINT
// r2014+
DWG_ENTITY (GEOPOSITIONMARKER)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbGeoPositionMarker)
  FIELD_BL (type, 90); // 0
  FIELD_3BD (position, 10);
  FIELD_BD (radius, 40);
  FIELD_T (notes, 1);
  FIELD_BD (landing_gap, 40);
  FIELD_B (mtext_visible, 290);
  FIELD_RCd (text_alignment, 280); // 0 left, 1 center, 2 right
  FIELD_B (enable_frame_text, 290);
  if (FIELD_VALUE (enable_frame_text))
    {
      DECODER {
        dwg_add_object (dwg);
        _obj->mtext = &dwg->object[dwg->num_objects - 1];
        dwg_setup_MTEXT (_obj->mtext);
      }
      CALL_ENTITY (MTEXT, _obj->mtext);
    }
  COMMON_ENTITY_HANDLE_DATA;
DWG_ENTITY_END

#define SweepOptions_fields  \
  FIELD_BD (draft_angle, 42); \
  FIELD_BD (draft_start_distance, 43); \
  FIELD_BD (draft_end_distance, 44); \
  FIELD_BD (twist_angle, 45); \
  FIELD_BD (scale_factor, 48); \
  FIELD_BD (align_angle, 49); \
  FIELD_VECTOR_N (sweep_entity_transmatrix, BD, 16, 46); \
  FIELD_VECTOR_N (path_entity_transmatrix, BD, 16, 47); \
  FIELD_B (is_solid, 290); \
  FIELD_BS (sweep_alignment_flags, 70); \
  FIELD_BS (path_flags, 71); \
  FIELD_B (align_start, 292); \
  FIELD_B (bank, 293); \
  FIELD_B (base_point_set, 294); \
  FIELD_B (sweep_entity_transform_computed, 295); \
  FIELD_B (path_entity_transform_computed, 296); \
  FIELD_3BD (reference_vector_for_controlling_twist, 11)

// r2007+
DWG_ENTITY (EXTRUDEDSURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  //FIELD_BS (modeler_format_version, 70); //def 1
  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  SUBCLASS (AcDbExtrudedSurface)
#ifdef IS_DXF
  //FIELD_BL (class_version, 90); // or entity type?
  CALL_SUBENT (_obj->entity, 90)
#else
  // here and at SweptSurface
  SweepOptions_fields;
#endif
  FIELD_3BD (sweep_vector, 10);
  FIELD_VECTOR_N (sweep_transmatrix, BD, 16, 40);
#ifdef IS_DXF
  SweepOptions_fields;
#else
  //FIELD_BL (class_version, 90); // or entity type?
  CALL_SUBENT (_obj->entity, 90)
#endif

  COMMON_ENTITY_HANDLE_DATA;
  //FIELD_HANDLE (sweep_entity, 5, 0);
  //FIELD_HANDLE (path_entity, 5, 0);

DWG_ENTITY_END

// r2007+
DWG_ENTITY (LOFTEDSURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  FIELD_BS (modeler_format_version, 70); //def 1
  VALUEOUTOFBOUNDS (modeler_format_version, 3)

  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  SUBCLASS (AcDbLoftedSurface)
  FIELD_VECTOR_N (loft_entity_transmatrix, BD, 16, 40);
  //90 77
  //90 544
  //310
  //90 77
  //90 608
  //310
  //FIELD_BL (class_version, 90);
  FIELD_BL (plane_normal_lofting_type, 70);
  FIELD_BD (start_draft_angle, 41);
  FIELD_BD (end_draft_angle, 42);
  FIELD_BD (start_draft_magnitude, 43);
  FIELD_BD (end_draft_magnitude, 44);
  FIELD_B (arc_length_parameterization, 290);
  FIELD_B (no_twist, 291);
  FIELD_B (align_direction, 292);
  FIELD_B (simple_surfaces, 293);
  FIELD_B (closed_surfaces, 294);
  FIELD_B (solid, 295);
  FIELD_B (ruled_surface, 296);
  FIELD_B (virtual_guide, 297);
  FIELD_BS (num_cross_sections, 0);
  FIELD_BS (num_guide_curves, 0);
  VALUEOUTOFBOUNDS (num_cross_sections, 5000)
  VALUEOUTOFBOUNDS (num_guide_curves, 5000)

  COMMON_ENTITY_HANDLE_DATA;
  HANDLE_VECTOR (cross_sections, num_cross_sections, 5, 310);
  HANDLE_VECTOR (guide_curves, num_guide_curves, 5, 310);
  FIELD_HANDLE (path_curve, 5, 0);

DWG_ENTITY_END

// r2007+
DWG_ENTITY (REVOLVEDSURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  FIELD_BS (modeler_format_version, 70); //def 1

  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  SUBCLASS (AcDbRevolvedSurface)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)

  FIELD_BL (id, 90);
  //FIELD_BL (bindata_size, 90);
  //FIELD_BINARY (bindata, FIELD_VALUE (bindata_size), 310);
  FIELD_3BD (axis_point, 10);
  FIELD_3BD (axis_vector, 11);
  FIELD_BD (revolve_angle, 40);
  FIELD_BD (start_angle, 41);
  FIELD_VECTOR_N (revolved_entity_transmatrix, BD, 16, 42);
  FIELD_BD (draft_angle, 43);
  FIELD_BD (draft_start_distance, 44);
  FIELD_BD (draft_end_distance, 45);
  FIELD_BD (twist_angle, 46);
  FIELD_B (solid, 290);
  FIELD_B (close_to_axis, 291);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

DWG_ENTITY (SWEPTSURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  FIELD_BS (modeler_format_version, 70); //def 1

  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  SUBCLASS (AcDbSweptSurface)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)

  FIELD_BL (sweep_entity_id, 90);
#ifndef IS_JSON
  FIELD_BL (sweepdata_size, 90);
#endif
  VALUEOUTOFBOUNDS (sweepdata_size, 5000)
  FIELD_BINARY (sweepdata, FIELD_VALUE (sweepdata_size), 310);
  FIELD_BL (path_entity_id, 90);
#ifndef IS_JSON
  FIELD_BL (pathdata_size, 90);
#endif
  VALUEOUTOFBOUNDS (pathdata_size, 5000)
  FIELD_BINARY (pathdata, FIELD_VALUE (pathdata_size), 310);
  // here and at ExtrudedSurface
  SweepOptions_fields;

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

// missing coverage
DWG_ENTITY (NURBSURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  FIELD_BS (modeler_format_version, 70); //def 1
  //FIELD_BL (bindata_size, 90);
  //FIELD_TF (bindata, FIELD_VALUE (bindata_size), 1); // in DXF as encrypted ASCII

  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  //SUBCLASS (AcDbNurbSurface)
  //FIELD_BL (class_version, 90);
  //if (FIELD_VALUE (class_version) > 10)
  //  return DWG_ERR_VALUEOUTOFBOUNDS;

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END


DWG_ENTITY (PLANESURFACE)

  DECODE_UNKNOWN_BITS
  ACTION_3DSOLID;
  FIELD_BS (modeler_format_version, 70); //def 1
  //FIELD_BL (bindata_size, 90);
  //FIELD_TF (bindata, FIELD_VALUE (bindata_size), 1); // in DXF as encrypted ASCII

  SUBCLASS (AcDbSurface)
  FIELD_BS (u_isolines, 71);
  FIELD_BS (v_isolines, 72);
  //SUBCLASS (AcDbPlaneSurface)
  //FIELD_BL (class_version, 90);
  //if (FIELD_VALUE (class_version) > 10)
  //  return DWG_ERR_VALUEOUTOFBOUNDS;

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

// (varies) DEBUGGING
// call as dwg_##action_ASSOCACTION_private
DWG_OBJECT (ASSOCACTION)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocAction)
  /* until r2010: 1, 2013+: 2 */
  FIELD_BS (class_version, 90);
  FIELD_BL (geometry_status, 90); /* 0 */
  FIELD_HANDLE (owningnetwork, 5, 330);
  FIELD_HANDLE (actionbody, 4, 360);
  FIELD_BL (action_index, 90);
  FIELD_BL (max_assoc_dep_index, 90);
  FIELD_BL (num_deps, 90);
  REPEAT (num_deps, deps, Dwg_ASSOCACTION_Deps)
  REPEAT_BLOCK
  {
    int dxf = _obj->deps[rcount1].is_soft ? 360 : 330;
    int code = _obj->deps[rcount1].is_soft ? DWG_HDL_SOFTPTR : DWG_HDL_HARDPTR;
    SUB_FIELD_B (deps[rcount1], is_soft, 0);
    SUB_FIELD_HANDLE (deps[rcount1], dep, code, dxf);
  }
  END_REPEAT_BLOCK
  END_REPEAT (deps);
  if (FIELD_VALUE (class_version) > 1)
  {
    VALUE_BS (0, 90);
    FIELD_BL (num_owned_params, 90);
    HANDLE_VECTOR (owned_params, num_owned_params, DWG_HDL_SOFTPTR, 360);
    VALUE_BS (0, 90);
    FIELD_BL (num_owned_value_param_names, 90); // TODO which hdl_code?
    HANDLE_VECTOR (owned_value_param_names, num_owned_value_param_names, 5, 360);
  }
DWG_OBJECT_END

// DEBUGGING
DWG_OBJECT (ASSOCOSNAPPOINTREFACTIONPARAM)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocActionParam)
  FIELD_B  (unknown1, 0); //
  FIELD_RC (unknown, 0); //01010101
  FIELD_T (name, 1); //@9-10
  DEBUG_HERE_OBJ
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
  FIELD_BS (status, 90); //0
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
  //DEBUG_HERE_OBJ
  SUBCLASS (AcDbAssocCompoundActionParam)
  FIELD_BD (unknown3, 40); //-1 32-97
  FIELD_BS (flags, 90); //0 read/write deps
  //...
  DEBUG_HERE_OBJ
  FIELD_BS (num_actions, 90); //1
  VALUEOUTOFBOUNDS (num_actions, 1000)
  DEBUG_HERE_OBJ

  bit_advance_position (dat, 122-118);
  START_OBJECT_HANDLE_STREAM;
  DEBUG_POS_OBJ
  FIELD_HANDLE (writedep, ANYCODE, 360); //122-129
  bit_advance_position (dat, 168-130);
  DEBUG_POS_OBJ
  HANDLE_VECTOR (actions, num_actions, 4, 330);
DWG_OBJECT_END

//??
DWG_OBJECT (ASSOCVERTEXACTIONPARAM)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocActionParam)
  FIELD_B  (unknown1, 0); //
  FIELD_RC (unknown, 0); //01010101
  FIELD_T (name, 1); //@9-10
  DEBUG_HERE_OBJ
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
  FIELD_BS (status, 90); //0
  FIELD_B  (unknown1, 0); //
  DEBUG_HERE_OBJ
DWG_OBJECT_END

// (varies)
// works ok on all example_20* but this coverage seems limited
// The static variant
DWG_OBJECT (PERSUBENTMGR)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbPersSubentManager)
  FIELD_BL (class_version, 90); //2
  VALUEOUTOFBOUNDS (class_version, 3)
  FIELD_BL (unknown_0, 90); //always 0
  FIELD_BL (unknown_2, 90); //always 2

  FIELD_BL (numassocsteps, 90);  //3
  FIELD_BL (numassocsubents, 90);//0
  FIELD_BL (num_steps, 90);      //1
  FIELD_VECTOR (steps, BL, num_steps, 90); //1
  FIELD_BL (num_subents, 90);
  // nope: 3x BL and CALL_SUBENT
  FIELD_VECTOR (subents, BL, num_subents, 90);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// See AcDbAssocPersSubentIdPE.h
// The dynamic variant
DWG_OBJECT (ASSOCPERSSUBENTMANAGER)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbAssocPersSubentManager)
  FIELD_BL (class_version, 90); //1 or 2 (r2013+)
  FIELD_BL (unknown_3, 90); //3
  FIELD_BL (unknown_0, 90); //0
  FIELD_BL (unknown_2, 90); //2

  FIELD_BL (num_steps, 90);   //3
  FIELD_VECTOR (steps, BL, num_steps, 90);
  FIELD_BL (num_subents, 90);
  // TODO subent struct
  FIELD_BL (unknown_bl6, 90); //5
  FIELD_BL (unknown_bl6a, 90); //0 10 0100000100 0100000011
  FIELD_BL (unknown_bl7a, 90); //4
  FIELD_BL (unknown_bl7, 90); //3 0b0100000011
  FIELD_BL (unknown_bl7, 90); //2
  FIELD_BL (unknown_bl8, 90); //2
  FIELD_BL (unknown_bl9, 90); //2
  FIELD_BL (unknown_bl10, 90); //21
  FIELD_BL (unknown_bl11, 90); //0
  FIELD_BL (unknown_bl12, 90); //0
  FIELD_BL (unknown_bl13, 90); //0
  FIELD_BL (unknown_bl14, 90); //0
  FIELD_BL (unknown_bl15, 90); //1 [[133,142]]
  FIELD_BL (unknown_bl16, 90); //3
  FIELD_BL (unknown_bl17, 90); //1
  FIELD_BL (unknown_bl18, 90); //1000000000
  FIELD_BL (unknown_bl19, 90); //1001
  FIELD_BL (unknown_bl20, 90); //1
  FIELD_BL (unknown_bl21, 90); //1000000000
  FIELD_BL (unknown_bl22, 90); //51001
  FIELD_BL (unknown_bl23, 90); //1
  FIELD_BL (unknown_bl24, 90); //1000000000
  FIELD_BL (unknown_bl25, 90); //351001
  FIELD_BL (unknown_bl26, 90); //0
  FIELD_BL (unknown_bl27, 90); //0
  FIELD_BL (unknown_bl28, 90); //0
  FIELD_BL (unknown_bl29, 90); //900
  FIELD_BL (unknown_bl30, 90); //0
  FIELD_BL (unknown_bl31, 90); //900
  FIELD_BL (unknown_bl32, 90); //0
  FIELD_BL (unknown_bl33, 90); //2
  FIELD_BL (unknown_bl34, 90); //2
  FIELD_BL (unknown_bl35, 90); //3 0100000011
  FIELD_BL (unknown_bl36, 90); //0
  FIELD_B  (unknown_b37, 290); //0

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// Class AcDbAssoc2dConstraintGroup
// see https://help.autodesk.com/view/OARX/2018/ENU/?guid=OREF-AcDbAssoc2dConstraintGroup
DWG_OBJECT (ASSOC2DCONSTRAINTGROUP)
  DECODE_UNKNOWN_BITS
  ASSOCACTION_fields;

  SUBCLASS (AcDbAssocNetwork)
  FIELD_BL (l5, 90); //2
  FIELD_B (b1, 70);  //0
  FIELD_3BD (workplane[0], 10); // 0,0,0
  FIELD_3BD (workplane[1], 10); // 1,0,0
  FIELD_3BD (workplane[2], 10); // 0,1,0
  FIELD_HANDLE (h1, 0, 360);
  FIELD_BL (num_actions, 90); //2
  HANDLE_VECTOR (actions, num_actions, 0, 360);
  FIELD_BL (l7, 90); //9
  FIELD_BL (l8, 90); //9

  FIELD_T (t1, 1);
  //DXF { FIELD_TFF ("AcConstrainedCircle", 1); }
  FIELD_HANDLE (h2, 0, 330);
  FIELD_BL (cl1, 90); //1
  FIELD_RC (cs1, 70); //1
  FIELD_BL (cl2, 90); //1
  FIELD_BL (cl3, 90); //3
  FIELD_HANDLE (h3, 0, 330);
  FIELD_BL (cl4, 90); //0
  FIELD_3BD (c1, 10); // @133
  FIELD_3BD (c2, 10);
  FIELD_3BD (c3, 10);
  FIELD_BD (w1, 40); // @279
  FIELD_BD (w2, 40);
  FIELD_BD (w3, 40);

  FIELD_T (t2, 1);
  //DXF { FIELD_TFF ("AcConstrainedImplicitPoint", 1); }
  // ...
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

#define AcDbShSubentMaterial_fields                                           \
    SUBCLASS (AcDbShSubentMaterial)                                           \
    FIELD_BL (material.major, 90);                                            \
    FIELD_BL (material.minor, 91);                                            \
    FIELD_BL (material.reflectance, 92);                                      \
    FIELD_BL (material.displacement, 93);                                     \
    FIELD_HANDLE (material.material, 5, 331)

#define AcDbShSubentColor_fields                                              \
    SUBCLASS (AcDbShSubentColor)                                              \
    FIELD_BL (color.major, 90); /* 33 */                                      \
    FIELD_BL (color.minor, 91); /* 1 */                                       \
    FIELD_BL (color.transparency, 92);                                        \
    FIELD_BL (color.bl93, 93);                                                \
    FIELD_BL (color.is_face_variable, 290);                                   \
    FIELD_CMC (color.color,62)

#define CLASS_HAS(x) 1

// Class AcDbSweepOptions? DEBUGGING
// dbSweepOptions.h dbsurf.h
DWG_OBJECT (ACSH_SWEEP_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShSweepBase)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_3BD (direction, 10); //0,0,0
  // sweep_options
  // sweep_entity
  // path_entity
  FIELD_BL (bl92, 92); //77
#ifndef IS_JSON
  FIELD_BL (shsw_text_size, 90); //744
#endif
  FIELD_BINARY (shsw_text, FIELD_VALUE (shsw_text_size), 310);
  FIELD_BL (shsw_bl93, 93); //77
#ifndef IS_JSON
  FIELD_BL (shsw_text2_size, 90); //480
#endif
  FIELD_BINARY (shsw_text2, FIELD_VALUE (shsw_text2_size), 310);
  FIELD_BD (draft_angle, 42); //0.0
  FIELD_BD (start_draft_dist, 43); //0.0
  FIELD_BD (end_draft_dist, 44); //0.0
  FIELD_BD (scale_factor, 45); //1.0
  FIELD_BD (twist_angle, 48); //0.0
  FIELD_BD (align_angle, 49); //0.0
  FIELD_VECTOR_N (sweepentity_transform, BD, 16, 46);
  FIELD_VECTOR_N (pathentity_transform, BD, 16, 47);
  FIELD_RC (align_option, 70); //2
  FIELD_RC (miter_option, 71); //2
  FIELD_B (has_align_start, 290); //1
  FIELD_B (bank, 292); //1
  FIELD_B (check_intersections, 293); //0
  FIELD_B (shsw_b294, 294); //1
  FIELD_B (shsw_b295, 295); //1
  FIELD_B (shsw_b296, 296); //1
  FIELD_3BD (pt2, 11); //0,0,0

  SUBCLASS (AcDbShSweep)
  // align_option
  // miter_option

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_EXTRUSION_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShSweepBase)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_3BD (direction, 10); //0,0,0
  // sweep_options
  // sweep_entity
  // path_entity
  FIELD_BL (bl92, 92); //77
#ifndef IS_JSON
  FIELD_BL (shsw_text_size, 90); //744
#endif
  FIELD_BINARY (shsw_text, FIELD_VALUE (shsw_text_size), 310);
  FIELD_BL (shsw_bl93, 93); //77
#ifndef IS_JSON
  FIELD_BL (shsw_text2_size, 90); //480
#endif
  FIELD_BINARY (shsw_text2, FIELD_VALUE (shsw_text2_size), 310);
  FIELD_BD (draft_angle, 42); //0.0
  FIELD_BD (start_draft_dist, 43); //0.0
  FIELD_BD (end_draft_dist, 44); //0.0
  FIELD_BD (scale_factor, 45); //1.0
  FIELD_BD (twist_angle, 48); //0.0
  FIELD_BD (align_angle, 49); //0.0
  FIELD_VECTOR_N (sweepentity_transform, BD, 16, 46);
  FIELD_VECTOR_N (pathentity_transform, BD, 16, 47);
  FIELD_RC (align_option, 70); //2
  FIELD_RC (miter_option, 71); //2
  FIELD_B (has_align_start, 290); //1
  FIELD_B (bank, 292); //1
  FIELD_B (check_intersections, 293); //0
  FIELD_B (shsw_b294, 294); //1
  FIELD_B (shsw_b295, 295); //1
  FIELD_B (shsw_b296, 296); //1
  FIELD_3BD (pt2, 11); //0,0,0

  SUBCLASS (AcDbShExtrusion)

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_HISTORY_CLASS)
  DECODE_UNKNOWN_BITS
#ifndef IS_DXF
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
#endif
  SUBCLASS (AcDbShHistory)
  FIELD_BL (major, 90);
  FIELD_BL (minor, 91);
  FIELD_HANDLE (owner, 2, 360);
  FIELD_BL (h_nodeid, 92);
  FIELD_B (b280, 280);
  FIELD_B (b281, 281);
#ifdef IS_DXF
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
#endif
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_LOFT_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShLoft)
  FIELD_BL (major, 90);
  FIELD_BL (minor, 91);
  FIELD_BL (num_crosssects, 92);
  REPEAT (num_crosssects, crosssects, BITCODE_H)
  REPEAT_BLOCK
  {
    CALL_SUBENT (_obj->crosssects[rcount1], 93);
  }
  END_REPEAT_BLOCK
  END_REPEAT (crosssects);

  FIELD_BL (num_guides, 95);
  REPEAT (num_guides, guides, BITCODE_H)
  REPEAT_BLOCK
  {
    CALL_SUBENT (_obj->guides[rcount1], 96);
  }
  END_REPEAT_BLOCK
  END_REPEAT (guides);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACSH_REVOLVE_CLASS)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  AcDbShHistoryNode_fields;
  SUBCLASS (AcDbShPrimitive)
  SUBCLASS (AcDbShRevolve)
  FIELD_BL (major, 90); //33
  FIELD_BL (minor, 91); //29
  FIELD_3BD (axis_pt, 10);
  FIELD_2RD (direction, 11); // 3d in dxf
  FIELD_BD (revolve_angle, 40);
  FIELD_BD (start_angle, 41);
  FIELD_BD (draft_angle, 43);
  FIELD_BD (bd44, 44);
  FIELD_BD (bd45, 45);
  FIELD_BD (twist_angle, 46);
  FIELD_B (b290, 290);
  FIELD_B (is_close_to_axis, 291);
  CALL_SUBENT (obj->sweep_entity, 90);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// called COORDINATION_MODEL in the DXF docs
DWG_ENTITY (NAVISWORKSMODEL)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbNavisworksModel)
  DEBUG_HERE_OBJ
  FIELD_HANDLE (defhandle, 2, 340);
  FIELD_VECTOR_N (transmatrix, BD, 16, 40);
  FIELD_BD (unitfactor, 40);

  COMMON_ENTITY_HANDLE_DATA;

DWG_ENTITY_END

// (varies) TODO
// no coverage. Stored in ACAD_BIM_DEFINITIONS dictionary
DWG_OBJECT (NAVISWORKSMODELDEF)

  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbNavisworksModelDef)
  DEBUG_HERE_OBJ
  FIELD_T (path, 1);
  FIELD_B (status, 290);
  FIELD_3BD (min_extent, 10);
  FIELD_3BD (max_extent, 11);
  FIELD_B (host_drawing_visibility, 290);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// officially documented, dbRender.h
// ACAD_RENDER_ENVIRONMENT
DWG_OBJECT (RENDERENVIRONMENT)
  DECODE_UNKNOWN_BITS

  SUBCLASS (AcDbRenderEnvironment)
  DEBUG_HERE_OBJ
  FIELD_BL (class_version, 90);     /*!< default 1 */
  FIELD_B (fog_enabled, 290);
  FIELD_B (fog_background_enabled, 290);
  FIELD_CMC (fog_color, 280);
  FIELD_BD (fog_density_near, 40); /* default 100.0 (opaque fog) */
  FIELD_BD (fog_density_far, 40);
  FIELD_BD (fog_distance_near, 40); /* default 100.0 (at the far clipping plane) */
  FIELD_BD (fog_distance_far, 40);
  FIELD_B (environ_image_enabled, 290);
  FIELD_T (environ_image_filename, 1);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// officially documented, dbRender.h
DWG_OBJECT (RENDERGLOBAL)
  DECODE_UNKNOWN_BITS

  SUBCLASS (AcDbRenderGlobal)
  DEBUG_HERE_OBJ
  FIELD_BL (class_version, 90);     /*!< default 2 */
  FIELD_BL (procedure, 90);         /*!< 0 view, 1 crop, 2 selection */
  FIELD_BL (destination, 90);       /*!< 0 window, 1 viewport */
  FIELD_B (save_enabled, 290);
  FIELD_T (save_filename, 1);
  FIELD_BL (image_width, 90);
  FIELD_BL (image_height, 90);
  FIELD_B (predef_presets_first, 290);
  FIELD_B (highlevel_info, 290);

  START_OBJECT_HANDLE_STREAM;

DWG_OBJECT_END

// LiveMap raster image underlay r2015+
DWG_OBJECT (GEOMAPIMAGE)
  DECODE_UNKNOWN_BITS

  //SUBCLASS (AcDbImage)
  //SUBCLASS (AcDbRasterImage)
  SUBCLASS (AcDbGeomapImage)
  FIELD_BL (class_version, 90);
  VALUEOUTOFBOUNDS (class_version, 10)
  FIELD_3DPOINT (pt0, 10);
  //FIELD_3DPOINT (uvec, 11);
  //FIELD_3DPOINT (vvec, 12);
  FIELD_2RD (size, 13);
  FIELD_BS (display_props, 70);
  FIELD_B (clipping, 280); // i.e. clipping_enabled
  FIELD_RC (brightness, 281);
  FIELD_RC (contrast, 282);
  FIELD_RC (fade, 283);

/* VBA props:
origin
  FIELD_BD (rotation, 0);
image_width
image_height
name
image_file
image_visibility
transparency
height
width
  FIELD_B (show_rotation, 0);
  FIELD_BD (scale_factor, 0);
geoimage_brightness
geoimage_contrast
geoimage_fade
geoimage_position
geoimage_width
geoimage_height
*/
DWG_OBJECT_END

#define AcDbObjectContextData_fields                                    \
  SUBCLASS (AcDbObjectContextData);                                     \
  FIELD_BS (class_version, 70);                                         \
  FIELD_B (is_default, 290);                                            \
  FIELD_B (in_dwg, 0)

#define AcDbAnnotScaleObjectContextData_fields                          \
  AcDbObjectContextData_fields;                                         \
  SUBCLASS (AcDbAnnotScaleObjectContextData);                           \
  FIELD_HANDLE (scale, 2, 340)

// DXF: 2 293 10 294 140 298 291 70 292 71 280 295 296 297
//  #ifdef IS_DXF
//    FIELD_HANDLE_NAME (block, 2, BLOCK_HEADER);
#define AcDbDimensionObjectContextData_fields           \
  SUBCLASS (AcDbDimensionObjectContextData);            \
  DXF { FIELD_HANDLE (dimension.block, 5, 2); }         \
  DXF { FIELD_B (dimension.b293, 293); }                \
  FIELD_2RD (dimension.def_pt, 10); /* text location */ \
  DXF { VALUE_RD (0.0, 30); }                           \
  FIELD_B (dimension.is_def_textloc, 294); /* 1 */      \
  FIELD_BD (dimension.text_rotation, 140);              \
  FIELD_HANDLE (dimension.block, 5, 0);                 \
  FIELD_B (dimension.b293, 0);                          \
  FIELD_B (dimension.dimtofl, 298);                     \
  FIELD_B (dimension.dimosxd, 291);                     \
  FIELD_B (dimension.dimatfit, 70);                     \
  FIELD_B (dimension.dimtix, 292);                      \
  FIELD_B (dimension.dimtmove, 71);                     \
  FIELD_RC (dimension.override_code, 280);              \
  FIELD_B (dimension.has_arrow2, 295);                  \
  FIELD_B (dimension.flip_arrow2, 296);                 \
  FIELD_B (dimension.flip_arrow1, 297)

DWG_OBJECT (ALDIMOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbAlignedDimensionObjectContextData)
  FIELD_3BD (dimline_pt, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ANGDIMOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbAngularDimensionObjectContextData)
  FIELD_3BD (arc_pt, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (DMDIMOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbDiametricDimensionObjectContextData)
  FIELD_3BD (first_arc_pt, 11);
  FIELD_3BD (def_pt, 12);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ORDDIMOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbOrdinateDimensionObjectContextData)
  FIELD_3BD (feature_location_pt, 11); // = origin
  FIELD_3BD (leader_endpt, 12);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (RADIMOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbRadialDimensionObjectContextData)
  FIELD_3BD (first_arc_pt, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (RADIMLGOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  AcDbDimensionObjectContextData_fields;
  SUBCLASS (AcDbRadialDimensionLargeObjectContextData)
  FIELD_3BD (ovr_center, 12);
  FIELD_3BD (jog_point, 13);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (BLKREFOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbBlkrefObjectContextData);
  FIELD_BD (rotation, 50)
  FIELD_3BD (insertion_pt, 10);
  FIELD_3BD_1 (scale_factor, 42);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// TOLERANCE
DWG_OBJECT (FCFOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbFcfObjectContextData)
  FIELD_3BD (location, 10);
  FIELD_3BD (horiz_dir, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (LEADEROBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbLeaderObjectContextData)
  FIELD_BL (num_points, 70); /* 3 */
  FIELD_3DPOINT_VECTOR (points, num_points, 10);
  FIELD_3DPOINT (x_direction, 11);
  FIELD_B (b290, 290); /* 1 */
  FIELD_3DPOINT (inspt_offset, 12);
  FIELD_3DPOINT (endptproj, 13);

  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (MLEADEROBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbMLeaderObjectContextData)
  // ?? ...
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (TEXTOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbTextObjectContextData)
  FIELD_BS (flag, 70); // 0
  FIELD_BD (rotation, 50); // 0.0 or 90.0
  FIELD_2RD (insertion_pt, 10);
  FIELD_2RD (alignment_pt, 11);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (MTEXTATTRIBUTEOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbMTextAttributeObjectContextData)
  // ?? ...
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (MTEXTOBJECTCONTEXTDATA)
  DECODE_UNKNOWN_BITS
  AcDbAnnotScaleObjectContextData_fields;
  SUBCLASS (AcDbMTextObjectContextData)
  FIELD_BS (flag, 70); // 6
  FIELD_3RD (insertion_pt, 11);
  FIELD_3RD (x_axis_dir, 10);
  FIELD_BD (text_height, 40);
  FIELD_BD (rect_width, 41);
  FIELD_BD (extents_width, 42);
  FIELD_BD (extents_height, 43);
  FIELD_BS (attachment, 71); // or column_type?
  if (FIELD_VALUE (attachment))
    {
      FIELD_BS (drawing_dir, 72);
      FIELD_BS (linespace_style, 73);
      FIELD_BD (linespace_factor, 44);
      FIELD_BD (bd45, 45);
      FIELD_BS (bs74, 74);
      FIELD_BD (rect_height, 46);
    }
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// (varies) TODO
DWG_OBJECT (DATATABLE)
  DECODE_UNKNOWN_BITS
#ifdef IS_DXF
  UNTIL (R_2000) {
    SUBCLASS (ACDBDATABLE)
  } LATER_VERSIONS {
    SUBCLASS (AcDbDataTable)
  }
#endif
  DEBUG_HERE_OBJ
  FIELD_BS (flags, 70);
  FIELD_BL (num_cols, 90);
  FIELD_BL (num_rows, 91);
  FIELD_T (table_name, 1);
  REPEAT (num_cols, cols, Dwg_DATATABLE_column)
  REPEAT_BLOCK
      SUB_FIELD_BL (cols[rcount1],type, 92);
      SUB_FIELD_T (cols[rcount1],text, 2);

      REPEAT2 (num_rows, cols[rcount1].rows, Dwg_DATATABLE_row) //CellType?
      REPEAT_BLOCK
          // almost like Dwg_TABLE_value
          //switch case 1:
          SUB_FIELD_BL (cols[rcount1].rows[rcount2],value.data_long, 93);
          //switch case 2:
          SUB_FIELD_BD (cols[rcount1].rows[rcount2],value.data_double, 40);
          //switch case 3:
          SUB_FIELD_T (cols[rcount1].rows[rcount2],value.data_string, 3);
      END_REPEAT_BLOCK
      SET_PARENT_OBJ (cols[rcount1].rows);
      END_REPEAT (cols[rcount1].rows)
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (cols);
  END_REPEAT (cols)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (DATALINK)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbDataLink)
  FIELD_T (data_adapter, 1);
  FIELD_T (description, 300);
  FIELD_T (tooltip, 301);
  FIELD_T (connection_string, 302);
  FIELD_BL (option, 90); // 2
  FIELD_BL (update_option, 91); // 1179649
  FIELD_BL (bl92, 92); // 1
  FIELD_BS (year, 170);
  FIELD_BS (month, 171);
  FIELD_BS (day, 172);
  FIELD_BS (hour, 173);
  FIELD_BS (minute, 174);
  FIELD_BS (seconds, 175);
  FIELD_BS (msec, 176);
  FIELD_BS (path_option, 177); // 1
  FIELD_BL (bl93, 93); // 0
  FIELD_T (update_status, 304);
  FIELD_BL (num_customdata, 94); // 2
  DXF { VALUE_TFF ("CUSTOMDATA", 305); }
  DEBUG_HERE_OBJ
  DXF { VALUE_TFF ("DATAMAP_BEGIN", 1); }
  REPEAT (num_customdata, customdata, Dwg_DATALINK_customdata)
  REPEAT_BLOCK
      SUB_FIELD_HANDLE (customdata[rcount1],target, DWG_HDL_HARDOWN, 330);
      // ACEXCEL_UPDATEOPTIONS, ACEXCEL_CONNECTION_STRING, ACEXCEL_SOURCEDATA
      SUB_FIELD_T (customdata[rcount1],text, 304);
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (customdata);
  END_REPEAT (customdata)
  DXF { VALUE_TFF ("DATAMAP_END", 309); }
  FIELD_HANDLE (hardowner, DWG_HDL_HARDOWN, 360);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

#endif /* DEBUG_CLASS || IS_FREE */

DWG_OBJECT (DETAILVIEWSTYLE)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbModelDocViewStyle)
  FIELD_BS (class_version, 70); // 0
  FIELD_T (desc, 3);
  FIELD_B (is_modified_for_recompute, 290);
  SINCE (R_2018) {
    FIELD_T (display_name, 300);
    FIELD_BL (viewstyle_flags, 90);
  }

  SUBCLASS (AcDbDetailViewStyle)
  FIELD_BS (class_version, 70); // 0
  DXF { VALUE_BS (0, 71); }
  FIELD_BL (flags, 90);
  DXF { VALUE_BS (1, 71); }
  FIELD_HANDLE (identifier_style, 5, 340); // textstyle
  FIELD_CMC (identifier_color, 62); // in dxf all colors only r2004+
  FIELD_BD (identifier_height, 40); // 5.0
  DXF {
    FIELD_HANDLE (arrow_symbol, 5, 340);
    FIELD_CMC (arrow_symbol_color, 62);
    FIELD_BD (arrow_symbol_size, 40);
  }
  FIELD_T (identifier_exclude_characters, 300);
  FIELD_BD (identifier_offset, 40);
  FIELD_RC (identifier_placement, 280);
  FIELD_HANDLE (arrow_symbol, 5, 0);
  FIELD_CMC (arrow_symbol_color, 0);
  FIELD_BD (arrow_symbol_size, 0);
  DXF { VALUE_BS (2, 71); }
  FIELD_HANDLE (boundary_ltype, 5, 340); // ltype
  FIELD_BLd (boundary_linewt, 90);
  FIELD_CMC (boundary_line_color, 62);
  DXF { VALUE_BS (3, 71); }
  FIELD_HANDLE (viewlabel_text_style, 5, 340); // textstyle
  FIELD_CMC (viewlabel_text_color, 62);
  FIELD_BD (viewlabel_text_height, 40);
  FIELD_BL (viewlabel_attachment, 90);
  FIELD_BD (viewlabel_offset, 40);
  FIELD_BL (viewlabel_alignment, 90);
  FIELD_T (viewlabel_pattern, 300);
  DXF { VALUE_BS (4, 71); }
  FIELD_HANDLE (connection_ltype, 5, 340); // ltype
  FIELD_BLd (connection_linewt, 90);
  FIELD_CMC (connection_line_color, 62);
  FIELD_HANDLE (borderline_ltype, 5, 340);
  FIELD_BLd (borderline_linewt, 90);
  FIELD_CMC (borderline_color, 62);
  FIELD_RC (model_edge, 280); // type, origin, direction
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// subclass: VIEWSTYLE_ModelDoc => "AcDbModelDocViewStyle"
DWG_OBJECT (SECTIONVIEWSTYLE)
  //DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbModelDocViewStyle)
  FIELD_BS (class_version, 70); // 0
  FIELD_T (desc, 3);
  FIELD_B (is_modified_for_recompute, 290);
  SINCE (R_2018) {
    FIELD_T (display_name, 300);
    FIELD_BL (viewstyle_flags, 90);
  }

  SUBCLASS (AcDbSectionViewStyle)
  FIELD_BS (class_version, 70); // 0
  DXF { VALUE_BS (0, 71); }
  FIELD_BL (flags, 90); // 102
  DXF { VALUE_BS (1, 71); }
  FIELD_HANDLE (identifier_style, 5, 340); // textstyle
  FIELD_CMC (identifier_color, 62); // in dxf all colors only r2004+
  FIELD_BD (identifier_height, 40); // 5.0
  FIELD_HANDLE (arrow_start_symbol, 5, 340);
  FIELD_HANDLE (arrow_end_symbol, 5, 340);
  FIELD_CMC (arrow_symbol_color, 62);
  FIELD_BD (arrow_symbol_size, 40);
  FIELD_T (identifier_exclude_characters, 300); // I, O, Q, S, X, Z
  DXF {
    FIELD_BLd (identifier_position, 90);
    FIELD_BD (identifier_offset, 40);
    FIELD_BLd (arrow_position, 90);
    VALUE_BS (2, 71);
  }
  FIELD_BD (arrow_symbol_extension_length, 0);
  FIELD_HANDLE (plane_ltype, 5, 340); // ltype
  FIELD_BLd (plane_linewt, 90);
  FIELD_CMC (plane_line_color, 62);
  FIELD_HANDLE (bend_ltype, 5, 340); // ltype
  FIELD_BLd (bend_linewt, 90);
  FIELD_CMC (bend_line_color, 62);
  FIELD_BD (bend_line_length, 40);
  DXF {
    FIELD_BD (end_line_overshoot, 40);
  }
  FIELD_BD (end_line_length, 40);
  DXF { VALUE_BS (3, 71); }
  FIELD_HANDLE (viewlabel_text_style, 5, 340); // textstyle
  FIELD_CMC (viewlabel_text_color, 62);
  FIELD_BD (viewlabel_text_height, 40);
  FIELD_BL (viewlabel_attachment, 90);
  FIELD_BD (viewlabel_offset, 40); // 5.0
  FIELD_BL (viewlabel_alignment, 90);
  FIELD_T (viewlabel_pattern, 300);
  DXF { VALUE_BS (4, 71); }
  FIELD_CMC (hatch_color, 62);
  FIELD_CMC (hatch_bg_color, 62);
  FIELD_T (hatch_pattern, 300);
  FIELD_BD (hatch_scale, 40);
  FIELD_BLd (hatch_transparency, 90);
  FIELD_B (unknown_b1, 290);
  FIELD_B (unknown_b2, 290);
  FIELD_BLd (identifier_position, 0);
  FIELD_BD (identifier_offset, 0);
  FIELD_BLd (arrow_position, 0);
  FIELD_BD (end_line_overshoot, 0);
  FIELD_BL (num_hatch_angles, 90);
  FIELD_VECTOR (hatch_angles, BD, num_hatch_angles, 40);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (BACKGROUND)
  DECODE_UNKNOWN_BITS
  FIELD_BL (class_version, 90); // 1 or 2
  DECODER { // subytped by dxfname
    decode_BACKGROUND_type (obj);
  }
  switch (FIELD_VALUE (type))
  {
  case Dwg_BACKGROUND_type_Sky:
    SUBCLASS (AcDbSkyBackground);
    FIELD_HANDLE (u.sky.sunid, 5, 340);
    break;
  case Dwg_BACKGROUND_type_Image:
    SUBCLASS (AcDbImageBackground)
    FIELD_T (u.image.filename, 300);
    FIELD_B (u.image.fit_to_screen, 290);
    FIELD_B (u.image.maintain_aspect_ratio, 291);
    FIELD_B (u.image.use_tiling, 292);
    FIELD_2BD_1 (u.image.offset, 140);
    FIELD_2BD_1 (u.image.scale, 142);
    break;
  case Dwg_BACKGROUND_type_Solid:
    SUBCLASS (AcDbSolidBackground)
    FIELD_BLx (u.solid.color, 90);
    break;
  case Dwg_BACKGROUND_type_IBL:
    SUBCLASS (AcDbIBLBackground)
    FIELD_B (u.ibl.enable, 290);
    FIELD_T (u.ibl.name, 1);
    FIELD_BD (u.ibl.rotation, 40);
    FIELD_B (u.ibl.display_image, 290);
    FIELD_HANDLE (u.ibl.secondary_background, 5, 340);
    break;
  case Dwg_BACKGROUND_type_GroundPlane:
    SUBCLASS (AcDbGroundPlaneBackground)
    // all rgb's with method c2
    FIELD_BLx (u.ground_plane.color_sky_zenith, 90);
    FIELD_BLx (u.ground_plane.color_sky_horizon, 91);
    FIELD_BLx (u.ground_plane.color_underground_horizon, 92);
    FIELD_BLx (u.ground_plane.color_underground_azimuth, 93);
    FIELD_BLx (u.ground_plane.color_near, 94);
    FIELD_BLx (u.ground_plane.color_far, 95);
    break;
  case Dwg_BACKGROUND_type_Gradient:
    SUBCLASS (AcDbGradientBackground)
    // all rgb's with method c2
    FIELD_BLx (u.gradient.color_top, 90);
    FIELD_BLx (u.gradient.color_middle, 91);
    FIELD_BLx (u.gradient.color_bottom, 92);
    FIELD_BD (u.gradient.horizon, 140);
    FIELD_BD (u.gradient.height, 141);
    FIELD_BD (u.gradient.rotation, 142);
    break;
  default:
    LOG_ERROR ("Invalid BACKGROUND.type %d", _obj->type)
    break;
  }
DWG_OBJECT_END

#if defined (DEBUG_CLASSES) || defined (IS_FREE)

DWG_OBJECT (LAYOUTPRINTCONFIG)
  DECODE_UNKNOWN_BITS
  SUBCLASS (CAcLayoutPrintConfig)
  FIELD_BS (class_version, 0);
  DEBUG_HERE_OBJ
  FIELD_BS (flag, 93);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// see unknown 34/117=29.1%
// possible: [......29    7 7 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx9 99   7  9........5...9 99 9.9 9.........5...9    9..9 99    9....]
// 90 -10000 at offset 16/117
DWG_OBJECT (ASSOCGEOMDEPENDENCY)
  DECODE_UNKNOWN_BITS
  //90 2 DependentOnObjectStatus (ok, NotInitializedYet, InvalidObjectId)
  //90 -10000
  //330 -> CIRCLE
  AcDbAssocDependency_fields;
  SUBCLASS (AcDbAssocGeomDependency)
  FIELD_BS (bs90_4, 90);
  FIELD_B (b290_6, 290);
  FIELD_T (t, 1);
  FIELD_B (dependent_on_compound_object, 290);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// AutoCAD Mechanical
DWG_OBJECT (ACMESCOPE)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcMeScope)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACMECOMMANDHISTORY)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcMeCommandHistory)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (ACMESTATEMGR)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcMeStateMgr)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// CDocDataContainer
DWG_OBJECT (CSACDOCUMENTOPTIONS)
  DECODE_UNKNOWN_BITS
  //size 161
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (MOTIONPATH)
  FIELD_BL (class_version, 90);
  FIELD_HANDLE (camera_path, 5, 340);
  FIELD_HANDLE (target_path, 5, 340);
  FIELD_HANDLE (viewtable, 5, 340);
  FIELD_BS (frames, 90);
  FIELD_BS (frame_rate, 90);
  FIELD_B (corner_decel, 290);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// dxfname: ACDBCURVEPATH
DWG_OBJECT (CURVEPATH)
  //SUBCLASS (AcDbNamedPath)
  SUBCLASS (AcDbCurvePath)
  FIELD_BL (class_version, 90);
  FIELD_HANDLE (entity, 5, 340);
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

DWG_OBJECT (POINTPATH)
  //SUBCLASS (AcDbNamedPath)
  SUBCLASS (AcDbPointPath)
  FIELD_BS (class_version, 90);
  FIELD_3BD (point, 10);
DWG_OBJECT_END

//not in dxf
DWG_OBJECT (TVDEVICEPROPERTIES)
  FIELD_BLx (flags, 0); // bitmask
  FIELD_BS (max_regen_threads, 0);
  FIELD_BL (use_lut_palette, 0);
  FIELD_BLL (alt_hlt, 0);
  FIELD_BLL (alt_hltcolor, 0);
  FIELD_BLL (geom_shader_usage, 0);
  // ver > 3
  FIELD_BL (blending_mode, 0)
  //ver 2 or >4:
  FIELD_BD (antialiasing_level, 0)
  FIELD_BD (bd2, 0)
  START_OBJECT_HANDLE_STREAM;
DWG_OBJECT_END

// part of ACAD_RENDER_ENTRIES
DWG_OBJECT (RENDERENTRY)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbRenderEntry);
  FIELD_BL (class_version, 90);
  FIELD_T (image_file_name, 1);
  FIELD_T (preset_name, 1);
  FIELD_T (view_name, 1);
  FIELD_BL (dimension_x, 90);
  FIELD_BL (dimension_y, 90);
  FIELD_BS (start_year, 70);
  FIELD_BS (start_month, 70);
  FIELD_BS (start_day, 70);
  FIELD_BS (start_minute, 70);
  FIELD_BS (start_second, 70);
  FIELD_BS (start_msec, 70);
  FIELD_BD (render_time, 40);
  FIELD_BL (memory_amount, 90);
  FIELD_BL (material_count, 90);
  FIELD_BL (light_count, 90);
  FIELD_BL (triangle_count, 90);
  FIELD_BL (display_index, 90);
DWG_OBJECT_END

// r2000+ expresstools. ARCALIGNEDTEXT
DWG_ENTITY (ATEXT)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbArcAlignedText);
  DXF {
    FIELD_T (text_value, 1);
    FIELD_T (t2, 2);
    FIELD_T (t3, 3);
    FIELD_T (style, 7); // as name
    FIELD_3BD (center, 10);
    FIELD_BD (radius, 40);
    FIELD_D2T (xscale, 41);
    FIELD_D2T (text_size, 42);
    FIELD_D2T (char_spacing, 43);
    FIELD_D2T (offset_from_arc, 44);
    FIELD_D2T (right_offset, 45);
    FIELD_D2T (left_offset, 46);
    FIELD_BD (start_angle, 50);
    FIELD_BD (end_angle, 51);
    FIELD_BS (is_reverse, 70);
    FIELD_BS (text_direction, 71);
    FIELD_BS (alignment, 72);
    FIELD_BS (text_position, 73);
    FIELD_BS (font_19, 74);
    FIELD_BS (bs2, 75);
    FIELD_BS (is_underlined, 76);
    FIELD_BS (bs1, 77);
    FIELD_BS (font, 78);
    FIELD_BS (is_shx, 79);
    FIELD_BL (color, 90);
    FIELD_3BD (extrusion, 210);
    FIELD_B (wizard_flag, 280);
    FIELD_HANDLE (arc_handle, 5, 330);
  } else { // DWG
    FIELD_D2T (text_size, 42);
    FIELD_D2T (xscale, 41);
    FIELD_D2T (char_spacing, 43);
    FIELD_T (style, 7);
    FIELD_T (t2, 2);
    FIELD_T (t3, 3);
    FIELD_T (text_value, 1);
    FIELD_D2T (offset_from_arc, 44);
    FIELD_D2T (right_offset, 45);
    FIELD_D2T (left_offset, 46);
    FIELD_3BD (center, 10);
    FIELD_BD (radius, 40);
    FIELD_BD (start_angle, 50);
    FIELD_BD (end_angle, 51);
    FIELD_3BD (extrusion, 210);
    FIELD_BL (color, 90);
    FIELD_BS (bs1, 77);
    FIELD_BS (font, 78);
    FIELD_BS (is_shx, 79);
    FIELD_BS (font_19, 74);
    FIELD_BS (bs2, 75);
    FIELD_BS (is_underlined, 76);
    FIELD_BS (alignment, 72);
    FIELD_BS (is_reverse, 70);
    FIELD_BS (wizard_flag, 280);
    FIELD_BS (text_position, 73);
    FIELD_BS (text_direction, 71);
    FIELD_HANDLE (arc_handle, 5, 330);
  }
DWG_ENTITY_END

// r2000+ expresstools. ROTATEDTEXT
DWG_ENTITY (RTEXT)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbRotatedText);
  FIELD_3BD (pt, 10);
  DXF  {
    FIELD_BE (extrusion, 210);
  }
  else { FIELD_3DPOINT (extrusion, 210); }
  FIELD_BD (rotation, 50);
  FIELD_BD (height, 50);
  DXF {
    FIELD_HANDLE (style, 5, 7);
  }
  FIELD_BS (flags, 70);
  FIELD_T (text_value, 1); // TODO can be split into mult.
  FIELD_HANDLE (style, 5, 0);
DWG_ENTITY_END

// related to dynblock, aka ACAD_ENHANCEDBLOCK
DWG_OBJECT (BLOCKVISIBILITYPARAMETER)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbBlockVisibilityParameter)
  FIELD_B (is_initialized, 0);
  FIELD_T (name, 0);
  FIELD_T (desc, 0);
  FIELD_B (b2, 0);
  FIELD_BL (num_states, 0);
  REPEAT (num_states, states, Dwg_BLOCKVISIBILITYPARAMETER_state)
  REPEAT_BLOCK
      SUB_FIELD_HANDLE (states[rcount1],block, DWG_HDL_HARDOWN, 330);
      SUB_FIELD_BL (states[rcount1], bl1, 0);
      SUB_FIELD_BL (states[rcount1], bl2, 0);
  END_REPEAT_BLOCK
  SET_PARENT_OBJ (states);
  END_REPEAT (states)
DWG_OBJECT_END

DWG_OBJECT (BLOCKVISIBILITYGRIP)
  DECODE_UNKNOWN_BITS;
  AcDbEvalExpr_fields;
  SUBCLASS (AcDbBlockElement)
  FIELD_T (be_t, 0);
  FIELD_BL (be_bl1, 0);
  FIELD_BL (be_bl2, 0);
  FIELD_BL (be_bl3, 0);
  SUBCLASS (AcDbBlockGrip)
  FIELD_BL (bg_bl1, 0);
  FIELD_BL (bg_bl2, 0);
  FIELD_3BD (bg_pt, 0);
  FIELD_B (bg_insert_cycling, 0);
  FIELD_BL (bg_insert_cycling_weight, 0);
  //FIELD_3BD (bg_location, 0); //?
  //FIELD_3BD (bg_display_location, 0); // ?
  SUBCLASS (AcDbBlockVisibilityGrip)
DWG_OBJECT_END

DWG_OBJECT (BLOCKGRIPLOCATIONCOMPONENT)
  DECODE_UNKNOWN_BITS
  AcDbEvalExpr_fields;
  SUBCLASS (AcDbBlockGripExpr)
  FIELD_BL (grip_type, 91); //??
  FIELD_T (grip_expr, 300);
DWG_OBJECT_END

#define AcConstraintGroupNode_fields                             \
  PRE (R_2013) {                                                 \
    DXF { VALUE_HANDLE (obj->tio.object->ownerhandle, 4, 330); } \
  }                                                              \
  FIELD_BL (nodeid, 90);                                         \
  PRE (R_2013) {                                                 \
    FIELD_RC (rc70, 70);                                         \
  }                                                              \
  FIELD_BL (num_connections, 90);                                \
  FIELD_VECTOR (connections, BLd, num_connections, 90);          \
  SINCE (R_2013) {                                               \
    FIELD_RC (rc70, 70);                                         \
  }

#define AcGeomConstraint_fields                \
  AcConstraintGroupNode_fields;                \
  SUBCLASS (AcGeomConstraint);                 \
  FIELD_BL (ownerid, 90);                      \
  FIELD_B (is_implied, 290);                   \
  FIELD_B (is_active, 290)

#define AcConstraintGeometry_fields            \
  AcConstraintGroupNode_fields;                \
  SUBCLASS (AcConstraintGeometry);             \
  FIELD_HANDLE (geom_dep, 4, 330);             \
  FIELD_BL (nodeid, 90)

#define AcExplicitConstraint_fields             \
  AcGeomConstraint_fields;                      \
  SUBCLASS (AcExplicitConstraint)               \
  FIELD_HANDLE (value_dep, 3, 340);             \
  FIELD_HANDLE (dim_dep, 3, 340)

#define AcAngleConstraint_fields                \
    AcExplicitConstraint_fields;                \
    SUBCLASS (AcAngleConstraint);               \
    FIELD_RC (sector_type, 280)

DWG_OBJECT (ASSOCVARIABLE)
  DECODE_UNKNOWN_BITS
  ASSOCACTION_fields;
  SUBCLASS (AcDbAssocVariable)
  FIELD_BL (av_class_version, 90); /* 2 */
  FIELD_T (name, 1);
  FIELD_T (t58, 1);
  FIELD_T (evaluator, 1);
  FIELD_T (desc, 1);
  AcDbEvalVariant_fields;
  FIELD_B (has_t78, 290);
  FIELD_T (t78, 1);
  FIELD_B (b290, 290);
DWG_OBJECT_END

#endif /* DEBUG_CLASSES || IS_FREE */
/*=============================================================================*/

/* Those undocumented objects are also stored as raw UNKNOWN_OBJ */

#if 0

/* Missing DXF names:
  ACDBPOINTCLOUDEX ARRAY
  ATTBLOCKREF ATTDYNBLOCKREF BLOCKREF DYNBLOCKREF XREF
  CENTERMARK CENTERLINE
*/

// EXACXREFPANELOBJECT
DWG_OBJECT (XREFPANELOBJECT)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

DWG_OBJECT (NPOCOLLECTION)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

// TODO POINTCLOUDEX
DWG_OBJECT (POINTCLOUD)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

// NanoSPDS License Parser (flexlm) or nanoCAD SPDS.
// Probably used by 3rd party extensions or
// AEC/MAP/MECH to mark or protect their objects.
// Entity Wall PtDbWall
// Entity Format mcsDbObjectFormat
// Entity NOTEPOSITION mcsDbObjectNotePosition
// Entity mcsDbObject mcsDbObject
// Entity spdsLevelMark mcsDbObjectLevelMark
// Entity McDbContainer2 McDbContainer2
// Entity spdsRelationMark mcsDbObjectRelationMark
// Entity McDbMarker McDbMarker

DWG_OBJECT (ACDSRECORD)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

DWG_OBJECT (ACDSSCHEMA)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

DWG_OBJECT (RAPIDRTRENDERENVIRONMENT)
  DECODE_UNKNOWN_BITS
DWG_OBJECT_END

DWG_OBJECT (VISIBILITYPARAMETERENTITY)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbBlockVisibilityParameterEntity)
DWG_OBJECT_END

DWG_OBJECT (VISIBILITYGRIPENTITY)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbBlockVisibilityGripEntity)
DWG_OBJECT_END

DWG_OBJECT (COMPOUNDOBJECT)
  DECODE_UNKNOWN_BITS
  SUBCLASS (AcDbCompoundObjectId)
  FIELD_B (has_data, 290);
  if (FIELD_VALUE (has_data))
    {
      //...
      FIELD_T (name, 1);
      //...
    }
DWG_OBJECT_END

#endif
