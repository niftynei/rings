import asyncio
import time

import uvloop


NODES = 10000
N_MESSAGES = 10000


class Node():

    def __init__(self, sendq, rcvq=None):
        self.first = False
        self.rcvq = rcvq
        self.sendq = sendq

    async def start_node(self):
        while True:
            message = await self.rcvq.get()
            if message is 0:
                # print(message)
                self.sendq.put_nowait(message)
                break
            if self.first:
                message -= 1
            # print(message)
            self.sendq.put_nowait(message)


async def run():
    sendq = asyncio.Queue()
    firstnode = Node(sendq)
    firstnode.first = True
    nodes = []
    nodes.append(firstnode.start_node())
    for _ in range(NODES - 1):
        rcvq = sendq
        sendq = asyncio.Queue()
        node = Node(sendq, rcvq)
        nodes.append(node.start_node())
    firstnode.rcvq = sendq
    firstnode.rcvq.put_nowait(N_MESSAGES)
    start = time.time()
    await asyncio.wait(nodes)
    end = time.time()
    time_ms = (end - start) * 1000
    print("Loop took {}ms".format(time_ms))


def main():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    coro = run()
    task = loop.create_task(coro)
    loop.run_until_complete(task)


if __name__ == '__main__':
    main()
