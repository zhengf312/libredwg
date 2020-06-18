/*****************************************************************************/
/*  LibreDWG - free implementation of the DWG file format                    */
/*                                                                           */
/*  Copyright (C) 2009-2020 Free Software Foundation, Inc.                   */
/*  Copyright (C) 2010 Thien-Thi Nguyen                                      */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

/*
 * dwgread.c: read a DWG file, print verbose logging, and output to
 *            various formats.
 * written by Felipe Castro
 * modified by Felipe Corrêa da Silva Sances
 * modified by Rodrigo Rodrigues da Silva
 * modified by Thien-Thi Nguyen
 * modified by Reini Urban
 */

#include "../src/config.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
// strings.h or string.h
#ifdef AX_STRCASECMP_HEADER
#  include AX_STRCASECMP_HEADER
#endif
#include <getopt.h>
#ifdef HAVE_VALGRIND_VALGRIND_H
#  include <valgrind/valgrind.h>
#endif

#include "dwg.h"
#include "common.h"
#include "out_json.h"
#include "out_dxf.h"

static int opts = 1;

static int
usage (void)
{
  printf ("\nUsage: dwgread [-v[0-9]] [-O FMT] [--as rNNNN] [-o OUTFILE] [DWGFILE|-]\n");
  return 1;
}
static int
opt_version (void)
{
  printf ("dwgread %s\n", PACKAGE_VERSION);
  return 0;
}
static int
help (void)
{
  printf ("\nUsage: dwgread [OPTION]... DWGFILE\n");
  printf ("Reads the DWG into some optional output format to stdout or some "
          "file,\n"
          "and prints error, success or verbose internal progress to stderr.\n"
          "\n");
#ifdef HAVE_GETOPT_LONG
  printf ("  -v[0-9], --verbose [0-9]  verbosity\n");
  printf ("  -O fmt,  --format fmt     fmt: DXF, DXFB, JSON, GeoJSON\n");
  printf ("           Planned output formats:  YAML, XML/OGR, GPX, SVG, PS\n");
  printf ("  --as rNNNN                save as other version\n");
  printf ("           Valid versions:\n");
  printf ("                r12, r14, r2000, r2004, r2007, r2010, r2013, r2018\n");
  printf ("           Planned versions:\n");
  printf ("             r9, r10, r11\n");
  printf ("  -o outfile                also defines the output fmt. Default: "
          "stdout\n");
  printf ("           --help           display this help and exit\n");
  printf ("           --version        output version information and exit\n"
          "\n");
#else
  printf ("  -v[0-9]     verbosity\n");
  printf ("  -O fmt      fmt: DXF, DXFB, JSON, GeoJSON\n");
  printf ("              Planned output formats:  YAML, XML/OGR, GPX, SVG, PS\n");
  printf ("  -o outfile  also defines the output fmt. Default: stdout\n");
  printf ("  -a rNNNN    save as other version\n");
  printf ("              Valid versions:\n");
  printf ("                r12, r14, r2000, r2004, r2007, r2010, r2013, r2018\n");
  printf ("              Planned versions:\n");
  printf ("                r9, r10, r11\n");
  printf ("  -h          display this help and exit\n");
  printf ("  -i          output version information and exit\n"
          "\n");
#endif
  printf ("GNU LibreDWG online manual: "
          "<https://www.gnu.org/software/libredwg/>\n");
  return 0;
}

int
main (int argc, char *argv[])
{
  int i = 1;
  int error;
  Dwg_Data dwg;
  const char *fmt = NULL;
  const char *outfile = NULL;
  const char *version = NULL;
  Dwg_Version_Type dwg_version = R_INVALID;
  int has_v = 0;
  int force_free = 0;
  int c;
#ifdef HAVE_GETOPT_LONG
  int option_index = 0;
  static struct option long_options[]
      = { { "verbose", 1, &opts, 1 }, // optional
          { "format", 1, 0, 'O' },    { "file", 1, 0, 'o' },
          { "as", 1, 0, 'a' },        { "help", 0, 0, 0 },
          { "version", 0, 0, 0 },
          { "force-free", 0, 0, 0 },
          { NULL, 0, NULL, 0 } };
#endif

  if (argc < 2)
    return usage ();

  while
#ifdef HAVE_GETOPT_LONG
      ((c = getopt_long (argc, argv, "a:v::O:o:h", long_options, &option_index))
       != -1)
#else
      ((c = getopt (argc, argv, "a:v::O:o:hi")) != -1)
#endif
    {
      if (c == -1)
        break;
      switch (c)
        {
        case ':': // missing arg
          if (optarg && !strcmp (optarg, "v"))
            {
              opts = 1;
              has_v = 1;
              break;
            }
          fprintf (stderr, "%s: option '-%c' requires an argument\n", argv[0],
                   optopt);
          break;
#ifdef HAVE_GETOPT_LONG
        case 0:
          /* This option sets a flag */
          if (!strcmp (long_options[option_index].name, "verbose"))
            {
              if (opts < 0 || opts > 9)
                return usage ();
#  if defined(USE_TRACING) && defined(HAVE_SETENV)
              {
                char v[2];
                *v = opts + '0';
                *(v + 1) = 0;
                setenv ("LIBREDWG_TRACE", v, 1);
              }
#  endif
              has_v = 1;
              break;
            }
          if (!strcmp (long_options[option_index].name, "version"))
            return opt_version ();
          if (!strcmp (long_options[option_index].name, "help"))
            return help ();
          if (!strcmp (long_options[option_index].name, "force-free"))
            force_free = 1;
          break;
#else
        case 'i':
          return opt_version ();
#endif
        case 'O':
          fmt = optarg;
          break;
        case 'a':
          dwg_version = dwg_version_as (optarg);
          if (dwg_version == R_INVALID)
            {
              fprintf (stderr, "Invalid version '%s'\n", argv[1]);
              return usage ();
            }
          version = optarg;
          break;
        case 'o':
          outfile = optarg;
          if (!fmt && outfile != NULL)
            {
#ifndef DISABLE_DXF
              if (strstr (outfile, ".json") || strstr (outfile, ".JSON"))
                fmt = (char *)"json";
              else if (strstr (outfile, ".dxf") || strstr (outfile, ".DXF"))
                fmt = (char *)"dxf";
              else if (strstr (outfile, ".dxfb") || strstr (outfile, ".DXFB"))
                fmt = (char *)"dxfb";
              else if (strstr (outfile, ".geojson")
                       || strstr (outfile, ".GeoJSON"))
                fmt = (char *)"geojson";
              else
#endif
                fprintf (stderr, "Unknown output format for %s\n", outfile);
            }
          break;
        case 'v': // support -v3 and -v
          i = (optind > 0 && optind < argc) ? optind - 1 : 1;
          if (!memcmp (argv[i], "-v", 2))
            {
              opts = argv[i][2] ? argv[i][2] - '0' : 1;
            }
          if (opts < 0 || opts > 9)
            return usage ();
#if defined(USE_TRACING) && defined(HAVE_SETENV)
          {
            char v[2];
            *v = opts + '0';
            *(v + 1) = 0;
            setenv ("LIBREDWG_TRACE", v, 1);
          }
#endif
          has_v = 1;
          break;
        case 'h':
          return help ();
        case '?':
          fprintf (stderr, "%s: invalid option '-%c' ignored\n", argv[0],
                   optopt);
          break;
        default:
          return usage ();
        }
    }
  i = optind;

  memset (&dwg, 0, sizeof (Dwg_Data));
  if (has_v || !fmt)
    dwg.opts = opts;
#if defined(USE_TRACING) && defined(HAVE_SETENV)
  if (!has_v)
    setenv ("LIBREDWG_TRACE", "1", 0);
#endif

  if (optind != argc)
    {
      if (opts > 1)
        fprintf (stderr, "Reading DWG file %s\n", argv[i]);
      error = dwg_read_file (argv[i], &dwg);
    }
  else
    {
      if (opts > 1)
        fprintf (stderr, "Reading DWG from stdin\n");
      error = dwg_read_file ("-", &dwg); // i.e. from stdin
    }

  if (error >= DWG_ERR_CRITICAL)
    goto done;

  if (fmt)
    {
      Bit_Chain dat = { 0 };
      if (outfile)
        dat.fh = fopen (outfile, "w");
      else
        dat.fh = stdout;

      if (version)
        dat.version = dwg.header.version = dwg_version;
      else
        dat.version = dwg.header.version;

      fprintf (stderr, "\n");
#ifndef DISABLE_DXF
      if (!strcasecmp (fmt, "json"))
        {
          if (opts > 1 && outfile)
            fprintf (stderr, "Writing JSON file %s\n", outfile);
          error = dwg_write_json (&dat, &dwg);
        }
      else if (!strcasecmp (fmt, "dxfb"))
        {
          if (opts > 1 && outfile)
            fprintf (stderr, "Writing Binary DXF file %s\n", outfile);
          error = dwg_write_dxfb (&dat, &dwg);
        }
      else if (!strcasecmp (fmt, "dxf"))
        {
          if (opts > 1 && outfile)
            fprintf (stderr, "Writing Binary DXF file %s\n", outfile);
          error = dwg_write_dxf (&dat, &dwg);
        }
      else if (!strcasecmp (fmt, "geojson"))
        {
          if (opts > 1 && outfile)
            fprintf (stderr, "Writing GeoJSON file %s\n", outfile);
          error = dwg_write_geojson (&dat, &dwg);
        }
      else
#endif
        fprintf (stderr, "Invalid output format '%s'\n", fmt);

      if (outfile)
        fclose (dat.fh);
    }

 done:
#if defined __SANITIZE_ADDRESS__ || __has_feature(address_sanitizer)
  {
    char *asanenv = getenv("ASAN_OPTIONS");
    if (!asanenv)
      force_free = 1;
    // detect_leaks is enabled by default. see if it's turned off
    else if (strstr (asanenv, "detect_leaks=0") == NULL) /* not found */
      force_free = 1;
  }
#endif

  // forget about valgrind. really huge DWG's need endlessly here.
  if ((dwg.header.version && dwg.num_objects < 1000)
      || force_free
#ifdef HAVE_VALGRIND_VALGRIND_H
      || (RUNNING_ON_VALGRIND)
#endif
  )
    {
      dwg_free (&dwg);
    }

  if (error >= DWG_ERR_CRITICAL)
    {
      fprintf (stderr, "ERROR 0x%x\n", error);
      if (error && opts > 2)
        dwg_errstrings (error);
    }
  else
    {
      if (opts > 1)
        {
          fprintf (stderr, "SUCCESS 0x%x\n", error);
          if (error && opts > 2)
            dwg_errstrings (error);
        }
      else
        fprintf (stderr, "SUCCESS\n");
    }

  return error >= DWG_ERR_CRITICAL ? 1 : 0;
}
