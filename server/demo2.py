from client import BankClient
import asyncio
from random import choice, randrange
import sys

global names
with open("names.txt") as file:
    lines = file.readlines()
    names = [line.rstrip() for line in lines]
names = names

async def init_tables(c, n):
    await c.CREATE_CUSTOMERS_TABLE()
    for name in names[:n]:
        await c.CREATE_ACCOUNT(name)

async def rundemo(c, n, r):
    options = ["deposit", "transfer", "withdrawal"]
    for i in range(r):
        o = choice(options)
        a = randrange(1, 100)
        pk1 = choice(names[:n])
        pk2 = choice(names[:n])
        if o == "deposit":
            await c.DEPOSIT(pk1, a)
        elif o == "withdrawal":
            await c.DEPOSIT(pk1, a)
        elif o == "transfer":
            await c.TRANSFER(pk1, pk2, a)
    print(await c.CHECK_BALANCES(names[:n]))


async def demo(c, n, r):
    url_stub = "localhost:4915"
    numclients = c
    clients = []
    tasks = []
    for i in range(numclients):
        url = url_stub + str(i)
        clients.append(BankClient(url)) 

    await init_tables(clients[0], n)

    for c in clients:
        print("RUNNING!")
        task = asyncio.create_task(rundemo(c, n, r))  # add task to event loop
        tasks.append(task)
        await asyncio.sleep(0)  # return control to loop so task can start

    for t in tasks:
        await t
        print("JOINED")


if __name__ == "__main__":
    asyncio.run(demo(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))