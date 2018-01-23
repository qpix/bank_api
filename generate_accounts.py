import shutil
import csv

def random_account():
    from random import randint
    return randint(1e9, 1e10 - 1)


generated_accounts = []
def unique_account():
    global generated_accounts

    account = random_account()
    while account in generated_accounts:
        account = random_account()

    generated_accounts.append(account)
    return account

group_list = {}
def generate_accounts_for_group(group, num_of_accounts = 5):
    global group_list
    group_list[group] = []
    for x in range(num_of_accounts):
        account = unique_account()
        group_list[group].append(account)
        shutil.copyfile('accounts/1234567890.json', 'accounts/' + str(account) + '.json')

def create_csv(num_of_accounts = 5):
    with open('group_accounts.csv', 'w') as csvfile:
        fieldnames = ['Grupp']
        for x in range(num_of_accounts):
            fieldnames.append('Konto ' + str(x))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for group in group_list:
            row = {'Grupp':group}
            for x in range(num_of_accounts):
                row['Konto ' + str(x)] = group_list[group][x]
            writer.writerow(row)

generate_accounts_for_group('G101')
generate_accounts_for_group('G102')
generate_accounts_for_group('G103')
generate_accounts_for_group('G104')
generate_accounts_for_group('G105')
generate_accounts_for_group('G106')
generate_accounts_for_group('G107')
generate_accounts_for_group('G108')
generate_accounts_for_group('G109')
generate_accounts_for_group('G110')
generate_accounts_for_group('G111')
generate_accounts_for_group('G112')
generate_accounts_for_group('G113')
generate_accounts_for_group('G114')
generate_accounts_for_group('G115')
generate_accounts_for_group('G116')

create_csv()
