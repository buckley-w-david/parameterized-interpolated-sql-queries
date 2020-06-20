import inspect
import ast, _ast

def paramaterize_interpolated_querystring(query, placeholder='?'):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1]
    tree = ast.parse(f"f'{query}'")
    values = tree.body[0].value.values
    possible_query_values = {**globals(), **outer_frame.frame.f_locals}

    paramaterized_query = []
    query_values = []
    for node in values:
        if isinstance(node, _ast.Constant):
            paramaterized_query.append(node.value)
        elif isinstance(node, _ast.FormattedValue):
            paramaterized_query.append(placeholder)

            query_value = possible_query_values[node.value.id]
            query_values.append(query_value)

    return (''.join(paramaterized_query), query_values)

def paramaterize_interpolated_querystring_spicy(query, placeholder='?'):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1]
    tree = ast.parse(f"f'{query}'")
    values = tree.body[0].value.values

    temp_name = '__paramaterize_interpolated_querystring_spicy_temp'

    assign = ast.parse(f'{temp_name} = 0')

    paramaterized_query = []
    query_values = []
    for node in values:
        if isinstance(node, _ast.Constant):
            paramaterized_query.append(node.value)
        elif isinstance(node, _ast.FormattedValue):
            paramaterized_query.append(placeholder)

            # This may be the most cursed code I have ever written
            assign.body[0].value = node.value
            assign = ast.fix_missing_locations(assign)
            exec(compile(assign, '<string>', 'exec'), globals(), outer_frame.frame.f_locals)

            query_values.append(outer_frame.frame.f_locals[temp_name])

    return (''.join(paramaterized_query), query_values)
