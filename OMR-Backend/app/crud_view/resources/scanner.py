import sqlite3
from app.crud_view.resources import utilities
import json

# database = sqlite3.connect('AnswerKey.db',check_same_thread=False)
# cursor = database.cursor()



def main_omr(x,cursor,database):
    try:
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS Grades (Enrollment_ID INTEGER PRIMARY KEY, Test_ID INTEGER, Correct_Answers_Marked INTEGER,Aggregate_Score FLOAT)''')
    except:
        raise Exception('Cannot connect to database')
          

    path = x
# after cropping based on 4 corner points
    image = utilities.crop_excess(path)

    ID_number_box, ID_number_box_corners = utilities.crop_ID_Name(image)
    [x, y, w, h] = ID_number_box_corners

    cropped_img = image[y:474, x:714]
    cropped_img[0:h, 0:w] = (255, 255, 3)
    utilities.show_image(cropped_img, 'line 27')

    # Finding enrollment id
    enrollment_id, test_id = utilities.calc_enrollment_id(
        utilities.find_centre_points(ID_number_box[60:274, 0:374]), cursor)  # this is the region of interest, but it has to be generalised to any kind of vector

    score, aggregate = utilities.calculate_marks(cropped_img, cursor)
    dictionary = {'Enrollment Code': enrollment_id,
                  'Test_ID': test_id, 'Correct Answers Marked': score, 'Aggregate Score': round(aggregate, 2)}
    print(dictionary)

    json_data = json.dumps(dictionary, indent=4)
    print(json_data)

    try:
        cursor.execute('INSERT OR IGNORE INTO Grades (Enrollment_ID, Test_ID, Correct_Answers_Marked, Aggregate_Score) VALUES (?, ?, ?, ?)',
                       (enrollment_id, test_id, score, round(aggregate, 2)))
        database.commit()
        # database.close()
    except:
        raise Exception('Cannot connect to database')
    
    return True


