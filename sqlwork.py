import sqlite3


def TableCreating():
    try:
        connection = sqlite3.connect('SQLite.db')
        cursor = connection.cursor()
        print("\nSuccessfully Connected to SQLite")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS People(
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        image1 BLOB NOT NULL,
        image2 BLOB NOT NULL,
        image3 BLOB NOT NULL,
        image4 BLOB NOT NULL
        )
        ''')

    except sqlite3.Error as error:
        print("\nError while executing sqlite table", error)

    finally:
        if connection:
            connection.commit()
            connection.close()
            print("\nTable saved, sqlite connection closed")


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertInTable(id, full_name, image1, image2, image3, image4):
    try:
        connection = sqlite3.connect('SQLite.db')
        cursor = connection.cursor()
        print("\nSuccessfully Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO People
                                  (id, full_name, image1, image2, image3, image4) VALUES (?, ?, ?, ?, ?, ?)"""

        images = [convertToBinaryData(image) for image in [image1, image2, image3, image4]]
        data_tuple = (id, full_name, *images)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        connection.commit()
        print("\nImage and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("\nFailed to insert blob data into sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("\nThe sqlite connection is closed")


def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def readBlobData(empId):
    try:
        connection = sqlite3.connect('SQLite.db')
        cursor = connection.cursor()
        print("Successfully Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from People where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "full_name = ", row[1])
            full_name = row[1]
            images = row[2:6]
            photoPaths = [r"PATH\\" + full_name + f"{i + 1}.jpg" for i in range(4)]
            for img, path in zip(images, photoPaths):
                writeTofile(img, path)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The sqlite connection is closed")

def delete_person(id=None, full_name=None):
    try:
        connection = sqlite3.connect('SQLite.db')
        cursor = connection.cursor()
        print("\nSuccessfully Connected to SQLite")

        if id is not None:
            cursor.execute("DELETE FROM People WHERE id = ?", (id,))
            print(f"Person with id {id} deleted successfully.")
        elif full_name is not None:
            cursor.execute("DELETE FROM People WHERE full_name = ?", (full_name,))
            print(f"Person with full name '{full_name}' deleted successfully.")
        else:
            print("Error: You must provide either an id or a full name.")

        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("\nFailed to delete person from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("\nThe sqlite connection is closed")

def update_person(id, full_name=None, image1=None, image2=None, image3=None, image4=None):
    try:
        connection = sqlite3.connect('SQLite.db')
        cursor = connection.cursor()
        print("\nSuccessfully Connected to SQLite")

        images = [image1, image2, image3, image4]
        images = [convertToBinaryData(image) if image else None for image in images]
        updates = []
        parameters = []

        if full_name:
            updates.append("full_name = ?")
            parameters.append(full_name)
        for i, img in enumerate(images):
            if img:
                updates.append(f"image{i+1} = ?")
                parameters.append(img)

        if updates:
            parameters.append(id)
            sql_update_query = f"UPDATE People SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql_update_query, parameters)
            connection.commit()
            print(f"Person with id {id} updated successfully.")
        else:
            print("No updates provided.")

        cursor.close()

    except sqlite3.Error as error:
        print("\nFailed to update person in sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("\nThe sqlite connection is closed")


# Пример вызова функций:
# insertInTable(1, "Artyom", r"C:\someshit\Python\photos\image1.jpg", r"C:\someshit\Python\photos\image2.jpg", r"C:\someshit\Python\photos\image3.jpg", r"C:\someshit\Python\photos\image4.jpg")
# readBlobData(1)
# delete_person(id=1)
#delete_person(full_name="Artyom")
#update_person(1, full_name="New Name", image1="path/to/newimage1.jpg")