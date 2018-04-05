def unicode_clean(line):
    erase = ""
    lock = 0
    i = 0
    for character in line:
        if lock == 0:
            if character == '\\' and line[i + 1] == 'u':
                code = ""
                code += line[i] + line[i + 1] + line[i + 2] + line[i + 3] + line[i + 4] + line[i + 5]
                erase = erase + ' ' + code
                lock = 5
            elif character == '\\' and line[i + 1] == 'U':
                code = ""
                code += line[i] + line[i + 1] + line[i + 2] + line[i + 3] + line[i + 4]
                code += line[i + 5] + line[i + 6] + line[i + 7] + line[i + 8] + line[i + 9]
                erase = erase + ' ' + code
                lock = 9
            elif character == '\\' and line[i + 1] == 'n':
                code = ""
                code += line[i] + line[i + 1]
                erase = erase + ' ' + code
                lock = 1
            elif character == '\\' and line[i + 1] == 'x':
                code = ''
                code += line[i] + line[i + 1] + line[i + 2] + line[i + 3]
                erase = erase + ' ' + code
                lock = 3
        else:
            lock -= 1
        i += 1
    erase = erase.split()
    for uni_code in erase:
        line = line.replace(uni_code, " ")
    return line


def expression_clean(line):
    search = "&amp;"
    replace = ""
    line = line.replace(search, replace)
    return line


def hexadecimal_conversion(line):
    convert = ''
    lock = 0
    i = 0
    for character in line:
        if lock == 0:
            if character == '\\' and line[i + 1] == 'x':
                code = ''
                code += line[i] + line[i + 1] + line[i + 2] + line[i + 3]
                convert = convert + ' ' + code
                lock = 3
        else:
            lock -= 1
        i += 1
    convert = convert.split()
    for hexadecimal in convert:
        ascii = int(hexadecimal[2] + hexadecimal[3], 16)
        # Latin capital letter 'A' with accent
        if 192 <= ascii <= 197:
            replace = 'A'
        # Latin capital letter cedilla  (usually from French)
        elif ascii == 199:
            replace = 'C'
        # Latin capital letter 'E' with accent
        elif 200 <= ascii <= 203:
            replace = 'E'
        # Latin capital letter 'I' with accent
        elif 204 <= ascii <= 207:
            replace = 'I'
        # Latin capital letter 'N' with accent (usually from Spanish)
        elif ascii == 209:
            replace = 'Nn'
        # Latin capital letter 'O' with accent
        elif 210 <= ascii <= 214:
            replace = 'O'
        # Latin capital letter 'U' with accent
        elif 217 <= ascii <= 220:
            replace = 'U'
        # Germanic letter 'B' or eszett (usually from German)
        elif ascii == 223:
            replace = 'ss'
        # Latin letter 'a' with accent
        elif 224 <= ascii <= 229:
            replace = 'a'
        # Latin letter cedilla (usually from French)
        elif ascii == 231:
            replace = 'c'
        # Latin letter 'e' with accent
        elif 232 <= ascii <= 235:
            replace = 'e'
        # Latin letter 'i' with accent
        elif 236 <= ascii <= 239:
            replace = 'i'
        # Latin letter 'n' with accent (usually from Spanish)
        elif ascii == 241:
            replace = 'nn'
        # Latin letter 'o' with accent
        elif 242 <= ascii <= 246:
            replace = 'o'
        # Latin letter 'u' with accent
        elif 249 <= ascii <= 252:
            replace = 'u'
        else:
            continue
        line = line.replace(hexadecimal, replace)
    return line
