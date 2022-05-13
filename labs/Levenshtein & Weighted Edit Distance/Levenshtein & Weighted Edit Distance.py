import numpy as np
import json
 
# Opening JSON file
f1 = open('confusing_row.json')
f2 = open('confusing_column.json')
f3 = open('confusing_matrix.json')
 
# returns JSON object as
# a dictionary
deletion = json.load(f1)
insertion = json.load(f2)
sub = json.load(f3)


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 2,
                    matrix[x,y-1] + 1
                )
    return matrix

def weighted(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + insertion[word2[y-1]],
                    matrix[x-1, y-1] + sub[word1[x-1]][word2[y-1]],
                    matrix[x, y-1] + deletion[word1[x-1]]
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + insertion[word2[y-1]],
                    matrix[x-1,y-1] + sub[word1[x-1]][word2[y-1]],
                    matrix[x,y-1] + deletion[word1[x-1]]
                )
    return matrix

word1 = "intention"
word2 = "execution"
res = levenshtein("intention", "execution")
res2 = weighted("intention", "execution")
j = res.shape[0]-1
i = res.shape[1]-1
res_lst = []
while i != 0 or j != 0:
    if i != 0 and j == 0:
        while i > 0: 
            res_lst.append('insertion')
            i -= 1    

    if j != 0 and i == 0 :
        while j > 0 : 
            res_lst.append('remove')
            j -= 1

    res_min = min(res[j-1][i-1] + (0 if word1[j - 1] == word2[i - 1] else 2), res[j-1][i] + 1, res[j][i-1] + 1)
    if (word1[j - 1] == word2[i - 1] and res_min == res[j][i]):
        res_lst.append('')
        i -= 1
        j -= 1
    elif res_min == res[j - 1][i - 1] + 2:
        res_lst.append('switch')
        i -= 1
        j -= 1
    elif res_min == res[j-1][i] + 1:
        res_lst.append('deletion')
        j -= 1
    elif res_min == res[j][i-1] + 1:
        res_lst.append('insertion')
        i -= 1
    #print(i, j, res_min)
res_lst.reverse()
print(res)
print(res_lst)
print(res2)

