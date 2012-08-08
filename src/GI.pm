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


# GuiaInvest Class
package GI;

use strict;
use warnings;

BEGIN {
    our @ISA = qw(Exporter);
    our @EXPORT = qw(&fetch &get_pe &get_pvb);
}

# downloads the stock info of the stocks passed as a parameter and
# can be used with the LIST returned by init_stock_conf
# TODO: prototype to put constraints on the parameter list
sub fetch { # class method
    my $class = shift;

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
sub _get_id {
    my $tag = shift;
    my $STOCK = shift;
    my $stock = lc $STOCK;

    open (STOCK, "<", "$ENV{HOME}/.idigger/rawdata/$stock.aspx") ||
        die "can't open $stock.aspx\n";

    my $value;
    while (<STOCK>) {
        if (/$tag/) {
            s/.*\">//;
            s/<.*//;
            s/,/./;
            chomp;
            $value = $_;
        }
    }

    return $value;
}

# P/E ratio (P/L in portuguese)
# returns P/E
# note: lower is better 
# TODO: prototype to put constraints on the parameter list
sub get_pe {
    my $class = shift;
    my $stock = shift;

    return _get_id('lbPrecoLucroAtual', $stock);
}

# P/VB ratio (P/VPA in portuguese)
# returns P/VB
# note: lower is better
# TODO: prototype to put constraints on the parameter list
sub get_pvb {
    my $class = shift;
    my $stock = shift;

    return _get_id('lbPrecoValorPatrimonialAtual', $stock);
}

END { }

1;
