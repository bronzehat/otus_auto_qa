def dicts_contain_value(d, x):
    if x in d.values(): 
        return True
    else: return False

def dicts_contain_key_modify(d, x):
    if x in d.keys():
        d[x] = None
        return(d[x])
