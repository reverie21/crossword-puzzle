use strict;

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

sub remove_options($$) {
    my $orientations_ref = shift(@_);
    my $remove_coords_ref = shift(@_);
    
    my @new_ry = ();
     for my $o_coord_set (@{$orientations_ref}) {
        my @coords = @{$o_coord_set};
        my @saved_coords = ();
        #print "--\n";
        my $match_count = 0;
        for my $c (@coords) {
            my ($cx, $cy) = @{$c};
            for my $remove_set (@{$remove_coords_ref}) {
                my ($remove_x, $remove_y) = @{$remove_set};
                #print "does $cx, $cy match $remove_x, $remove_y?\n";
                if (!($cx == $remove_x && $cy == $remove_y)) {
                    $match_count++;
                }
            }
        }
        if($match_count != @coords) {
            push(@new_ry, \@coords);
        }
    }
    
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

sub find_coords_with_wordlen($$) {
    my $options_hash_ref = shift(@_);
    my $wordlen = shift(@_);
    
    my %options_hash = %{$options_hash_ref};
    my @orientations = keys(%options_hash);
    
    my $coords_of_interest_ref = "";
    
    for my $orient (@orientations) {
        #print "$orient ::\n";
        for my $o_coord_set (@{$options_hash{$orient}}) {
            #print "---\n";
            my @coords = @{$o_coord_set};
            if (@coords == $wordlen) {
                $coords_of_interest_ref = $o_coord_set;
            }
        }
    }
    
    return $coords_of_interest_ref;
}
sub find_matching_word($$$) {
    my $word_list_ref = shift(@_);
    my $new_char_index = shift(@_);
    my $orig_char = shift(@_);
    
    my @words = @{$word_list_ref};
    
    my @ry = ();
    for my $w (@words) {
        #print "does this word '$w' have '$orig_char' at position $new_char_index?\n";
        my $candidate_letter = substr($w, $new_char_index, 1);
        if ($candidate_letter eq $orig_char) {
            #print "Yes!\n";
            push(@ry, $w);
        #} else {
        #   print "No... $candidate_letter does not equal $orig_char\n";
        }
    }
    
    return (\@ry);
}

sub save_found_word_coords($$$) {
    my $found_word = shift(@_);
    my @found_coords = @{shift(@_)};
    my @found_ry = @{shift(@_)};
    
    for (my $f_index=0; $f_index < @found_coords; $f_index++) {
        my ($f_x, $f_y) = @{$found_coords[$f_index]};
        my $f_char = substr($found_word,$f_index,1);
        $found_ry[$f_x][$f_y] = $f_char;
        print "saving $f_x, $f_y as $f_char\n";
    }
    return \@found_ry;
}

sub find_word_intersect($$$$$$$) {
    my $word_char = shift(@_);
    my $x = shift(@_);
    my $y = shift(@_);
    my $word_orient = shift(@_);
    my $length_hash_ref = shift(@_);
    my $opt_ref = shift(@_);
    my $found_ref = shift(@_);
    
    my %opts = %{$opt_ref};
    my %lens = %{$length_hash_ref};
    my @found_ry = @{$found_ref};
    
    my @remaining_words = ();
    for my $w_len (keys(%lens)) {
        for my $w_with_len (@{$lens{$w_len}}) {
            push(@remaining_words, $w_with_len);
        }
    }
    
    print "remaining_words: ".@remaining_words."\n";
    if(@remaining_words == 0) {
        print "Found everything!\n";
        return $found_ref;
    } else {
        my $new_orient = "row";
        if ($word_orient eq $new_orient) {
            $new_orient = "col";
        }
        print "#######################\n";
        print "I will be looking for a new word within a $new_orient\n";
        print "This new word will intersect with $word_char\n";
        print "Does the intersection happen at ($x, $y)?\n";
        print "Available words: \n";
        for my $len (keys(%lens)) {
            print "- Length $len:\n";
            for my $w_ref ($lens{$len}) {
                for my $w (@{$w_ref}) {
                    print "   $w\n";
                }
            }
        }
        
        for my $o_coord_set (@{$opts{$new_orient}}) {
            print "---\n";
            my @coords = @{$o_coord_set};
            my $char_index = 0;
            for my $c (@coords) {
                my ($cx, $cy) = @{$c};
                print "$cx, $cy\n";
                if ($cx == $x && $cy == $y) {
                    print "Found a matching coord!\n";
                    print "Position is $char_index\n";
                    print "Word length is ".@coords."\n";
                    my @candidates = @{find_matching_word($lens{@coords}, $char_index, $word_char)};
                    
                    if (@candidates == 1) {
                        ## cleanup
                        my $found_word = $candidates[0];
                        
                        print "cleaning up.... for $found_word\n";
                        my @found_coords = @{$o_coord_set};
                        my $found_orient = $new_orient;
        
                        @found_ry = @{save_found_word_coords($found_word, $o_coord_set, \@found_ry)};
                        
                        my $found_word_length = length($found_word);
                        my $new_word_len_ref = remove_item_from_array($found_word, $lens{$found_word_length});
                        
                        $lens{$found_word_length} = $new_word_len_ref;
                        
                        $opts{$found_orient} = remove_options($opts{$found_orient}, \@found_coords);
                        
                        my $new_char_index = 0;
                        #for my $coord_set (@found_coords) {
                        my $coord_set = $found_coords[0];
                        my ($x, $y) = @{$coord_set};
                        print "new fxn call ::: $x and $y\n";
                        find_word_intersect(substr($found_word,$new_char_index,1), $x, $y, $found_orient, 
                        \%lens, \%opts, \@found_ry);
                        #$new_char_index++;
                        #}
                    }
                }
                $char_index++;
            }
        }
        
        return \@found_ry;
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

my @found_ry = (["-","-","-","-"],["-","-","-","-"],["-","-","-","-"],["-","-","-","-"]);


my $found_word = "";
my @found_coords = ();

## go through length hash array 
## and see if there are any word lengths with only one word
for my $len (keys(%length_hash)) {
    print "length is $len\n";
    my @num_words = @{$length_hash{$len}};
    print "\t has ".@num_words." num words\n";
    if (@num_words == 1) {
        $found_word = $num_words[0];
        my $found_coords_ref = find_coords_with_wordlen(\%options_hash, $len);
        @found_coords = @{$found_coords_ref};
        my $char_index = 0;
        for my $coord_set (@found_coords) {
            my ($c_x, $c_y) = @{$coord_set};
            $found_ry[$c_x][$c_y] = substr($found_word, $char_index++,1);
            #print "$found_word must be at $c_x and $c_y\n";
        }
    }
}

## TODO: find the orientation of the found coordinates
## TODO: if any of the words are not a unique length, choose one

#$found_ry[2][3] = "D";
#$found_ry[3][3] = "0";

#my @found_coords = ([2,3],[3,3]);
#my $found_word = "DO";
my $found_orient = "col";

###############
    ## cleanup
    my $new_ry_ref = remove_item_from_array($found_word,\@w_choices);
    my $found_word_length = length($found_word);
    my $new_word_len_ref = remove_item_from_array($found_word, $length_hash{$found_word_length});
    
    
    @w_choices = @{$new_ry_ref};
    $length_hash{$found_word_length} = $new_word_len_ref;
    
    print "now choices: @w_choices\n";
    
    $options_hash{$found_orient} = remove_options($options_hash{$found_orient}, \@found_coords);
    
    print "REMOVAL. now options: \n";
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
################


## go through each of the found coordinates
## search for intersecting words by coord and letter
my $char_index = 0;
#for my $coord_set (@found_coords) {
my $coord_set = $found_coords[0];
    my ($x, $y) = @{$coord_set};
    print "$x and $y\n";
    my @final_found = @{find_word_intersect(substr($found_word,$char_index,1), $x, $y, $found_orient, 
    \%length_hash, \%options_hash, \@found_ry)};
    $char_index++;
#}
print "#######################\n";
print "#######################\n";
print "#######################\n";

for (my $fi=0; $fi < @final_found; $fi++) {
    print join('', @{$final_found[$fi]})."\n";
}

