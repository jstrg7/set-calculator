from consts import DEFAULT_UNIVERSAL_SET, SET_POSSIBLE_NAMES, SYSTEM_NAMES


def validate_set(set_: tuple) -> tuple:
    result = []
    for element in set_: 
        if element not in result and element in DEFAULT_UNIVERSAL_SET: result.append(element)
    return result


def validate_brackets(operations_str: str) -> bool:
    stack = []
    for token in operations_str:
        if token == '(': stack.append('(')
        elif token == ')':
            if len(stack) == 0: return False 
            del stack[-1]
    return stack == []


def is_valid_element(e: str) -> bool:
    if e == "":
        return False
    if len(e) == 1 and (e in SYSTEM_NAMES or e in SET_POSSIBLE_NAMES):
        return True
    return all(ch in "0123456789" for ch in e)


def validate_set_input(name: str, elements: str) -> tuple[bool, str, tuple]:
    if name not in SET_POSSIBLE_NAMES: 
        return (False, 
                'As name you can use only A-Z letters.', 
                ())
    result = []
    for raw in elements.split(","):
        element = raw.strip()
        if element == "":
            return (False,
                    'Empty element - check for double commas or trailing comma.',
                    ())
        if not is_valid_element(element):
            return (False,
                    'As elements you can use only A-Z, a-z or numbers.',
                    ())
        result.append(element)
    return (True, "", tuple(result))


def validate_operators(operations_str: str) -> bool:
    for i in range(len(operations_str)):
        token = operations_str[i]
        if token == "'":
            if i != len(operations_str) - 1 and operations_str[i+1] not in "+-/%')": return False
            if (i == 0 
                or (operations_str[i-1] not in SET_POSSIBLE_NAMES 
                and operations_str[i-1] != ')'
                and operations_str[i-1] not in SYSTEM_NAMES
                and operations_str[i-1] != "'")): return False
        elif token in '+-/%':
            if (i == 0 or i == len(operations_str) - 1 
                or (operations_str[i-1] not in SET_POSSIBLE_NAMES
                and operations_str[i-1] not in SYSTEM_NAMES
                and operations_str[i-1] != ')'
                and operations_str[i-1] != "'")
                or (operations_str[i+1] not in SET_POSSIBLE_NAMES
                and operations_str[i+1] not in SYSTEM_NAMES
                and operations_str[i+1] != '(')):
                return False
    return True


def validate_letters(operations_str: str) -> bool:
    for i in range(len(operations_str)):
        token = operations_str[i]
        if token not in SET_POSSIBLE_NAMES and token not in SYSTEM_NAMES: continue
        if i != 0:
            if (operations_str[i-1] in SET_POSSIBLE_NAMES 
                or operations_str[i-1] in SYSTEM_NAMES
                or operations_str[i-1] == ')'
                or operations_str[i-1] == "'"): return False
        if i != len(operations_str) - 1:
            if (operations_str[i+1] in SET_POSSIBLE_NAMES
                or operations_str[i+1] in SYSTEM_NAMES
                or operations_str[i+1] == '('): return False
    return True


def has_important_symbols(operations_str: str) -> bool:
    was_letter = False
    for token in operations_str:
        if (token not in SYSTEM_NAMES
            and token not in SET_POSSIBLE_NAMES
            and token not in "()'+-/%"): return False
        elif (token in SYSTEM_NAMES or token in SET_POSSIBLE_NAMES): was_letter = True
    return was_letter


def operations_is_valid(operation_str: str) -> bool:
    return (has_important_symbols(operation_str)
            and validate_brackets(operation_str)
            and validate_operators(operation_str)
            and validate_letters(operation_str))


def validate_expression_output(expression: str = '', to_latex: bool = False, to_system_format = False) -> str:
    expression = expression.replace(" ", '')
    if to_latex:
        expression = expression.replace('+', r" \cup ")
        expression = expression.replace('-', r" \cap ")
        expression = expression.replace("/", r" \setminus ")
        expression = expression.replace("%", r" \triangle ")
        expression = expression.replace("'", r' ^c ')
    elif to_system_format:
        expression = expression.replace(r"\cup", '+')
        expression = expression.replace(r"\cap", '-')
        expression = expression.replace(r"\setminus", '/')
        expression = expression.replace(r"\triangle", "%")
        expression = expression.replace(r'^c', "'")
    return expression