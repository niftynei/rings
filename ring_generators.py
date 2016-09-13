import itertools
import time


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
    #while True:
    start = time.time()
    for gen in itertools.cycle(nodes):
        message = gen.send(message)
        if message == 0:
            break
    print(time.time() - start)


if __name__ == '__main__':
    main()
