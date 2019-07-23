import re


colors = {
    "F": "pink",
    "L": "red",
    "R": "green",
    "(": None,
    ")": None,
}


def highlight(code):
    # Implement your syntax highlighter here
    reg = re.compile(r"[F]+|[R]+|[0-9]+|[L]+|[()]+")
    ret = []
    for m in reg.findall(code):
        color = colors.get(m[0], "orange")
        if color:
            ret.append('<span style="color: {}">{}</span>'.format(color, m))
        else:
            ret.append(m)

    return "".join(ret)
