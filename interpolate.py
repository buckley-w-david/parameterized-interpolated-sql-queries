import inspect
import ast, _ast

# Old "safer" version that only attempts to look up variable names
# The f-string generation is vulnerable to injection itself (How ironic)
# because at the time I did not account for strings that themselves contained
# the quote character I used (').
# def parameterize_interpolated_querystring(query, placeholder='?'):
#     frame = inspect.currentframe()
#     outer_frame = inspect.getouterframes(frame)[1]
#     tree = ast.parse(f"f'{query}'")
#     values = tree.body[0].value.values
#     possible_query_values = {**globals(), **outer_frame.frame.f_locals}
#
#     paramaterized_query = []
#     query_values = []
#     for node in values:
#         if isinstance(node, _ast.Constant):
#             paramaterized_query.append(node.value)
#         elif isinstance(node, _ast.FormattedValue):
#             paramaterized_query.append(placeholder)
#
#             query_value = possible_query_values[node.value.id]
#             query_values.append(query_value)
#
#     return (''.join(paramaterized_query), query_values)

def parameterize_interpolated_querystring(query, placeholder='?'):
    # Create an f-string AST tree of the query
    # This is done to avoid having to write crappy f-string parsing logic
    # We also run it through repr so that all quotes are escaped correctly
    #
    # This is to prevent strings containing the quote character I would have otherwise used to
    # construct the f-string from breaking the parsing by ending the string
    # (Much like an SQL injection)
    tree = ast.fix_missing_locations(ast.parse("f" + repr(query)))
    if not isinstance(tree.body[0].value, _ast.JoinedStr):
        raise ValueError("You've found a way to break my string parsing")

    values = tree.body[0].value.values

    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1] # element 1 is the parent stack frame

    # We create a shallow copy so that when we add a new variable within it
    # the outer frame is not polluted with a new variable.
    # However since it is a shallow copy any side effects from
    # code that is run via the exec call should be retained
    outer_locals = outer_frame.frame.f_locals.copy()


    # We create a dummy assignment AST tree so that we can extract
    # the result of our computation
    temp_name = '__parameterize_interpolated_querystring_temp'
    assign = ast.fix_missing_locations(ast.parse(f'{temp_name} = 0'))

    paramaterized_query = []
    query_values = []

    # An f-string has two parts
    for node in values:
        # Constants, which are just sections of static strings
        if isinstance(node, _ast.Constant):
            paramaterized_query.append(node.value)
        # And FormattedValue's, that have whatever is needed to calculate the result of the interpolation
        elif isinstance(node, _ast.FormattedValue):
            paramaterized_query.append(placeholder)

            # This may be the most cursed code I have ever written
            assign.body[0].value = node.value # We pull off the calculation node and attach it to our dummy assignment
            exec(compile(assign, '<string>', 'exec'), globals(), outer_locals)

            query_values.append(outer_locals[temp_name])

    return (''.join(paramaterized_query), query_values)
