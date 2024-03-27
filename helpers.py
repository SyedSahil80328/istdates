# helpers.py

import random,re

def randId():
    myList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"*7
    return "".join(random.sample(myList, 20))

def emailValid(myEmail):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, myEmail):
        return True
    return False
    

