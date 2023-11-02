"""
Variabile: pozitiile din tabla initiala care sunt 0
Domenii: {1..9}
Restrictii: Nu se poate repeta aceeasi cifra pe linie, coloana, sau intr-unul din patratele de 3x3
            De asemenea, pe pozitiile marcate pot fi doar cifre pare
"""
import copy
import model_util
import arc_consistency
import forward_checking
import forward_checking2


print("forward_checking".center(50,'='))
forward_checking.print_sol(model_util.problem)

print("forward_checking2".center(50,'='))
forward_checking2.print_sol(model_util.problem)

print("arc_consistency".center(50,'='))
arc_consistency.print_sol(model_util.problem)

model_util.initial_board[0][2] = 0
model_util.initial_board[6][4] = 4
model_util.initial_board[4][4] = 8
model_util.problem = (model_util.initial_board, model_util.par_pos)
# for row in model_util.problem[0]:
#     print(row)

print("forward_checking".center(50,'='))
forward_checking.print_sol(model_util.problem)

print("forward_checking2".center(50,'='))
forward_checking2.print_sol(model_util.problem)

print("arc_consistency".center(50,'='))
arc_consistency.print_sol(model_util.problem)