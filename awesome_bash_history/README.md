 ## Awesome Bash History

### Features: 
- remains on disk forever 
- **working directory** of the command is also stored
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

```
4. Mkdir ~/.history
```
mkdir ~/.history
```
5. Add a cron job to move the history files to ~/.history
```bash
0 0 * * 0 ~/scripts/move_bash_history.sh
```


### Usage:
```
Usage: bh [OPTIONS] [PATH]
Options:
  -d     Show duplicate entries
  -c     Filter history by the current working dir
  PATH   Filter history by the specified path (overrides -c)
```

### Authors
Me and GPT3.5

Some screenshots:
![image](https://github.com/kalyan0510/ScriptDump/assets/14043633/1b147797-085a-4a05-9a27-185ab73d4b84)
