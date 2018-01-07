from authorization import authorize, create_token, create_challenge, valid_challenge_response
from flask import Flask, request
from api import response, ERROR
import re
app = Flask(__name__)

re_account = re.compile('^[0-9]{10}$')
re_amount = re.compile('^[1-9][0-9]*$')
re_challenge = re.compile('^[0-9]{6}$')

def bad_parameter (value, regex):
    if not value or not regex.match(value):
        return True
    return False

def options_response():
    return '', 200, {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET','Access-Control-Allow-Headers':'Authorization'}

@app.route('/get_challenge')
def get_challenge():
    account = request.args.get('account')

    if bad_parameter(account, re_account):
        return ERROR('The account parameter is either missing or has a bad format.')

    return response({
        'type' : 'challenge',
        'value' : create_challenge(account)
    })

@app.route('/get_token')
def get_token():
    account = request.args.get('account')
    challenge_response = request.args.get('challenge_response')

    if bad_parameter(account, re_account):
        return ERROR('The account parameter is either missing or has a bad format.')

    if bad_parameter(challenge_response, re_challenge):
        return ERROR('The challenge_response parameter is either missing or has a bad format.')

    if valid_challenge_response(challenge_response, account):
        return response({
            'type' : 'token',
            'value' : create_token(account)
        })

    return ERROR('The challenge response is not valid.')

@app.route('/account_get_balance', methods=['OPTIONS'])
def account_get_balance_options():
    return options_response()

@app.route('/account_get_balance')
@authorize
def account_get_balance():
    from account_get_balance import handler
    account = request.args.get('account')

    if bad_parameter(account, re_account):
        return ERROR('The account parameter is either missing or has a bad format.')

    return handler(account)

@app.route('/account_make_transfer', methods=['OPTIONS'])
def account_make_transfer_options():
    return options_response()

@app.route('/account_make_transfer')
@authorize
def account_make_transfer():
    from account_make_transfer import handler

    sender = request.args.get('account')
    receiver = request.args.get('receiver')
    amount = request.args.get('amount')

    if bad_parameter(sender, re_account):
        return ERROR('The account parameter is either missing or has a bad format.')

    if bad_parameter(receiver, re_account):
        return ERROR('The receiver parameter is either missing or has a bad format.')

    if bad_parameter(amount, re_amount):
        return ERROR('The amount parameter is either missing or has a bad format.')

    return handler(sender, receiver, amount)

@app.route('/account_get_history', methods=['OPTIONS'])
def account_get_history_options():
    return options_response()

@app.route('/account_get_history')
@authorize
def account_get_history():
    from account_get_history import handler
    account = request.args.get('account')

    if bad_parameter(account, re_account):
        return ERROR('The account parameter is either missing or has a bad format.')

    return handler(account)
