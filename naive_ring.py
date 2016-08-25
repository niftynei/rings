import time
from queue import Queue
from threading import Thread

NUMBER_OF_NODES = 2046
NUMBER_OF_MESSAGES = 48876


class Node():
    def __init__(self, parent):
        self.is_start_node = False
        self.parent = parent
        self.outbox = Queue()

    def run(self):
        self.thread = Thread(target=self.pass_message)
        self.thread.start()


    def pass_message(self):
        while True:
            message = self.parent.outbox.get()
            if self.is_start_node:
                message -= 1
            self.outbox.put(message)
            if message <= 0:
                break
        if self.is_start_node:
            self.endtime = time.time()
            print(self.endtime - self.starttime)


class StartNode(Node):
    def __init__(self):
        self.is_start_node = True
        self.outbox = Queue()


    def start_message(self, number):
        self.starttime = time.time()
        self.outbox.put(number)
        self.run()


def main():
    start_node = StartNode()
    previous_node = start_node
    for i in range(NUMBER_OF_NODES):
        new_node = Node(previous_node)
        new_node.run()
        previous_node = new_node
    start_node.parent = previous_node
    start_node.start_message(NUMBER_OF_MESSAGES)



if __name__ == '__main__':
    main()



# need some sort of way to keep track of performance (messages per second?, total time? cProfile?)