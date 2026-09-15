from queue import Queue

q = Queue()

# add things to the queue
q.put('a')
q.put('b')
q.put('c')
print('current queue size:', q.qsize())

# get things from the queue
print(q.get())
print('current queue size:', q.qsize())