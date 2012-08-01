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

# the function that really do the job for get_*(), like get_pe(),
# get_pvb(), etc.
sub _gi_get_id {
    my (%ratio, $key);

    my ($tag, @args) = @_;
    
    foreach my $stock (@args) {
        open (STOCK, "<", "$ENV{HOME}/.idigger/rawdata/$stock.aspx") ||
            die "can't open $stock.aspx\n";

        while (<STOCK>) {
            if (/$tag/) {
                s/.*\">//;
                s/<.*//;
                s/,/./;
                chomp;
                $ratio{$stock} = $_;
            }
        }
    }
    
    return %ratio;
}

# P/E ratio (P/L in portuguese)
# returns a hash of P/E ordered from lower to higher
# note: lower is better 
# TODO: prototype to put constraints on the parameter list
sub get_pe {
    my %pe = _gi_get_id('lbPrecoLucroAtual', @_);
    return %pe;
}

# P/VB ratio (P/VPA in portuguese)
sub get_pvb {
    my %pvb = _gi_get_id('lbPrecoValorPatrimonialAtual', @_);
    return %pvb;
}

# check for command line options
our ($opt_d,, $opt_f);
getopts('df:');

# initializes some data structures
my ($ofile);
@stock = init_stock_conf;

# real processing starts here
my %pe = get_pe (@stock);
my %pvb = get_pvb (@stock);

# concatenate
my %stock;
foreach my $stock (@stock) {
    #print "$stock:\n";
    # pe
    $stock{$stock}{pe} = $pe{$stock};
    #print "  pe = $stock{$stock}{pe}\n";

    # pvb
    $stock{$stock}{pvb} = $pvb{$stock};
    #print "  pvb = $stock{$stock}{pvb}\n";
}

# process command line options
if (!$opt_f) {
    print "$0: no file name specified for the -f option\n";
    exit 1;
} else {
    $ofile = $opt_f;

    open (OFILE, ">", $ofile) ||
        die "$0: can't create/write to $ofile, quiting\n";
}

if ($opt_d) {
    _gi_dl_stock_info(@stock);
}

# print to html
print OFILE start_html('idigger');
print OFILE h1('idigger');

print OFILE "<table border=1>\n";
print OFILE "<tr bgcolor=#c0c0c0>",
            "<th>A&ccedil;&atilde;o</th>", 
            "<th>P/L</th>",
            "<th>P/VPA</th></tr>\n";

foreach my $key (sort keys %stock) {
    my $KEY;
    $KEY = uc ($key);
    print OFILE "<tr><td>$KEY</td>";

    # validate
    
    print OFILE "<td>", $stock{$key}{pe}, "</td>";
    print OFILE "<td>", $stock{$key}{pvb}, "</td>";
    print OFILE "</tr>\n";
}

print OFILE "</table>\n";
print OFILE end_html;
