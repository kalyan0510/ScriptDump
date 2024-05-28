import multiprocessing
from tqdm import tqdm
import time

class MPDisplay:
    _instance = None
    bars = {}
    queue = None
    listener_process = None
    manager = None
    positions = {}  # Store progress bar positions.
    next_position = 0  # Next available position.
    free_positions = set()  # Set to store reusable positions.
    counter = 0  # Counter for generating unique names.
    _lock = multiprocessing.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MPDisplay, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    @classmethod
    def init(cls):
        cls.manager = multiprocessing.Manager()
        cls.queue = cls.manager.Queue()
        cls.listener_process = multiprocessing.Process(target=cls._listen_to_queue, daemon=True)
        cls.listener_process.start()

    @classmethod
    def _listen_to_queue(cls):
        while True:
            message = cls.queue.get()
            if message is None:
                break  # Terminate listener.
            action, bar_id, value = message
            if action == "new":
                with cls._lock:
                    if cls.free_positions:
                        pos = cls.free_positions.pop()
                    else:
                        pos = cls.next_position
                        cls.next_position += 1
                    cls.positions[bar_id] = pos
                cls.bars[bar_id] = tqdm(total=value, desc=bar_id + '/' + str(pos), position=pos)
            elif action == "update" and bar_id in cls.bars:
                desc, value = value
                if desc:
                    cls.bars[bar_id].set_description(desc)
                else:
                    cls.bars[bar_id].set_description(f'=> Job:{bar_id}')
                cls.bars[bar_id].update(value)
            elif action == "close" and bar_id in cls.bars:
                cls.bars[bar_id].close()
                with cls._lock:
                    cls.free_positions.add(cls.positions[bar_id])
                    del cls.bars[bar_id]
                    del cls.positions[bar_id]

    @classmethod
    def new_pbar(cls, bar_id, size):
        cls.queue.put(("new", bar_id, size))
        return bar_id

    @classmethod
    def update(cls, bar_id, value, desc=None):
        cls.queue.put(("update", bar_id, (desc, value)))

    @classmethod
    def close_bar(cls, bar_id):
        cls.queue.put(("close", bar_id, 0))

    @classmethod
    def terminate(cls):
        cls.queue.put(None)
        cls.listener_process.join()


def code_run_in_multiprocess_env(params):
    bar_id = MPDisplay.new_pbar(params['name'], params['size'])
    for _ in range(params['size']):
        time.sleep(0.002)  # Simulating work
        MPDisplay.update(bar_id, 1)
    MPDisplay.close_bar(bar_id)


if __name__ == "__main__":

    MPDisplay()
    MPDisplay.init()
    # multiprocessing.set_start_method('fork')  # Required on some platforms like MacOS
    params_list = [{'name': f'Job {i}', 'size': 1000 + i*100} for i in range(10)]
    with multiprocessing.Pool(processes=3) as pool:
        pool.map(code_run_in_multiprocess_env, params_list)

    MPDisplay.terminate()
