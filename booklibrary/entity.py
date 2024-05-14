class Entity:

    def __init__(self, id: int, name: str, patterns: list[str], path: str):
        self._id = id
        self._name = name
        self._patterns = patterns
        self._path = path

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_patterns(self):
        return self._patterns

    def get_path(self):
        return self._path

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_patterns(self, patterns):
        self._patterns = patterns

    def set_path(self, path):
        self._path = path

    def __str__(self):
        return f'Entity(id={self.id}; name={self.name}; patterns={self.patterns}; path={self.path})'

    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(f'{self._name}{self._path}')

    @classmethod
    def from_string(cls, string):
        data = string.split(';')
        id = int(data[1])
        name = data[2]
        patterns = data[3].split()
        path = data[4]
        return cls(id, name, patterns, path)
