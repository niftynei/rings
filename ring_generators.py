import itertools
import time


# int_in needs to be set to something for the "priming" step
def pass_message(int_in = -1):
    while True:
        int_in = yield int_in


def pass_and_decrement(int_in = -1):
    while True:
        int_in -= 1
        int_in = yield int_in


def main():
    nodes = []
    # set up and prime our starter object
    starter = pass_and_decrement()
    starter.send(None)
    nodes.append(starter)
    print("made starter")
    # make and prime all of our nodes
    for _ in range(10000):
        node = pass_message()
        node.send(None)
        nodes.append(node)
    print("made nodes")
    message = 10000
    # start tracking time
    start = time.time()
    # itertools.cycle gives us an infinite cycle of nodes
    for gen in itertools.cycle(nodes):
        message = gen.send(message)
        if message == 0:
            break
    print(time.time() - start)


if __name__ == '__main__':
    main()
