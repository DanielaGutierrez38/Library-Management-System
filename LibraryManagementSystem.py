import csv #This library will help reading the csv file
import random #I'm using this library to create random numbers for the customer IDs
from datetime import date, timedelta

class LibraryManagementSystem:
  def __init__(self):
    self.books = {}  # Dictionary: ISBN -> Book object
    self.authors = {}  # Dictionary: name -> Author object
    self.customers = {}  # Dictionary: customerID -> Customer object
    self.genre_classification = {}  # Dictionary: Genre -> {set of ISBNs}
    self.waitlist = {}  # Dictionary: ISBN -> [list of customerIDs]

  def add_book(self, isbn, title, author_name, author_birth_year, year, copies, genre):

    if (isbn in self.books): #Check if the book is already in the library, and return if it is
      return "This book is already in the library system."

    #Otherwise, create a new Book object with the parameters passed in
    new_book = Book(isbn, title, author_name, author_birth_year, year, copies, genre)
    self.books[isbn] = new_book #Add this book to the dictionary, with the ISBN as the key and the object itself as the value

    #If this author is not in the library's author dictionary, add them
    if (author_name not in self.authors):
      #Create a new Author object
      new_author = Author(author_name, author_birth_year)
      #Add the author to the dictionary, with their name as the key and the Author object as the value
      self.authors[author_name] = new_author
    #Once the author is already in the dictionary (or if they already were there), add the book to their books set
    self.authors[author_name].add_book(new_book)

    #If the genre already exists in the genre_classification dictionary, just add the isbn to the set
    if (genre in self.genre_classification):
      self.genre_classification[genre].add(isbn)
    else: #Otherwise, create a set and all the isbn
      self.genre_classification[genre] = set([isbn])

  def register_customer(self, name, email):

    #Create a random customer id by generating a random number between 1 and 1000000
    customer_id = random.randint(1, 1000000)

    #Create a new Customer object with the customer id that was created and the two parameters passed in (name and email)
    new_customer = Customer(customer_id, name, email)
    #Add this customer to the customers dictionary, with the customer id as the key and the Customer object as the value
    self.customers[customer_id] = new_customer

    return customer_id

  def borrow_book(self, isbn, customer_id):

    #Check if the customer id exists in the customers dictionary. If it doesn't, print message and return
    if customer_id not in self.customers:
      print("This customer doesn't exist.")
      return None

    #If this book's copies are less than or equal to 0, print message and return
    if self.books[isbn].copies <= 0:
      print("This book is not available.")
      return None

    #Otherwise, add the book to the customer's borrowed_books dictionary.
    else:
      self.customers[customer_id].borrow_book(self.books[isbn])
      #Subtract one from the book's copies
      self.books[isbn].copies -= 1

  def return_book(self, isbn, customer_id):

    #Check if the customer is in the customers dictionary. If it isn't, print a message and return
    if customer_id not in self.customers:
      print("This customer doesn't exist.")
      return None

    #If the book is in the customer's borrowed books, call the return book method from the Customer class
    if self.books[isbn] in self.customers[customer_id].borrowed_books:
      self.customers[customer_id].return_book(self.books[isbn])
      #Add 1 to the book's copies
      self.books[isbn].copies += 1
    #If the customer didn't borrow this book, print message and return
    else:
      print("This customer did not borrow this book.")
      return None

  def search_books(self, query):

    #Search a book by using its tile
    if query == 1:
      #Receive the title of the book
      title = input("Please enter the title of the book you want to look for: ")

      #Look thorugh the library's books
      for book in self.books:
        #If there is a match in title, print that book using the __str__ function
        if self.books[book].title == title:
          print(self.books[book])

      print("Book not found") #In case the book doesn't exist in the library

    #Search an author's books
    if query == 2:
      #Receive the name of the author
      author = input("Please enter the name of the author you are looking for: ")

      #If the author is in the authors dictionary, print all of their books by using the author's books set
      if author in self.authors:
        for book in self.authors[author].books:
          print(book)
      else:
        print("Author not found")

    #Search for a book using its ISBN
    if query == 3:
      #Receive the book's ISBN
      isbn = input("Please enter the ISBN of the book you are looking for: ")

      #Check if the isbn is in the books dictionary. If it is, print that book using the __str__ function
      if isbn in self.books:
        print(self.books[isbn])

      print("ISBN not found")

  def display_available_books(self):

    #Traverse through the books in the books dictionary
    for book in self.books:

      #Print the book's entire information. Do this only if there are copies available
      if self.books[book].copies > 0:

        print("............................................")
        print("Title: ", self.books[book].title)
        print("ISBN: ", self.books[book].isbn)
        print("Author: ", self.books[book].author)
        print("Year: ", self.books[book].year)
        print("Copies available: ", self.books[book].copies)
        print("Genre: ", self.books[book].genre)
        print("............................................")

  def display_customer_books(self, customer_id):

    #Check if the customer id is in the customers dictionary. If it is, print all their borrowed books by calling the get_borrowed_books method in the
    #Customer class.
    if customer_id in self.customers:
      self.customers[customer_id].get_borrowed_books()

    #If the customer id is not in the dictionary, print message and return
    else:
      print("Invalid customer ID")
      return None

  def recommend_books(self, customer_id):

    #Create genres dictionary that will store the name of the genre as the key and the amount of times it appears in the customer's borrowed books dictionary as the value
    genres = {}
    #Create list that will store the recommended books
    recommended_books = []

    #Traverse customer's borrowed books
    for book in self.customers[customer_id].borrowed_books:
      #Check if the current genre is already in the dictionary. If it is, just add 1 to the value
      if book.genre in genres:
        genres[book.genre] +=1
      #If it isn't, create a new key and value pair
      else:
        genres.update({book.genre: 1})

    #Variable that will store the number of appearances of the most common genre
    most_common_genre = 0
    #Variable that will store the name of the most common genre
    genre_name = " "

    #Traverse the genres in genre to determine the most common
    for genre in genres:
      #If the current genre's value is greater than most_common_genre, then set the current genre as the most common genre and change the variables
      if genres[genre] > most_common_genre:
        most_common_genre = genres[genre]
        genre_name = genre

    #For loop that will go through 5 books from the most common genre and add them to the recommended_books list
    for i in range(5):
      recommended_books.append(list(self.genre_classification[genre_name])[i])

    #return the list
    return recommended_books

  def add_to_waitlist(self, isbn, customer_id):
    #Add customer id to the book's waitlist if there are 0 copies available.
    self.waitlist[isbn].append(customer_id)

  def check_late_returns(self, customer_id, days_threshold=14):

    #Get current date using imported library
    current_date = datetime.datetime.now(pytz.timezone('America/Chihuahua'))

    #Create list that will store the customer's late returns
    late_returns = []

    #Traverse customer's borrowed books
    for book in self.customers[customer_id].borrowed_books:
      #Create a variable that compares and gives back the difference between the current date and the date the book was borrowed in
      delta = current_date - self.customers[customer_id].borrowed_books.get(book)
      #If the difference is greater than the established threshold, append the book to the late_returns list
      if delta.days > days_threshold:
        late_returns.append(self.customers[customer_id].borrowed_books[book])

    #If the list is empty, print message
    if len(late_returns) == 0:
      print("This customer has no late returns!")

  def load_books_from_csv(self, filename):

      #try except block that will help with file reading
      try:
        #Read csv file
        with open(filename, newline = '', encoding = 'utf-8') as csvfile:
          reader = csv.DictReader(csvfile)
          #Traverse rows of csv file
          for row in reader:
            #Assign values to variables based on what is being read from the file. Use row['Column Name'] to access each element
            isbn = row['ISBN']
            title = row['Title']
            author_name = row['Author Name']
            author_birth_year = row['Author Birth Year']
            year = row['Year']
            copies = row['Copies']
            int_copies = int(copies)
            genre = row['Genre']

            #Add the book to the books dictionary
            self.add_book(isbn, title, author_name, author_birth_year, year, int_copies, genre)

      #If there is an exception, print message and print what exception is occuring
      except Exception as e:
        print("An error occurred during file reading", e)

  #Method that will show the menu and all the user interactions
  def run(self):

    choice = 0 #Variable to store the user's menu selection

    #while loop that will show the menu as long as choice is a positive number
    while choice >= 0:

      #Menu
      print("------------Library Management System------------")

      print(" 1-. Add Book")
      print(" 2-. Register Customer")
      print(" 3-. Borrow Book")
      print(" 4-. Return Book")
      print(" 5-. Search Books")
      print(" 6-. Display Available Books")
      print(" 7-. Display Customer's Borrowed Books")
      print(" 8-. Recommend Books")
      print(" 9-. Check Late Returns")
      print(" 10-. Exit")
      print("-------------------------------------------------- ")

      choice = input(" Welcome! Please type in a number from 1 to 10: ")
      choice = int(choice) #Take in user choice and parse to int

      #Option for user to add in a book to the library
      if (choice == 1):
        #Take in book information through user input
        print("Please enter the following information about the book")
        isbn_in = input("ISBN: ")
        title_in = input("Title: ")
        author_name_in = input("Author Name: ")
        author_birth_year_in = input("Author's Birth Year: ")
        year_in = input("Year of Publication: ")
        copies_in = input("Number of Copies: ")
        copies_int = int(copies_in) #Parse copies to int so the number can be compared and manipulated
        genre_in = input("Genre: ")

        #Add book to the books library by using the input data as parameters
        self.add_book(isbn_in, title_in, author_name_in, author_birth_year_in, year_in, copies_int, genre_in)

      #Register a new customer
      if (choice == 2):

        #Ask for customer's name and email
        customer_name = input("Please enter customer name: ")
        customer_email = input("Please enter customer email: ")
        #Call register_customer. Store the new ID in new_id
        new_id = self.register_customer(customer_name, customer_email)

        print("Customer successfully added. Customer ID: ", new_id)

      #Borrow a book
      if (choice == 3):

        #Enter customer ID and isbn of the book to be borrowed
        customer_id = input("Please enter customer ID: ")
        int_customer_id = int(customer_id)
        isbn = input("Please enter the ISBN of the book to be borrowed: ")
        #Check if the ISBN is in the library. If it is, call borrow_book
        if isbn in self.books:
          self.borrow_book(isbn, int_customer_id)
        #If it isn't, print message
        else:
          print("Invalid ISBN. Books not in library")

      #Return book
      if (choice == 4):
        #Enter customer ID and isbn of the book to be returned
        customer_id = input("Please enter customer ID: ")
        int_customer_id = int(customer_id)
        isbn = input("Please enter the ISBN of the book to be returned: ")
        #Check if the ISBN is in the library. If it is, call return_book
        if isbn in self.books:
          self.return_book(isbn, int_customer_id)
        #If it isn't, print message
        else:
          print("Invalid ISBN. Book not in library")

      if (choice == 5):

        #Display menu options. Depending on the input, the user will be able to search by tile, author name, or ISBN
        print("Please type: ")
        print("1 if you want to search by title")
        print("2 if you want to search by author name")
        print("3 if you want to search by ISBN")
        search = int(input()) #Take in user input and parse it to int

        #Call search books method and pass in search as the parameter, which will take care of the choice selected
        self.search_books(search)

      #Call display_available_books to print all the information about all the available books
      if (choice == 6):
        self.display_available_books()

      #Display customer's borrowed books
      if (choice == 7):
        #Take in customer id and parse to int
        customer_id = input("Please enter customer ID: ")
        int_customer_id = int(customer_id)

        #Check if the customer id is in the customers dictionary. If it is, call display_customer_books
        if int_customer_id in self.customers:
          self.display_customer_books(int_customer_id)
        #If it isn't, print message
        else:
          print("Customer not registered in the library.")

      if (choice == 8):
        #Enter customer ID
        customer_id = input("Please enter Customer ID: ")
        int_customer_id = int(customer_id) #Parse it to int

        #Check if the ID is in the customers dictionary
        if int_customer_id in self.customers:
          #If it is, call the recommend_books function
          recommended = self.recommend_books(int_customer_id)

          #Print list of recommended books
          print("Here are the ISBNs of some books that you might like based on your previously borrowed books: ")
          print(recommended)

        else: #If it isn't, print message
          print("Invalid Customer ID")

      if (choice == 9):
        #Enter customer ID
        customer_id = input("Please enter Customer ID: ")
        int_customer_id = int(customer_id) #Parse it to int

        #Check if the ID is in the customers dictionary
        if int_customer_id in self.customers:
          #If it is, call the check_late_returns function
          self.check_late_returns(int_customer_id)
        else: #Otherwise, print message
          print("Invalid Customer ID")

      #Exit library
      if (choice == 10):
        print("Thank you for using the library! See you next time")
        break #Immediatly stop the program from running

      #If the user enters an invalid number, print this message
      else:
        print("Please introduce a number from 1 to 10 to perform a valid command")


#Create a new LibraryManagementSystem object called system
system = LibraryManagementSystem()

#Call load_books_from_csv to read file
system.load_books_from_csv("Books.csv")
#Run the library, display menu and take in user input
system.run()
