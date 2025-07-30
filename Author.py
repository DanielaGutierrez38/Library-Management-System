class Author:
  def __init__(self, name, birth_year):
    self.name = name
    self.birth_year = birth_year
    self.books = set()

#Function that adds the book Object passed in to the author's books set
  def add_book(self, book):
    self.books.add(book)
