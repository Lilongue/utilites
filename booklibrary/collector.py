import os
import sys
import pyperclip

THRESHOLD = 80
SEP_FOR_STAT = '_-+. /|\\'
SKIP_EXTENSIONS = ['zip', 'rar', 'gif', 'htm', 'html', 'auto', 'info', 'last']
BOOK_EXTENSIONS = ['pdf', 'djvu', 'doc', 'chm', 'docx', 'rtf', 'txt', 'fb2', 'djv', 'epub']


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
        path = pyperclip.paste()

    # Check if path is valid
    if not (path and os.path.exists(path)):
        print(f'Error: Path {path} does not exist.')
        return None

    return path


def get_patterns(inp_str, delimiter=None):
    """
    Extracts patterns from a string based on delimiters.

    Args:
        inp_str: The input string.
        delimiter: A custom delimiter to split the string on.

    Returns:
        A tuple of patterns extracted from the string.
    """

    # Define default delimiters.
    delimiters = "_-. /"

    # Use the custom delimiter if specified.
    if delimiter:
        delimiters = delimiter

    # Initialize output list.
    out = []

    # Split the string based on delimiters.
    for separator in delimiters:
        # Handle first delimiter.
        if not out:
            if separator in inp_str:
                tmp = inp_str.split(separator)
                out = [s for s in tmp if s]
            continue

        # Split subsequent parts recursively.
        tmp = []
        for temp_part in out:
            tmp1 = temp_part.split(separator)
            for peace in tmp1:
                tmp.append(peace)
        out = [s for s in tmp if s]

    # Remove empty strings from the output.
    return tuple(filter(lambda x: x.strip() != '', out))


def check_pattern(pat1, pat2):
    """
    Checks the similarity between two patterns.

    Args:
        pat1: The first pattern.
        pat2: The second pattern.

    Returns:
        A percentage indicating the degree of similarity between the patterns.
    """
    pat_len = max(len(pat1), len(pat2))
    if pat_len == 0:
        return 0
    matches = 0
    s_part1, s_part2 = ([], [])
    if type(pat1) is type('string'):
        s_part1.append(pat1)
    else:
        s_part1 = pat1
    if type(pat2) is type('string'):
        s_part2.append(pat2)
    else:
        s_part2 = pat2
    for p in s_part1:
        if p in s_part2:
            matches += 1
            continue
    return int(100 * (matches / pat_len))


def count_separators(dictionary, separators):
    """
    Calculates the number of times each separator appears in the values of a dictionary.

    Args:
        dictionary: A dictionary of values.
        separators: A list of separators to count.

    Returns:
        A list of counts for each separator.
    """
    separator_counts = []
    for _ in separators:
        separator_counts.append(0)
    for value in dictionary.values():
        for i, separator in enumerate(separators):
            separator_counts[i] += value.count(separator)
    return separator_counts


def get_filenames_and_paths(start_path):
    """
    Recursively iterates over a directory tree and returns a dictionary of filenames and paths.

    Args:
        start_path: The root directory to search.

    Returns:
        Two dictionaries containing: 'names' and 'paths'.
    """
    dic_names = {}
    dic_paths = {}

    if start_path:
        i = 1
        for p, dirs, files in os.walk(start_path):
            for f in files:
                dic_names[i] = f
                dic_paths[i] = os.path.join(p, f)
                i += 1
    return dic_names, dic_paths


def find_same2(dir_names):
    """
    Finding duplicate files based on their patterns.

    This function iterates over a patterns listing and compares the patterns to every other
one in the listing.
    If the ratio of shared pattern parts between two patterns exceeds a specified threshold, the function identifies
them as duplicates and returns a list of tuples containing the duplicate patterns.

    Args:
        dir_names: A dictionary of file name patterns.

    Returns:
        A list of tuples containing the names of duplicate patterns.
    """
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
            if check_pattern(dir_names[i], j[1]) > THRESHOLD:
                tmp.append(j[0])
        if len(tmp) > 1:
            out.append(tuple(tmp))
            print(f'Найдено {len(out)} дубликaтов')
        print(f'Просмотрено {k} вариантов \r', end="")
    return out


def get_file_extension_statistics(filenames):
    """
    Calculates statistics on file extensions in a list of filenames.

    Args:
        filenames: A list of filenames.

    Returns:
        A dictionary of extension statistics.
    """

    extension_stats = {}
    extension_stats_percents = {}

    for filename in filenames:
        # Extract the file extension.
        extension = os.path.splitext(filename)[1][1:]

        # Increment the count of the extension.
        if extension not in extension_stats:
            extension_stats[extension] = 0
        extension_stats[extension] += 1

    # Calculate the percentage of each extension.
    for extension, count in extension_stats.items():
        extension_stats_percents[extension] = (count / len(filenames)) * 100

    return extension_stats, extension_stats_percents


def get_filenames(input_path):
    """
    Gets all filenames from an input path without subpaths.

    Args:
        input_path: The input directory path.

    Returns:
        A list of filenames.
    """
    filenames = []
    for filename in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, filename)):
            filenames.append(filename)
    return filenames


if __name__ == '__main__':
    dic_pattern = {}
    start_path = get_path()
    dic_names, dic_paths = get_filenames_and_paths(start_path)
    print(list(SEP_FOR_STAT))
    print(count_separators(dic_names, SEP_FOR_STAT))
    sep = SEP_FOR_STAT
    print('Статистика разрешений:')
    extension_stats, extension_stats_percents = get_file_extension_statistics(dic_names.values())
    print(extension_stats)
    print('-' * 20)
    print(extension_stats_percents)

    for k in dic_names.keys():
        skip_pattern = False
        for ext in SKIP_EXTENSIONS:
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

    repited = find_same2(dic_pattern)

    with open('matches.log', 'w', encoding='utf-8') as f:
        for rep in repited:
            for n in rep:
                f.write(str(n) + ' \t ' + str(dic_names[n]) + ' \t ' + str(dic_paths[n]) + '\r\n')

    with open('result.log', 'w', encoding='utf-8') as f:
        for i in dic_names:
            out_str = str(i) + ' \t ' + str(dic_names[i]) + ' \t ' + str(dic_paths[i]) + ' \t ' + str(
                dic_pattern[i]) + ' \t ' + '\r\n'
            f.write(out_str)

    print('Все сделано')
