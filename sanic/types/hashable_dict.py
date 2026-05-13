# ff:type feature=util type=model
# ff:what Dictionary subclass that supports hashing by converting items to a so


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
