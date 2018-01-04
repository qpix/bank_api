import account
from api import response, ERROR

def handler(a):
    try:
        return response ({
            'account' : a,
            'history' : account.read(a)['history']
        })
    except FileNotFoundError:
        return ERROR('Account does not exist.')
