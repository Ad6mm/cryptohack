from operator import xor

def bin_to_dev(bin):
    result = 0
    for x in range(len(bin)):
        mult = len(bin)-1-x
        val = 2 ** mult
        if (bin[x] == '0'):
            val = 0
        result += val
    return result


string = "label"
integer = 13
integerBinary = bin(integer)[2:]

while len(integerBinary) < 7:
    integerBinary = '0' + integerBinary

result = []
for char in string:
    charBinary = bin(ord(char))[2:]
    charXOR = ''
    for x in range(len(charBinary)):
        if charBinary[x] == integerBinary[x]:
            charXOR += '0'
        else :
            charXOR += '1'
    result.append(bin_to_dev(charXOR))

resultString = ''
for char in result:
    resultString += chr(char)

print(resultString)