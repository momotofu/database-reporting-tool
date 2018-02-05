def format_row(values, max_width, top_line):
    """
    Returns a formated row as a string.

    Parameters:
    values: a list ove values for each column
    max_width: (int) max column width
    top_line: (boolean) print a top-line
    """

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


def print_result_table(message, col_names, list_of_tup):
    """
    Takes a list of table rows as tuples, and prints out a table.

    Parameters:
    message: print a message before the table
    col_names: names of each column in the table.
    list_of_tup: a list of tuples
    """
    print(message)
    output_list = []
    col_width = 0
    padding = 3

    # find logest col
    for item in list_of_tup:
        for item_a in item:
            width = len(str(item_a))
            if width > col_width:
                col_width = width

    # Add column labels
    output_list.append(format_row(col_names, col_width + padding, True))
    for item in list_of_tup:
        row_items = []
        for item_a in item:
            row_items.append(item_a)
        output_list.append(format_row(row_items, col_width + padding,
            False))

    for item in output_list:
        print(item)
    print('\n')

