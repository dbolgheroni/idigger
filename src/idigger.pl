#!/usr/bin/perl -w
#
# Copyright (c) 2012, Daniel Bolgheroni. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
# 
# THIS SOFTWARE IS PROVIDED BY DANIEL BOLGHERONI ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DANIEL BOLGHERONI OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

use strict;
use warnings;

#use WWW::Curl::Easy;
use Getopt::Std;
use CGI qw/:standard/;

# classes
use Conf;
use GI;
use Stock;

#my $curl = new WWW::Curl::Easy;
#$curl->setopt(CURLOPT_URL, 'http://www.guiainvest.com.br/raiox/abcb4.aspx');
#open (my $FILE, ">", "curl_output.txt");
#$curl->setopt(CURLOPT_WRITEDATA, $FILE);
#$curl->perform;

# check for command line options
our ($opt_d,, $opt_f, $opt_E);
getopts('df:E:');

# process command line options
if (!$opt_f) {
    print "$0: no file name specified for the -f option\n";
    exit 1;
} else {
    open (OFILE, ">", $opt_f) ||
        die "$0: can't create/write to $opt_f, quiting\n";
}

my $Engine;
if (!$opt_E) {
    print "$0: Engine not specified, using default\n";
    exit 1;
} else {
    $Engine = "GI";
}

my @stockconf;
if ($opt_d) {
    $Engine->fetch(@stockconf);
}

# loads conf file
@stockconf = Conf->init;

# instantiate every stock in conf file
my @Stock;
foreach my $stock (@stockconf) {
    my $newStock = Stock->new($stock);

    my $pe = $Engine->get_pe($stock);   # class method
    $newStock->pe($pe);            # instance method

    my $pvb = $Engine->get_pvb($stock); # class method
    $newStock->pvb($pvb);          # instance method

    push @Stock, $newStock;
}

# debug
#foreach my $Stock (@Stock) {
#    print "Stock: ", $Stock->name, "\n";
#    print "  PE = ", $Stock->pe, "\n";
#    print "  PVB = ", $Stock->pvb, "\n";
#    print "\n";
#}

# print to html
print OFILE start_html('idigger');
print OFILE h1('idigger');

print OFILE "<table border=1>\n";
print OFILE "<tr bgcolor=#c0c0c0>",
            "<th>A&ccedil;&atilde;o</th>", 
            "<th>P/L</th>",
            "<th>P/VPA</th></tr>\n";

foreach my $Stock (@Stock) {
    print OFILE "<tr><td>", $Stock->name, "</td>";
    
    print OFILE "<td>", $Stock->pe, "</td>";
    print OFILE "<td>", $Stock->pvb, "</td>";
    print OFILE "</tr>\n";
}

print OFILE "</table>\n";
print OFILE end_html;
