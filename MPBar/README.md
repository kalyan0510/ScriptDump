## Multi process progress bar

A thread/process safe concurrent progress display bar

https://github.com/kalyan0510/ScriptDump/assets/14043633/c0a25094-8212-41af-9656-f103a295af41


### Use:
Write the sub-process code like:
```python
def code_run_in_multiprocess_env(params):
    bar_id = MPDisplay.new_pbar(params['name'], params['size'])
    for _ in range(params['size']):
        # your code
        MPDisplay.update(bar_id, 1)
    MPDisplay.close_bar(bar_id)
```


Run your sub-processes in a concurrent env like:
```python
with multiprocessing.Pool(processes=3) as pool:
    pool.map(code_run_in_multiprocess_env, params_list)

```


Note:  MPDisplay.new_pbar(name, size), name must be a unique identifier per process
