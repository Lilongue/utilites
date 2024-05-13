import os
import sys
import pyperclip


THRESHOLD = 80
SEPARATOR = "_"
SEP_FOR_STAT = "_-+. /|\\"
SKIP_EXTENTIONS = ["zip", "rar", "gif", "htm", "html", "auto", "info", "last"]

def get_path():
    """
    Get path from console user input or clipboard or from argument.

    Returns:
        str: The path as a string.
    """

    path = None

    # Try to get path from argument
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        if not os.path.exists(path):
            path = None
    
    # Try to get path from console input
    if path is None:
        path = input('Скопируйте или введите путь к папке: ')

    # Try to get path from clipboard
    if not path:
        try:
            path = pyperclip.paste()
        except:
            pass

    # Check if path is valid
    if not (path and os.path.exists(path)):
        print(f'Error: Path {path} does not exist.')
        return None

    return path


def get_patterns(inp_str, delimiter = None):
    delimiters = "_-. /"
    out = []
    if delimiter:
        delimiters = delimiter
    tmp = []
    tmp1 = []
    for sep in delimiters:
        if not out:
            if sep in inp_str:
                tmp = str(inp_str).split(sep)
                out = [s for s in tmp if s]
            continue
        tmp = []
        for part in out:
            tmp1 = str(part).split(sep)
            for pease in tmp1:
                tmp.append(pease)
        out = [s for s in tmp if s]
    return tuple(filter (lambda x: x.strip() != "", out))

def check_pattern(pat1, pat2):
    pat_len = max(len(pat1), len(pat2))
    if pat_len == 0:
        return 0
    matches = 0
    s_part1, s_part2 = ([],[])
    if type(pat1) is type("string"):
        s_part1.append(pat1)
    else:
        s_part1 = pat1
    if type(pat2) is type("string"):
        s_part2.append(pat2)
    else:
        s_part2 = pat2
    for p in s_part1:
        if p in s_part2:
            matches += 1
            continue
    return int(100*(matches/pat_len))


def count_separators(dictionary, separators):
    separator_counts = []
    for separator in separators:
        separator_counts.append(0)
    for value in dictionary.values():
        for i, separator in enumerate(separators):
            separator_counts[i] += value.count(separator)
    return separator_counts


dic_names = {}
dic_paths = {}
dic_pattern = {}

start_path = get_path()
if start_path:
    i = 1
    for p, dirs, files in os.walk(start_path):
        for f in files:
            dic_names[i] = f
            dic_paths[i] = os.path.join(p,f)
            i += 1
    print ("Найдено %s файлов" %(i))




print (list(SEP_FOR_STAT))
print (count_separators(dic_names, SEP_FOR_STAT))
#sep = input("Enter the separator: ")
sep = SEP_FOR_STAT

for k in dic_names.keys():
    skip_pattern = False
    for ext in SKIP_EXTENTIONS:
        if dic_names[k].endswith(ext):
            skip_pattern = True
            break
    if skip_pattern:
        dic_pattern[k] = ""
        continue
    part = get_patterns(dic_names[k][:-4], sep)
    if part:
        dic_pattern[k] = part
    else:
        dic_pattern[k] = dic_names[k][:-4]

def find_same2(dir_names):
    listic = dir_names.items()
    tmp_set = set()
    out = []
    k = 0
    for i in tuple(dir_names.keys()):
        k += 1
        tmp = []
        if i in tmp_set:
            continue
        tmp_set.add(i)
        for j in listic:
            if check_pattern(dir_names[i],j[1]) > THRESHOLD:
                tmp.append(j[0])
        if len(tmp) > 1:
            out.append(tuple(tmp))
            print ("Найдено %s дубликaтов" %(str(len(out))))    
        print("Просмотрено %s вариантов \r" %(k), end="")   
    return out

repited = find_same2(dic_pattern)

with open("matches.log","w") as f:
    for rep in repited:
        for n in rep:
            f.write(str(n) + " \t " + str(dic_names[n]) + " \t " + str(dic_paths[n]) + "\r\n")

with open("result.log", "w", encoding='utf-8') as f:
    for i in dic_names:
        out_str = str(i) + " \t " + str(dic_names[i]) + " \t " + str(dic_paths[i]) + " \t " + str(dic_pattern[i]) + " \t " + "\r\n"
        f.write(out_str)
    
print("Все сделано")

