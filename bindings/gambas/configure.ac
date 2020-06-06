dnl ---- configure.ac for gb.dwg
dnl version.m4 needs to be symlinked here
m4_include([version.m4])
AC_INIT(gambas3-gb-dwg, GB_VERSION, GB_MAIL, [], GB_URL)
AC_CONFIG_MACRO_DIR([m4])

GB_INIT_SHORT([gb.dwg])
GB_SYSTEM
GB_LIBTOOL
AC_PROG_CXX
AC_PROG_LIBTOOL

dnl if in libredwg srcdir skip that
if test -e ../dwg.i && test ../../bindings/gambas ; then
  have_libredwg=yes
  if test -e gambas.h ; then
    hdr=$(realpath gambas.h)
    srcdir=$(dirname "$hdr")
    prefix="$srcdir"
  fi
  AC_DEFINE_UNQUOTED(LIBREDWG_VERSION_0_10_1, 1, LibreDWG version >= 0.10.1)
else
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
fi

AC_OUTPUT( \
Makefile \
src/Makefile \
)

GB_PRINT_MESSAGES
