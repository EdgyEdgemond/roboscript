from collections import defaultdict


def stringify(l, joiner=""):
    return joiner.join(l)


def execute(code):
    grid = defaultdict(int)

    scope = {}
    tokens = tokenize(code, scope)
    moves = compiler(tokens, scope)

    position = (0, 0)
    movement = (0, 1)

    grid[position] = 1

    for move in moves:
        if move in "LR":
            movement = move_robot(movement, move)
        else:
            position = (position[0] + movement[0], position[1] + movement[1])
            grid[position] = 1

    return render(grid)


def compiler(tokens, scope):
    ret = []
    for token in tokens:
        if len(token) == 1:
            token = "{}1".format(token)

        cmd, count = token[0], token[1:]
        if cmd == "P":
            ident = count
            pattern_code = scope[ident]["code"]
            ret.extend(compiler(pattern_code, scope))
        else:
            for i in range(int(count)):
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
        rows.append(stringify(row))

    return stringify(rows, "\r\n")


def move_robot(movement, direction):
    movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    index = (movements.index(movement) + (1 if direction == "R" else -1)) % 4
    return movements[index]


def extract_patterns(code):
    ptr = 0

    ret = []
    patterns = []

    while ptr < len(code):
        t = code[ptr]

        if t == "p":
            pattern = [t]
            stack = 1
            while stack > 0:
                ptr += 1
                if code[ptr] == "p":
                    stack += 1
                if code[ptr] == "q":
                    stack -= 1
                pattern.append(code[ptr])
            patterns.append(stringify(pattern)[1:-1])
        else:
            ret.append(t)

        ptr += 1

    return stringify(ret), patterns


def tokenize(code, scope):
    ptr = 0

    code, patterns = extract_patterns(code)

    for pattern in patterns:
        ident = []
        start = 0
        for i in range(len(pattern)):
            if pattern[i].isdigit():
                ident.append(pattern[i])
            else:
                start = i
                break
        ident = stringify(ident)

        if ident in scope:
            raise SyntaxError("Multiple definitions for P{}".format(ident))

        scope[ident] = {
            "code": tokenize(pattern[start:], scope),
        }

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
            token = tokenize(stringify(token[1:-1]), scope)

        count = []
        while ptr < len(code) and code[ptr].isdigit():
            count.append(code[ptr])
            ptr += 1

        if count:
            count = stringify(count)
            if not group:
                token.append(count)
            else:
                token = token * int(count)

        if group:
            tokens.extend(token)
        else:
            tokens.append(stringify(token))

    return tokens
