import sqlite3
from app.crud_view.resources import utilities

# database = sqlite3.connect('AnswerKey.db')
# cursor = database.cursor()

def main_key(x,cursor,database):
    try:
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS coordinates (ID INTEGER PRIMARY KEY, X INTEGER, Y INTEGER)''')
    except:
        raise Exception("Cannot Connect to database")



    path = x

    image = utilities.crop_excess(path)  # after cropping based on 4 corner points

    ID_number_box, ID_number_box_corners = utilities.crop_ID_Name(image)
    [x, y, w, h] = ID_number_box_corners

    cropped_img = image[y:474, x:714]
    cropped_img[0:h, 0:w] = (255, 255, 3)

    utilities.analyse_answer_key(cropped_img, cursor, database)
    print("Answers uploaded successfully")
    database.commit()
    # database.close()
    return True


