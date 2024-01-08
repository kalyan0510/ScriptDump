 ## Awesome Bash History
![image](https://github.com/kalyan0510/ScriptDump/assets/14043633/1b147797-085a-4a05-9a27-185ab73d4b84)

### Features: 
- history of commands remains on disk forever 
- **working directory** of the command is also stored
- also add the time, & period of execution 
- browse history of any given directory
- colorized history for easy reading

### Setup:
1. Put this in your ~/.bashrc and run source
```bash
  export HISTTIMEFORMAT="%F %T "
  export PROMPT_COMMAND='echo "$(date "+%Y-%m-%d %T") - $(pwd): $(history 1 | sed -r "s/^\s*[0-9]+\s*//")" >> ~/.my_bash_hist'
  export HISTCONTROL=""
  alias bh='~/scripts/bh'
  alias bhc='~/scripts/bh -c'
```
2. Copy above 3 files to ~/scripts
```
mkdir ~/scripts
cd ~/scripts
wget https://raw.githubusercontent.com/kalyan0510/ScriptDump/main/awesome_bash_history/bash_hist.py
wget https://raw.githubusercontent.com/kalyan0510/ScriptDump/main/awesome_bash_history/move_bash_history.sh
wget https://raw.githubusercontent.com/kalyan0510/ScriptDump/main/awesome_bash_history/bh

```
3. Mkdir ~/.history
```
mkdir ~/.history
```
4. Add a cron job to move the history files to ~/.history
```bash
0 0 * * 0 ~/scripts/move_bash_history.sh
```


### Usage:
```
Usage: bh [OPTIONS] [PATH]
Options:
  -d, --show_dups   Show duplicate entries
  -i, --ignore_recursion   Do not filter recursively
  -c, --filter_path Filter by the specified path
  PATH              Filter by the specified path (overrides -c)
```

### Authors
Me and GPT3.5
