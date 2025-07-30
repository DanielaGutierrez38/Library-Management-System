import datetime #library to get the date and time the book was borrowed/returned

import pytz #also for date/time

class Customer:
  def __init__(self, customer_id, name, email):
    self.customer_id = customer_id
    self.name = name
    self.email = email
    self.borrowed_books = {} #Book object -> date/time (date/time library)

  def borrow_book(self, book):
    if (book in self.borrowed_books): #Check in borrowed_books dictionary if the book is already there. Print a message and return if this is the case
      print("This book has already been borrowed.")
      return None

    #Store the current date and time (with El Paso's timezone)
    borrow_date = datetime.datetime.now(pytz.timezone('America/Chihuahua'))

    #Add the book object as the key on the dictionary and borrow_date as its value
    self.borrowed_books.update({book:borrow_date})
    print(book, "borrowed by", self.name, "on", borrow_date)

  def return_book(self, book):
    if (book not in self.borrowed_books): #If book is not in the borrowed_books dictionary, print message and return
      print("This book was not borrowed by", self.name)
      return None

    #Otherwise, pop this book object from the dictionary
    self.borrowed_books.pop(book)

    #Store the current date and time (with El Paso's timezone)
    returned_date = datetime.datetime.now(pytz.timezone('America/Chihuahua'))

    print(book, "returned to the library by", self.name, "on", returned_date)

  def get_borrowed_books(self):
    #Print the books in the borrowed_books dictionary (this will use the __str__ method to print them)
    for book in self.borrowed_books:
      print(book)
