#logic: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
def transact_dynamo(self, tx):
    table = self.config.table
    action = tx.action[0] if tx.action != "" else ""
    if tx.access == "read":
        response = table.get_item(
            Key={
                "pk": tx.pk
            }
        )
        if tx.column == "":
            return response['Item']
        return response['Item'][tx.column] if tx.column in response['Item'] else None
    elif tx.access == "write":
        if action == "&":
            response = table.put_item(
                Key={
                    "pk": tx.pk,
                    "balance": 0
                }
            )
        elif action == "~":
            response = table.delete_item(
                Key={
                    "pk": tx.pk
                }
            )
        elif action == '+':
            # TODO: add operation (make sure column is int first)
            pass
        elif action == '-':
            # TODO: subtract operation (make sure column is int first)
            pass



class BankClient(Client):
    def DEPOSIT(self, account, amount):
        # op1 = {
        #     "access": "write",
        #     "pk": account,
        #     "column": "balance",
        #     "action": "+" + str(amount)
        # }
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + account + "';"
        }
        self.makeRequest([op1])

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    def WITHDRAW(self, account, amount):
        # op1 = {
        #     "access": "write",
        #     "pk": account,
        #     "column": "balance",
        #     "action": "-" + str(amount)
        # }
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + account + "';"
        }
        self.makeRequest([op1])

    def TRANSFER(self, from_account, to_account, amount):
        # op1 = {
        #     "access": "write",
        #     "pk": from_account,
        #     "column": "balance",
        #     "action": "-" + str(amount)
        # }
        # op2 = {
        #     "access": "write",
        #     "pk": to_account,
        #     "column": "balance",
        #     "action": "+" + str(amount)
        # }

        op1 = {
            "pk": from_account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + from_account + "';"
        }
        op2 = {
            "pk": to_account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + to_account + "';"
        }
        self.makeRequest([op1, op2])

    def CHECK_BALANCE(self, account):
        # op1 = {
        #     "access": "read",
        #     "pk": account,
        #     "column": "balance"
        # }
        op1 = {
            "pk": account,
            "sql": "SELECT balance FROM customers WHERE pk='" + account + "';"
        }
        self.makeRequest([op1])

    def CREATE_ACCOUNT(self, account):
        # op1 = {
        #     "access": "write",
        #     "pk": account,
        #     "action": "&"
        # }
        op1 = {
            "pk": account,
            "sql": "INSERT INTO customers (pk, balance) VALUES ('" + account + "', 0);"
        }
        self.makeRequest([op1])

    def DELETE_ACCOUNT(self, account):
        # op1 = {
        #     "access": "write",
        #     "pk": account,
        #     "action": "~"
        # }
        op1 = {
            "pk": account,
            "sql": "DELETE FROM customers WHERE pk='" + account + "';"
        }
        self.makeRequest([op1])

# message Transaction {
#     string access = 1;
#     string pk = 2;
#     string column = 3;
#     string action = 4;
# }

import boto3
from nodeconfig import aws_key, aws_secret

dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
                          aws_access_key_id=aws_key,
                          aws_secret_access_key=aws_secret)

table0 = dynamodb.Table('2PC-0')
table1 = dynamodb.Table('2PC-1')
table2 = dynamodb.Table('2PC-2')

tables = [table0, table1, table2]
