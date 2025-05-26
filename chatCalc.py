def split_expression(expr):
    # Split expression into list of elements (numbers, operators, parentheses)
    import re
    pattern = r'\d+\.\d+|\d+|[()+\-*/^]'
    return re.findall(pattern, expr)

def group_parentheses(elements):
    stack = [[]]  # stack of groups, start with one top-level group
    for el in elements:
        if el == '(':
            stack.append([])  # start new group
        elif el == ')':
            group = stack.pop()
            stack[-1].append(group)  # add group as element of previous group
        else:
            stack[-1].append(el)
    if len(stack) != 1:
        raise ValueError("Mismatched parentheses")
    return stack[0]

def insert_implicit_multiplication(group):
    i = 0
    while i < len(group) - 1:
        current = group[i]
        next_el = group[i + 1]

        # Condition: if current is number or group (parenthesis) and next_el is number or group
        if ( (isinstance(current, str) and (current.isdigit() or current.replace('.', '', 1).isdigit()))
             or isinstance(current, list) ):
            if ( (isinstance(next_el, str) and (next_el.isdigit() or next_el.replace('.', '', 1).isdigit()))
                 or isinstance(next_el, list) ):
                group.insert(i + 1, '*')
                i += 1  # skip the inserted operator
        i += 1

    # Recursively do this for sublists (parentheses)
    for i, el in enumerate(group):
        if isinstance(el, list):
            insert_implicit_multiplication(el)

def evaluate_group(group):
    # If group is just a number, return it as float
    if isinstance(group, str):
        return float(group)
    if len(group) == 1:
        # If group is a single element inside a list, evaluate it recursively
        return evaluate_group(group[0])

    # First, recursively evaluate any subgroups (parentheses)
    for i, el in enumerate(group):
        if isinstance(el, list):
            group[i] = evaluate_group(el)

    precedence_levels = [
        ['^'],
        ['*', '/'],
        ['+', '-']
    ]

    for ops in precedence_levels:
        i = 0
        while i < len(group):
            if group[i] in ops:
                operator = group[i]

                # Convert operands to float if they're strings
                left = float(group[i - 1]) if isinstance(group[i - 1], str) else group[i - 1]
                right = float(group[i + 1]) if isinstance(group[i + 1], str) else group[i + 1]

                if operator == '+':
                    result = left + right
                elif operator == '-':
                    result = left - right
                elif operator == '*':
                    result = left * right
                elif operator == '/':
                    result = left / right
                elif operator == '^':
                    result = left ** right

                # Replace left, operator, right with result
                group[i - 1:i + 2] = [result]
                i -= 1  # step back to handle chained operations
            else:
                i += 1

    if len(group) != 1:
        raise ValueError("Could not fully evaluate expression")
    return group[0]


while True:
    try:
        expression = input("Type an expression (or 'q' to quit): ").strip()
        if expression.lower() == 'q':
            print("Goodbye!")
            break
        
        elements = split_expression(expression)
        grouped = group_parentheses(elements)
        insert_implicit_multiplication(grouped)
        result = evaluate_group(grouped)

        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}. Please try again.")