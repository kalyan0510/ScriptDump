from datetime import datetime
import argparse
import os
import re
from datetime import datetime
import hashlib


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LIGHT_GREY = '\033[37m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'
    LIGHT_BLACK = '\033[90m'
    LIGHT_ORANGE = '\033[38;5;214m'
    LIGHT_PINK = '\033[38;5;207m'
    LIGHT_PURPLE = '\033[38;5;171m'
    LIGHT_LIME = '\033[38;5;154m'
    LIGHT_TEAL = '\033[38;5;38m'
    LIGHT_AQUA = '\033[38;5;51m'
    LIGHT_LAVENDER = '\033[38;5;183m'
    LIGHT_BROWN = '\033[38;5;136m'
    LIGHT_PEACH = '\033[38;5;203m'
    LIGHT_MINT = '\033[38;5;121m'
    LIGHT_OLIVE = '\033[38;5;100m'
    LIGHT_MAROON = '\033[38;5;88m'
    LIGHT_CORAL = '\033[38;5;210m'
    LIGHT_BEIGE = '\033[38;5;180m'
    LIGHT_SKY_BLUE = '\033[38;5;111m'
    LIGHT_ROSE = '\033[38;5;211m'
    LIGHT_GOLD = '\033[38;5;220m'
    LIGHT_CYAN_BLUE = '\033[38;5;75m'
    LIGHT_TAN = '\033[38;5;215m'
    LIGHT_SEA_GREEN = '\033[38;5;39m'
    LIGHT_OLIVE_GREEN = '\033[38;5;192m'
    LIGHT_AZURE = '\033[38;5;74m'

lightcolors = [bcolors.LIGHT_GREY, bcolors.LIGHT_RED, bcolors.LIGHT_GREEN, bcolors.LIGHT_YELLOW, bcolors.LIGHT_BLUE, bcolors.LIGHT_MAGENTA, bcolors.LIGHT_WHITE, bcolors.LIGHT_BLACK, bcolors.LIGHT_ORANGE, bcolors.LIGHT_PINK, bcolors.LIGHT_PURPLE, bcolors.LIGHT_LIME, bcolors.LIGHT_TEAL, bcolors.LIGHT_AQUA, bcolors.LIGHT_LAVENDER, bcolors.LIGHT_BROWN, bcolors.LIGHT_PEACH, bcolors.LIGHT_MINT, bcolors.LIGHT_OLIVE, bcolors.LIGHT_MAROON, bcolors.LIGHT_CORAL, bcolors.LIGHT_BEIGE, bcolors.LIGHT_SKY_BLUE, bcolors.LIGHT_ROSE, bcolors.LIGHT_GOLD, bcolors.LIGHT_CYAN_BLUE, bcolors.LIGHT_TAN, bcolors.LIGHT_SEA_GREEN, bcolors.LIGHT_OLIVE_GREEN]
len_lightcolors = len(lightcolors)

pre_hashed = {}
def myhash(input_string):
    if input_string in pre_hashed.keys():
        return pre_hashed[input_string]
    hashed_value = int(hashlib.sha256(input_string.encode()).hexdigest(), 16) % len_lightcolors
    pre_hashed[input_string] = hashed_value
    return hashed_value

def printt(sts, rt, pt, cm):
    clr = lightcolors[myhash(pt)%len_lightcolors]
    print(f"{bcolors.OKCYAN}{sts} ({rt}){bcolors.ENDC} - {clr}{pt}{bcolors.ENDC}: {cm}")


def parse_log_and_format(content, filter_path=None, no_dup=False):
    # Define the pattern to match each log line
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.*?): (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.*)")

    # Split the content into lines
    lines = content.split('\n')
    # Prepare a list to store the formatted log lines
    formatted_logs = []

    if filter_path:
        filter_path = filter_path.rstrip('/')
    # We will keep the previous timestamp to calculate the run time difference
    # prev_timestamp = None
    prev_print_cm = ''
    cmds = []
    for line in lines:
        # Use regex pattern to extract the necessary parts of the log line
        match = pattern.match(line)
        # print(line)
        if match:
            if len(cmds) > 0:
                sts, rt, pt, cm = cmds.pop(0)
                if not (filter_path and filter_path != pt or no_dup and prev_print_cm==cm):
                    printt(sts, rt, pt, cm)
                    prev_print_cm = cm
            start_time_str, path, command_time_str, command = match.groups()
            # Parse the datetime from the string representations
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            command_time = datetime.strptime(command_time_str, "%Y-%m-%d %H:%M:%S")

            # Calculate time difference in a human-readable format
            time_diff_sec = int((start_time - command_time).total_seconds())
            hours, remainder = divmod(time_diff_sec, 3600)
            minutes, seconds = divmod(remainder, 60)
            run_time_parts = []
            if hours:
                run_time_parts.append(f"{hours}h")
            if minutes:
                run_time_parts.append(f"{minutes}m")
            if seconds or not run_time_parts:
                run_time_parts.append(f"{seconds}s")
            run_time = ' '.join(run_time_parts)
            cmds.append((start_time, run_time, path, command))
            # print("APPDED", cmds)
        else:
            # print("LEN", len(cmds))
            cmds[-1] = (cmds[-1][0], cmds[-1][1], cmds[-1][2], cmds[-1][3] + '\n' +  line)
        # print(cmds)

        # If the filter_path is provided and does not match the current path, continue to the next iteration
        #     continue
    while cmds:
        sts, rt, pt, cm = cmds.pop(0)
        if filter_path and filter_path != pt:
            continue
        printt(sts, rt, pt, cm)


def main():
    parser = argparse.ArgumentParser(description='Parse and format bash history.')
    # parser.add_argument('history_file', type=str, help='Path to bash history file', default='/home/kalyan/.my_bash_hist')
    parser.add_argument('--filter_path', type=str, default=None, help='Filter output by path')
    parser.add_argument('--show_dups', type=bool, default=False, help='Show dups')
    args = parser.parse_args()
    history_directory = os.path.expanduser("~/.history/")
    pattern = re.compile(r"bh_(\d{8})")

    # Get a list of files in ~/.history/ matching the pattern
    matching_files = [file for file in os.listdir(history_directory) if pattern.match(file)]

    # Sort files chronologically based on the date in the filename
    matching_files.sort(key=lambda x: datetime.strptime(pattern.match(x).group(1), "%Y%m%d"))
    matching_files = list(map(lambda x: os.path.join(history_directory, x), matching_files))
    matching_files.append('~/.my_bash_hist')
    print(matching_files)

    for file_path in matching_files:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    # print(args.filter_path)
        parse_log_and_format("".join(lines), args.filter_path, no_dup=not args.show_dups)
        # print(out)
if __name__ == "__main__":
    main()
