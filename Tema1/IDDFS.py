import model

def __IDDFS__(state, current_depth, depth):
    #print(state, current_depth, depth)
    if current_depth == depth:
        if model.is_final(state):
            return []
        else:
            return None
    for move in model.dirs:
        if model.validate(state, move):
            st = model.transition(state, move)
            rez = __IDDFS__(st, current_depth + 1, depth)
            if rez is not None:
                return [move] + rez


def IDDFS(state):
    i = 0
    rez = __IDDFS__(state, 0, i)
    while rez is None:
        i += 1
        rez = __IDDFS__(state, 0, i)
    return rez