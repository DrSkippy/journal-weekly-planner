def columns(doc, n=2):
    sep = " | "
    res = []
    doc_len = len(doc)
    if n == 1:
        col_width = 13 + 7 * 18  # for activities + 7 days
        for line in doc:
            if line == "<hr>":
                line = "-" * col_width
            res.append(line)
    else:
        n_lines = 1 + int(doc_len / n)
        col_width = int((80 - n * 3) / n)
        for i in range(n_lines):
            line = []
            for j in range(n):
                idx = i + (j * n_lines)
                try:
                    if doc[idx] == "<hr>":
                        line_str = "-" * col_width
                    else:
                        line_str = doc[idx] + " " * (col_width - len(doc[idx]))
                except IndexError:
                    line_str = " " * col_width
                line.append(line_str)
                line.append(sep)
            res.append("".join(line))
    return "\n".join(res)
