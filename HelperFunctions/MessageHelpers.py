def checkIfTokenExists(message):
    try:
        message.index("Spots")
    except ValueError:
        return False
    else:
        return True


def checkIfChange(prev, current):
    if prev == current:
        return False
    else:
        return True


def isNewSignal(body):
    try:
        body.index("New signal")
    except ValueError:
        return False
    else:
        return True


def isSignalClose(body):
    try:
        body.index("closed")
    except ValueError:
        return False
    else:
        return True


def isTargetOne(body):
    try:
        body.index("Target 1 done")
    except ValueError:
        return False
    else:
        return True


def isTargetTwo(body):
    try:
        body.index("Target 2 done")
    except ValueError:
        return False
    else:
        return True


def isTargetThree(body):
    try:
        body.index("Target 3 done")
    except ValueError:
        return False
    else:
        return True


def getSymbol(title):
    symbol = title[title.index("$") + 1:]
    return symbol


def getToken(title):
    token = title[title.index("$") + 1:title.index("USDT")]
    return token


def getLastMessageItem(data):
    return data[-1]


def getMessageTitle(message):
    return message['messageTitle']


def getMessageBody(message):
    return message['messageBody']
