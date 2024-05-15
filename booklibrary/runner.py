
import os

import pyperclip
import collector
from book import Book
from library import Library


def get_book_from_file_path(filename, path, id):
    extension = os.path.splitext(filename)[1][1:]
    patterns = [] if extension not in collector.BOOK_EXTENTIONS else collector.get_patterns(os.path.splitext(filename)[0], collector.SEP_FOR_STAT)
    return Book(id, filename, patterns, path, '')

def collect_library(start_path):
    library = Library()
    current_id = 1
    if  os.path.exists(os.path.join(start_path, library.DEFAULT_LIB_FILE)):
        library.load_books_from_file(library.DEFAULT_LIB_FILE)
        current_id = max(book.get_id() for book in library.get_books())
    else:
        dic_names, dic_paths =  collector.get_filenames_and_paths(start_path)
        for i in dic_names.keys():
            library.add_book(get_book_from_file_path(dic_names.get(i), dic_paths.get(i), current_id))
            current_id += 1
    return library

def find_similar(library: Library, filename: str, count: int):
    patterns = collector.get_patterns(filename, collector.SEP_FOR_STAT)
    book_dict = {book.get_id(): 0 for book in library.get_books()}
    book_ranged = sorted(library.get_books(), key=lambda x: collector.check_pattern(x.get_patterns(), patterns), reverse=True)
    if len(book_ranged) <= count:
        return book_ranged
    return book_ranged[:count]

def find_similar2(library: Library, filename: str, count: int):
    patterns = collector.get_patterns(filename, collector.SEP_FOR_STAT)
    book_dict = {book.get_id(): book for book in library.get_books()}
    similar_dict = {item[0]: collector.check_pattern(item[1].get_patterns(), patterns)  for item in book_dict.items()}
    similar_sorted = sorted(similar_dict.items(), key=lambda item: item[1], reverse=True)
    return [f'{item[1]} : {book_dict.get(item[0])}' for item in similar_sorted[:count]]

def execute_commands(library):
    while True:
        command = input('Enter command: ').strip()

        if command.lower().startswith('quit'):
            break
        elif command.lower().startswith('one'):
            filename = pyperclip.paste()
            print('filename : {filename}')
            if filename:
                print(find_similar(library, filename, 5))
        elif command.lower().startswith('calc'):
            filename = pyperclip.paste()
            print('filename : {filename}')
            if filename:
                print('\n'.join(find_similar2(library, filename, 5)))
   
        # Handle other commands here.
        elif command == 'hello':
            print('Hello, world!')
        
        else:
            print('Unknown command. Please enter a valid command.')


if __name__ == '__main__':
    start_path = collector.get_path()
    library = collect_library(start_path)
    library.save_books_to_file()
    execute_commands(library)
