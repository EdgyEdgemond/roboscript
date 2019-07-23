from collections import defaultdict


def execute(code):
    grid = defaultdict(int)

    tokens = tokenize(code)
    moves = compiler(tokens)

    position = (0, 0)
    movement = (0, 1)

    grid[position] = 1

    for move in moves:
        if move == "L":
            movement = left(movement)
        elif move == "R":
            movement = right(movement)
        else:
            position = (position[0] + movement[0], position[1] + movement[1])
            grid[position] = 1

    return render(grid)


def compiler(tokens):
    ret = []
    for token in tokens:
        if len(token) == 1:
            token = "{}1".format(token)

        cmd, count = token[0], int(token[1:])
        for i in range(count):
            ret.append(cmd)

    return ret


def render(grid):
    x = sorted([k[1] for k in grid])
    y = sorted([k[0] for k in grid])

    x_range = (x[0], x[-1])
    y_range = (y[0], y[-1])

    rows = []
    for i in range(y_range[0], y_range[1] + 1):
        row = []
        for j in range(x_range[0], x_range[1] + 1):
            row.append("*" if grid[(i, j)] else " ")
        rows.append("".join(row))

    return "\r\n".join(rows)


def left(movement):
    movements = [(0, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]
    return movements[movements.index(movement) + 1]


def right(movement):
    movements = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 1)]
    return movements[movements.index(movement) + 1]


def tokenize(code):
    ptr = 0

    tokens = []

    while ptr < len(code):
        t = code[ptr]
        ptr += 1
        token = [t]
        group = False
        if t == "(":
            group = True
            stack = 1
            while stack > 0:
                if code[ptr] == "(":
                    stack += 1
                if code[ptr] == ")":
                    stack -= 1
                token.append(code[ptr])
                ptr += 1
            token = tokenize("".join(token[1:-1]))

        count = []
        while ptr < len(code) and code[ptr].isdigit():
            count.append(code[ptr])
            ptr += 1

        if count:
            count = "".join(count)
            if not group:
                token.append(count)
            else:
                token = token * int(count)

        if group:
            tokens.extend(token)
        else:
            tokens.append("".join(token))

    return tokens
