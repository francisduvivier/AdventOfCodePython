splitter = lambda char: lambda line: line.split(char)


def runAssembly(assembly: str):
    doubleSplit = map(splitter(' '), assembly.splitlines())
    code: [[str, int]] = list(map(lambda elements: [elements[0], int(elements[1])], doubleSplit))

    global ip
    global accVal

    def reset():
        global ip
        global accVal
        ip = 0
        accVal = 0

    reset()
    alreadyDone = []
    while ip < len(code) and ip not in alreadyDone:
        alreadyDone.append(ip)
        op = code[ip][0]
        arg = code[ip][1]

        def acc(arg):
            global accVal
            global ip
            accVal += arg
            ip += 1

        def jmp(arg):
            global ip
            ip += arg

        def nop(arg):
            global ip
            ip += 1

        switcher = {
            'acc': acc,
            'jmp': jmp,
            'nop': nop,
        }
        switcher[op](arg)
    if (ip in alreadyDone):
        return 'error, lastVal: ' + str(accVal)
    return accVal
