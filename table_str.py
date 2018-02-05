def format_row(values, top_line, max_width):
    output = ''
    # formate center of row
    for value in values:
        output += ' | ' + str(value).center(max_width, ' ')
    output = '|' + output[1:] + ' ||'

    # add top and or bottom lines
    row_width = len(output)
    if top_line:
        output = '-' * row_width + '\n' + output + '\n' + '-' * row_width
    else:
        output += '\n' + '-' * row_width

    return output
