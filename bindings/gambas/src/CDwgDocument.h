/***************************************************************************

  CDwgDocument.h

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

#ifndef __CDWGDOCUMENT_H
#define __CDWGDOCUMENT_H

#include "gambas.h"

#include <stdint.h>
#include <dwg.h>
#include <dwg_api.h>
//#include <SplashOutputDev.h>
//#include <Page.h>
//#if POPPLER_VERSION_0_76
//#include <vector>
//#include <Outline.h>
//#else
//#include <goo/GooList.h>
//#endif

#if LIBREDWG_VERSION_0_76
	#define const_LinkAction const LinkAction
	#define const_LinkDest const LinkDest
	#define const_GooList const std::vector<OutlineItem*>
	#define GooList std::vector<OutlineItem*>
	#define const_GooString const GooString
#elif LIBREDWG_VERSION_0_64
	#define const_LinkAction const LinkAction
	#define const_LinkDest const LinkDest
	#define const_GooList const GooList
	#define const_GooString const GooString
#else
	#define const_LinkAction LinkAction
	#define const_LinkDest LinkDest
	#define const_GooList GooList
	#define const_GooString GooString
#endif

#ifndef __CDWGDOCUMENT_C

extern GB_DESC DxfDocumentDesc[];
extern GB_DESC DwgDocumentDesc[];

#else

#define THIS ((CDWGDOCUMENT *)_object)
#//define THIS_RECT ((CDWGRECT *)_object)

#endif

#if LIBREDWG_VERSION_0_76

#define CDWG_list_get(_list, _i) ((_list)->at(_i))
#define CDWG_list_count(_list) ((_list)->size())

#else

#define CDWG_list_get(_list, _i) ((OutlineItem *)(_list)->get(_i))
#define CDWG_list_count(_list) ((_list)->getLength())

#endif

#define CDWG_index_get(_i) CDWG_list_get(THIS->index, _i)
#define CDWG_index_count() CDWG_list_count(THIS->index)

typedef
	struct {
		GB_BASE ob;

		char *buf;
		int len;

		Dwg_Data *data;
		Bit_Chain *stream;
	}
	CDWGDOCUMENT;

typedef CDWGDOCUMENT CDXFDOCUMENT;

#endif
