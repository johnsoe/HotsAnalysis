from Queue import Queue
from threading import Thread
def execute_task(worker, source):
	q = Queue()
	for i in range(100):
	     t = Thread(target=worker, args=(q,))
	     t.daemon = True
	     t.start()

	for item in source:
	    q.put(item)

	q.join()