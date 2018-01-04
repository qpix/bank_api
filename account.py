import json

def read(account):
    return json.load(open('accounts/' + str(account) + '.json'))

def write(account, data):
    with open('accounts/' + account + '.json', 'w') as outfile:
        json.dump(data, outfile)
