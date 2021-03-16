# Assignment 5
# GUI application that allows the user to browse, search, and sort the Restaurants database
import tkinter
import sqlite3
import os

# GUI customizations for color, fonts, and spacing (you may change)
bg_color = 'lightblue'
fg_color = 'black'
label_fg = '#1d3549'
data_font = "Verdana 12 normal"
label_font = "Verdana 12 bold"
pad = 20

db = None  # db object is a global variable, that initially has no value


# GUI object that represents the Restaurant Browser application
class RestaurantBrowser:
    def __init__(self, records):
        # Main window and Label
        self.main_window = tkinter.Tk()
        self.main_window.title("Restaurant Browser")
        self.main_window.geometry('660x650')
        self.main_window.configure(background=bg_color)
        tkinter.Label(self.main_window, text='Restaurant Browser', fg=label_fg, bg=bg_color, padx=pad, pady=pad,
                      font=label_font).grid(row=0, column=0, sticky=tkinter.constants.W)

        # Search Button and Entry field
        self.search_value = tkinter.StringVar()
        tkinter.Button(self.main_window, text="Search", command=self.search_db, fg=label_fg, bg="#adebad", padx=10,
                       font=label_font, borderwidth=0).grid(row=0, column=2, sticky=tkinter.constants.W)
        self.search_value_entry = tkinter.Entry(self.main_window, width=15, font=data_font,
                                                textvariable=self.search_value).grid(row=0, column=3)

        # Column header Buttons -- when a button is clicked, the restaurant data is sorted by the selected column
        try:
            tkinter.Button(self.main_window, text='Name', command=lambda: self.sort_db('Name'), fg=label_fg,
                           bg="#2db92d", anchor="w", padx=pad, font=label_font, borderwidth=0).grid(row=1, column=0,
                                                                                                    sticky=tkinter.constants.EW)
            tkinter.Button(self.main_window, text='City', command=lambda: self.sort_db('City'), fg=label_fg,
                           bg="#32cd32", anchor="w", padx=pad, font=label_font, borderwidth=0).grid(row=1, column=1,
                                                                                                    sticky=tkinter.constants.EW)
            tkinter.Button(self.main_window, text='State', command=lambda: self.sort_db('State'), fg=label_fg,
                           bg="#5bd75b", anchor="w", padx=pad, font=label_font, borderwidth=0).grid(row=1, column=2,
                                                                                                    sticky=tkinter.constants.EW)
            tkinter.Button(self.main_window, text='Cuisine', command=lambda: self.sort_db('Cuisine'), fg=label_fg,
                           bg="#84e184", anchor="w", padx=pad, font=label_font, borderwidth=0).grid(row=1, column=3,
                                                                                                    sticky=tkinter.constants.EW)

            # When the GUI is initialized, call this function to display all of the records in the restaurant database
            self.display_records(records)

            tkinter.mainloop()
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)

    # Display all of the restaurant data in the records parameter. 'records' will contain the results of the most
    # recent SQL query
    def display_records(self, records):
        # Clear any previous records before displaying results of most recent SQL query For example, if a query that
        # displays all records is followed by one that displays fewer results (as in a search), then you must first
        # clear the previous results from the window.

        try:
            self.clear_previous_results()

            row_number = 2
            for record in records:
                tkinter.Label(self.main_window, text=record[1], fg=fg_color, bg=bg_color, padx=pad,
                              font=data_font).grid(
                    row=row_number, column=0, sticky=tkinter.constants.W)
                tkinter.Label(self.main_window, text=record[2], fg=fg_color, bg=bg_color, padx=pad,
                              font=data_font).grid(
                    row=row_number, column=1, sticky=tkinter.constants.W)
                tkinter.Label(self.main_window, text=record[3], fg=fg_color, bg=bg_color, padx=pad,
                              font=data_font).grid(
                    row=row_number, column=2, sticky=tkinter.constants.W)
                tkinter.Label(self.main_window, text=record[4], fg=fg_color, bg=bg_color, padx=pad,
                              font=data_font).grid(
                    row=row_number, column=3, sticky=tkinter.constants.W)
                row_number = row_number + 1

        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)

    def clear_previous_results(self):
        # Clear any previous records before displaying results of current SQL query
        for label in self.main_window.grid_slaves():
            if int(label.grid_info()['row']) > 1:
                label.grid_forget()

    # Search the database across all columns using a wildcard search with the user-provided search value
    def search_db(self):
        try:
            # get the database cursor so we can execute queries
            cursor = db.cursor()

            # add the user-provided search_value to the SQL query
            # use the OR operator to search across all columns
            # use LIKE to do wildcard search
            sql = "SELECT * FROM RESTAURANT WHERE Name LIKE '%" + self.search_value.get() + "%' \
                 OR City LIKE '%" + self.search_value.get() + "%' \
                 OR State LIKE '%" + self.search_value.get() + "%' \
                 OR Cuisine LIKE  '%" + self.search_value.get() + "%'ORDER BY Name"
            # execute the query
            cursor.execute(sql)
            records = cursor.fetchall()

            # if at least one record found, call self.display_records to display the results of the query
            if len(records) > 0:
                self.display_records(records)
            else:
                # clear all previous displayed data
                self.clear_previous_results()
                # print not found message
                tkinter.Label(self.main_window, text="No results found", fg=fg_color, bg=bg_color, padx=pad,
                              font=data_font).grid(row=2, column=0, sticky=tkinter.constants.W)
        # error handling
        except sqlite3.IntegrityError as err:
            print('Integrity Error:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error:', err)
        except sqlite3.Error as err:
            print('Error:', err)
            # catch all error handler, if the above handlers do not apply
        except Exception as err:
            print(err)

        # print("search_db function")
        # TODO Define, execute, and fetch the results of the SQL query
        # TODO Call self.display_records to display the results of the query
        # TODO If no search value is provided, display all of the restaurants in the database

    # Sort the database on the column selected by the user
    def sort_db(self, column_name):
        try:
            # get the database cursor so we can execute queries
            cursor = db.cursor()

            # add the user-provided search_value to the SQL query
            # use the given column name to sort
            sql = "SELECT * FROM RESTAURANT ORDER BY " + column_name

            # execute the query
            cursor.execute(sql)
            records = cursor.fetchall()
            self.display_records(records)

        except sqlite3.IntegrityError as err:
            print('Integrity Error:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error:', err)
        except sqlite3.Error as err:
            print('Error:', err)
            # catch all error handler, if the above handlers do not apply
        except Exception as err:
            print(err)
        # print("sort_db function")
        # TODO Define, execute, and fetch the results of the SQL query
        # TODO Call self.display_records to display the results of the query


# Connect to the database
# Define, execute, and fetch the results of the SQL query that retrieves all restaurant data
# Create the GUI object, RestaurantBrowser, and pass it the records containing the restaurant data
def main():
    global db
    try:
        dbname = 'restaurants.db'
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            sql = 'SELECT * FROM RESTAURANT ORDER BY Name'
            cursor.execute(sql)
            records = cursor.fetchall()
            RestaurantBrowser(records)
            db.close()
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


main()
