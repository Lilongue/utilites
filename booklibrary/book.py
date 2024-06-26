from entity import Entity


class Book(Entity):

    def __init__(self: 'Book', id: int, name: str, patterns: list[str], path: str, author: str = '', has_real_copy: bool = False, periodic_number: str = None, publishing_year: int = None) -> None:
        super().__init__(id, name, patterns, path)
        self._author = author
        self._has_real_copy = has_real_copy
        self._periodic_number = periodic_number
        self._publishing_year = publishing_year

    def __str__(self: 'Book') -> str:
        return f'Book(id={self._id}; name={self._name}; patterns={self._patterns}; path={self._path}; author={self._author})'

    def __repr__(self: 'Book') -> str:
        return str(self)
    
    def get_author(self: 'Book') -> str:
        return self._author
    
    def set_author(self: 'Book', author: str) -> None:
        self._author = author
    
    def get_has_real_copy(self: 'Book') -> bool:
        return self._has_real_copy
    
    def set_has_real_copy(self: 'Book', has_real_copy: bool) -> None:
        self._has_real_copy = has_real_copy
    
    def get_periodic_number(self: 'Book') -> str:
        return self._periodic_number
    
    def set_periodic_number(self: 'Book', periodic_number: str) -> None:
        self._periodic_number = periodic_number
    
    def get_publishing_year(self: 'Book') -> int:
        return self._publishing_year
    
    def set_publishing_year(self: 'Book', publishing_year: int) -> None:
        self._publishing_year = publishing_year
    
    def __eq__(self: 'Book', other: 'Book') -> bool:
        if not isinstance(other, Book):
            return False
        return self._name == other._name and self._patterns == other._patterns and self._path == other._path and self._author == other._author
    
    def __hash__(self: 'Book') -> int:
        return super().__hash__()
    
    def to_full_string(self: 'Book') -> str:
        return f'{self._id};{self._name};{",".join(self._patterns)};{self._path};{self._author};{self._has_real_copy};{self._periodic_number};{self._publishing_year}'
    
    @classmethod
    def from_string(cls: 'Book', string: str) -> 'Book':
        data = string.split(';')
        id = int(data[0])
        name = data[1]
        patterns = data[2].split(',')
        path = data[3]
        author = data[4]
        return cls(id, name, patterns, path, author)
    
    @classmethod
    def from_full_string(cls: 'Book', string: str) -> 'Book':
        data = string.split(';')
        id = int(data[0])
        name = data[1]
        patterns = data[2].split(',')
        path = data[3]
        author = data[4]
        has_real_copy = data[5] == 'True'
        periodic_number = data[6]
        publishing_year = int(data[7])
        return cls(id, name, patterns, path, author, has_real_copy, periodic_number, publishing_year)
