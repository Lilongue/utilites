import os
import shutil
import sys

sys.path.append(os.getcwd())

import pyperclip
from literation import detect_russian_letters, re_transliterate
from booklibrary.dbutils.book_dao import BookDao
import collector
from book import Book
from library import Library


def get_book_from_file_path(filename, path, id):
    extension = os.path.splitext(filename)[1][1:]
    patterns = [] if extension.lower() not in collector.BOOK_EXTENSIONS else collector.get_patterns(
        os.path.splitext(filename)[0], collector.SEP_FOR_STAT)
    return Book(id, filename, patterns, path, '')


def collect_library(start_path: str, load_from_file: bool = True) -> Library:
    library = Library()
    current_id = 1
    if os.path.exists(os.path.join(start_path, library.DEFAULT_LIB_FILE)) and load_from_file:
        print('Загружаю библиотеку из файла')
        library.load_books_from_file(library.DEFAULT_LIB_FILE)
    else:
        dic_names, dic_paths = collector.get_filenames_and_paths(start_path)
        for i in dic_names.keys():
            library.add_book(get_book_from_file_path(dic_names.get(i), dic_paths.get(i), current_id))
            current_id += 1
    return library


def find_similar(library: Library, path: str):
    files = collector.get_filenames(path)
    out = {}
    if files:
        for filename in files:
            out[filename] = find_similar2(library, filename, 4)
    with open('similar.log', 'w', encoding='utf-8') as f:
        for item in out.items():
            f.write('\n' + item[0] + '\n' + '-' * 20 + '\n')
            f.write('\n'.join(item[1]))


def find_similar2(library: Library, filename: str, count: int):
    patterns = collector.get_patterns(filename, collector.SEP_FOR_STAT)
    book_dict = {book.get_id(): book for book in library.get_books()}
    similar_dict = {item[0]: collector.check_pattern(item[1].get_patterns(), patterns) for item in book_dict.items()}
    similar_sorted = sorted(similar_dict.items(), key=lambda item: item[1], reverse=True)
    return [f'{item[1]} : {book_dict.get(item[0])}' for item in similar_sorted[:count]]


def re_translate_files(path: str):
    files = collector.get_filenames(path)
    new_path = os.path.join(path, 'retranslated')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    copy_re_translated_files(files, path, new_path)


def copy_re_translated_files(filenames, source_path, target_path):
    for filename in filenames:
        if detect_russian_letters(filename):
            continue
        new_filename = re_transliterate(os.path.splitext(filename)[0]) + os.path.splitext(filename)[1]
        file_path = os.path.join(source_path, filename)
        target_file_path = os.path.join(target_path, new_filename)
        shutil.copy(file_path, target_file_path)


def save_books_to_db(library: Library, db_file: str = 'home_lib.db') -> None:
    book_dao = BookDao(db_file)
    for book in library.get_books():
        book_dao.create_book(book)


def check_lib_update(library: Library, path: str) -> None:
    print('Загружаю обновленную коллекцию...')
    new_library = collect_library(path, False)
    print('Ищу потерянные книги...')
    diff_lost = '\n'.join([book.to_full_string() for book in collect_the_difference(library, new_library)])
    print('Ищу новые книги...')
    diff_new = '\n'.join([book.to_full_string() for book in collect_the_difference(new_library, library)])
    print('Lost books:', diff_lost)
    print('New books:', diff_new)
    with open('differ.log', 'w', encoding='utf-8') as f:
        f.write('Lost books: \n')
        f.write(diff_lost)
        f.write('\n New books: \n')
        f.write(diff_new)


def collect_the_difference(library1: Library, library2: Library) -> list[Book]:
    out_difference = []
    for book1 in library1.get_books():
        is_found = False
        for book2 in library2.get_books():
            if book1 == book2:
                print('!found!!')
                is_found = True
                break
        if not is_found:
            out_difference.append(book1)
    return out_difference


def execute_commands(library):
    last_command = None
    while True:
        command = input('Enter command: ').strip().lower()
        if not command and last_command:
            command = last_command

        if command.startswith('quit'):
            break
        elif command.startswith('calc'):
            last_command = command
            filename = pyperclip.paste()
            print(f'filename : {filename}')
            if filename:
                print('\n'.join(find_similar2(library, filename, 5)))

        elif command.startswith('many'):
            last_command = command
            path = pyperclip.paste()
            print(f'path : {path}')
            if path:
                find_similar(library, path)

        elif command.startswith('lit'):
            last_command = command
            path = pyperclip.paste()
            print(f'path : {path}')
            if path:
                re_translate_files(path)

        elif command.startswith('differ'):
            last_command = command
            path = pyperclip.paste()
            print(f'path : {path}')
            if path:
                check_lib_update(library, path)

        elif command.startswith('dbsave'):
            last_command = None
            save_books_to_db(library)

        # Handle other commands here.
        elif command.startswith('hello'):
            last_command = command
            print('Hello, world!')

        else:
            print('Unknown command. Please enter a valid command.')


if __name__ == '__main__':
    start_path = collector.get_path()
    library = collect_library(start_path)
    library.save_books_to_file()
    execute_commands(library)
