/*****************************************************************************/
/*  LibreDWG - Free DWG library                                              */
/*  http://code.google.com/p/libredwg/                                       */
/*                                                                           */
/*    based on LibDWG - Free DWG read-only library                           */
/*    http://sourceforge.net/projects/libdwg                                 */
/*    originally written by Felipe Castro <felipo at users.sourceforge.net>  */
/*                                                                           */
/*  Copyright (C) 2008, 2009 Free Software Foundation, Inc.                  */
/*  Copyright (C) 2009 Felipe Sanches <jucablues@users.sourceforge.net>      */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "../src/bits.h"
#include "../src/common.h"
#include <dwg.h>

int
test_dwg_c(char *filename);

void
test_map_R2000();

int
num_vars(enum DWG_VERSION_TYPE version);

int
main(int argc, char *argv[])
{
  printf("Starting to test the type-map for DWG version R2000.\n");
  test_map_R2000();
  printf("End of type-map test.\n");

  printf("Testing number of header variables:\n");

  printf("R13: %d\n", num_vars(R_13));
  printf("R14: %d\n", num_vars(R_14));
  printf("R2000: %d\n", num_vars(R_2000));
  printf("R2004: %d\n", num_vars(R_2004));
  printf("R2007: %d\n\n", num_vars(R_2007));

  if (argc > 1)
    return (test_dwg_c(argv[1]));
  else
    return (test_dwg_c(NULL));
}

#define FILENAME "example"

int
test_dwg_c(char *filename)
{
  int error;
  Dwg_Data dwg_struct;

  if (filename)
    error = dwg_read_file(filename, &dwg_struct);
  else
    error = dwg_read_file(FILENAME ".dwg", &dwg_struct);

  if (!error)
    {
      //I have temporarily disabled the print module. ~Juca
      //dwg_print(&dwg_struct);
      /*
       unlink ("new_result.dwg");
       error = error || dwg_write_file ("new_result.dwg", &dwg_struct);
       */
    }

  dwg_free(&dwg_struct);

  if (error)
    puts(" \"dwg.c\" ==> Error...");
  else
    {
      puts(" \"dwg.c\" ==> SUCCESS!");
    }

  return error;
}

int
num_vars(Dwg_Version_Type version)
{
  int i;
  for (i = 0; dwg_var_map(version, i) != DWG_END_OF_HEADER_VARIABLES; i++)
    {
    };
  return i - 1;
}

void
test_map_R2000()
{
  int i;
  static unsigned int map_R2000[] =
    { DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_T, DWG_DT_T, DWG_DT_T,
        DWG_DT_T, DWG_DT_BL, DWG_DT_BL, DWG_DT_H, DWG_DT_B, DWG_DT_B, DWG_DT_B,
        DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B,
        DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B,
        DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_T, DWG_DT_BL, DWG_DT_BL,
        DWG_DT_BL, DWG_DT_BL, DWG_DT_BL, DWG_DT_BL, DWG_DT_BL, DWG_DT_BL,
        DWG_DT_CMC, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H,
        DWG_DT_BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_2RD, DWG_DT_2RD,
        DWG_DT_BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_H, DWG_DT_H,
        DWG_DT_BS, DWG_DT_H, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD,
        DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_2RD,
        DWG_DT_2RD, DWG_DT_BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_H,
        DWG_DT_H, DWG_DT_BS, DWG_DT_H, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD,
        DWG_DT_3BD, DWG_DT_3BD, DWG_DT_3BD, DWG_DT_T, DWG_DT_T, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B,
        DWG_DT_B, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD, DWG_DT_BD,
        DWG_DT_BD, DWG_DT_B, DWG_DT_BS, DWG_DT_B, DWG_DT_B, DWG_DT_B, DWG_DT_B,
        DWG_DT_CMC, DWG_DT_CMC, DWG_DT_CMC, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_B, DWG_DT_B, DWG_DT_BS, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_BS, DWG_DT_B, DWG_DT_BS, DWG_DT_H, DWG_DT_H,
        DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_BS, DWG_DT_BS, DWG_DT_H, DWG_DT_H,
        DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H,
        DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_BS, DWG_DT_BS, DWG_DT_T,
        DWG_DT_T, DWG_DT_H, DWG_DT_H, DWG_DT_H, DWG_DT_BL, DWG_DT_BS,
        DWG_DT_BS, DWG_DT_H, DWG_DT_T, DWG_DT_T, DWG_DT_H, DWG_DT_H, DWG_DT_H,
        DWG_DT_H, DWG_DT_H, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS, DWG_DT_BS };

  for (i = 0; i < 233; i++)
    {
      if (map_R2000[i] != dwg_var_map(R_2000, i))
        {
          fprintf(stderr, "map_R2000[%d]=%d\t\tdwg_var_map(R_2000, %d)=%d\n",
              i, map_R2000[i], i, dwg_var_map(R_2000, i));
          fprintf(stderr, "Did not pass the test.\nFailed at index=%d\n\n", i);
          return;
        }
    }
}
