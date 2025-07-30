class Book:
  def __init__(self, isbn, title, author, author_birth_year, year, copies, genre):
    self.isbn = isbn
    self.title = title
    self.author = author
    self.author_birth_year = author_birth_year
    self.year = year
    self.copies = copies
    self.available_copies = copies
    self.genre = genre

  #Prints out the title, author and year of the book as a string
  def __str__(self):
    return f"{self.title} by {self.author} ({self.year})"
