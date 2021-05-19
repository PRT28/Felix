def arrows(text, start, end):
    result = ''

    idx_start = max(text.rfind('\n', 0, start.index), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    line_count = end.ln - start.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = start.cn if i == 0 else 0
        col_end = end.cn if i == line_count - 1 else len(line) - 1

        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')