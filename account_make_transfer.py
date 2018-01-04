import account
from api import response, ERROR
from authorization import epoch
from datetime import datetime

def handler(sender, receiver, amount):
    try:
        senderData = account.read(sender)
    except FileNotFoundError:
        return ERROR('The sender is not a valid account.')
    try:
        receiverData = account.read(receiver)
    except FileNotFoundError:
        return ERROR('The receiver does not have a account within this bank.', 400)
    
    amount = int(amount)

    if senderData['balance'] - amount < 0:
        return ERROR('The sender does not have enough money for the transaction.', 406)

    if sender == receiver:
        return ERROR('Sender and receiver can not be the same. Please send your apology to Christian.')

    e = epoch()
    if e < senderData['transfer_hold']:
        return ERROR('Accounts can only perform one transfer every 10 seconds. Time remaining: ' + str(senderData['transfer_hold'] - e))
    senderData['transfer_hold'] = e + 10

    transaction = {
        'sender' : sender,
        'receiver' : receiver,
        'amount' : amount,
        'timestamp' : str(datetime.now())
    }

    senderData['history'].append(transaction)
    receiverData['history'].append(transaction)
    senderData['balance'] -= amount
    receiverData['balance'] += amount

    account.write(sender, senderData)
    account.write(receiver, receiverData)

    return response({
        'account' : sender,
        'transaction' : transaction
    })
