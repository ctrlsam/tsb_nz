# TSB API


## Accounts JSON Properties
>get_accounts()
```json
[
    {
        "oid":"xxxx.xxxxxx",
        "category":"EVERYDAY",
        "hasStatements":true,
        "name":"Connect Plus",
        "type":"CQ",
        "title":"Spending",
        "number":"0000000000",
        "numberFormatted":"XX-XXXX-XXXXXXX-XX",
        "balance":0000.00,
        "availableBalance":0000.00,
        "details":[
            {"title":"Account Number","detail":"XX-XXXX-XXXXXXX-XX"},{"title":"Account Type","detail":"XXXXXXXX"},
            {"title":"Account Status","detail":"Active"},
            {"title":"Account Opened","detail":"DAY, MONTH_NUM MONTH YEAR"},{"title":"Account holder(s)","detail":"YOUR NAME"}
        ],
        "allowTransfersIn":true,"allowTransfersOut":true,"allowPaymentsOut":true,"allowDebitCard":true,"allowUseAsEmailFeeDeductAccount":true,"customerNumber":"00000000000","interestRatePerAnnum":null,"allowedToViewTransactions":true,"canUpdateImage":true,"allowNicknameUpdate":true,"showAvailableBalance":true,"balanceFormatted":"$0","availableBalanceFormatted":"$0","interestRatePerAnnumFormatted":null
    }
]
```

## Payees JSON Properties
>get_payees()
```json
{
    "customerSavedBankAuthorityPayeeList":[...],
    "customerSavedCompanyPayeeList":[...],
    "customerSavedPersonalPayeeList":[

        {"name":"Person's Name","customerSavedPayeeIdentifier":"XXXX.XXXXXXX","payerStatementDetails":{"particulars":"particular message","code":"","reference":""},"personalPayeeTypeIdentifier":"XXXX.XXX","disabled":false,"status":""},

    ],

    "customerSavedTaxPayeeList":[...]
}
```