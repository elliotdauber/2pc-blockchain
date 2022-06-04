from client import BankClient
import asyncio
from random import choice, randrange
import threading

names = [
    "Anna",
    "Bailey",
    "Cameron",
    "Drew",
    "Elliot",
    "Fernando",
    "Greg",
    "Hailey",
    "Isaac",
    "Jackie",
    "Kent",
    "Lucas",
    "Manny",
    "Nora"
]

async def init_tables(c):
    await c.CREATE_CUSTOMERS_TABLE()
    for name in names:
        await c.CREATE_ACCOUNT(name)

async def rundemo(c):
    options = ["deposit", "transfer", "withdrawal"]
    for i in range(20):
        o = choice(options)
        a = randrange(1, 100)
        pk1 = choice(names)
        pk2 = choice(names)
        if o == "deposit":
            await c.DEPOSIT(pk1, a)
        elif o == "withdrawal":
            await c.DEPOSIT(pk1, a)
        elif o == "transfer":
            await c.TRANSFER(pk1, pk2, a)
    print(await c.CHECK_BALANCES(names))


async def demo():
    url_stub = "localhost:4915"
    numclients = 3
    clients = []
    tasks = []
    for i in range(numclients):
        url = url_stub + str(i)
        clients.append(BankClient(url))

    await init_tables(clients[0])


    for c in clients:
        print("RUNNING!")
        task = asyncio.create_task(rundemo(c))  # add task to event loop
        tasks.append(task)
        await asyncio.sleep(0)  # return control to loop so task can start

    for t in tasks:
        await t
        print("JOINED")


if __name__ == "__main__":
    asyncio.run(demo())

