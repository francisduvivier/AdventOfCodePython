splitter = lambda char: lambda line: line.split(char)


def runAssembly(assembly: str):
    doubleSplit = map(splitter(' '), assembly.splitlines())
    code: [[str, int]] = list(map(lambda elements: [elements[0], int(elements[1])], doubleSplit))

    ip = 0
    accVal = 0
    alreadyDone = []
    while ip < len(code) and ip not in alreadyDone:
        alreadyDone.append(ip)
        op = code[ip][0]
        args = code[ip][1:]

        def acc(args, ip):
            nonlocal accVal
            accVal += args[0]

        def jmp(args, ip):
            return ip + args[0]

        def nop(args, ip):
            pass

        switcher = {
            'acc': acc,
            'jmp': jmp,
            'nop': nop,
        }
        newIp = switcher[op](args, ip)
        ip = newIp if newIp else ip + 1

    if ip in alreadyDone:
        return 'error, lastVal: ' + str(accVal)
    return accVal
