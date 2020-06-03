/***************************************************************************

  CDwgDocument.cpp

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

#define __CDWGDOCUMENT_C

#include "CDwgDocument.h"

#include "gambas.h"
#include "main.h"

#include <stdio.h>
#include <stdint.h>
#include <math.h>

#include <dwg.h>
#include <dwg_api.h>

//#if LIBREDWG_VERSION_0_72
//#define getCString c_str
//#endif

/***************************************************************************/
/* TODO: ignore the pdf leftover objects/methods */

static CDWGRECT *create_rect(void)
{
	return (CDWGRECT *)GB.New(GB.FindClass("DwgRect"), NULL, NULL);
}

BEGIN_PROPERTY(DwgRect_X)

	GB.ReturnFloat(THIS_RECT->x);

END_PROPERTY

BEGIN_PROPERTY(DwgRect_Y)

	GB.ReturnFloat(THIS_RECT->y);

END_PROPERTY

BEGIN_PROPERTY(DwgRect_Width)

	GB.ReturnFloat(THIS_RECT->w);

END_PROPERTY

BEGIN_PROPERTY(DwgRect_Height)

	GB.ReturnFloat(THIS_RECT->h);

END_PROPERTY

BEGIN_PROPERTY(DwgRect_Right)

	GB.ReturnFloat(THIS_RECT->x + THIS_RECT->w);

END_PROPERTY

BEGIN_PROPERTY(DwgRect_Bottom)

	GB.ReturnFloat(THIS_RECT->y + THIS_RECT->h);

END_PROPERTY



/****************************************************************************

 Translations from Poppler universe to Gambas universe

****************************************************************************/

static void return_unicode_string(const Unicode *unicode, int len)
{
	GooString gstr;
	char buf[8]; /* 8 is enough for mapping an unicode char to a string */
	int i, n;

#if LIBREDWG_VERSION_0_85
	const UnicodeMap *uMap = globalParams->getUtf8Map();
#else
	static UnicodeMap *uMap = NULL;
	if (uMap == NULL) 
	{
		GooString *enc = new GooString("UTF-8");
		uMap = globalParams->getUnicodeMap(enc);
		uMap->incRefCnt();
		delete enc;
	}
#endif
		
	for (i = 0; i < len; ++i) {
		n = uMap->mapUnicode(unicode[i], buf, sizeof(buf));
		gstr.append(buf, n);
	}

	GB.ReturnNewZeroString(gstr.getCString());
}


static void aux_return_string_info(void *_object, const char *key)
{
	Object obj;
	Object dst;
	const_GooString *goo_value;
	Dict *info_dict;
	char *tmpstr;

	#if LIBREDWG_VERSION_0_58
	obj = THIS->doc->getDocInfo ();
	#else
	THIS->doc->getDocInfo (&obj);
	#endif
	if (!obj.isDict()) { GB.ReturnNewZeroString(""); return; }
		
	info_dict=obj.getDict();
	#if LIBREDWG_VERSION_0_58
	dst = info_dict->lookup ((char *)key);
	#else
	info_dict->lookup ((char *)key, &dst);
	#endif
	if (!dst.isString ()) { GB.ReturnNewZeroString(""); }
	else {
		goo_value = dst.getString();

		if (goo_value->hasUnicodeMarker())
		{
			GB.ConvString (&tmpstr,goo_value->getCString()+2,goo_value->getLength()-2,"UTF-16BE","UTF-8");
			GB.ReturnNewZeroString(tmpstr);		
		}		
		else
			GB.ReturnNewString(goo_value->getCString(),goo_value->getLength());		
	}
	#if ! LIBREDWG_VERSION_0_58
	dst.free();
	obj.free();		
	#endif
}

static void aux_return_date_info(void *_object, const char *key)
{
	// TODO: Y2K effect
	GB_DATE_SERIAL ds;
	GB_DATE ret;
	Object obj;
	Object dst;
	const_GooString *goo;
	Dict *info_dict;
	char *datestr=NULL,*tofree=NULL;
	int nnum;

	GB.ReturnDate(NULL);
	
	#if LIBREDWG_VERSION_0_58
	obj = THIS->doc->getDocInfo ();
	#else
	THIS->doc->getDocInfo (&obj);
	#endif
	if (!obj.isDict()) return;

	info_dict=obj.getDict();
	#if LIBREDWG_VERSION_0_58
	dst = info_dict->lookup ((char *)key);
	#else
	info_dict->lookup ((char *)key, &dst);
	#endif
	if (dst.isString ())
	{
		goo = dst.getString();
		if (goo->hasUnicodeMarker())
			GB.ConvString (&datestr,goo->getCString()+2,goo->getLength()-2,"UTF-16BE","UTF-8");
		else
		{
			datestr = GB.NewString(goo->getCString(),goo->getLength());
			tofree=datestr;		
		}

		if (datestr)
		{
			if (datestr[0] == 'D' && datestr[1] == ':') datestr += 2;
			nnum=sscanf(datestr, "%4d%2d%2d%2d%2d%2d",&ds.year, &ds.month, &ds.day, &ds.hour, &ds.min, &ds.sec);
			if (nnum == 6)
			{
				if (!GB.MakeDate(&ds,&ret))
					GB.ReturnDate(&ret);
			}		
		}
		
	}

	if (tofree) GB.FreeString(&tofree);
	#if ! LIBREDWG_VERSION_0_58
	dst.free();
	obj.free();
	#endif
}

static const_LinkDest *get_dest(const_LinkAction *act)
{
	if (!act)
		return 0;
	
	switch (act->getKind())
	{
		case actionGoTo: return ((LinkGoTo*)act)->getDest();
		case actionGoToR: return ((LinkGoToR*)act)->getDest();
		default: return 0;
	}
}

static uint32_t aux_get_page_from_action(void *_object, const_LinkAction *act)
{
	Ref pref;       
	const_LinkDest *dest = get_dest(act);
	const_GooString *name;

	if (!dest)
	{
		// try to use NamedDest to get dest
		if (!act)
			return 0;
		if (act->getKind () == actionGoTo)
		{
			name = ((LinkGoTo*)act)->getNamedDest();
			if (name) {
			#if LIBREDWG_VERSION_0_86
				dest = THIS->doc->findDest(name).get();
			#elif LIBREDWG_VERSION_0_64
				dest = THIS->doc->findDest(name);
			#else
				dest = THIS->doc->findDest((GooString *) name);
			#endif
			}
		}
	}

	if (!dest)
		return 0;

	if (dest->isPageRef() )
	{
		pref= dest->getPageRef();
#if LIBREDWG_VERSION_0_76
		return THIS->doc->findPage(pref);
#else
		return THIS->doc->findPage(pref.num, pref.gen);
#endif
	}
	else
		return dest->getPageNum();
}


static void aux_get_dimensions_from_action(const_LinkAction *act, CDWGRECT *rect)
{
	const_LinkDest *dest = get_dest(act);
	if (!dest)
		return;
	
	rect->x = dest->getLeft();
	rect->w = dest->getRight() - rect->x;
	rect->y = dest->getTop();
	rect->h = dest->getBottom() - rect->y;
}

static double aux_get_zoom_from_action(const_LinkAction *act)
{
	const_LinkDest *dest = get_dest(act);
	if (dest)
		return dest->getZoom();
	else
		return 1;
}

static char* aux_get_target_from_action(const_LinkAction *act)
{
	char *vl = NULL;
	char *uni = NULL;	
	const_GooString *tmp = NULL;
#if LIBREDWG_VERSION_0_86
	GooString gstr;
#endif

	switch (act->getKind())
	{
		case actionGoToR:
			tmp=((LinkGoToR*)act)->getFileName(); break;

		case actionLaunch:
			tmp=((LinkLaunch*)act)->getFileName(); break;

		case actionURI:
#if LIBREDWG_VERSION_0_86
			gstr = GooString(((LinkURI*)act)->getURI());
			tmp = &gstr;
#else
			tmp = ((LinkURI*)act)->getURI(); 
#endif
			break;
			
		case actionNamed:
#if LIBREDWG_VERSION_0_86
			gstr = GooString(((LinkNamed*)act)->getName());
			tmp = &gstr;
#else
			tmp = ((LinkNamed*)act)->getName(); 
#endif
			break;

		case actionMovie:
#if LIBREDWG_VERSION_0_86
			gstr = GooString(((LinkMovie*)act)->getAnnotTitle());
			tmp = &gstr;
#else
			tmp = ((LinkMovie*)act)->getAnnotTitle();
#endif
			break;

		default:
			break;
	}

	if (!tmp) return NULL;

	if (tmp->hasUnicodeMarker())
	{
			GB.ConvString (&uni,tmp->getCString()+2,tmp->getLength()-2,"UTF-16BE","UTF-8");
			vl = GB.AddString(vl, uni, 0);	
	}	
	else
			vl = GB.AddString(vl,tmp->getCString(),tmp->getLength());
	

	return vl;

}

/*****************************************************************************

 DWG document

******************************************************************************/


static void free_all(void *_object)
{
	if (THIS->doc)
	{
		delete THIS->doc;
		THIS->doc=NULL;
	}

	if (THIS->dev)
	{
		delete THIS->dev;
		THIS->dev=NULL;
	}

	if (THIS->buf)
	{
		GB.ReleaseFile(THIS->buf,THIS->len);
		THIS->buf=NULL;
	}

	if (THIS->Found)
	{		
		GB.FreeArray(POINTER(&THIS->Found));
		THIS->Found=NULL;
	}

	if (THIS->links)
	{
		delete THIS->links;	
		THIS->links=NULL;
	}

	if (THIS->pindex)
	{		
		GB.FreeArray(POINTER(&THIS->pindex));
		GB.FreeArray(POINTER(&THIS->oldindex));
		THIS->pindex=NULL;
		THIS->oldindex=NULL;
	}

	THIS->index=NULL;
	THIS->currpage=-1;
}

BEGIN_METHOD_VOID (DWGDOCUMENT_free)

	free_all(_object);

END_METHOD

BEGIN_PROPERTY(DWGDOCUMENT_scale)

	if (READ_PROPERTY){ GB.ReturnFloat(THIS->scale); return; }
	
	if (VPROP(GB_FLOAT)>0) { THIS->scale = VPROP(GB_FLOAT); return; }

	GB.Error("Zoom must be a positive value");

END_PROPERTY

BEGIN_PROPERTY(DWGDOCUMENT_rotation)

	int32_t rot;

	if (READ_PROPERTY)
	{
		GB.ReturnInteger(THIS->rotation);
		return;
	}
	
	rot=VPROP(GB_INTEGER);

	while (rot<0) rot+=360;
	while (rot>=360) rot-=360;

	switch (rot)
	{
		case 0:
		case 90:
		case 180:
		case 270: 
			THIS->rotation = VPROP(GB_INTEGER);
			break;
	}

END_PROPERTY


int32_t open_document (void *_object, char *sfile, int32_t lfile)
{
	SplashColor white;
	DWGDoc *test;
	MemStream *stream;
	Object obj;
	Outline *outline;
	char *buf=NULL;
	int32_t len=0;
	int32_t ret;


	if ( GB.LoadFile(sfile,lfile,&buf,&len) ) return -1;

	#if LIBREDWG_VERSION_0_58
	stream=new MemStream(buf,0,(uint)len,std::move(obj));
	#else
	obj.initNull();
	stream=new MemStream(buf,0,(uint)len,&obj);
	#endif
	test=new DWGDoc (stream,0,0);

	if (!test->isOk())
	{
		GB.ReleaseFile(buf,len);
		ret=test->getErrorCode();
		delete test;
		test=NULL;
		if (ret == errEncrypted) return -2;
		return -3;
	}

	free_all(_object);

	THIS->doc=test;
	THIS->buf=buf;
	THIS->len=len;

	white[0] = 0xFF; white[1] = 0xFF; white[2] = 0xFF;
	THIS->dev=new SplashOutputDev(splashModeRGB8, 3, false, white);
	THIS->dev->startDoc(THIS->doc);
	outline=THIS->doc->getOutline();
	if (outline) THIS->index=outline->getItems();
	
	//if (THIS->index)
	//	if (!THIS->index->getLength()) THIS->index=NULL;

	THIS->currindex=0;
	THIS->currpage=-1;

	return 0;

}


BEGIN_METHOD(DWGDOCUMENT_new, GB_STRING File)

	THIS->scale = 1;
	THIS->rotation = 0;

	if (!MISSING(File))
	{
		switch (open_document( _object, STRING(File), LENGTH(File)) )
		{
			case -1: GB.Error("File not found"); return;
			case -2: GB.Error("DWG is encrypted"); return;
			case -3: GB.Error("Bad DWG File"); return;
		}
	}

END_METHOD

BEGIN_METHOD (DWGDOCUMENT_open, GB_STRING File;)

	switch (open_document( _object, STRING(File), LENGTH(File)) )
	{
		case -1: GB.Error("File not found"); return;
		case -2: GB.Error("DWG is encrypted"); return;
		case -3: GB.Error("Bad DWG File"); return;
	}

END_METHOD

BEGIN_METHOD_VOID(DWGDOCUMENT_close)

	free_all(_object);

END_METHOD

BEGIN_METHOD(DWGDOCUMENT_get,GB_INTEGER index;)

	if (!THIS->doc || (VARG(index)<1) || ( VARG(index)>THIS->doc->getNumPages() ) )
	{
		GB.Error("Invalid page number");
		return;
	}

	if (THIS->currpage != (uint32_t)VARG(index) )
	{
		if (THIS->Found)
		{		
			GB.FreeArray(POINTER(&THIS->Found));
			THIS->Found=NULL;
		}

		if (THIS->links)
		{
			delete THIS->links;	
			THIS->links=NULL;
		}

		THIS->page=THIS->doc->getCatalog()->getPage(VARG(index));
		THIS->currpage=VARG(index);
	}
		
	RETURN_SELF();

END_METHOD

BEGIN_PROPERTY(DWGDOCUMENT_ready)

	GB.ReturnBoolean( (bool)THIS->doc );

END_PROPERTY

BEGIN_PROPERTY(DWGDOCUMENT_count)

	GB.ReturnInteger( (int32_t) (THIS->doc ? THIS->doc->getNumPages() : 0));

END_PROPERTY

BEGIN_PROPERTY(DWGDOCUMENT_info)

	if (THIS->doc) RETURN_SELF();
	else GB.ReturnNull();

END_PROPERTY

/*****************************************************************************

DWG.SummaryInfo section

******************************************************************************/

BEGIN_PROPERTY(DWGINFO_title)

	aux_return_string_info(_object,"Title");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_format)

	char ctx[16];
	snprintf(ctx, sizeof(ctx), "%.2g", THIS->doc->getDWGMajorVersion () + THIS->doc->getDWGMinorVersion() / 10.0);
	GB.ReturnNewZeroString(ctx);

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_author)

	aux_return_string_info(_object,"Author");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_subject)

	aux_return_string_info(_object,"Subject");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_keywords)

	aux_return_string_info(_object,"Keywords");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_creator)

	aux_return_string_info(_object,"Creator");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_producer)

	aux_return_string_info(_object,"Producer");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_linearized)

	GB.ReturnBoolean(THIS->doc->isLinearized());

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_layout)

	Catalog *catalog;

	catalog=THIS->doc->getCatalog();
	if (!catalog) { GB.ReturnInteger(Catalog::pageLayoutNone); return; }
	if (!catalog->isOk())  { GB.ReturnInteger(Catalog::pageLayoutNone); return; }

	GB.ReturnInteger(catalog->getPageLayout());

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_mode)

	Catalog *catalog;

	catalog=THIS->doc->getCatalog();
	if (!catalog) { GB.ReturnInteger(Catalog::pageModeNone); return; }
	if (!catalog->isOk())  { GB.ReturnInteger(Catalog::pageModeNone); return; }

	GB.ReturnInteger(catalog->getPageMode());


END_PROPERTY

BEGIN_PROPERTY(DWGINFO_canprint)
	
	GB.ReturnBoolean(THIS->doc->okToPrint());      

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_canmodify)

	GB.ReturnBoolean(THIS->doc->okToChange());

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_cancopy)

	GB.ReturnBoolean(THIS->doc->okToCopy());

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_canaddnotes)

	GB.ReturnBoolean(THIS->doc->okToAddNotes());

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_creation)

	aux_return_date_info(_object,"CreationDate");

END_PROPERTY

BEGIN_PROPERTY(DWGINFO_modification)

	aux_return_date_info(_object,"ModDate");

END_PROPERTY

/*****************************************************************************

 DWG pages

******************************************************************************/

static int get_rotation(void *_object)
{
	return (THIS->rotation + THIS->page->getRotate() + 720) % 360;
}

static void get_page_size(void *_object, int *w, int *h)
{
	int rotation = get_rotation(THIS);

	if (rotation == 90 || rotation == 270)
	{
		if (w) *w =  (int)(THIS->page->getMediaHeight() * THIS->scale);
		if (h) *h = (int)(THIS->page->getMediaWidth() * THIS->scale);
	}
	else
	{
		if (w) *w = (int)(THIS->page->getMediaWidth() * THIS->scale);
		if (h) *h =  (int)(THIS->page->getMediaHeight() * THIS->scale);
	}
}

BEGIN_PROPERTY (DWGPAGE_width)

	int w;
	get_page_size(THIS, &w, NULL);
	GB.ReturnInteger(w);

END_PROPERTY

BEGIN_PROPERTY (DWGPAGE_height)

	int h;
	get_page_size(THIS, NULL, &h);
	GB.ReturnInteger(h);

END_PROPERTY

static uint32_t *get_page_data(CDWGDOCUMENT *_object, int32_t x, int32_t y, int32_t *width, int32_t *height, double scale, int32_t rotation)
{
	SplashBitmap *map;
	uint32_t *data;
	int32_t w, h;
	int rw;
	int rh;

	get_page_size(THIS, &rw, &rh);

	w = *width;
	h = *height;

	if (w < 0) w = rw;
	if (h < 0) h = rh;

	if (x<0) x=0;
	if (y<0) y=0;
	if (w<1) w=1;
	if (h<1) h=1;


	if ( (x+w) > rw ) w=rw-x;
	if ( (y+h) > rh ) h=rh-y;

	if ( (w<0) || (h<0) ) return NULL;

	THIS->page->displaySlice(THIS->dev,72.0*scale,72.0*scale,
			   rotation,
			   false,
			   true,
			   x,y,w,h,
			   false);
	
	map=THIS->dev->getBitmap();
	
	data=(uint32_t*)map->getDataPtr();


	*width = w;
	*height = h;

	return data;
}

BEGIN_METHOD(DWGPAGE_image, GB_INTEGER x; GB_INTEGER y; GB_INTEGER w; GB_INTEGER h)

	uint32_t *data;
	int32_t x,y, w, h;

	x = VARGOPT(x, 0);
	y = VARGOPT(y, 0);
	w = VARGOPT(w, -1);
	h = VARGOPT(h, -1);

	data = get_page_data(THIS, x, y, &w, &h, THIS->scale, THIS->rotation);
	if (!data) { GB.ReturnNull(); return; }
	/*GB.Image.Create(&img, data, w, h, GB_IMAGE_RGB);
	GB.ReturnObject(img);*/

	GB.ReturnObject(IMAGE.Create(w, h, GB_IMAGE_RGB, (unsigned char *)data));

END_METHOD

BEGIN_PROPERTY (DWGPAGE_property_image)

	int32_t w=-1;
	int32_t h=-1;
	uint32_t *data;

	data = get_page_data(THIS, 0, 0, &w, &h, THIS->scale, THIS->rotation);
	if (!data) { GB.ReturnNull(); return; }
	/*GB.Image.Create(&img, data, w, h, GB_IMAGE_RGB);
	GB.ReturnObject(img);*/

	GB.ReturnObject(IMAGE.Create(w, h, GB_IMAGE_RGB, (unsigned char *)data));

END_PROPERTY

BEGIN_METHOD(DWGPAGE_select, GB_INTEGER X; GB_INTEGER Y; GB_INTEGER W; GB_INTEGER H)

	TextOutputDev *dev;
	GooString *str;
	Gfx *gfx;
	int32_t x,y,w,h;

	x = VARGOPT(X, 0);
	y = VARGOPT(Y, 0);
	w = VARGOPT(W, (int32_t)THIS->page->getMediaWidth());
	h = VARGOPT(H, (int32_t)THIS->page->getMediaHeight());

	dev = new TextOutputDev (NULL, true, 0, false, false);
	gfx = THIS->page->createGfx(dev,72.0,72.0,0,false,true,-1, -1, -1, -1, false, NULL, NULL);

	THIS->page->display(gfx);
	dev->endPage();

	str=dev->getText((double)x,(double)y,(double)(w+x),(double)(h+y));

	delete gfx;
	delete dev;

	if (!str)
	{
		GB.ReturnNewZeroString("");
		return;
	}
	
	GB.ReturnNewString(str->getCString(),str->getLength());	
	delete str;

END_METHOD

/*****************************************************************************

 Bookmarks of a DWG page

******************************************************************************/

void aux_fill_links(void *_object)
{
	THIS->links = new Links (THIS->page->getAnnots ());
}

BEGIN_PROPERTY (DWGPAGELINKS_count)

	if (!THIS->links) aux_fill_links(_object);
	if (!THIS->links) { GB.ReturnInteger(0); return; }
	GB.ReturnInteger(THIS->links->getNumLinks());


END_PROPERTY

BEGIN_METHOD (DWGPAGELINKS_get,GB_INTEGER ind;)

	bool pok=true;

	if (!THIS->links) aux_fill_links(_object);
	if (!THIS->links) pok=false;
	else
	{
		if (VARG(ind)<0) pok=false;
		else
		{
			if (VARG(ind)>=THIS->links->getNumLinks()) pok=false;
		}
	}

	if (!pok) { GB.Error("Out of bounds"); return; }

	THIS->lcurrent=VARG(ind);
	THIS->action=THIS->links->getLink(THIS->lcurrent)->getAction();

	RETURN_SELF();

END_METHOD

BEGIN_PROPERTY (DWGPAGELINKDATA_parameters)

	if (THIS->action->getKind() != actionLaunch )
	{
		GB.ReturnNewZeroString("");
		return;	
	}

	GB.ReturnNewZeroString(((LinkLaunch*)THIS->action)->getParams()->getCString());

END_PROPERTY

BEGIN_PROPERTY (DWGPAGELINKDATA_uri)

	char *uri;

	uri=aux_get_target_from_action(THIS->action);

	GB.ReturnNewZeroString(uri);
	if (uri) GB.FreeString(&uri);

END_PROPERTY

BEGIN_PROPERTY(DwgPageLinkData_Rect)

	CDWGRECT *rect = create_rect();
	aux_get_dimensions_from_action(THIS->action, rect);
	GB.ReturnObject(rect);

END_PROPERTY

BEGIN_PROPERTY(DWGPAGELINKDATA_zoom)

	GB.ReturnFloat(aux_get_zoom_from_action(THIS->action));

END_PROPERTY

BEGIN_PROPERTY(DWGPAGELINKDATA_page)

	GB.ReturnInteger(aux_get_page_from_action(_object,THIS->action));

END_PROPERTY

BEGIN_PROPERTY (DWGPAGELINKDATA_type)

	GB.ReturnInteger ( (int32_t)THIS->action->getKind() );

END_PROPERTY

BEGIN_PROPERTY(DWGPAGELINKDATA_check)

	if (THIS->action)
		RETURN_SELF();
	else
		GB.ReturnNull();

END_PROPERTY

static void aux_get_link_dimensions(void *_object, CDWGRECT *rect)
{
	double l,t,w,h;
	double pw,ph;

	pw=THIS->page->getMediaWidth();	
	ph=THIS->page->getMediaHeight();

	THIS->links->getLink(THIS->lcurrent)->getRect(&l, &t, &w, &h);
	w=w-l;
	h=h-t;	

	switch (get_rotation(THIS))
	{
		case 0:
			rect->x = (l*THIS->scale);
			rect->y = ((ph-t-h)*THIS->scale);
			rect->w = (w*THIS->scale);
			rect->h = (h*THIS->scale);
			break;
	
		case 90:
			rect->y = (l*THIS->scale);
			rect->x = (t*THIS->scale);
			rect->h = (w*THIS->scale);
			rect->w = (h*THIS->scale);
			break;

		case 180:
			rect->x = ((l-w)*THIS->scale);
			rect->y = (t*THIS->scale);
			rect->w = (w*THIS->scale);
			rect->h = (h*THIS->scale);
			break;

		case 270:
			rect->y = ((pw-l-w)*THIS->scale);
			rect->x = ((ph-t-h)*THIS->scale);
			rect->h = (w*THIS->scale);
			rect->w = (h*THIS->scale);
			break;
	}
}

BEGIN_PROPERTY(DwgPageLink_rect)

	CDWGRECT *rect = create_rect();
	aux_get_link_dimensions(THIS, rect);
	GB.ReturnObject(rect);

END_PROPERTY


/*****************************************************************************

 Finding a text in a DWG page

******************************************************************************/

BEGIN_METHOD (DWGPAGE_find,GB_STRING Text; GB_BOOLEAN Sensitive;)

	TextOutputDev *textdev;
	double x0=0, y0=0;
	double x1, y1;
	CDWGFIND *el;	
	Unicode *block=NULL;
	int nlen=0;
	bool sensitive=false;
	int count;
	double x, y, w, h, wp, hp;
	int rotation;

	// TODO: Use UCS-4BE on big endian systems?
	if (GB.ConvString ((char **)(void *)&block,STRING(Text),LENGTH(Text),"UTF-8",GB_SC_UNICODE))
	{	
		GB.Error("Invalid UTF-8 string");
		return;
	}

	nlen=GB.StringLength((char*)block)/sizeof(Unicode);

	if (!MISSING(Sensitive)) sensitive=VARG(Sensitive);

	textdev = new TextOutputDev (NULL, true, 0, false, false);
	THIS->page->display (textdev, 72, 72, 0, false, false, false);

	if (THIS->Found) { GB.FreeArray(POINTER(&THIS->Found)); THIS->Found=NULL; }

	count = 0;
	while (textdev->findText (block,nlen,false,true,true,false,sensitive,false,false,&x0,&y0,&x1,&y1))
	{
		if (!THIS->Found)
			GB.NewArray(POINTER(&THIS->Found),sizeof(CDWGFIND),1);
		else
			GB.Add(POINTER(&THIS->Found));

		el = &(THIS->Found[count++]); //(CDWGFIND*)&((CDWGFIND*)THIS->Found)[GB.Count(POINTER(THIS->Found))-1];
		
		x = x0;
		y = y0;
		w = x1 - x0;
		h = y1 - y0;

		wp = THIS->page->getMediaWidth();
		hp = THIS->page->getMediaHeight();
		rotation = THIS->page->getRotate();
		if (rotation == 90 || rotation == 270)
		{
			x0 = wp; wp = hp; hp = x0;
		}

		rotation = THIS->rotation; //get_rotation(THIS);
		while (rotation > 0)
		{
			x0 = wp; wp = hp; hp = x0;

			x0 = wp - y - h;
			y0 = x;

			x = w; w = h; h = x;

			x = x0;
			y = y0;

			rotation -= 90;
		}

		el->x0 = x * THIS->scale;
		el->y0 = y * THIS->scale;
		el->x1 = w * THIS->scale;
		el->y1 = h * THIS->scale;
	}

	delete textdev;

	GB.ReturnBoolean(count == 0);

END_METHOD


BEGIN_METHOD(DWGPAGERESULT_get,GB_INTEGER Index)

	CDWGRECT *rect;
	CDWGFIND *el;
	int index;

	index = VARG(Index);
	
	if (!THIS->Found || index < 0 || index >= GB.Count(THIS->Found))
	{
		GB.Error("Out of bounds");
		return;
	}

	el = &(THIS->Found[index]);
	rect = create_rect();
	
	rect->x = el->x0;
	rect->y = el->y0;
	rect->w = el->x1;
	rect->h = el->y1;
	
	GB.ReturnObject(rect);

END_METHOD

BEGIN_PROPERTY (DWGPAGERESULT_count)

	if (!THIS->Found) { GB.ReturnInteger(0); return; } 
	GB.ReturnInteger( GB.Count(POINTER(THIS->Found)) );

END_PROPERTY


/**********************************************************************

Gambas Interface

***********************************************************************/

/*
GB_DESC DwgRectDesc[] =
{
	GB_DECLARE("DwgRect", sizeof(CDWGRECT)), GB_NOT_CREATABLE(),
	
	GB_PROPERTY_READ("X", "f", DwgRect_X),
	GB_PROPERTY_READ("Y", "f", DwgRect_Y),
	GB_PROPERTY_READ("Width", "f", DwgRect_Width),
	GB_PROPERTY_READ("Height", "f", DwgRect_Height),
	GB_PROPERTY_READ("W", "f", DwgRect_Width),
	GB_PROPERTY_READ("H", "f", DwgRect_Height),
	GB_PROPERTY_READ("Left", "f", DwgRect_X),
	GB_PROPERTY_READ("Top", "f", DwgRect_Y),
	GB_PROPERTY_READ("Right", "f", DwgRect_Right),
	GB_PROPERTY_READ("Bottom", "f", DwgRect_Bottom),
	
	GB_END_DECLARE
};


GB_DESC DwgResultDesc[]=
{
	GB_DECLARE(".DwgDocumentPage.Result",0), GB_VIRTUAL_CLASS(),

	GB_METHOD("_get","DwgRect",DWGPAGERESULT_get,"(Index)i"),
	GB_PROPERTY_READ("Count","i",DWGPAGERESULT_count),

	GB_END_DECLARE
};


GB_DESC DwgLinkDataDesc[]=
{
	GB_DECLARE(".DwgDocumentPage.Link.Data",0), GB_VIRTUAL_CLASS(),

	GB_PROPERTY_READ("Type","i",DWGPAGELINKDATA_type),
	GB_PROPERTY_READ("Target","s",DWGPAGELINKDATA_uri),
	GB_PROPERTY_READ("Parameters","s",DWGPAGELINKDATA_parameters),
	GB_PROPERTY_READ("Page","i",DWGPAGELINKDATA_page),
	GB_PROPERTY_READ("Zoom","f",DWGPAGELINKDATA_zoom),
	GB_PROPERTY_READ("Rect", "DwgRect", DwgPageLinkData_Rect),

	GB_END_DECLARE
};


GB_DESC DwgLinkDesc[]=
{
	GB_DECLARE(".DwgDocumentPage.Link",0), GB_VIRTUAL_CLASS(),

	GB_PROPERTY_READ("Rect", "DwgRect", DwgPageLink_rect),
	GB_PROPERTY_READ("Data",".DwgDocumentPage.Link.Data", DWGPAGELINKDATA_check),

	GB_END_DECLARE
};


GB_DESC DwgIndexDesc[]=
{
	GB_DECLARE(".DwgDocument.Index",0), GB_VIRTUAL_CLASS(),

	GB_PROPERTY("Expanded","b",DWGINDEX_is_open),
	GB_PROPERTY_READ("Count","i",DWGINDEX_count),
	GB_PROPERTY_READ("HasChildren","b",DWGINDEX_has_children),
	GB_PROPERTY_READ("Title","s",DWGINDEX_title),
	GB_PROPERTY_READ("Text","s",DWGINDEX_title),

	GB_PROPERTY_READ("Data", ".DwgDocumentPage.Link.Data", DWGPAGELINKDATA_check),
	GB_METHOD("MovePrevious","b",DWGINDEX_prev,0),
	GB_METHOD("MoveNext","b",DWGINDEX_next,0),
	GB_METHOD("MoveChild","b",DWGINDEX_child,0),
	GB_METHOD("MoveParent","b",DWGINDEX_parent,0),
	GB_METHOD("MoveRoot",0,DWGINDEX_root,0),

	GB_END_DECLARE
};


GB_DESC DwgPageDesc[]=
{
	GB_DECLARE(".DwgDocumentPage",0), GB_VIRTUAL_CLASS(),

	GB_PROPERTY_READ("W","f",DWGPAGE_width),
	GB_PROPERTY_READ("H","f",DWGPAGE_height),
	GB_PROPERTY_READ("Width","f",DWGPAGE_width),
	GB_PROPERTY_READ("Height","f",DWGPAGE_height),
	
	GB_PROPERTY_READ("Image","Image",DWGPAGE_property_image),
	GB_PROPERTY_SELF("Result",".DwgDocumentPage.Result"),

	GB_METHOD("GetImage","Image",DWGPAGE_image,"[(X)i(Y)i(Width)i(Height)i]"),
	GB_METHOD("Find","b",DWGPAGE_find,"(Text)s[(CaseSensitive)b]"),
	GB_METHOD("Select","s",DWGPAGE_select,"[(X)i(Y)i(W)i(H)i]"),

	GB_METHOD("_get",".DwgDocumentPage.Link",DWGPAGELINKS_get,"(Index)i"),
	GB_PROPERTY_READ("Count","i",DWGPAGELINKS_count),

	GB_END_DECLARE
};
*/

GB_DESC DwgDocumentSummaryInfo[] =
{
   GB_DECLARE(".DwgDocument.SummaryInfo",0), GB_NOT_CREATABLE(),

   GB_PROPERTY_READ("Title","s",DWGINFO_title),
   GB_PROPERTY_READ("Author","s",DWGINFO_author),
   GB_PROPERTY_READ("Subject","s",DWGINFO_subject),
   GB_PROPERTY_READ("Keywords","s",DWGINFO_keywords),
   GB_PROPERTY_READ("Comments","s",DWGINFO_comments),
   //GB_PROPERTY_READ("??Date","d",DWGINFO_tdindwg),
   GB_PROPERTY_READ("CreationDate","d",DWGINFO_tdcreate),
   GB_PROPERTY_READ("ModificationDate","d",DWGINFO_tdupdate),

   GB_END_DECLARE
};

/*
GB_DESC DwgLayoutDesc[] =
{
   GB_DECLARE("DwgLayout", 0), GB_NOT_CREATABLE(),

   GB_CONSTANT("Unset","i",Catalog::pageLayoutNone),
   GB_CONSTANT("SinglePage","i",Catalog::pageLayoutSinglePage),
   GB_CONSTANT("OneColumn","i",Catalog::pageLayoutOneColumn),
   GB_CONSTANT("TwoColumnLeft","i",Catalog::pageLayoutTwoColumnLeft),
   GB_CONSTANT("TwoColumnRight","i",Catalog::pageLayoutTwoColumnRight),
   GB_CONSTANT("TwoPageLeft","i",Catalog::pageLayoutTwoPageLeft),
   GB_CONSTANT("TwoPageRight","i",Catalog::pageLayoutTwoPageRight),

   GB_END_DECLARE
};

GB_DESC DwgModeDesc[] =
{
   GB_DECLARE("DwgPageMode",0), GB_NOT_CREATABLE(),

   GB_CONSTANT("Unset","i",Catalog::pageModeNone),
   GB_CONSTANT("UseOutlines","i",Catalog::pageModeOutlines),
   GB_CONSTANT("UseThumbs","i",Catalog::pageModeThumbs),
   GB_CONSTANT("FullScreen","i",Catalog::pageModeFullScreen),
   GB_CONSTANT("UseOC","i",Catalog::pageModeOC),
   GB_CONSTANT("UseAttachments","i",Catalog::pageModeAttach),

   GB_END_DECLARE
};
*/

// This is mostly the same as the DwgDocument, just the importers and exporters are different.
// It really should create a DwgDocument, and just provide some methods.
GB_DESC DxfDocumentDesc[] =
{
  GB_DECLARE("DxfDocument", sizeof(CDXFDOCUMENT)),

  GB_METHOD("_new", 0, DXFDOCUMENT_new, "[(File)]"),
  GB_METHOD("_free", 0, DXFDOCUMENT_free, 0),

  GB_METHOD("Open",0,DXFDOCUMENT_open,"File"),
  GB_METHOD("Save",0,DXFDOCUMENT_save,"(File)"),
  GB_METHOD("SaveAs",0,DXFDOCUMENT_saveas,"[File, (Version)]"),
  GB_METHOD("Close",0,DXFDOCUMENT_close,0),

  GB_END_DECLARE
}

GB_DESC DwgDocumentDesc[] =
{
  GB_DECLARE("DwgDocument", sizeof(CDWGDOCUMENT)),

  // Versions:
  GB_CONSTANT("R_INVALID","i", R_INVALID),
  GB_CONSTANT("R_1_1","i", R_1_1),	/* MC0.0  MicroCAD Release 1.1 */
  GB_CONSTANT("R_1_2","i", R_1_2),	/* AC1.2  AutoCAD Release 1.2 */
  GB_CONSTANT("R_1_3","i", R_1_3),	/* AC1.3  AutoCAD Release 1.3 */
  GB_CONSTANT("R_1_4","i", R_1_4),	/* AC1.40 AutoCAD Release 1.4 */
  GB_CONSTANT("R_2_0","i", R_2_0),	/* AC1.50 AutoCAD Release 2.0 */
  GB_CONSTANT("R_2_1","i", R_2_1),	/* AC2.10 AutoCAD Release 2.10 */
  GB_CONSTANT("R_2_4","i", R_2_4),	/* AC1001 AutoCAD Release 2.4 */
  GB_CONSTANT("R_2_5","i", R_2_5),	/* AC1002 AutoCAD Release 2.5 */
  GB_CONSTANT("R_2_6","i", R_2_6),	/* AC1003 AutoCAD Release 2.6 */
  GB_CONSTANT("R_9","i", R_9),		/* AC1004 AutoCAD Release 9 */
  GB_CONSTANT("R_10","i", R_10),	/* AC1006 AutoCAD Release 10 */
  GB_CONSTANT("R_11","i", R_11),	/* AC1009 AutoCAD Release 11/12 (LT R1/R2) */
  GB_CONSTANT("R_13","i", R_13),	/* AC1012 AutoCAD Release 13 */
  GB_CONSTANT("R_13c3","i", R_13c3),	/* AC1013 AutoCAD Release 13C3 */
  GB_CONSTANT("R_14","i", R_14),	/* AC1014 AutoCAD Release 14 */
  GB_CONSTANT("R_2000","i", R_2000),	/* AC1015 AutoCAD Release 2000 */
  GB_CONSTANT("R_2004","i", R_2004),	/* AC1018 AutoCAD Release 2004 (includes versions AC1019/0x19 and AC1020/0x1a) */
  GB_CONSTANT("R_2007","i", R_2007),	/* AC1021 AutoCAD Release 2007 */
  GB_CONSTANT("R_2010","i", R_2010),	/* AC1024 AutoCAD Release 2010 */
  GB_CONSTANT("R_2013","i", R_2013),	/* AC1027 AutoCAD Release 2013 */
  GB_CONSTANT("R_2018","i", R_2018),	/* AC1032 AutoCAD Release 2018 */
  GB_CONSTANT("R_AFTER","i", R_AFTER)   // also invalid

  GB_METHOD("_new", 0, DWGDOCUMENT_new, "[(File)]"),
  GB_METHOD("_free", 0, DWGDOCUMENT_free, 0),

  GB_METHOD("Open",0,DWGDOCUMENT_open,"File"),
  GB_METHOD("Save",0,DWGDOCUMENT_save,"(File)"),
  GB_METHOD("SaveAs",0,DWGDOCUMENT_saveas,"[File, (Version)]"),
  GB_METHOD("Export",0,DWGDOCUMENT_export,"[File, Extension ]"),
  GB_METHOD("Close",0,DWGDOCUMENT_close,0),
  //GB_METHOD("_get",".DwgDocumentPage",DWGDOCUMENT_get,"(Index)i"),

  //GB_PROPERTY("Zoom", "f", DWGDOCUMENT_scale),
  //GB_PROPERTY("Orientation", "i", DWGDOCUMENT_rotation),

  //GB_PROPERTY_READ("Ready","b",DWGDOCUMENT_ready),
  //GB_PROPERTY_READ("Count","i",DWGDOCUMENT_count),
  //GB_PROPERTY_READ("HasIndex","b",DWGDOCUMENT_has_index),
  //GB_PROPERTY_READ("Index",".DwgDocument.Index",DWGDOCUMENT_index),
  GB_PROPERTY_READ("SummaryInfo",".DwgDocument.SummaryInfo",DWGDOCUMENT_summaryinfo),

  GB_END_DECLARE
};
