from bank import Bank
import config
import json

if __name__ == "__main__":

    tsb = Bank(config.username, config.password)
    accounts = tsb.get_accounts()

    for account in accounts:
        for transaction in tsb.get_transactions(account['number']):
            print(transaction)
