import itertools
import time

'''
This isn't really a proper implementation of a message passing ring, because
the nodes aren't exactly running concurrently; execution stops completely
within a generator between each yield and the next time send() gets called
on that generator. This is sort of the case in the asyncio implementation as
well because each coroutine blocks while awaiting the next message in its "in"
queue, but in that case we are constantly checking all of the loops for more
work instead of ignoring them entirely.
'''


def node_gen():
    int_in = -1
    while True:
        int_in = yield int_in


def first_node():
    int_in = -1
    while True:
        int_in -= 1
        int_in = yield int_in


def main():
    nodes = []

    # set up and prime our starter object
    fn = first_node()
    fn.send(None)
    nodes.append(fn)

    # make and prime all of our nodes
    for _ in range(10000):
        node = node_gen()
        node.send(None)
        nodes.append(node)
    message = 10000
    # start tracking time
    start = time.time()

    # itertools.cycle gives us an infinite cycle of nodes
    for gen in itertools.cycle(nodes):
        message = gen.send(message)
        if message == 0:
            break
    print("Loop took {}ms".format((time.time() - start) * 1000))


if __name__ == '__main__':
    main()
