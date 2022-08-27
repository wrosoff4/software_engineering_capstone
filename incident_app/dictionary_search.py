
# Created by Terrence Hernandez


def float_validation(single_item):
    """
    This function determines if the passed value is valid for
    the draw component to use. The value of (-1) is inserted
    into the measurements dictionary by the data management
    component if data is missing or incorrect. If the value
    is less than 0.00 (ie. -1). False is returned, preventing
    the draw component from executing. If the value is valid,
    True is returned and the draw component is granted
    permission to execute.

    :param single_item: A single value contained in a tuple or a single
    item in the measurements dictionary

    :return: <Boolean> True | False
    """
    # If value is not valid, return FALSE
    if single_item < 0.00:
        return False
    else:
        # Value is valid, return TRUE
        return True


def tuple_validation(tuple_item):
    """
    This function serves to iterate through the values contained
    in a tuple item contained in the measurements dictionary. Each
    value in the tuple is passed to the float_validation function
    to determine if the value is valid. If False is returned from
    the float_validation function, a break statement is executed
    to stop the iteration through the tuple. False is returned
    from the tuple_validation function and the draw component
    is denied execution.

    :param tuple_item: A tuple contained in the measurements dictionary
    :return: <Boolean> True | False
    """
    # Initialize validation variable
    tv_permission = False

    # Iterate through the tuple values
    for tuple_value in tuple_item:
        # Send tuple valid to float validation function
        tv_permission = float_validation(tuple_value)
        # If tuple value not valid, stop the search return FALSE
        if not tv_permission:
            break

    return tv_permission


def tup_list_validation(list_item):
    """
    This function serves to iterate through a list item contained
    in the measurements dictionary. This list item contains tuples
    as its elements. Each list element (ie. (70.00, 86.00)) is
    passed to the tuple_validation function to  determine if the
    data contained in the tuple is valid. If False is returned
    from the tuple_validation function, the break statement is
    executed to stop the iteration through the list. False is
    returned from the tup_list_validation function and the draw
    component is denied execution.

    :param list_item: A list of tuples contained in the measurements dictionary
    :return: <Boolean> True | False
    """
    # Initialize validation variable
    tlv_validation = False

    # Iteration through a list element in the dictionary
    for list_element in list_item:
        # Send list item to tuple validation function
        tlv_validation = tuple_validation(list_element)
        # If tuple not valid, stop the search, return FALSE
        if not tlv_validation:
            break

    return tlv_validation

# def item_error(key, value):
#     print(f'ERROR: Unknown Data Received @ Key: {key}, Value: {value}')
