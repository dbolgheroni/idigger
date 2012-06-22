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
#
# TODO
# x interface to functions
# x functions prototypes
# x module/package (?)
# x log file
# x parameter to only download stock info if asked to (debugging)

use strict;
#use WWW::Curl::Easy;
use Getopt::Std;
use CGI qw/:standard/;

#my $curl = new WWW::Curl::Easy;
#$curl->setopt(CURLOPT_URL, 'http://www.guiainvest.com.br/raiox/abcb4.aspx');
#open (my $FILE, ">", "curl_output.txt");
#$curl->setopt(CURLOPT_WRITEDATA, $FILE);
#$curl->perform;

my (@stock);

# returns the stock list stored in config file
# TODO: prototype to put constraints on the parameter list
sub init_stock_conf {
    my $stock;
    
    open (STOCKCONF, "<", "$ENV{HOME}/.idigger/stock.conf") ||
        die "can't open .stock.conf\n";

    while (<STOCKCONF>) {
        $stock = lc; # lowercase
        push @_, $stock;
    }
    chomp @_;

    close (STOCKCONF);
    return @_;
}

# downloads the stock info of the stocks passed as a parameter and
# can be used with the LIST returned by init_stock_conf
# TODO: prototype to put constraints on the parameter list
sub _gi_dl_stock_info {
    my ($ret, $stock);

    foreach (@_) {
        $ret = system ("curl -s \'http://www.guiainvest.com.br/raiox/$_.aspx\' > $ENV{HOME}/.idigger/rawdata/$_.aspx");

        $stock = lc $_;
        if ($ret == 0) {
            print "$stock info downloaded OK\n";
        } else {
            print "$stock info download FAILED\n";
        }
    }
}

# P/E ratio
# returns a hash of P/E ordered from lower to higher
# note: lower is better 
# TODO: prototype to put constraints on the parameter list
sub _gi_get_current_pe {
    my (%pe, $stock, $key);

    foreach $stock (@_) {
        open (STOCK, "<", "$ENV{HOME}/.idigger/rawdata/$stock.aspx") ||
            die "can't open $stock.aspx\n";

        while (<STOCK>) {
            if (/lbPrecoLucroAtual/) {
                s/.*\">//;
                s/<.*//;
                s/,/./;
                chomp;
                $pe{$stock} = $_;
            }
        }
    }
    
    return %pe;
}

# check for command line options
our ($opt_d,, $opt_f);
getopts('df:');

# initializes some data structures
my ($ofile);
@stock = init_stock_conf;

# real processing starts here
my %pe = _gi_get_current_pe (@stock);

if (!$opt_f) {
    print "need to specify a file for output with -f\n";
    exit 1;
} else {
    $ofile = $opt_f;

    open (OFILE, ">", $ofile) ||
        die "can't create/write to $ofile, quiting\n";
}

print OFILE start_html('invest system');
print OFILE h1('Rela&ccedil;&atilde;o P/L');

print OFILE "<table border=1>\n";
print OFILE "<tr bgcolor=#c0c0c0><th>A&ccedil;&atilde;o</th><th>P/L</th><tr>\n";

foreach my $key (sort keys %pe) {
    print OFILE "<tr><td>$key</td>";

    if (($pe{$key} < 6.0) && ($pe{$key} >= 0.0)) {
        print OFILE "<td style=\"background-color:lightgreen\">",
              uc ($pe{$key}), "</td></tr>\n";
    } else {
        print OFILE "<td>", uc ($pe{$key}), "</td></tr>\n";
    }
}

print OFILE "</table>\n";
print OFILE end_html;
