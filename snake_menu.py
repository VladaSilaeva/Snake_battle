class Snake:
    def __init__(self, name=None, chips=None, skin=None):
        self.name = name
        self.chips = []
        self.skin = ['head.png', 'body.png', 'turn.png', 'tail.png']
        if chips is not None:
            self.chips = chips
        if skin is not None:
            self.skin = skin
        self.rang = 0

    def __str__(self):
        if self.name is None:
            return ''
        return f'{self.name} --- {self.rang}'
