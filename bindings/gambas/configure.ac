dnl ---- configure.ac for gb.dwg

m4_include([../version.m4])
AC_INIT(gambas3-gb-dwg, GB_VERSION, GB_MAIL, [], GB_URL)
AC_CONFIG_MACRO_DIR([m4])

GB_INIT(gb.dwg)
AC_PROG_LIBTOOL

GB_COMPONENT_SEARCH(
  libredwg, LIBREDWG, gb.dwg, [src],
  'libredwg >= 0.10.1',
  [GB_FIND(dwg.h, `pkg-config --variable=includedir libredwg`, libredwg)],
  [],
  [],
  []
)

if test "$have_libredwg" = "yes"; then
  pkg-config --atleast-version=0.10.1 libredwg
  AC_DEFINE_UNQUOTED(LIBREDWG_VERSION_0_10_1, $((1-$?)), LibreDWG version >= 0.10.1)
fi

AC_OUTPUT( \
Makefile \
src/Makefile \
)

GB_PRINT_MESSAGES
