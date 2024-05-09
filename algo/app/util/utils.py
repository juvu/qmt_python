def gp_type_szsh(code):
    if code.find('60', 0, 3) == 0:
        code = code + '.SH'
    elif code.find('688', 0, 4) == 0:
        code = code + '.SH'
    elif code.find('900', 0, 4) == 0:
        code = code + '.SH'
    elif code.find('00', 0, 3) == 0:
        code = code + '.SZ'
    elif code.find('300', 0, 4) == 0:
        code = code + '.SZ'
    elif code.find('200', 0, 4) == 0:
        code = code + '.SZ'
    return code
