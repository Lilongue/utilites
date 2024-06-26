from entity import Entity


class Book(Entity):

    def __init__(self: 'Book', id: int, name: str, patterns: list[str], path: str, author: str = '') -> None:
        super().__init__(id, name, patterns, path)
        self._author = author

    def __str__(self: 'Book') -> str:
        return f'Book(id={self._id}; name={self._name}; patterns={self._patterns}; path={self._path}; author={self._author})'

    def __repr__(self: 'Book') -> str:
        return str(self)
    
    def get_author(self: 'Book') -> str:
        return self._author
    
    def set_author(self: 'Book', author: str) -> None:
        self._author = author
    
    def get_author(self: 'Book') -> str:
        return self._author
    
    def __eq__(self: 'Book', other: 'Book') -> bool:
        if not isinstance(other, Book):
            return False
        return self._name == other._name and self._patterns == other._patterns and self._path == other._path and self._author == other._author
    
    def __hash__(self: 'Book') -> int:
        return super().__hash__()
    
    @classmethod
    def from_string(cls: 'Book', string: str) -> 'Book':
        data = string.split(';')
        id = int(data[0])
        name = data[1]
        patterns = data[2].split(',')
        path = data[3]
        author = data[4]
        return cls(id, name, patterns, path, author)
