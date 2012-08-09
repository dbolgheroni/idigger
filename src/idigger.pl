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
our ($opt_d, $opt_s, $opt_E);
getopts('ds:E:');

# process command line options
my $ofile;
if ($ARGV[0]) {
    open ($ofile, ">", $ARGV[0]) ||
        die "$0: can't create/write to $ARGV[0]\n";
} else {
    $ofile = *STDOUT;
}

my @stockconf;
my ($conffile, $title);
if (!$opt_s) {
    print "$0: need to specify stock list\n";
    exit 1;
} else {
    $conffile = $opt_s;
    $title = $conffile;

    $title =~ s/.*\///;
    $title =~ s/\.conf//;

    # loads conffile
    @stockconf = Conf->init($conffile);
}

my $Engine;
if (!$opt_E) {
    print "$0: Engine not specified, using default (GI)\n";
    $Engine = "GI";
} else {
    $Engine = $opt_E;
}

if ($opt_d) {
    $Engine->fetch(@stockconf);
}
# end of processing command line options

# instantiate every stock in conf file
my @Stock;
foreach my $stock (@stockconf) {
    my $newStock = Stock->new($stock);

    my $pe = $Engine->get_pe($stock);   # class method
    $newStock->pe($pe);                 # instance method

    my $pvb = $Engine->get_pvb($stock); # class method
    $newStock->pvb($pvb);               # instance method

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
print $ofile start_html('idigger');
print $ofile h2($title);

# a little obscure date but it doesn't need external module
my @lt = localtime;
$lt[4]++;
$lt[5]+=1900;

print $ofile "<p>Atualizado: ", "$lt[3]/$lt[4]/$lt[5]\n", "</p>";

print $ofile "<table border=1>\n";
print $ofile "<tr bgcolor=#c0c0c0>",
            "<th>A&ccedil;&atilde;o</th>", 
            "<th>P/L</th>",
            "<th>P/VPA</th></tr>\n";

foreach my $Stock (@Stock) {
    print $ofile "<tr><td>", $Stock->name, "</td>";
    
    print $ofile "<td>", $Stock->pe, "</td>";
    print $ofile "<td>", $Stock->pvb, "</td>";
    print $ofile "</tr>\n";
}

print $ofile "</table>\n";
print $ofile end_html;
print $ofile "\n";
