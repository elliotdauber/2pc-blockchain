from clientlib import Client
import asyncio

class BankClient(Client):
    async def CREATE_CUSTOMERS_TABLE(self, blk=True):
        op1 = {
            "pk": "",
            "sql": "CREATE TABLE customers (pk text, balance real);"
        }
        await self.makeRequest([op1], blk=blk)

    async def DEPOSIT(self, account, amount, blk=True):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    async def WITHDRAW(self, account, amount, blk=True):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

    async def TRANSFER(self, from_account, to_account, amount, blk=True):
        op1 = {
            "pk": from_account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + from_account + "';"
        }
        op2 = {
            "pk": to_account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + to_account + "';"
        }
        await self.makeRequest([op1, op2], blk=blk)

    async def CHECK_BALANCE(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "SELECT pk, balance FROM customers WHERE pk='" + account + "';"
        }
        return await self.makeRequest([op1], blk=blk, access="r")

    async def CHECK_BALANCES(self, accounts, blk=True):
        ops = []
        for account in accounts:
            op = {
                "pk": account,
                "sql": "SELECT pk, balance FROM customers WHERE pk='" + account + "';"
            }
            ops.append(op)
        return await self.makeRequest(ops, blk=blk, access="r")

    async def CREATE_ACCOUNT(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "INSERT INTO customers (pk, balance) VALUES ('" + account + "', 0);"
        }
        await self.makeRequest([op1], blk=blk)

    async def DELETE_ACCOUNT(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "DELETE FROM customers WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

async def simple_test(c):
    await c.CREATE_CUSTOMERS_TABLE()
    await c.CREATE_ACCOUNT("elliot")
    await c.CREATE_ACCOUNT("nick")
    await c.CREATE_ACCOUNT("zach")
    await c.DEPOSIT("elliot", 15)
    await c.TRANSFER("elliot", "zach", 10)
    print(await c.CHECK_BALANCE("elliot"))
    print(await c.CHECK_BALANCE("nick"))
    print(await c.CHECK_BALANCE("zach"))
    print(await c.CHECK_BALANCES(["elliot", "nick", "zach"]))
    #await c.DELETE_ACCOUNT("nick")

async def init_tables(c):
    await c.CREATE_CUSTOMERS_TABLE()

async def small_test(c):
    await c.CREATE_ACCOUNT("isaac")
    await c.CREATE_ACCOUNT("sahit")
    await c.DEPOSIT("isaac", 15)
    await print(await c.CHECK_BALANCE("isaac"))
    await c.DEPOSIT("sahit", 5)
    print(await c.CHECK_BALANCE("sahit"))
    await c.TRANSFER("isaac", "sahit", 5)
    print(await c.CHECK_BALANCES(["isaac", "sahit"]))

async def balance(c):
    await c.CREATE_CUSTOMERS_TABLE()
    await c.CREATE_ACCOUNT("elliot")
    await c.DEPOSIT("elliot", 24)
    print(await c.CHECK_BALANCE("elliot"))

def client():
    url = "localhost:49155"
    c = BankClient(url)

    tests = {
        "simple": simple_test,
        "small": small_test,
        "balance": balance
    }   

    while True:
        test = input("Enter a test name for the client at url " + url + ": ")
        if test == "quit":
            break
        if test in tests:
            asyncio.run(tests[test](c))

    # asyncio.run(simple_test(c))
    c.stop_grpc()

if __name__ == "__main__":
    client()