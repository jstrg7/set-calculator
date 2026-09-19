from consts import DEFAULT_UNIVERSAL_SET

def get_intersection(A: tuple, B: tuple) -> tuple:
    C = []
    for a in A:
        if a in B: C.append(a)
    return tuple(C)


def get_union(A: tuple, B: tuple) -> tuple:
    C = list(A)
    for b in B:
        if b not in C: C.append(b)
    return tuple(C)


def get_difference(A: tuple, B: tuple) -> tuple:
    C = list(A)
    for b in B:
        if b in C: C.remove(b)
    return tuple(C)


def get_symmetric_difference(A: tuple, B: tuple) -> tuple:
    return get_union(get_difference(A, B), get_difference(B, A))


def get_complement(A: tuple, U: tuple = None) -> tuple:
    if U is None: U = DEFAULT_UNIVERSAL_SET
    return get_difference(U, A)