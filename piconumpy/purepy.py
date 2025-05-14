class array:
    __slots__ = ["data", "size"]

    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __add__(self, other):
        return array(
            number + other.data[index] for index, number in enumerate(self.data)
        )

    def __mul__(self, other):
        return array(other * number for number in self.data)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return array(number / other for number in self.data)

    def tolist(self):
        return list(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value


def empty(size):
    return array([0] * size)


def zeros(size):
    return array([0] * size)
