def is_positive_integer(value):
    try:
        result = int(value)
    except ValueError:
        return False
    if result < 0:
        return False
    return True
