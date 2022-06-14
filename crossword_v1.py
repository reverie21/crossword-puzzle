#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'crosswordPuzzle' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. STRING_ARRAY crossword
#  2. STRING words
#
## create_length_hash
## input: array of words
## output: hash where the key is the word length
##  and the value is an array of words with that length
def create_length_hash(word_ry):
    len_hash = {}

    for word in word_ry:
        #print(f"word is {word}")
        word_len = len(word)
        if word_len not in len_hash.keys():
            len_hash[word_len] = [];
        len_hash[word_len].append(word);
    
    return len_hash

def create_options_hash(open_coords):
    
    open_spaces = [];
    options_hash = {};

    for coord_set in open_coords:
        #print "coord_set: $coord_set\n";
        (x, y) = coord_set
        #print(f"x: {x}, y: {y}")
        #print "$x and $y for @open_spaces\n";
        if len(open_spaces) > 0:
            for prev_coord_set in open_spaces:
                (a, b) = prev_coord_set
                n_result = is_neighbor(x, y, a, b)
                #print(f"{n_result} for {x}, {y} and {a}, {b}")
                if n_result is not None:
                    if n_result not in options_hash.keys():
                        options_hash[n_result] = []
                        two_coords = [(a, b), (x, y)]
                        options_hash[n_result].append(two_coords)
                        #options_hash[n_result].append((x, y))
                    else:
                        added = 0
                        for i_ind, i_set in enumerate(options_hash[n_result]):
                            for (i_x, i_y) in i_set:
                                #print(f"i_x: {i_x} and i_y: {i_y} compared to {a} and {b}")
                                if i_x == a and i_y == b:
                                    options_hash[n_result][i_ind].append((x, y))
                                    added = 1
                                #print(f"\t\tadded: {added}")
                        if added == 0:
                            #options_hash[n_result].append((a,b))
                            #options_hash[n_result].append((x,y))
                            #two_coords = [(a, b), (x, y)]
                            next_ind = len(options_hash[n_result])
                            options_hash[n_result].append([])
                            options_hash[n_result][next_ind].append((a, b))
                            options_hash[n_result][next_ind].append((x, y))
                            #print(f"now options_hash with {n_result} for index {next_ind} has {options_hash[n_result][next_ind]}")
        open_spaces.append((x, y))
    return options_hash

def is_neighbor(x, y, a, b):
    neighbor = None
    if x == a and abs(y-b) <= 1:
        neighbor = "row"
    elif b == y and abs(x-a) <= 1:
        neighbor = "col";
    
    return neighbor;


def read_coords(coords):
    open_coords = []
    for rind, rval in enumerate(coords):
        for cind, cval in enumerate(list(rval)):
            #print(f"{rind},{cind}: {cval}")
            if cval == "-":
                open_coords.append((rind, cind))
                
    return open_coords

def find_coords_with_wordlen(options_hash, word_len):
    
    orientations = options_hash.keys()
    coords_of_interest = ""
    found_orient = None
    
    result_array = []
    
    for orient in orientations:
        #print "$orient ::\n";
        #print(f"{orient}")
        for o_coord_set in options_hash[orient]:
            num_coords = len(o_coord_set)
            #print(f"{num_coords} with {o_coord_set}")
            if num_coords == word_len:
                coords_of_interest = o_coord_set
                found_orient = orient
                result_array.append((found_orient, coords_of_interest))
    
    return result_array


def find_coords_with_wordlen_v0(options_hash, word_len):
    
    orientations = options_hash.keys()
    coords_of_interest = ""
    found_orient = None
    
    for orient in orientations:
        #print "$orient ::\n";
        #print(f"{orient}")
        for o_coord_set in options_hash[orient]:
            num_coords = len(o_coord_set)
            #print(f"{num_coords} with {o_coord_set}")
            if num_coords == word_len:
                coords_of_interest = o_coord_set
                found_orient = orient
    
    return (found_orient, coords_of_interest);

def find_word_intersect(word_char, x, y, word_orient, len_hash, options_hash, found_ry, all_found_coords):
    
    remaining_words = []
    for w_len in len_hash.keys():
        for w_with_len in len_hash[w_len]:
            remaining_words.append(w_with_len)
    
    #print(f"remaining_words: {remaining_words}")
    
    if len(remaining_words) == 0:
        #print("Found everything!")
        return (remaining_words, len_hash, options_hash, found_ry, all_found_coords)
    else:
        new_orient = word_orient
            
        for coords in options_hash[new_orient]:
            #print("---\n")
            char_index = 0
            for (cx, cy) in coords:
                #print(f"{cx}, {cy} == {x},{y}?");
                if cx == x and cy == y:
                    for char_index in range (0, len(coords)):
                        #print(f"Found a matching coord!\n");
                        #print(f"Position is {char_index}\n");
                        #print(f"Word length is ", len(coords),"\n");
                        candidates = find_matching_word(len_hash[len(coords)], char_index, word_char)
                        #print(f"candidates: {candidates}")
                        
                        if len(candidates) == 1:
                            ## cleanup
                            found_word = candidates[0]
                            
                            found_coords = coords
                            found_orient = new_orient
            
                            (found_ry, all_found_coords) = save_found_word_coords(found_word, coords, found_ry, all_found_coords)
                            
                            found_word_length = len(found_word)
                            if found_word in remaining_words:
                                #print(f"words: {remaining_words}")
                                remaining_words.remove(found_word)
                                #print(f"removing {found_word} from len_hash")
                            if len_hash[found_word_length] and found_word in len_hash[found_word_length]:
                                len_hash[found_word_length].remove(found_word)
                            #print(f"{len_hash}")
                            if found_coords in options_hash[found_orient]:
                                options_hash[found_orient].remove(found_coords)
                            (remaining_words, len_hash, options_hash, found_ry, all_found_coords) = check_multiple(remaining_words, len_hash, options_hash, found_ry, all_found_coords)
    return (remaining_words, len_hash, options_hash, found_ry, all_found_coords)

def find_matching_word(words, new_char_index, orig_char):
   
    matching_words = [];
    for word in words:
        #print "does this word '$w' have '$orig_char' at position $new_char_index?\n";
        #print(f"does this word {word} have {orig_char} at position {new_char_index}?")
        candidate_letter = word[new_char_index]
        if candidate_letter == orig_char:
            matching_words.append(word)
    
    return matching_words


def save_found_word_coords(found_word, found_coords, found_ry, all_found_coords):
    
    char_index = 0
    for (c_x, c_y) in found_coords:
        #print(f"{found_word} at {c_x},{c_y}: {found_word[char_index]} which is currently {found_ry[c_y][c_x]}")
        found_ry[c_x][c_y] = found_word[char_index]
        char_index += 1
        all_found_coords.append((c_x, c_y))
    return (found_ry, all_found_coords)

def check_single_wordlength(words, len_hash, options_hash, found_ry, all_found_coords):
    ## go through length hash array 
    ## and see if there are any word lengths with only one word
    for word_len in len_hash.keys():
        #print(f"length is {word_len}")
        num_words = len_hash[word_len]
        #print(f"\thas {num_words} num words\n")
        if len(num_words) == 1:
            found_word = num_words[0]
            result_array = find_coords_with_wordlen(options_hash, word_len)
            if len(result_array) > 0:
                (found_orient, found_coords) = result_array[0]
                char_index = 0
                for (c_x, c_y) in found_coords:
                    #print(f"{found_word} at {c_x},{c_y}: {found_word[char_index]} which is currently {found_ry[c_y][c_x]}")
                    found_ry[c_x][c_y] = found_word[char_index]
                    char_index += 1
                    all_found_coords.append((c_x, c_y))
                #print(found_ry)
                if found_word in words:
                    #print(f"words: {words}")
                    words.remove(found_word)
                #print(f"removing {found_word} from len_hash")
                if found_word in len_hash[word_len]:
                    len_hash[word_len].remove(found_word)
                #print(f"{len_hash}")
                if found_coords in options_hash[found_orient]:
                    options_hash[found_orient].remove(found_coords)
                #print("all found coords: {all_found_coords}")
                (words, len_hash, options_hash, found_ry, all_found_coords) = check_single_wordlength(words, len_hash, options_hash, found_ry, all_found_coords)
            
    return (words, len_hash, options_hash, found_ry, all_found_coords)

def check_multiple(words, len_hash, options_hash, found_ry, all_found_coords):
    ## go through length hash array 
    ## and see if there are any word lengths with only one word
    for word_len in len_hash.keys():
        #print(f"length is {word_len}")
        num_words = len_hash[word_len]
        #print(f"\thas {num_words} num words\n")
        if len(num_words) == 1:
            found_word = num_words[0]
            result_array = find_coords_with_wordlen(options_hash, word_len)
            if len(result_array) > 0:
                (found_orient, found_coords) = result_array[0]
                char_index = 0
                for (c_x, c_y) in found_coords:
                    #print(f"{found_word} at {c_x},{c_y}: {found_word[char_index]} which is currently {found_ry[c_y][c_x]}")
                    found_ry[c_x][c_y] = found_word[char_index]
                    char_index += 1
                    all_found_coords.append((c_x, c_y))
                #print(found_ry)
                if found_word in words:
                    #print(f"words: {words}")
                    words.remove(found_word)
                #print(f"removing {found_word} from len_hash")
                if found_word in len_hash[word_len]:
                    len_hash[word_len].remove(found_word)
                #print(f"{len_hash}")
                if found_coords in options_hash[found_orient]:
                    options_hash[found_orient].remove(found_coords)
                #print("all found coords: {all_found_coords}")
                (words, len_hash, options_hash, found_ry, all_found_coords) = check_single_wordlength(words, len_hash, options_hash, found_ry, all_found_coords)
        elif len(num_words) > 1:
            for test_word in num_words:
                #print(f"remaining options: {options_hash}")
                result_array = find_coords_with_wordlen(options_hash, word_len)
                if len(result_array) > 0:
                    for (test_orient, test_coords) in result_array:
                        for (c_x, c_y) in test_coords:
                            for (found_x, found_y) in all_found_coords:
                                #print(f"comparing test_coords {c_x},{c_y} with found {found_x},{found_y}")
                                if (found_x == c_x and found_y == c_y):
                                    #print(f"does {found_ry[c_x][c_y]} have a matching word in {len_hash}?")
                                    (words, len_hash, options_hash, found_ry, all_found_coords) = find_word_intersect(found_ry[c_x][c_y], found_x, found_y, test_orient, len_hash, options_hash, found_ry, all_found_coords)
                                    
    return (words, len_hash, options_hash, found_ry, all_found_coords)

def crosswordPuzzle(crossword, words):
    word_inputs = words.split(';')
    len_hash = create_length_hash(word_inputs)
    
    open_coords = read_coords(crossword)
    options_hash = create_options_hash(open_coords);
    
    found_ry = []
    for i in range(11):
        found_ry.append([])
        for j in range(11):
            found_ry[i].append('+')
    
    all_found_coords = []
    
    (words, len_hash, options_hash, found_ry, all_found_coords) = check_single_wordlength(word_inputs, len_hash, options_hash, found_ry, all_found_coords)
    
    (words, len_hash, options_hash, found_ry, all_found_coords) = check_multiple(word_inputs, len_hash, options_hash, found_ry, all_found_coords)
    
    return found_ry



if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    crossword = []

    #for _ in range(2):
    #    crossword_item = input()
    #    crossword.append(crossword_item)
    scenario = 3
    if scenario == 1:
        crossword.append('+-++++++++')
        crossword.append('+-++++++++')
        crossword.append('+-++++++++')
        crossword.append('+-----++++')
        crossword.append('+-+++-++++')
        crossword.append('+-+++-++++')
        crossword.append('+++++-++++')
        crossword.append('++------++')
        crossword.append('+++++-++++')
        crossword.append('+++++-++++')
    
        #words = input()
        words = 'LONDON;DELHI;ICELAND;ANKARA'
    elif scenario == 2:
        crossword.append('+-++++++++')
        crossword.append('+-++++++++')
        crossword.append('+-------++')
        crossword.append('+-++++++++')
        crossword.append('+-++++++++')
        crossword.append('+------+++')
        crossword.append('+-+++-++++')
        crossword.append('+++++-++++')
        crossword.append('+++++-++++')
        crossword.append('++++++++++')
       
        words = 'AGRA;NORWAY;ENGLAND;GWALIOR'
    elif scenario == 3:
        crossword.append('++++++-+++')
        crossword.append('++------++')
        crossword.append('++++++-+++')
        crossword.append('++++++-+++')
        crossword.append('+++------+')
        crossword.append('++++++-+-+')
        crossword.append('++++++-+-+')
        crossword.append('++++++++-+')
        crossword.append('++++++++-+')
        crossword.append('++++++++-+')
       
        words= 'ICELAND;MEXICO;PANAMA;ALMATY'
       
    
    result = crosswordPuzzle(crossword, words)
    
    for r in result:
        print(''.join(r))
    #print('\n'.join(result))
    #fptr.write('\n'.join(result))
    #fptr.write('\n')

    #fptr.close()
