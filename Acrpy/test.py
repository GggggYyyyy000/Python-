def insert(data):
    a = list(str(data))
    a.insert(2,"0")
    result = "".join(a)
    return result

b = "115"
c = insert(b)
print (c)