# imports
import mariadb
import datetime
import re

# INTIAL SECTION

# CAUTION: user and password fields must be changed according to the device of current user
# connecting to the root user first and check if the 'tasklistingdb' database exist
connInit = mariadb.connect(user="root", password="macmac924", host="localhost")

curInit = connInit.cursor()

# function to check whether or not 'tasklistingdb' database exist. If it doesn't exist, it should create the databases along with its tables
def databaseExist():
    # try-except-finally containing db existence checker and db tables creation
    try:
        curInit.execute("SHOW DATABASES")
        dbList = curInit.fetchall()
        databaseName = "tasklistingdb"  # database name for the project

        # Scenario 1: Database exist
        if (databaseName,) in dbList:
            print("Database found...")

        # Scenario 2: Database does not exist. Thus, create the database with its tables
        else:
            print("Database not found. Creating 'tasklistingdb' database...")
            curInit.execute("CREATE DATABASE {}".format(databaseName))

            # CAUTION: user and password fields must be changed according to the device of current user
            # genesis' connection
            conn = mariadb.connect(
                user="root",
                password="macmac924",
                host="localhost",
                database=databaseName,
            )

            cur = conn.cursor()

            # # mori's connection
            # conn = mariadb.connect(
            #     user="root",
            #     password="Arfarf123",
            #     host="localhost",
            #     database=databaseName,
            # )

            # cur = conn.cursor()

            # DDL statements for table: user
            userTable = """CREATE TABLE user(
                    user_id INT AUTO_INCREMENT,
                    username VARCHAR(20) NOT NULL,
                    password VARCHAR(15) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    CONSTRAINT user_user_id_pk PRIMARY KEY (user_id),
                    CONSTRAINT user_username_uk UNIQUE KEY (username),
                    CONSTRAINT user_email_uk UNIQUE KEY (email)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
                    """

            # DDL statements for table: category
            categoryTable = """CREATE TABLE category(
                    category_id INT AUTO_INCREMENT,
                    category_name VARCHAR(15),
                    creation_date DATE,
                    user_id INT,
                    CONSTRAINT category_user_id_fk FOREIGN KEY (user_id) REFERENCES user(user_id),
                    CONSTRAINT category_category_id_pk PRIMARY KEY (category_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
                    """

            # DDL statements for table: task
            taskTable = """CREATE TABLE task(
                    task_id INT AUTO_INCREMENT,
                    task_name VARCHAR(255),
                    task_details VARCHAR(255),
                    task_date DATE,
                    task_completed VARCHAR(10),
                    user_id INT,
                    category_id INT,
                    CONSTRAINT task_task_id_pk PRIMARY KEY (task_id),
                    CONSTRAINT task_user_id_fk FOREIGN KEY (user_id) REFERENCES user(user_id),
                    CONSTRAINT task_category_id_fk FOREIGN KEY (category_id) REFERENCES category(category_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
                    """

            # MariaDB to python code execution/commit
            cur.execute(userTable)
            conn.commit()
            cur.execute(categoryTable)
            conn.commit()
            cur.execute(taskTable)
            conn.commit()
            conn.close()

    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        connInit.close()


# function call
databaseExist()

# CAUTION: user and password fields must be changed according to the device of current user
conn = mariadb.connect(
    user="root", password="macmac924", host="localhost", database="tasklistingdb"
)
cur = conn.cursor()


# USER SECTION

# function for adding data to table: user
def addUser():
    print("\n=========== SIGN-UP ===========")

    email = input("Please enter your email: ")

    # email format validation
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email):  # when email format is valid
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        # user existence checker from table: user
        try:
            cur.execute("SELECT user_id FROM user WHERE username = ?", (username,))
            usernameResult = cur.fetchone()
            cur.execute("SELECT user_id FROM user WHERE email = ?", (email,))
            emailResult = cur.fetchone()

            if usernameResult is not None:
                print("Username already exists! Please use another username")
                return False
            elif emailResult is not None:
                print("Email already exists! Please use another email")
                return False
            else:
                loop = True
                while loop:
                    rePassword = input("Please re-type your password: ")
                    if password != rePassword:
                        print("Please match your password")
                    else:
                        cur.execute(  # add user to table: user using DML
                            "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                            (username, password, email),
                        )
                        loop = False
                        conn.commit()
                        return True
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
    else:  # when invalid email format
        print("Invalid Email! Please use an email domain")
        return False


# function for checking registered users/logging in
def userLogin():
    cur.execute("SELECT * FROM user")
    userResult = cur.fetchone()

    # taskinglistdb.user data checker
    if userResult is None:
        print("No users yet!")
        return False
    else:  # when taskinglistdb.user is not empty
        print("\n=========== LOG-IN ===========")

        email = input("Please enter your email: ")
        password = input("Please enter your password: ")

        # input checker: validate if email and password input is registered in taskinglistdb.user
        try:
            cur.execute(
                "SELECT user_id, username FROM user WHERE email = ? AND password = ?",
                (email, password),
            )
            result = cur.fetchone()
            if result is not None:
                return result
            else:
                print("User not found! Please make sure you have an account")
                return False

        except mariadb.Error as e:
            print(f"Error: {e}")


# TASK SECTION

# function for adding task/data to table: task
def addTask(userId):
    print("\n=========== CREATE TASK ===========")
    now = datetime.date.today()
    # CAUTION: taskname must be unique
    taskName = input("Please enter a task name: ")
    if taskName == "":
        print("Please enter a valid task name")
        return
    taskDetails = input("Please enter your task details: ")

    try:
        # add task to table: task using DML
        cur.execute(
            "INSERT INTO task (task_name, task_details, task_date, task_completed, user_id) VALUES (?, ?, ?, ?, ?)",
            (taskName, taskDetails, now, "No", userId),
        )
        conn.commit()
        print("Successfully created Task!")
    except mariadb.Error as e:
        print(f"Error: {e}")


# function for updating data from table: task
def editTask(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:

        print("\n=========== EDIT TASK ===========")
        findTask = input("Enter the task name that you want to edit: ")

        try:
            cur.execute("SELECT task_id FROM task WHERE task_name = ? AND user_id = ?", (findTask, userId))
            result = cur.fetchone()

            # task existence checker on table: task
            if result is not None:
                foundTaskId = result[0]
                newTaskName = input("Task found! Enter the new task name: ")
                newTaskDetails = input("Enter the new task details: ")

                cur.execute(  # update/modify task from table: task using DML
                    "UPDATE task SET task_name = ?, task_details = ? WHERE task_id = ?",
                    (newTaskName, newTaskDetails, foundTaskId),
                )
                conn.commit()

                while True:  # user has option to undo 'mark task as done' if needed
                    print("Is the task done?")
                    markDone = input("Y/N: ")
                    if markDone == "N" or markDone == "n":
                        cur.execute(  # update task_completed from table: task
                            "UPDATE task SET task_completed = 'No' WHERE task_id = ?",
                            (foundTaskId,),
                        )
                        break
                    elif markDone == "Y" or markDone == "y":
                        cur.execute(  # update task_completed from table: task
                            "UPDATE task SET task_completed = 'Yes' WHERE task_id = ?",
                            (foundTaskId,),
                        )
                        break
                    else:
                        print("Invalid output. Y/N?")
                conn.commit()
                print("Successfully edited Task!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for deleting task/data from table: task
def deleteTask(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()

    # task existence checker on table: task
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("\n=========== DELETE TASK ===========")
        findTask = input("Enter the task name that you want to delete: ")

        try:
            cur.execute("SELECT task_id FROM task WHERE task_name = ? AND user_id = ?", (findTask, userId))
            result = cur.fetchone()

            if result is not None:  # when task is found in table: task
                foundTaskId = result[0]

                # delete task from table: task using DML
                cur.execute("DELETE FROM task WHERE task_id = ?", (foundTaskId,))
                conn.commit()

                print("Task deleted!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for updating task_completed from table: task
def markTaskDone(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("\n=========== MARK TASK AS DONE ===========")
        findTask = input("Enter the task name that you want to mark as done: ")

        # task existence checker on table: task
        try:
            cur.execute(
                "SELECT task_id FROM task WHERE task_name = ? AND task_completed = 'No'",
                (findTask,),
            )
            result = cur.fetchone()
            if result is not None:  # when task is found
                foundTaskId = result[0]

                cur.execute(  # update task_completed from table: task
                    "UPDATE task SET task_completed = 'Yes' WHERE task_id = ?",
                    (foundTaskId,),
                )
                conn.commit()

                print("Task marked as done!")
            else:
                print("Task not found or it has already been completed!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for viewing date-categorized (day/month) data from table: task of the current user
def viewTask(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        try:
            monthName = ""
            dayOfmonth = ""

            for month in range(1, 12):
                for day in range(1, 31):
                    cur.execute(
                        "SELECT task_name, task_details, task_date, task_completed, DATE_FORMAT(task_date, '%M'), DATE_FORMAT(task_date, '%D'), category_id from task WHERE user_id = ? AND MONTH(task_date) = ? AND DAY(task_date) = ?",
                        (userId, month, day),
                    )
                    allTasks = cur.fetchall()
                    if allTasks is None:
                        continue
                    else:
                        for index, task in enumerate(allTasks, start=1):
                            if monthName == task[4] and dayOfmonth == task[5]:
                                print("{}.".format(index))
                                cur.execute(
                                    "SELECT category_name FROM category WHERE category_id = ?",
                                    (task[6],),
                                )
                                categoryName = cur.fetchone()
                                if categoryName is not None:
                                    print("Category name: {}".format(categoryName[0]))
                                else:
                                    print("Category name: None")
                                print("Task name: {}".format(task[0]))
                                print("Task details: {}".format(task[1]))
                                print("Created date: {}".format(task[2]))
                                print("Completed: {}".format(task[3]))

                            else:
                                monthName = task[4]
                                dayOfmonth = task[5]
                                print(
                                    "=========== VIEW TASK ({} {}) ===========".format(
                                        task[4], task[5]
                                    )
                                )
                                print("{}.".format(index))
                                cur.execute(
                                    "SELECT category_name FROM category WHERE category_id = ?",
                                    (task[6],),
                                )
                                categoryName = cur.fetchone()
                                if categoryName is not None:
                                    print("Category name: {}".format(categoryName[0]))
                                else:
                                    print("Category name: None")
                                print("Task name: {}".format(task[0]))
                                print("Task details: {}".format(task[1]))
                                print("Created date: {}".format(task[2]))
                                print("Completed: {}".format(task[3]))

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for viewing all data from table: task of the current user
def viewAllTasks(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()

    if taskResult is None:
        print("No tasks yet!")
    else:
        print("\n=========== VIEW ALL TASKS ===========")
        try:
            # show data from table: task using DML
            cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))

            allTasks = cur.fetchall()
            if allTasks is not None:
                for index, task in enumerate(allTasks, start=1):

                    print("{}.".format(index))

                    cur.execute(
                        "SELECT category_name FROM category WHERE category_id = ?",
                        (task[6],),
                    )
                    categoryName = cur.fetchone()
                    if categoryName is not None:
                        print("Category name: {}".format(categoryName[0]))
                    else:
                        print("Category name: None")

                    print("Task name: {}".format(task[1]))
                    print("Task details: {}".format(task[2]))
                    print("Created date: {}".format(task[3]))
                    print("Completed: {}".format(task[4]))

        except mariadb.Error as e:
            print(f"Error: {e}")


# CATEGORY SECTION

# function for adding category/data to table:category
def addCategory(userId):
    print("\n=========== ADD CATEGORY ===========")
    now = datetime.date.today()
    # CAUTION: categoryname must be not empty
    while True:
        categoryName = input("Please enter a category name: ")
        if categoryName == "":
            print("Please enter a valid category name")
        else:
            break
    try:
        # add category to taskinglistdb.category using DML
            cur.execute(
                "INSERT INTO category (category_name, creation_date, user_id) VALUES (?, ?, ?)",
                (categoryName, now, userId),
            )
            conn.commit()
            print("Successfully added category!")
    except mariadb.Error as e:
        print(f"Error: {e}")


# function for updating data from table:category
def editCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    else:
        print("\n=========== EDIT CATEGORY ===========")
        findCategory = input("Enter the category name that you want to edit: ")

        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ? AND user_id = ?",
                (findCategory, userId),
            )
            result = cur.fetchone()
            # category existence checker in table: category
            if result is not None:
                foundCategoryId = result[0]
                newCategory = input("Category found! Enter the new category name: ")

                cur.execute(  # update/modify category from table:category using DML
                    "UPDATE category SET category_name = ? WHERE category_id = ?",
                    (
                        newCategory,
                        foundCategoryId,
                    ),
                )
                conn.commit()
            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for deleting category/data from table:category
def deleteCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()

    # category existence checker on table: category
    if categoryResult is None:
        print("No categories yet!")
    else:

        print("\n=========== DELETE CATEGORY ===========")
        findCategory = input("Enter the category name that you want to delete: ")

        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ? AND user_id = ?",
                (findCategory, userId),
            )
            result = cur.fetchone()
            if result is not None:  # when category is found in table: category
                foundCategoryId = result[0]

                # delete category from table: category using DML
                cur.execute(
                    "DELETE FROM category WHERE category_id = ?", (foundCategoryId,)
                )
                conn.commit()

                print("Category deleted!")
            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for viewing data from taskinglistdb.category
def viewCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    else:
        print("\n=========== VIEW CATEGORY ===========")

        # category list for user reference
        cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
        allCategories = cur.fetchall()

        if allCategories is not None:
            for index, category in enumerate(allCategories, start=1):
                print("{}. {}".format(index, category[1]))

        findCategory = input("Enter the category name that you want to view: ")

        # category name existence checker on table: category
        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ? AND user_id = ?",
                (findCategory, userId),
            )
            result = cur.fetchone()
            if result is not None:  # when found
                foundCategoryId = result[0]

                cur.execute(
                    "SELECT category_name, creation_date FROM category WHERE category_id = ?",
                    (foundCategoryId,),
                )
                categoryResult = cur.fetchone()

                print("Category name:", (categoryResult[0]))
                print("Category date:", (categoryResult[1]))

            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for categorizing a task
def addTaskToCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    # checker for data existence in table: category
    if categoryResult is None:
        print("No categories yet!")
    elif taskResult is None:
        print("No tasks yet!")
    else:
        print("\n=========== ADD TASK TO CATEGORY ===========")
        # task finder from table: task
        findTask = input("Enter the task name: ")

        try:

            cur.execute("SELECT task_id FROM task WHERE task_name = ?", (findTask,))
            taskResult = cur.fetchone()

            if taskResult is not None:
                # category finder from table: category
                findCategory = input("Enter the category: ")
                cur.execute(
                    "SELECT category_id FROM category WHERE category_name = ? AND user_id = ?",
                    (findCategory, userId),
                )
                categoryResult = cur.fetchone()

                if categoryResult is not None:
                    # loop till user select a valid option
                    while True:
                        # confirmation for adding a task to a category
                        print(
                            "Category found! Do you want to add your task to this category?"
                        )
                        confirm = input("Y/N: ")

                        if confirm == "N" or confirm == "n":
                            print("Add-Task-To-Category stopped")
                            break
                        elif confirm == "Y" or confirm == "y":
                            cur.execute(  # add category_id to task from table: task
                                "UPDATE task SET category_id = ? WHERE task_id = ?",
                                (categoryResult[0], taskResult[0]),
                            )
                            conn.commit()
                            print("Successfully inserted Task to Category!")
                            break
                        else:
                            print("Invalid output. Y/N?")
                else:
                    print("Category not found!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# close connection to the database
def closeDatabase():
    conn.close()
