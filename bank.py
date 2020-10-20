import requests
from bs4 import BeautifulSoup
import datetime

import config

class TSB:
    def __init__(self, username, password):
        self.url = "https://homebank.tsbbank.co.nz/"
        self.nextSequenceID = None
        self.customerNumber = None

        self.session = self.login(username, password)
        if not self.session:
            exit('login failed')

    def login(self, username, password):
        ''' Login to TSB Dashboard '''
        post_data = {"op":"signon",
                    "isPoli":"",
                    "nextSequenceID":"",
                    "card":username,
                    "password":password}

        s = requests.Session()
        r = s.post(self.url, post_data)
        html = r.text
        if "<title>TSB - Dashboard</title>" in html:
            # login sucess, grap sequence ID and customer number
            soup = BeautifulSoup(html, "lxml")
            self.nextSequenceID = soup.find_all('input')[2]['value']
            self.customerNumber = soup.find_all('dashboard')[0]['customer-number']

            return s

    def get_transactions(self, account, number_of_transactions=99999):
        ''' Get some transactions from an account '''
        url = self.url + f"api/transactions/{self.customerNumber}/account/{account}"
        params = {"nextSequenceId":self.nextSequenceID,
                  "numberOfTransactions":number_of_transactions}
        return self.session.get(url, params=params).json()['data']['transactionList']

    def get_accounts(self):
        ''' Get all of your accounts '''
        url = self.url + f"api/accounts/{self.customerNumber}"
        params = {"nextSequenceId":self.nextSequenceID}
        return self.session.get(url, params=params).json()['data']['accountList']

    def get_payees(self):
        ''' Get your saved payees '''
        url = self.url + "api/payees"
        params = {"nextSequenceId":self.nextSequenceID}
        return self.session.get(url, params=params).json()['data']

    def transfer(self, amount, account_from, account_to, date=datetime.datetime.now()):
        ''' Transfer funds in between your OWN accounts '''
        url = self.url + f"api/transfers/{self.customerNumber}"
        params = {"nextSequenceId":self.nextSequenceID}

        json = {"primaryCustomerNumber":str(self.customerNumber),
                "transfer":{
                    "amount": str(amount),
                    "date": date.strftime("%Y-%m-%dT%H:%M:%S+12:00"),
                    "fromAccountIdentifier": account_from['oid'],
                    "fromAccountName": account_from['name'],
                    "fromAccountNumber": account_from['number'],
                    "fromAccountNumberFormatted": account_from['numberFormatted'],
                    "fromAccountOwner": str(self.customerNumber),
                    "fromAccountReference": None,

                    "toAccountIdentifier": account_to['oid'],
                    "toAccountName": account_to['name'],
                    "toAccountNumber": account_to['number'],
                    "toAccountNumberFormatted": account_to['numberFormatted'],
                    "toAccountOwner": str(self.customerNumber),
                    "toAccountReference": None,
                    "toAccountType": account_to['type']
                }}

        # validate
        r = self.session.post(url + "/validate", params=params, json=json)
        # TODO: add validation checks
        '''
        Example Responce:
        {"data":{"validationErrors":{},"authorizationRequired":false,"keepTransferAtEndOfMonth":false,"transferFee":null,"transferFeeMessage":null,"regularTransferSetupFee":null,"regularTransferSetupFeeMessage":null,"infoMessages":{},"validationPassed":true},"errorMessage":null,"success":true}
        '''

        
        # final
        r = self.session.post(url, params=params, json=json)
        return r.json()['success']

    def payment(self, amount, your_account, reciever_account_number, reciever_name, particular_message="", save_payee=False, date=datetime.datetime.now()):
        ''' Make a one-off payment '''
        url = self.url + f"api/payments/{self.customerNumber}"
        params = {"nextSequenceId":self.nextSequenceID}

        json = {
            "amount": str(amount),
            "date": date.strftime("%Y-%m-%dT%H:%M:%S+12:00"),
            "fromAccountOid": your_account['oid'],
            "payee":{
                "accountNumber": reciever_account_number, # no dashes
                "name": reciever_name,
                "payeeType": ".PaymentPayeeNewPersonal",
                "saveThisPayee": save_payee,
                "statementDetails": {"particulars":particular_message}
            },
            "payerStatementDetails": {"particulars":particular_message},
            "paymentProcessingTime": "TODAY"
        }

        # validate
        r = self.session.post(url + "/validate", params=params, json=json)
        if r.json()['data']['authorizationRequired']:
            print('Authorisation Needed: Transaction canceled')
            '''
            Example Responce:
            {"data":{"validationErrors":{},"authorizationRequired":false,"keepTransferAtEndOfMonth":false,"transferFee":null,"transferFeeMessage":null,"regularTransferSetupFee":null,"regularTransferSetupFeeMessage":null,"infoMessages":{},"validationPassed":true},"errorMessage":null,"success":true}
            '''
            return
        
        # final
        r = self.session.post(url, params=params, json=json)
        return r.json()['success']
