## Multi process progress bar

A thread/process safe concurrent progress display bar

https://github.com/kalyan0510/ScriptDump/assets/14043633/c0a25094-8212-41af-9656-f103a295af41


### Use:
Write the sub-process code like:
```python
import time

def your_custom_task_with_loop(params, mpbar=None):
    """
    params: your input params
    mpbar: 'mpbar' must be a keyword arg for your custom task.
    This is how the messaging queue is shared across processes.   
    """

    bar_id = mpbar.new_pbar(params['name'], params['size'])

    for i in range(params['size']):
        time.sleep(0.003)  # Simulating work
        mpbar.update(bar_id, 1, desc=f"{i}")

    mpbar.write(bar_id, f"done {bar_id}")
    mpbar.stat(bar_id, {"stat": f"done {bar_id}"})
    mpbar.close_bar(bar_id)
```
Run your sub-processes in a concurrent env like:

```python
params_list = [({'name': f'Job {i}', 'size': 200 + x * 100}, ) for i, x in enumerate([3, 11, 4, 2, 7,5,7,1, 4])]
# use  MPBarPool(processes=N) insted of multiprocessing.Pool(processes=N)
with MPBarPool(processes=3) as pool:
    pool.starmap(code_run_in_multiprocess_env, params_list) # note: mpbar object need not be present in the params list. It will be injected by the MPBarPool wrapper
```
Note:  
1. MPDisplay.new_pbar(name, size), name must be a unique identifier per process
2. Any `print` statements inside of the loops should be replaced by `mpbar.write()`
3. For updating any stats (of the looping processes) `mpbar.stat()` can be used

### How it works:
Tqdm progress updates from all the N processes are pushed to a shared queue. Messages from this queue are polled in a separate process which is completely responsible for the console output.
