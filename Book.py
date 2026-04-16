import uuid

class Book:
    def __init__(self, title, author, isbn, available=True, dropped=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

        self.uuid = str(uuid.uuid4())

        self.dropped = dropped

