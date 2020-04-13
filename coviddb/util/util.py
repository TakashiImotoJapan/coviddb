

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True

def is_int(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True