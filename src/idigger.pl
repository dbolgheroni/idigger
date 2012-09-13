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

# perlfaq8 by brian d foy
BEGIN {
    use File::Spec::Functions qw(rel2abs);
    use File::Basename qw(dirname);

    my $path   = rel2abs($0);
    our $dir = dirname($path);
}
use lib $dir;

use strict;
use warnings;

#use WWW::Curl::Easy;
use Getopt::Long;
use CGI qw/:standard/;
use Scalar::Util qw/looks_like_number/;

# classes
use Conf;
use Log;
use GI;
use Stock;

my $version = "0.1";

#my $curl = new WWW::Curl::Easy;
#$curl->setopt(CURLOPT_URL, 'http://www.guiainvest.com.br/raiox/abcb4.aspx');
#open (my $FILE, ">", "curl_output.txt");
#$curl->setopt(CURLOPT_WRITEDATA, $FILE);
#$curl->perform;

# check for command line options
our ($nodownload, $help, $stocklist, $engine);

# 'Dhs:E:'
my $opts = GetOptions("-D" => \$nodownload,
                      "-h" => \$help,
                      "-c=s" => \$stocklist,
                      "-E=s" => \$engine);

sub help {
    # always document changes here!
    print <<EOH;
usage: $0 [-h] [-D] [-e E] -c C output
idigger v$version
  -h   this help
  -D   don't download info from source (useful to debug)
  -e E specify which engine to use (default: GI)
  -c C specify config file
EOH

    exit 0;
}

# process command line options
if ($help) {
    help;
}

my $ofile;
if ($ARGV[0]) {
    open ($ofile, ">", $ARGV[0]) ||
        die "can't create/write to $ARGV[0]\n";
} else {
    #$ofile = *STDOUT;
    help;
    exit 1;
}

my (@conf, $conffile, $title);
if (!$stocklist) {
    print "need to specify stock list\n";
    exit 1;
} else {
    $conffile = $stocklist;
    $title = $conffile;

    $title =~ s/.*\///;
    $title =~ s/\.conf//;

    # loads conffile
    @conf = Conf->init($conffile);
}

my $Engine;
if (!$engine) {
    print "engine not specified, using default (GI)\n";
    $Engine = "GI";
} else {
    $Engine = $engine;
}

if (!$nodownload) {
    $Engine->fetch(@conf);
}
# end of processing command line options

# instantiate every stock in conf file
my @obj;
foreach my $stock (@conf) {
    my $obj = Stock->new(uc $stock);

    my $pe = $Engine->get_pe($stock);   # class method
    $obj->pe($pe);                      # instance method

    my $roe = $Engine->get_roe($stock); # class method
    $obj->roe($roe);                    # instance method

    push @obj, $obj;
}

# print to html
print $ofile start_html('idigger');
print $ofile h2(uc $title);

# a little obscure date but it doesn't need an external module
my @lt = localtime;
$lt[4]++;
$lt[5] += 1900;

print $ofile "<p>Atualizado: ", "$lt[3]/$lt[4]/$lt[5]\n", "</p>";

print $ofile "<table border=1>\n";
print $ofile "<tr bgcolor=#c0c0c0>",
            "<th>A&ccedil;&atilde;o</th>", 
            "<th>P/L</th>",
            #"<th>ordem P/L</th>",
            "<th>ROE (%)</th>",
            #"<th>ordem ROE</th>",
            "<th>ordem Greenblatt</th>",
            "</tr>\n";

# define ordering subroutines 
sub by_pe {
    $a->pe <=> $b->pe;
}

sub by_roe {
    $b->roe <=> $a->roe;
}

sub by_greenblatt_order {
    $a->greenblatt_order <=> $b->greenblatt_order;
}

# sort pe
#
# | pe_rotten || pe_ok |
# <------------0------->
# -                    + 
#
# becomes
#
# |     pe_ordered     | (1)
# | pe_ok || pe_rotten | 
# -------->------------>
#         +            - 

my @pe_ok;
my @pe_rotten;

# separate stocks 
# negative P/E -> @pe_rotten
# positive P/E -> @pe_ok
foreach my $stock (@obj) {
    if ($stock->pe > 0) {
        push @pe_ok, $stock;
    }
    else {
        push @pe_rotten, $stock;
    }
}

# order @pe_rotten and @pe_ok accordingly and join in @pe_ordered
# as in (1)
my @pe_ordered;

my $pe_order = 0;
foreach my $stock (sort by_pe @pe_ok) {
    $pe_order++;
    $stock->pe_order($pe_order);
    push @pe_ordered, $stock;
}

foreach my $stock (reverse sort by_pe @pe_rotten) {
    $pe_order++;
    $stock->pe_order($pe_order);
    push @pe_ordered, $stock;
}

# sort roe
my @roe_ordered = @obj;

foreach my $stock (@obj) {
    if (!looks_like_number($stock->roe)) {
        $stock->roe(-999);
    }
}

my $roe_order = 0;
foreach my $stock (sort by_roe @roe_ordered) {
    $roe_order++;
    $stock->roe_order($roe_order);
    push @roe_ordered, $stock;
}

# sorting greenblatt
foreach my $stock (@obj) {
    $stock->greenblatt_order($stock->pe_order + $stock->roe_order);
}

# outputing
foreach my $stock (sort by_greenblatt_order @obj) {
    print $ofile "<tr><td>", $stock->name, "</td>";
    print $ofile "<td>", $stock->pe, "</td>";
    #print $ofile "<td>", $stock->pe_order, "</td>";
    print $ofile "<td>", $stock->roe, "</td>";
    #print $ofile "<td>", $stock->roe_order, "</td>";
    print $ofile "<td>", $stock->greenblatt_order, "</td>";
    print $ofile "</tr>\n";
}

print $ofile "</table>\n";
print $ofile end_html;
print $ofile "\n";
