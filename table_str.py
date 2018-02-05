def format_row(values, max_width, top_line):
    output = ''

    # formate center of row
    for value in values:
        output += ' | ' + str(value).center(max_width, ' ')
    output = '|' + output[1:] + ' ||'

    # add top and or bottom lines
    row_width = len(output)
    line = '-' * row_width
    if top_line:
        line = '=' * row_width
        output = line + '\n' + output + '\n' + line
    else:
        output += '\n' + '-' * row_width

    return output
