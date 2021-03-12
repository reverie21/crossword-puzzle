#!/usr/bin/perl

use strict;
use warnings;

# Complete the crosswordPuzzle function below.
sub crosswordPuzzle {


}

open(my $fptr, '>', $ENV{'OUTPUT_PATH'});

my @crossword = ();

for (1..10) {
    my $crossword_item = <>;
    chomp($crossword_item);
    push @crossword, $crossword_item;
}

my $words = <>;
chomp($words);

my @result = crosswordPuzzle \@crossword, $words;

print $fptr join "\n", @result;
print $fptr "\n";

close $fptr;
