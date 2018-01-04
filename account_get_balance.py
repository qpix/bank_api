import account
from api import response

def handler(a):
    try:
        return response ({
            'account' : a,
            'balance' : account.read(a)['balance']
        })
    except FileNotFoundError:
        return 'Account does not exist.'
