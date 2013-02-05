def hashtable_get_bucket(htable,keyword):
    return htable[hash_string(keyword, len(htable))]

def hash_string(keyword,buckets):
    out = 0
    for s in keyword:
        out = (out + ord(s)) % buckets
    return out

def make_hashtable(nbuckets):
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table

def hashtable_add(htable,key,value):
    hashtable_get_bucket(htable,key).append([key,value])

def hashtable_lookup(htable,key):
    bucket = hashtable_get_bucket(htable, key)
    for i in bucket:
        if i[0] == key:
            return i[1]
    return None

def hashtable_update(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return
    bucket.append([key, value])

table = [[['Francis', 13], ['Ellis', 11]], [], [['Bill', 17],
['Zoe', 14]], [['Coach', 4]], [['Louis', 29], ['Rochelle', 4], ['Nick', 2]]]
