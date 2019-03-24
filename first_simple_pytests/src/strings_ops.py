def strings_concat(a, b):
    return a + b

def strings_common_symbols(a, b):
    for x in a:
        if x in b:
            return(x)

def strings_first_symbol(a, b):
<<<<<<< HEAD
    if a[0] == b[0]:
        return (a[0])
=======
    a = a.lower()
    b = b.lower()
    if (a[0]) == b[0]:
        return True
    else: return False
>>>>>>> 7aad9f1ea05cb9b1e235b28682278e3a25b79354
