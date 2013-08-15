#!/bin/sh
#
# HOW TO GENERATE AN UP-TO-DATE all.conf:
#
# Visit each page in the list below:
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=ICON&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IEE&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IFNC&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IMAT&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IMOB&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=INDX&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=MLCX&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=SMLL&idioma=pt-br
# http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=UTIL&idioma=pt-br
# (You can't use curl or wget to directly retrieve them.)
#
# Save each page as HTML only. Run the script, with a wildcard as
# argument, to match all the files downloaded. In this case, all files
# have the .aspx extension:
#
# $ ./bmfbov_init.sh *.aspx
#
# The output is a file containing the ordered stock list codes of
# BM&FBovespa of the day. A file with the `out-YYYYmmdd.conf' format is
# generated (e.g.  out-20130825.conf). Make a copy of this file to
# `all.conf':
#
# $ cp out-20130825.conf all.conf
#
# If you don't want to generate the list of all stocks, just specify
# individual files or group of files: 
#
# $ ./bmfbov_init.sh imat.aspx imob.aspx
#
# This list doesn't change too much, so don't worry to always update.
# Now you can use this file as the configuration for the `fetcher.py'
# utility.

all=$*
today=`date "+%Y%m%d"`
outfile="out-${today}.conf"

# remove old version if it exists
if [ -e "$outfile" ]; then
    rm $outfile
fi

# cycle through all files specified as argument
for a in $all; do
    cat $all | grep lblCodigo | sed 's/.*">//; s/<.*//' | \
        sort | uniq >> $outfile
done
