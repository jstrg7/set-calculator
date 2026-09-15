import set_calculation_manager as scm
from consts import DEFAULT_UNIVERSAL_SET, SYSTEM_NAMES


def save_set(set_: tuple, set_map: dict) -> str:
    for letter in SYSTEM_NAMES:
        if letter not in set_map:
            set_map[letter] = set_
            return letter
    return ''


def erase_system_set(set_names: list[str], set_map: dict) -> None:
    for set_name in set_names:
        if len(set_name) == 1 and set_name in SYSTEM_NAMES:
            set_map.pop(set_name, None)


def create_operation(sets: list[str], set_map: dict, operand: str = None) -> str:
    result = ()
    if operand == "'":
        U = None
        if len(sets) > 1 and sets[1] is not None:
            U = set_map[sets[1]]
        result = scm.get_complement(A=set_map[sets[0]], U=U)
        new_name = save_set(result, set_map)
        if new_name == '': return ''
        erase_system_set([sets[0]], set_map)
        return new_name
    if len(sets) != 2: return ''
    if operand == '+': result = scm.get_union(set_map[sets[0]], set_map[sets[1]])
    elif operand == '-': result = scm.get_intersection(set_map[sets[0]], set_map[sets[1]])
    elif operand == '/': result = scm.get_difference(set_map[sets[0]], set_map[sets[1]])
    elif operand == '%': result = scm.get_symmetric_difference(set_map[sets[0]], set_map[sets[1]])
    new_name = save_set(result, set_map)
    if new_name == '': return ''
    erase_system_set(sets, set_map)
    return new_name


def count_all_complements(operation_str: str, U: str, set_map: dict) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] == "'" and s[i - 1] != ')':
            letter = s[i - 1]
            operation_result = create_operation([letter, U], set_map, "'")
            s = s[:i - 1] + operation_result + s[i + 1:]
        else:
            i += 1
    return s


def count_all_brackets(operation_str: str, U: str, set_map: dict) -> str:
    s = operation_str
    while '(' in s:
        j = s.rfind('(')
        k = s.find(')', j)
        inside = s[j + 1 : k]
        s = s[:j] + get_operation(inside, set_map) + s[k + 1:]
    return s


def count_all_intersections(operation_str: str, set_map: dict) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] == '-':
            left_set, right_set = s[i - 1], s[i + 1]
            operation_result = create_operation([left_set, right_set], set_map, '-')
            s = s[:i - 1] + operation_result + s[i + 2:]
        else:
            i += 1
    return s


def count_other_operations(operation_str: str, set_map: dict) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] in '+/%':
            left_set, right_set = s[i - 1], s[i + 1]
            operation_result = create_operation([left_set, right_set], set_map, s[i])
            s = s[:i - 1] + operation_result + s[i + 2:]
        else:
            i += 1
    return s


def get_operation(operation_str: str, set_map: dict) -> str:
    U = 'U'
    if U not in set_map:
        set_map[U] = DEFAULT_UNIVERSAL_SET
    if "'" in operation_str: operation_str = count_all_complements(operation_str, U, set_map)
    if '(' in operation_str or ')' in operation_str: operation_str = count_all_brackets(operation_str, U, set_map)
    if "'" in operation_str: operation_str = count_all_complements(operation_str, U, set_map)
    if "-" in operation_str: operation_str = count_all_intersections(operation_str, set_map)
    if '+' in operation_str or '/' in operation_str or '%' in operation_str: operation_str = count_other_operations(operation_str, set_map)
    return operation_str