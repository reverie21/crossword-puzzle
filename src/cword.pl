#!/usr/bin/perl

use strict;
use warnings;

## create_length_hash
## input: array of words
## output: hash where the key is the word length
##  and the value is an array of words with that length
sub create_length_hash($) {
    my $w_choices_ref = shift(@_);
    my @w_choices = @{$w_choices_ref};
    
    my %length_hash = ();
    
    for my $c (@w_choices) {
        #print "choice $c\n";
        my $word_len = length($c);
        if($length_hash{$word_len} eq '') {
            $length_hash{$word_len} = [$c];
        } else {
            push(@{$length_hash{$word_len}}, $c);
        }
        my @tmp = @{$length_hash{length($c)}};
        #print "length hash for $c is now @tmp\n";
    }
    return \%length_hash;
}

sub create_options_hash($) {
    
    my $open_coords_ref = shift(@_);
    my @open_coords = @{$open_coords_ref};
    
    my @open_spaces = ();
    my %options_hash = ();

    for my $coord_set (@open_coords) {
        #print "coord_set: $coord_set\n";
        my ($x, $y) = @{$coord_set};
        #print "$x and $y for @open_spaces\n";
        if(@open_spaces > 0) {
            for my $prev_coord_set (@open_spaces) {
                my ($a, $b) = @{$prev_coord_set};
                my $n_result = is_neighbor($x, $y, $a, $b);
                #print "n_result for ($x,$y) and ($a,$b): $n_result\n";
                if ($n_result ne "none") {
                    #print "should I add $x, $y to $n_result?\n";
                    if (! defined $options_hash{$n_result}) {
                        #print "\tyes\n";
                        push(@{$options_hash{$n_result}[0]}, [$a, $b]);
                        push(@{$options_hash{$n_result}[0]}, [$x, $y]);
                    } else {
                        # "looking for which $n_result set\n";
                        my $added = 0;
                        for my $i (@{$options_hash{$n_result}}) {
                            #print "\t$n_result set $i -- ?\n";
                            for my $i_coords (@{$i}) {
                                my ($i_x, $i_y) = @{$i_coords};
                                #print "does $i_x == $a and $i_y == $b?\n";
                                if ($i_x == $a && $i_y == $b) {
                                    push(@{$i}, [$x, $y]);
                                    $added = 1;
                                    #push(@{$options_hash{$n_result}[$i]}, [$x, $y]);
                                }
                            }
                        }
                        if (!$added) {
                            my $next_ind = @{$options_hash{$n_result}}; 
                            push(@{$options_hash{$n_result}[$next_ind]}, [$a, $b]);
                            push(@{$options_hash{$n_result}[$next_ind]}, [$x, $y]);
                        }
                    }
                }
            } 
        }
        push(@open_spaces, [$x, $y]);
        #print "now open spaces has @open_spaces\n";
        #for my $oc (@open_spaces) {
        #    print "\t@{$oc}\n";
        #}
    }
    return \%options_hash;
}


sub remove_item_from_array($$) {
    my ($item, $ry_ref) = @_;
    my @ry = @{$ry_ref};
    #print "removing $item from @ry\n";
    
    my @new_ry = ();
    for my $i (@ry) {
        if ($i ne $item) {
            push(@new_ry, $i);
        }
    }
    #print "new ry: @new_ry\n";
    return(\@new_ry);
}

sub is_neighbor($$$$) {
    my ($x, $y, $a, $b) = @_;
    
    my $neighbor="none";
    if ($x == $a && abs($y-$b) <= 1) {
        $neighbor="row";
    } elsif ($b == $y && abs($x-$a) <= 1) {
        $neighbor="col";
    }
    
    return $neighbor;
}

sub find_word_intersect($$$$$$$) {
    my $word = shift(@_);
    my $x = shift(@_);
    my $y = shift(@_);
    my $word_orient = shift(@_);
    my $length_hash_ref = shift(@_);
    my $opt_ref = shift(@_);
    my $found_ref = shift(@_);
    
    my %opts = %{$opt_ref};
    
    if(keys(%opts) == 0) {
        print "Found everything!\n";
        return $found_ref;
    }
    
}

my @open_coords = ([1,1],[2,1],[2,2],[2,3],[3,1],[3,3]);
my @open_spaces = ();

my %options_hash = ();

%options_hash = %{create_options_hash(\@open_coords)};

my @orientations = keys(%options_hash);
print "there are @orientations in options hash\n";
for my $orient (@orientations) {
    print "$orient ::\n";
    for my $o_coord_set (@{$options_hash{$orient}}) {
        print "---\n";
        my @coords = @{$o_coord_set};
        for my $c (@coords) {
            my ($cx, $cy) = @{$c};
            print "$cx, $cy\n";
        }
    }
}



#my ($x,$y,$a,$b) = (1,2,1,3);
my ($x,$y,$a,$b) = (1,2,1,4);
my $neighbor_result = is_neighbor($x,$y,$a,$b);
print "$neighbor_result\n";

my @w_choices = ('BOB','ODD','DO');
my %length_hash = %{create_length_hash(\@w_choices)};

my %found_hash = ();


my @found_coords = ([1,3],[2,3]);
my $found_word = "DO";
my $found_orient = "col";
my $new_ry_ref = remove_item_from_array($found_word,\@w_choices);

@w_choices = @{$new_ry_ref};

print "now choices: @w_choices\n";

## go through each of the found coordinates
## search for intersecting words by coord and letter
for my $coord_set (@found_coords) {
    my ($x, $y) = @{$coord_set};
    print "$x and $y\n";
    #find_word_intersect($found_word, $x, $y, $found_orient, 
    #\%length_hash, \%options_hash, \%found_hash);
}





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
