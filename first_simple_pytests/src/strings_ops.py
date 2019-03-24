def strings_concat(a, b):
    return a + b

def strings_common_symbols(a, b):
    for x in a:
        if x in b:
            return(x)

def strings_first_symbol(a, b):
    a = a.lower()
    b = b.lower()
    if (a[0]) == b[0]:
        return True
    else: return False