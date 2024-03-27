xorTable = {'00': '0', '01': '1', '10': '1', '11': '0'}

def decToBin(decimalNumber):
    e = bin(decimalNumber)
    binaryNumber = e.split('0b')[1]
    while len(binaryNumber) < 4:
        binaryNumber = '0' + binaryNumber
    return binaryNumber

def binToDec(stringBits):
    decimalNumber = 0
    position = 0
    for bit in stringBits[::-1]:
        decimalNumber = decimalNumber + ((2 ** position) * int(bit))
        position += 1
    return decimalNumber

def getFourBitsFromSBox (bits, sBox):
    row = binToDec(bits[0] + bits[5])
    col = binToDec(bits[1:5])

    return decToBin(sBox[row][col])

def generatePermutation(input, permutation):
    permutedInput = ""
    for element in permutation:
        permutedInput += input[element - 1]
    
    return permutedInput

def shiftLeftKeys(key, shift):
    key1 = key[shift:28]
    key1 += key[0:shift]
    key2 = key[28+shift:]
    key2 += key[28:28+shift]

    return key1 + key2

def generateKeys(key):
    permutationKey = generatePermutation(key, permutationChoiceOne)
    keysList = []
    times = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    for time in times:
        temp = shiftLeftKeys(permutationKey, time)
        permutationKey = temp
        keysList.append(generatePermutation(temp, permutationChoiceTwo))

    return keysList

def bitwiseXOR(input1, input2):
    output = ''
    for i in range(len(input1)):
        output += xorTable[input1[i] + input2[i]]

    return output

def readCredentials(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        lineOne = lines[0].strip()  
        lineTwo = lines[1].strip()
        lineThree = lines[2].strip()
    
    return [lineOne, lineTwo, lineThree]

def readPermutations(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        lineOne = list(map(int, lines[0].strip().split(',')))
        lineTwo = list(map(int, lines[1].strip().split(',')))
        lineThree = list(map(int, lines[2].strip().split(',')))
        lineFour = list(map(int, lines[3].strip().split(',')))
        lineFive = list(map(int, lines[4].strip().split(',')))
        lineSix = list(map(int, lines[5].strip().split(',')))
    
    return lineOne, lineTwo, lineThree, lineFour, lineFive, lineSix

def readSubstitutionBoxes(fileName):
    subBoxes = []
    with open(fileName) as file:
        lines = file.readlines()
        for i in range(0, 32, 4):
            lineOne = list(map(int, lines[i].strip().split(',')))
            lineTwo = list(map(int, lines[i+1].strip().split(',')))
            lineThree = list(map(int, lines[i+2].strip().split(',')))
            lineFour = list(map(int, lines[i+3].strip().split(',')))
            subBoxes.append([lineOne, lineTwo, lineThree, lineFour])

    return subBoxes

def getBinaryData(textInput):
    binarySequence = ""
    for char in textInput:
        binarySequence += bin(ord(char))[2:].zfill(8)
    
    return binarySequence

def getTextData(binaryInput):
    textSequence = ""
    for i in range (0, len(binaryInput), 8):
        temp = binaryInput[i+1:i+8]
        textSequence += chr(int(temp, 2))
    
    return textSequence

def splitTexts(textInput):
    while len(textInput) % 8:
        textInput += '\0'
    textList = []
    for i in range(0, len(textInput), 8):
        textList.append(getBinaryData(textInput[i:i+8]))
    
    return textList


permutationChoiceOne, permutationChoiceTwo ,initialPermutation, expansionPermutation, straightPermutation, inversePermutation = readPermutations("Permutations.txt")
substitutionBoxes = readSubstitutionBoxes("SubstitutionBoxes.txt")