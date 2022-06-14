## https://www.hackerrank.com/challenges/magic-square-forming/problem?isFullScreen=true
#!/bin/python3

import math
import os
import random
import re
import sys

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

class magicMatrix:
    def __init__(self, s):
        self.original = s
        self.complete = False
    
    def populate(self, s):
        self.current_pts = []
        for i, i_val in enumerate(s):
            for j, j_val in enumerate(s[i]):
                pt = matPoint(i, j, j_val, False);
                print(f"found {pt.x},{pt.y} with value {pt.val}: {pt.frozen}")
                self.current_pts[i,j] = pt
        
    # def calcSums(self):
    #     s = self.original
    #     row_sums = []
    #     col_sums = []
    #     td_diag_sum = 0
    #     bu_diag_sum = 0
    #     for i, i_val in enumerate(s):
    #         row_sums.append(sum(s[i]))
    #         for j, j_val in enumerate(s):
    #             if j == 0:
    #                 col_sums[j] = j_val
    #             else:
    #                 col_sums[j] += j_val
    #             if i == j:
    #                 td_diag_sum += j_val
    #             if i == len(s) - j:
    #                 bu_diag_sum += j_val
    #         print(f"row sums: {row_sums}")
    #         print(f"col sums: {col_sums}")
    #         print(f"td_diag_sum: {td_diag_sum}")
    #         print(f"bu_diag_sum: {bu_diag_sum}")
    #     return(row_sums, col_sums, td_diag_sum, du_diag_sum)

def formingMagicSquare(s):
    # Write your code here
    magic_mat = magicMatrix(s)
    magic_mat.populate(s)
    matic_mat.calcSums()

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = []
    s.append([5 3 4])
    s.append([1 5 8])
    s.append([6 4 2])
    #for _ in range(3):
    #    s.append(list(map(int, input().rstrip().split())))

    result = formingMagicSquare(s)

    print(result)
    #fptr.write(str(result) + '\n')

    #fptr.close()
