def getUniqueItems(dicts, k:str = "itemName"):
    items = set()
    result = []
    for d in dicts:
        if not d[k] in items:
            items.add(d[k])
            result.append(d)
    return result
