
import os

import pyperclip
import collector
from book import Book
from library import Library


def get_book_from_file_path(filename, path, id):
    extension = os.path.splitext(filename)[1][1:]
    patterns = [] if extension.lower() not in collector.BOOK_EXTENTIONS else collector.get_patterns(os.path.splitext(filename)[0], collector.SEP_FOR_STAT)
    return Book(id, filename, patterns, path, '')

def collect_library(start_path):
    library = Library()
    current_id = 1
    if  os.path.exists(os.path.join(start_path, library.DEFAULT_LIB_FILE)):
        print('Загружаю библиотеку из файла')
        library.load_books_from_file(library.DEFAULT_LIB_FILE)
        current_id = max(book.get_id() for book in library.get_books())
    else:
        dic_names, dic_paths =  collector.get_filenames_and_paths(start_path)
        for i in dic_names.keys():
            library.add_book(get_book_from_file_path(dic_names.get(i), dic_paths.get(i), current_id))
            current_id += 1
    return library

def find_similars(library: Library, path: str):
    files = collector.get_filenames(path)
    out = {}
    if files:
        for filename in files:
            out[filename] = find_similar2(library, filename, 4)
    with open('similar.log', 'w', encoding='utf-8') as f:
        for item in out.items():
            f.write('\n' + item[0] + '\n' + '-'*20 + '\n')
            f.write('\n'.join(item[1]))
    
def find_similar2(library: Library, filename: str, count: int):
    patterns = collector.get_patterns(filename, collector.SEP_FOR_STAT)
    book_dict = {book.get_id(): book for book in library.get_books()}
    similar_dict = {item[0]: collector.check_pattern(item[1].get_patterns(), patterns)  for item in book_dict.items()}
    similar_sorted = sorted(similar_dict.items(), key=lambda item: item[1], reverse=True)
    return [f'{item[1]} : {book_dict.get(item[0])}' for item in similar_sorted[:count]]

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
            filename = pyperclip.paste()
            print(f'path : {filename}')
            if filename:
               find_similars(library, filename)
   
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
