import TDESUtils

def roundFunctions(binaryText, keysList):
    permutedBinaryText = TDESUtils.generatePermutation(binaryText, TDESUtils.initialPermutation)
    
    leftHalf = permutedBinaryText[:32]
    rightHalf = permutedBinaryText[32:]

    for i in range(16):    
        permutedRightHalf = TDESUtils.generatePermutation(rightHalf, TDESUtils.expansionPermutation)
        xorRightHalf = TDESUtils.bitwiseXOR(permutedRightHalf, keysList[i])

        sBoxText = ""
        for j in range (8):
            text = xorRightHalf[6*j:6*j + 7]
            sBoxText += TDESUtils.getFourBitsFromSBox(text, TDESUtils.substitutionBoxes[j])

        permutedSBoxText = TDESUtils.generatePermutation(sBoxText, TDESUtils.straightPermutation)
        xorSBoxText = TDESUtils.bitwiseXOR(leftHalf, permutedSBoxText)

        (leftHalf, rightHalf) = (rightHalf, xorSBoxText)

    (leftHalf, rightHalf) = (rightHalf, leftHalf)
    modifiedText = TDESUtils.generatePermutation(leftHalf + rightHalf, TDESUtils.inversePermutation)
    return modifiedText

def enpsd(plainText):
    keys = TDESUtils.readCredentials("Credentials.txt")
    plainTextList = TDESUtils.splitTexts(plainText)

    keysLists = []
    for key in keys:
        keysLists.append(TDESUtils.generateKeys(key))

    cipherText = ""

    for plainChunk in plainTextList:
        cipherText1 = roundFunctions(plainChunk, keysLists[0])
        cipherText2 = roundFunctions(cipherText1, keysLists[1][::-1])
        cipherText3 = roundFunctions(cipherText2, keysLists[2])

        cipherText += TDESUtils.getTextData(cipherText3)

    return cipherText
