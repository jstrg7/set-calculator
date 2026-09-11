import set_calculation_manager as scm
from consts import DEFAULT_UNIVERSAL_SET, SYSTEM_NAMES


#TODO move dict to funcs or to consts
set_map = {}

def save_set(set_: tuple) -> str:
    for letter in SYSTEM_NAMES: 
        if letter not in set_map:
            set_map[letter] = set_
            return letter
    return '' 


def erase_system_set(set_names: list[str]) -> None:
    for set_name in set_names:
        if len(set_name) == 1 and set_name in SYSTEM_NAMES: set_map.pop(set_name, None)


def create_operation(sets: list[str], operand: str = None) -> str:
    result = ()
    if operand == "'": 
        U = None
        if len(sets) > 1 and sets[1] is not None: U = set_map[sets[1]]
        result = scm.get_complement(A=set_map[sets[0]], U=U)
        new_name = save_set(result)
        if new_name == '': return ''
        erase_system_set([sets[0]]) 
        return new_name
    if len(sets) != 2: return ''
    if operand == '+': result = scm.get_union(A=set_map[sets[0]], B=set_map[sets[1]])
    elif operand == '-': result = scm.get_intersection(A=set_map[sets[0]], B=set_map[sets[1]])
    elif operand == '/': result = scm.get_difference(A=set_map[sets[0]], B=set_map[sets[1]])
    elif operand == '%': result = scm.get_symmetric_difference(A=set_map[sets[0]], B=set_map[sets[1]])
    new_name = save_set(result)
    if new_name == '': return ''
    erase_system_set(sets)
    return new_name


def count_all_complements(operation_str: str, U: str) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] == "'" and s[i - 1] != ')':
            letter = s[i - 1]
            operation_result = create_operation([letter, U], "'")
            s = s[:i - 1] + operation_result + s[i + 1:]
        else:
            i += 1
    return s


def count_all_brackets(operation_str: str, U: str) -> str:
    s = operation_str
    while '(' in s:
        j = s.rfind('(')
        k = s.find(')', j)
        
        inside = s[j + 1 : k]
        s = s[:j] + get_operation(inside, U) + s[k + 1:]
    return s



def count_all_intersections(operation_str: str) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] == '-':
            left_set, right_set = s[i - 1], s[i + 1] 
            operation_result = create_operation([left_set, right_set], '-')
            s = s[:i - 1] + operation_result + s[i + 2:]
        else:
            i += 1
    return s


def count_other_operations(operation_str: str) -> str:
    s = operation_str
    i = 0
    while i < len(s):
        if s[i] in '+/%':
            left_set, right_set = s[i - 1], s[i + 1]
            operation_result = create_operation([left_set, right_set], s[i])
            s = s[:i - 1] + operation_result + s[i + 2:]
        else:
            i += 1
    return s


def get_operation(operation_str: str, U: str) -> str:
    if "'" in operation_str: operation_str = count_all_complements(operation_str, U)
    if '(' in operation_str or ')' in operation_str: operation_str = count_all_brackets(operation_str, U)
    if "'" in operation_str: operation_str = count_all_complements(operation_str, U)
    if "-" in operation_str: operation_str = count_all_intersections(operation_str)
    if '+' in operation_str or '/' in operation_str or '%' in operation_str: operation_str = count_other_operations(operation_str)
    return operation_str

