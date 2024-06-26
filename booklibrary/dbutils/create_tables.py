import sqlite3

CREATE_BOOK_TABLE_SCRIPT = """create table if not exists book
(
    book_id         integer not null
        constraint book_pk
            primary key AUTOINCREMENT,
    title           text    not null,
    book_path       text,
    patterns        text,
    has_real_copy   bool,
    author          text,
    periodic_number text,
    publishing_year integer
)"""

CREATE_READ_RECORD_TABLE_SCRIPT = """create table if not exists read_record
(
    record_id      integer not null
        constraint read_record_pk
            primary key AUTOINCREMENT,
    book_id        integer not null
        constraint read_record_book_book_id_fk
            references book,
    theme_id       text    not null,
    book_record_id integer not null,
    record_number  integer not null,
    special_mark   text,
    record_text    text    not null,
    comment        text
)"""

if __name__ == '__main__':
    connection = sqlite3.connect('home_lib.db')
    cursor = connection.cursor()
    cursor.execute(CREATE_BOOK_TABLE_SCRIPT)
    cursor.execute(CREATE_READ_RECORD_TABLE_SCRIPT)

    connection.commit()
    connection.close()
