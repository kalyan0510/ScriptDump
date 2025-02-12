# Check Installed Python Packages

## Overview
`check_req` is a script to verify installed Python packages against the `requirements.txt` file. It categorizes packages into:
- Installed with a newer version than required
- Installed with the exact required version
- Not installed
- Installed with an older version than required

## Usage
1. Activate the corresponding Conda environment:
   ```sh
   conda activate your_env_name
   ```
2. Ensure `requirements.txt` is in the current directory.
3. Run the script using the alias:
   ```sh
   check_req
   ```

## Setting Up the Alias
To use `check_req` as a command, add the following line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):
   ```sh
   alias check_req='python path/to/check_pkgs.py'
   ```
Then, apply the changes:
   ```sh
   source ~/.bashrc  # or source ~/.zshrc
   ```

(written by GPT)
