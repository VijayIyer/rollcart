import logging

def getUniqueItems(dicts, k:str = "itemName"):
    items = set()
    result = []
    for d in dicts:
        if not d[k] in items:
            items.add(d[k])
            result.append(d)
    return result

def logExceptionInRetailerClass(methodName:str, retailerClassName:str):
    logging.exception("{} method failed in {} with following exception:".format(methodName,retailerClassName))
