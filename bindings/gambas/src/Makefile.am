COMPONENT = gb.dwg
include ../component.am

gblib_LTLIBRARIES = gb.dwg.la

gb_dwg_la_LIBADD = -lredwg -lm
gb_dwg_la_LDFLAGS = -module @LD_FLAGS@ @LIBREDWG_LDFLAGS@
gb_dwg_la_CXXFLAGS = $(AM_CXXFLAGS) $(GB_CXXFLAGS_STD_CPP11)
gb_dwg_la_CPPFLAGS = @LIBREDWG_INC@

gb_dwg_la_SOURCES = main.h main.cpp \
                    CDwgDocument.h CDwgDocument.cpp 

