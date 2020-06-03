/***************************************************************************

  main.cpp

  (C) 2020 Reini Urban <rurban@cpan.org>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2, or (at your option)
  any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.

***************************************************************************/

#define __MAIN_C

#include "CDwgDocument.h"
#include "main.h"

#include <stdio.h>

#include <GlobalParams.h>

extern "C" {

GB_INTERFACE GB EXPORT;

GB_DESC *GB_CLASSES[] EXPORT =
{
	DwgRectDesc,
	DwgDocumentDesc,
	DwgPageDesc,
	DwgResultDesc,
	DwgIndexDesc,
	DwgLinkDesc,
	DwgLinkDataDesc,
	DwgDocumentInfo,
	DwgLayoutDesc,
	DwgModeDesc,
	NULL
};


int EXPORT GB_INIT(void)
{
	if (!globalParams)
	{
#if POPPLER_VERSION_0_83
		globalParams = std::unique_ptr<GlobalParams>(new GlobalParams());
#else
		globalParams = new GlobalParams();
#endif
	}

	//GB.GetInterface("gb.image", IMAGE_INTERFACE_VERSION, &IMAGE);
	
	return 0;
}



void EXPORT GB_EXIT()
{

}


}
