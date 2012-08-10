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

# Stock Class 

# this class makes use of a "support" class that downloads files to
# extract data, such as GI or other 
package Stock;

use strict;
use warnings;
use Exporter;

BEGIN {
    our @ISA = qw(Exporter);
    our @EXPORT = qw(&new &name &pe &roe &pvb);
}

our $Stock;

sub new {
    my $class = shift;
    my $self = {};
    $Stock++;

    # instance attributes
    if (@_) {
        $self->{NAME} = shift;
    } else {
        $self->{NAME} = undef;
    }
    $self->{PE} = undef;
    $self->{ROE} = undef;
    $self->{PVB} = undef;

    bless ($self, $class);
    return $self;
}

sub name {
    my $self = shift;

    if (@_) { 
        $self->{NAME} = shift;
        print "set NAME to $self->{NAME}\n";
    }
    return $self->{NAME};
}

sub pe {
    my $self = shift;

    if (@_) {
        $self->{PE} = shift;
    }

    return $self->{PE};
}

sub roe {
    my $self = shift;

    if (@_) {
        $self->{ROE} = shift;
    }

    return $self->{ROE};
}

sub pvb {
    my $self = shift;

    if (@_) {
        $self->{PVB} = shift;
    }

    return $self->{PVB};
}

END { }

1;
