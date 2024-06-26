# utilites

utilites for home usage

## Library processing (booklibrary package)

utilites for work with home library

**Основные компоненты**

### collector

Содержит методы для сбора информации о файлах на диске.
При запуске из консоли, ищет в файлах из указанной папки, включая вложенные папки, похожие по названию.
Имена файлов деляться на кусочки на основании стандартных разделителей.

По результатам выполнения сохраняется 2 файла:
- result.log - список всех найденных файлов
- matches.log - список похожих файлов

**Основные методы**

| Метод  | Описание |
| ------------- | ------------- |
| get_path  | позволяет ввести или взять из буфера обмена стартовую папку  |
| get_patterns  | делит строку на паттерны используя группу разделителей слов  |
| check_pattern  | сравнивает два набора паттернов  |
| count_separators  | подсчитывает колличество встреченных разделителей в переданном словаре  |
| get_filenames_and_paths  | возвращает список файлов и путей до них начиная с переданной папки, включая вложенные  |
| find_same2  | ищет похожие файлы на основе их паттернов (в переданном словаре имен)  |
| get_file_extension_statistics  | выводит статистику расширений файлов  |
| get_filenames  | получает список файлов в папке без учета вложенных  |


### runner
Содержит методы для построения и обработки библиотеки.
Призапуске из консоли строит библиотеку из файлов начиная со стартовой папки или читает ее из файла и запускает обработчик команд. Построенная библиотека сохраняется в файле по умолчанию library.log
**Доступные команды:**

| Команда  | Действие |
| ------------- | ------------- |
| quit  | выход  |
| calc  | выводит 5 самых похожих файлов библиотеки на переданный (взятый из буфера обмена)  |
| many  | для всех файлов из переданной папки ищет 3 максимально похожих в библиотеке и сохраняет результат в файл similar.log (файлы с русскими буквами в именах  не обрабатываются и не копируются)  |
| lit  | для всех файлов из переданной папки делает копии с обратной транслитерацией и сохраняет их в папке /retranslated  |
| dbsave  | сохраняет библиотеку в базу данных  |
| hello  | просто выводит Hello, world!  |

> [!NOTE]
> Если команда оставлена пустой - то повторяется последняя использованная, если она была. 

### literation
Содерщит метод транслитерации и обратной транслитерации (transliterate и re_transliterate)
А также детектор русских кукв в тексте detect_russian_letters.
Самостоятельно - не запускается

## Утилиты для работы с SqlLite (booklibrary.dbutils)

utilites for work with SqlLite database

**Основные компоненты**

### create_tables
Создает пустую базу данных со структурой таблиц для библиотеки

### book_dao
Содержит класс BookDao, который содержит основные методы для работы с базой данных.

**Доступные методы:**

| Метод  | Параметры | Действие |
| ------------- | ------------- | ------------- |
| create_book  | book: Book | создает запись в таблице books  |
| get_book  | book_id: int | получет запись из таблицы books по id |
| update_book  | book: Book | сетит в таблице books запись по id |
| delete_book  | book_id: int | удаляет запись из таблицы books по id  |

