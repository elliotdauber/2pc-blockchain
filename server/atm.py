import sys
from client import BankClient
import asyncio
from random import choice, randrange
import subprocess


async def init_tables(c):
    await c.CREATE_CUSTOMERS_TABLE()

def check_input(tx, n):
    if len(tx) < n:
        print("NOT ENOUGH ARGUMENTS FOR THIS COMMAND")
        return True


async def call(c, tx):
    action = tx[0]
    if action == "deposit":
        if check_input(tx, 3):
            return
        await c.DEPOSIT(tx[1], tx[2])
    elif action == "add_account":
        if check_input(tx, 2):
            return
        await c.CREATE_ACCOUNT(tx[1])
    elif action == "withdrawal":
        if check_input(tx, 3):
            return
        await c.DEPOSIT(tx[1], tx[2])
    elif action == "transfer":
        if check_input(tx, 4):
            return
        await c.TRANSFER(tx[1], tx[3], tx[2])
    elif action == "balance":
        if check_input(tx, 2):
            return
        print(await c.CHECK_BALANCES([tx[1]]))
    else:
        print("Valid Transaction Actions are: [deposit, add_account, withdrawl, transfer, balance]")

if __name__ == "__main__":
    url = "localhost:49150"
    c = BankClient(url)
    asyncio.run(init_tables(c))
    new_node_outputs = []
    while True:
        x = input("Action | Account1 | Amount | Acccount2:  ")
        tx = x.split(" | ")
        for i in range(len(tx)):
           tx[i] = tx[i].strip() 
        if tx[0] == 'exit':
           break
        elif tx[0] == "add_node":
            new_node_outputs.append(
                subprocess.Popen(
                    ['python3', 'xnode.py',str(tx[1]), str(tx[2])], 
                    stdout=sys.stdout,
                    stderr=sys.stdout, 
                    universal_newlines=True
                )
            )
        else:
            asyncio.run(call(c, tx))