def rot13(string):
    q = "abcdefghijklmnopqrstuvwxyz"
    dictn = [(q[i], q[(i+13)%26]) for i in range(26)]
    d = dict(dictn)
    result = ""
    for i in string:
        if i in d:
            result = result+d[i]
        elif i.lower() in d:
            result = result+d[i.lower()].upper()
        else:
            result = result+i
    return result

string = "haha"
print rot13(string)

text = """
I love you

how abou you?
"""
print rot13(text)
