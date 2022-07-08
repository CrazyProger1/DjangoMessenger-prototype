class Sender:
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
