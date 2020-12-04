from sudokutools.Sudoku.Generator import *

# setting difficulties and their cutoffs for each solve method
difficulties = {
    'easy': (35, 0), 
    'medium': (81, 5), 
    'hard': (81, 10), 
    'extreme': (81, 15)
}


def generate(difficulty = 'easy'):
    difficulty = difficulties[difficulty]
    gen = Generator()
    gen.randomize(100)

    solution = str(gen.board.copy())

    gen.reduce_via_logical(difficulty[0])

    if difficulty[1] != 0:
        gen.reduce_via_random(difficulty[1])

    final = str(gen.board.copy())

    return final, solution
    # printing out board after reduction
    
