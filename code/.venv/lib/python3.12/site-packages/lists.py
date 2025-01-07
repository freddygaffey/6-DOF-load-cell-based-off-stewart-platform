""" some functions for list
    print_list(the_list)
    
    @author Tony Zhou
"""

def print_list (the_list, indent = false, level = 0):
    # print the list with nested list
    # insert some tab
    # level has default value
    # indent: true, print tab; false, don't
    
    for item in the_list:
        if isinstance(item, list):
            print_list(item, indent, level + 1)
        else:
            if indent:
                for tab in range(level):
                    print("\t", end='')
            print(item)
