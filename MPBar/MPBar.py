# mbar.py
import multiprocessing
from tqdm import tqdm
import curses
curses.setupterm()
COLUMN_SIZE = curses.tigetnum('cols')
import sys


class MPDisplayProxy:
    def __init__(self, queue):
        self.queue = queue

    def new_pbar(self, bar_id, size):
        self.queue.put(("new", bar_id, size))
        return bar_id

    def update(self, bar_id, value, desc=None):
        self.queue.put(("update", bar_id, (desc, value)))

    def write(self, bar_id, value):
        self.queue.put(("write", bar_id, value))

    def stat(self, bar_id, value):
        self.queue.put(("stat", bar_id, value))

    def close_bar(self, bar_id):
        self.queue.put(("close", bar_id, None))



def process_queue(queue):
    print("Starting loop")
    positions = {}
    free_positions = []
    bars = {}
    next_position = 0

    while True:
        message = queue.get()
        if message is None:
            break  # Terminate listener.
        action, bar_id, value = message

        if action == "new":
            if free_positions:
                pos = free_positions.pop()
            else:
                pos = next_position
                next_position += 1
            positions[bar_id] = pos
            bars[bar_id] = tqdm(total=value, desc=f'{bar_id}/{pos}', position=pos, file=sys.stdout)

        elif action == "update" and bar_id in bars:
            desc, value = value
            if desc:
                bars[bar_id].set_description(f'{bar_id} => {desc}')
            else:
                bars[bar_id].set_description(f'=> Job:{bar_id}')
            bars[bar_id].update(value)

        elif action == "close" and bar_id in bars:
            bars[bar_id].close()
            free_positions.append(positions[bar_id])
            del bars[bar_id]
            del positions[bar_id]

        elif action == "stat" and bar_id in bars:
            bars[bar_id].set_postfix(value)

        elif action == "write" and bar_id in bars:
            bars[bar_id].write('\r' + " " * COLUMN_SIZE + "\r" + value) # Adjust if needed to avoid interference with tqdm

def worker_init(queue):
    print("start init")
    global mpbar
    mpbar = MPDisplayProxy(queue)
    # print(mpbar)


class MPBarPool:
    def __init__(self, processes=None):
        self.manager = multiprocessing.Manager()
        self.queue = self.manager.Queue()
        self.processes = processes
        self.pool = multiprocessing.Pool(processes=processes, initializer=worker_init, initargs=(self.queue,))
        self.listener_process = multiprocessing.Process(target=process_queue, args=(self.queue,))

    def map(self, func, iterable, chunksize=None):
        return self.pool.map(func, iterable, chunksize)

    def starmap(self, func, iterable, chunksize=None):
        mpbar = MPDisplayProxy(self.queue)
        def wrap_with_mbar(iterable):
            for item in iterable:
                yield (*item, mpbar)
        return self.pool.starmap(func, wrap_with_mbar(iterable), chunksize)

    def __enter__(self):
        self.listener_process.start()
        self.pool._check_running()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.queue.put(None)  # Send termination signal to listener
        self.listener_process.join()
        for _ in range(self.processes):
            print("\r" + ' ' * COLUMN_SIZE + '\r\n')
        self.pool.terminate()



####################### TEST CODE ##################################################

import time

def code_run_in_multiprocess_env(params, mpbar=None):
    # global mpbar
    assert mpbar is not None
    print("mpbar", mpbar)
    bar_id = mpbar.new_pbar(params['name'], params['size'])

    for i in range(params['size']):
        time.sleep(0.003)  # Simulating work
        mpbar.update(bar_id, 1, desc=f"{i}")

    mpbar.write(bar_id, f"done {bar_id}")
    mpbar.stat(bar_id, {"stat": f"done {bar_id}"})
    mpbar.close_bar(bar_id)

if __name__ == "__main__":
    params_list = [({'name': f'Job {i}', 'size': 200 + x * 100}, ) for i, x in enumerate([3, 11, 4, 2, 7,5,7,1, 4])]
    with MPBarPool(processes=3) as pool:
        pool.starmap(code_run_in_multiprocess_env, params_list)
