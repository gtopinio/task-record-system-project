from db_helper_task import *

# function for showing main menu
def showMenu(User):
    userId = User[0]
    userName = User[1]

    # task listing application menu loop until valid option is selected/satistfied
    loop = True
    while loop:
        print("")
        print("=========== What would you like to do, {}? ===========".format(userName))
        print("[1] Add task")
        print("[2] Edit task")
        print("[3] Delete task")
        print("[4] View tasks per month/day")
        print("[5] View all tasks")
        print("[6] Mark task as done")
        print("[7] Add category")
        print("[8] Delete category")
        print("[9] View category")
        print("[10] Add task to category")
        print("[0] Log-out")

        choice = input("Enter choice: ")

        # input validity checker
        if choice.isnumeric() == False:
            print("Please enter a valid integer!\n")
        else:
            val = int(choice)
            if val < 0 or val > 10:
                print("Please enter a valid choice!\n")
            else:
                if val == 1:
                    addTask(userId)
                elif val == 2:
                    editTask(userId)
                elif val == 3:
                    deleteTask(userId)
                elif val == 4:
                    viewTask(userId)
                elif val == 5:
                    viewAllTasks(userId)
                elif val == 6:
                    markTaskDone(userId)
                elif val == 7:
                    addCategory(userId)
                elif val == 8:
                    deleteCategory(userId)
                elif val == 9:
                    viewCategory(userId)
                elif val == 10:
                    addTaskToCategory(userId)
                elif val == 0:
                    return False


# function for showing user login/signup menu
def showUserPage():

    # user menu loop till a valid option is chosen/satisfied
    loop = True
    while loop:
        print("\n=========== WELCOME TO THE TASK LISTER APP ===========")
        print("[1] Log-in")
        print("[2] Sign-up")
        print("[0] Shut-down Application")

        choice = input("Enter choice: ")

        # input validity checker
        if choice.isnumeric() == False:
            print("Please enter a valid integer!")
        else:
            val = int(choice)
            if val < 0 or val > 2:
                print("Please enter a valid choice!")
            elif val == 1:
                check = userLogin()
                if check == False:
                    loop = True
                else:  # when user is already registered
                    print("User found! Redirecting to the application...")
                    menu = showMenu(check)
                    if menu == False:
                        loop = True
                    else:
                        loop = True
            elif val == 2:  # user registration
                check = addUser()
                if check == False:
                    print("Sign-up not successful!")
                else:
                    print("Sign-up successful!")
            else:  # exit application
                print("Goodbye! Thanks for using the Task Listing App!\n")
                closeDatabase()
                loop = False


# Main Section
showUserPage()

# Group 1:
# Main Author: Mark Genesis C. Topinio
# Co-author: Glenn M. Arieta


# References:
#   MySQL implementation in Python: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
#   MySQL Connector/Python Developer Guide: https://dev.mysql.com/doc/connector-python/en/
#   Indexing while printing tuples: https://stackoverflow.com/a/23886515
#   RegEx email validation:         https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
