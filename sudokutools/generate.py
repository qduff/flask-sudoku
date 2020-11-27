def generate():
    sudoku =   [[0, 0, 4,   0, 0, 0,   0, 6, 7],
                [3, 0, 0,   4, 7, 0,   0, 0, 5],
                [1, 5, 0,   8, 2, 0,   0, 0, 3],

                [0, 0, 6,   0, 0, 0,   0, 3, 1],
                [8, 0, 2,   1, 0, 5,   6, 0, 4],
                [4, 1, 0,   0, 0, 0,   9, 0, 0],

                [7, 0, 0,   0, 8, 0,   0, 4, 6],
                [6, 0, 0,   0, 1, 2,   0, 0, 0],
                [9, 3, 0,   0, 0, 0,   7, 1, 0]]
    
    solution = [[2, 8, 4,   5, 9, 3,   1, 6, 7],
                [3, 6, 9,   4, 7, 1,   8, 2, 5],
                [1, 5, 7,   8, 2, 6,   4, 9, 3],

                [5, 7, 6,   9, 4, 8,   2, 3, 1],
                [8, 9, 2,   1, 3, 5,   6, 7, 4],
                [4, 1, 3,   2, 6, 7,   9, 5, 8],

                [7, 2, 1,   3, 8, 9,   5, 4, 6],
                [6, 4, 5,   7, 1, 2,   3, 8, 9],
                [9, 3, 8,   6, 5, 4,   7, 1, 2]]
    
    sudokustr = ''
    for y in sudoku:
        for x in y:
            sudokustr+=str(x)
    
    solutionstr = ''
    for y in solution:
        for x in y:
            solutionstr+=str(x)
            

    return sudokustr, solutionstr

#sudoku, solution = generate()

#print(sudoku, solution)