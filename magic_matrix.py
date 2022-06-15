#!/bin/python3

import math
import os
import random
import re
import sys
import collections

#
# Complete the 'formingMagicSquare' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY s as parameter.
#

class matPoint:
    def __init__(self, x, y, val, frozen):
        self.x = x
        self.y = y
        self.val = val
        self.frozen = frozen
    def __str__(self):
        return "pt: ("+str(self.x)+","+str(self.y)+") with value "+str(self.val)+": "+str(self.frozen)
    def clone(self):
        new_x = self.x
        new_y = self.y
        new_val = self.val
        new_frozen = self.frozen
        return matPoint(new_x, new_y, new_val, new_frozen)

class magicMatrix:
    def __init__(self, s):
        self.original = s
        self.complete = False
        self.current_pts = matPoint(0,0,0,False)
        self.magic_number = 15
        self.row_matches = [10000] * 3
        self.col_matches = [10000] * 3
        self.td_diag_matches = 10000
        self.bu_diag_matches = 10000
        self.replacement_cost = 0
    
    def __str__(self):
        ret_str = ""
        for list_a in self.current_pts:
            for a in list_a:
                ptA = matPoint(a.x, a.y, a.val, a.frozen)
                ret_str += str(ptA)+"\n"
        return ret_str
    
    def populate(self, s):
        self.current_pts = []
        for i, i_val in enumerate(s):
            if i == 0:
                self.current_pts = [[]]
            else:
                self.current_pts.append([])
            for j, j_val in enumerate(s[i]):
                pt = matPoint(i, j, j_val, False);
                #print(f"found {pt.x},{pt.y} with value {pt.val}: {pt.frozen}")
                #print(pt)
                if i == 0:
                    #self.current_pts[0].append()
                    #ptB = pt.clone()
                    self.current_pts[0].append(pt)
                else:
                    #print(self.current_pts[i])
                    self.current_pts[i].append(pt)
                #print(f"\t{i},{j}:: ",self.current_pts[i][j])
        
    def calcSums_v0(self):
        s = self.original
        row_sums = []
        col_sums = []
        td_diag_sum = 0
        bu_diag_sum = 0
        for i, i_val in enumerate(s):
            row_sums.append(sum(s[i]))
            for j, j_val in enumerate(s[i]):
                if i == 0:
                    col_sums.append(j_val)
                else:
                    col_sums[j] += j_val
                if i == j:
                    td_diag_sum += j_val
                if i+j+1 == len(s):
                    bu_diag_sum += j_val
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.td_diag_sum = td_diag_sum
        self.bu_diag_sum = bu_diag_sum
        print(f"row sums: {row_sums}")
        print(f"col sums: {col_sums}")
        print(f"td_diag_sum: {td_diag_sum}")
        print(f"bu_diag_sum: {bu_diag_sum}")
        return(row_sums, col_sums, td_diag_sum, bu_diag_sum)
    
    def calcSums(self):
        print(self)
        s = self.current_pts
        row_sums = [0] * 3
        col_sums = [0] * 3
        td_diag_sum = 0
        bu_diag_sum = 0
        for list_idx, list_i in enumerate(s):
            for i, i_val in enumerate(list_i):
                col_sums[i] += i_val.val
                if i_val.x == i_val.y:
                    td_diag_sum += i_val.val
                if i_val.x + i_val.y + 1 == len(s):
                    bu_diag_sum += i_val.val
                row_sums[list_idx] += i_val.val
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.td_diag_sum = td_diag_sum
        self.bu_diag_sum = bu_diag_sum
        print(f"row sums: {row_sums}")
        print(f"col sums: {col_sums}")
        print(f"td_diag_sum: {td_diag_sum}")
        print(f"bu_diag_sum: {bu_diag_sum}")
        return(row_sums, col_sums, td_diag_sum, bu_diag_sum)
    
    def freeze_bu_diag(self):
        for list_idx, list_i in enumerate(self.current_pts):
            for idx, i in enumerate(list_i):
                #print(i.x, ",", i.y)
                if i.x+i.y+1 == len(self.current_pts):
                    self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val, True)
    
    def freeze_td_diag(self):
        for list_idx, list_i in enumerate(self.current_pts):
            for idx, i in enumerate(list_i):
                #print(i.x, ",", i.y)
                if i.x == i.y:
                    self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val, True)
    
    def freeze_row(self, row_num):
        for list_idx, list_i in enumerate(self.current_pts):
            for idx, i in enumerate(list_i):
                if i.x == row_num:
                    print("freeze row: ", i.x, ",", i.y)
                    self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val, True)
    
    def freeze_col(self, col_num):
        for list_idx, list_i in enumerate(self.current_pts):
            for idx, i in enumerate(list_i):
                if i.y == col_num:
                    print("freeze col: ", i.x, ",", i.y)
                    self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val, True)
    
    def findDiagMatch(self):
        change_count = 0
        if self.td_diag_matches == 0 and self.bu_diag_matches != 0:
            print("now?")
            for list_idx, list_i in enumerate(self.current_pts):
                print("here, ", list_i)
                for idx, i in enumerate(list_i):
                    print("in find diag match:", i.x, ",", i.y)
                    if i.x+i.y+1 == len(self.current_pts):
                        row_diff = self.row_matches[i.x]
                        col_diff = self.col_matches[i.y]
                        bu_diag_diff = self.bu_diag_matches
                        overlaps = list(set([row_diff, col_diff, bu_diag_diff]))
                        print("overlaps: ", overlaps)
                        if len(overlaps) < 3 and bu_diag_diff != 0:
                            print("\toverlaps: ", overlaps)
                            if ((row_diff == col_diff or row_diff == bu_diag_diff) and row_diff != 10000):
                                print(f"\trow diff for {i}: ", row_diff)
                                print(f"\tadjusting {i.x},{i.y} to be {i.val}+{row_diff}")
                                self.replacement_cost += abs(row_diff)
                                self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val+row_diff, True)
                                change_count += 1
                                self.calcSums()
                                self.findMagicMatches()
        if self.bu_diag_matches == 0 and self.td_diag_matches != 0:
            for list_idx, list_i in enumerate(self.current_pts):
                #print("here, ", list_i)
                for idx, i in enumerate(list_i):
                    print("in find diag match for td_diag_matches:", i.x, ",", i.y)
                    if i.x == i.y:
                        row_diff = self.row_matches[i.x]
                        col_diff = self.col_matches[i.y]
                        td_diag_diff = self.td_diag_matches
                        print("\t td diag diff: ", td_diag_diff)
                        overlaps = list(set([row_diff, col_diff, td_diag_diff]))
                        if len(overlaps) < 3 and td_diag_diff != 0:
                            print("\toverlaps: ", overlaps)
                            if ((row_diff == col_diff or row_diff == td_diag_diff) and row_diff != 10000):
                                print(f"\trow diff for {i}: ", row_diff)
                                print(f"\tadjusting {i.x},{i.y} to be {i.val}+{row_diff}")
                                self.replacement_cost += abs(row_diff)
                                self.current_pts[list_idx][idx] = matPoint(i.x, i.y, i.val+row_diff, True)
                                change_count += 1
                                self.calcSums()
                                self.findMagicMatches()
        if change_count > 0:
            print(self)
            self.calcSums()
            self.findMissingMatches()
    
    def findMissingMatches(self):
        change_count = 0
        row_sum_diff = sum(self.row_matches)
        print(f"row matches: {self.row_matches} and row_sum_diff: {row_sum_diff}")
        print(f"col matches: {self.col_matches} and col_sum_diff....")
        if self.row_matches != [0, 0, 0]:
            for row_num, r_val in enumerate(self.row_matches):
                if self.row_matches[row_num] != 0:
                    print(f"searching for a row match for {self.row_matches[row_num]} within {self.col_matches}")
                    col_idx = (self.col_matches).index(self.row_matches[row_num])
                    if col_idx is not None:
                        print(f"* found a match at index {col_idx}: {self.col_matches}")
                        prev_pt_val = self.current_pts[row_num][col_idx].val
                        print(f"* adjust row: {col_idx},{row_num} to now have {prev_pt_val}+{self.row_matches[row_num]}")
                        self.replacement_cost += abs(self.row_matches[row_num])
                        self.current_pts[row_num][col_idx] = matPoint(col_idx, row_num, prev_pt_val+self.row_matches[row_num], True)
                        change_count += 1
                        self.calcSums()
                        self.findMagicMatches()
                        next
        col_sum_diff = sum(self.col_matches)
        print(f"col matches: {self.col_matches} and col_sum_diff: {col_sum_diff}")
        #row_with_missing = (self.row_matches).index(row_sum_diff) 
        #if row_with_missing is not None:
        #    print("Calculate the missing value for row ", row_with_missing)
        if change_count > 0:
            print(self)
            #pass
            self.calcSums()
            self.findMagicMatches()
    
    
    def findMagicMatches(self):
        for r, r_val in enumerate(self.row_sums):
            print("comparing ", r_val," and ",self.magic_number, " while known match ", self.row_matches[r])
            if self.row_matches[r] != 0:
                row_sum_diff = self.magic_number - r_val
                self.row_matches[r] = row_sum_diff
                if row_sum_diff == 0:
                    print("\t freeze row ",r)
                    self.freeze_row(r)
        for c, c_val in enumerate(self.col_sums):
            print("comparing ", c_val," and ",self.magic_number,  " while known match ", self.col_matches[c])
            if self.col_matches[c] != 0:
                col_sum_diff = self.magic_number - c_val
                self.col_matches[c] = col_sum_diff
                if col_sum_diff == 0:
                    print("\t freeze col", c)
                    self.freeze_col(c)
        if self.td_diag_matches != 0:
            td_diag_diff = self.magic_number - self.td_diag_sum
            self.td_diag_matches = td_diag_diff
            if td_diag_diff == 0:
                print("\tfreeze td diag")
                self.freeze_td_diag()
        if self.bu_diag_matches != 0:
            bu_diag_diff = self.magic_number - self.bu_diag_sum
            self.bu_diag_matches = bu_diag_diff
            if bu_diag_diff == 0:
                print("\tfreeze bu diag")
                self.freeze_bu_diag()
        print("row matches", self.row_matches)
        print("col matches", self.col_matches)
        print("td_diag_matches", self.td_diag_matches)
        print("bu_diag_matches", self.bu_diag_matches)
        #print(self)
        #self.calcSums()
        #self.findDiagMatch()
        #self.findMissingMatches()


def formingMagicSquare(s):
    # Write your code here
    magic_mat = magicMatrix(s)
    magic_mat.populate(s)
    magic_mat.calcSums()
    magic_mat.findMagicMatches()
    magic_mat.calcSums()
    magic_mat.findDiagMatch()
    
    print("#"*10)
    print(magic_mat)
    print(magic_mat.replacement_cost)

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = []
    scenario = 3
    if scenario == 1:
        s.append([5, 3, 4])
        s.append([1, 5, 8])
        s.append([6, 4, 2])
    elif scenario == 2:
        s.append([4, 9, 2])
        s.append([3, 5, 7])
        s.append([8, 1, 5]) 
    elif scenario == 3:
        s.append([4, 8, 2])
        s.append([4, 5, 7])
        s.append([6, 1, 6]) 
    #for _ in range(3):
    #    s.append(list(map(int, input().rstrip().split())))

    result = formingMagicSquare(s)
    print(result)
    #fptr.write(str(result) + '\n')

    #fptr.close()
