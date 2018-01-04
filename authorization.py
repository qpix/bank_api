from functools import wraps
from flask import request
from api import ERROR

def epoch():
    from calendar import timegm
    from time import gmtime
    return timegm(gmtime())

def create_token(account, time = None):
    from hashlib import sha224

    if not time:
        time = epoch()

    return sha224((account + str(time)).encode('UTF-8')).hexdigest()

def create_challenge(account, time = None):
    challenge = str(int(create_token(account, time), 16) % 1000000)
    return '0' * (6 - len(challenge)) + challenge

def valid_challenge_response(response, account):
    e = epoch()
    for x in range(60):
        if response == create_challenge(create_challenge(account, e - x), account):
            return True
    return False

def authorize(f):
    @wraps(f)
    def decorated():
        account = request.args.get('account')
        if not account:
            return ERROR('Missing the account-parameter.')
        try:
            e = epoch()
            for x in range(3000):
                if request.headers['Authorization'] == 'Bearer ' + create_token(account, e - x):
                    return f()
            return ERROR('The token is not valid for the specified account.')
        except KeyError:
            return ERROR('Missing the Authorization-header.')
    return decorated
