#!/bin/sh
# need to know the gambas srcdir
test -z "$GB_SRCDIR" && GB_SRCDIR="$1"
thisdir=$(realpath "$0")
thisdir=$(dirname "$thisdir")

find_gbsrc () {
	dir="$1"
	if [ -d "$dir" ] && [ -d "$dir/main/share" ]
	then
		GB_SRCDIR=$(realpath "$dir")
	fi
}
test -z "$GB_SRCDIR" && find_gbsrc ../gambas
test -z "$GB_SRCDIR" && find_gbsrc ../../../gambas
test -z "$GB_SRCDIR" && find_gbsrc /usr/src/gambas

cd "$thisdir" || exit
for f in component.am reconf m4 COPYING version.m4 missing acinclude.m4 NEWS
do
	if [ ! -e $f ]
	then
		ln -s "$GB_SRCDIR"/$f $f
	fi
done
for f in gambas.h gb_common.h
do
	if [ ! -e $f ]
	then
		ln -s "$GB_SRCDIR"/main/share/$f $f
	fi
done
cd - || exit
