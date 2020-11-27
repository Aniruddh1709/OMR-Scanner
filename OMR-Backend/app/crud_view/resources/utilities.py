import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import sqlite3
import math
import sys


def crop_excess(path):  # This function crops the original image into ROI based on 4 corner points in the document

    image = cv2.imread(str(path))
    if np.shape(image) == ():
        raise Exception('The URL link is invalid or corrupted.')

    # gray it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur it
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # canny edge detection
    edged = cv2.Canny(gray, 30, 35)
    # edged = cv2.bitwise_not(edged)
    show_image(edged, '1st image that is going to be cropped')

    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # cv2.drawContours(image, contours, -1, (0,255,0), 3)
    # show_image(image)

    if len(contours) == 0:
        raise Exception('Upload a better image - line 32')

    sorted_contours = sorted(contours, key=cv2.contourArea)[:50]
    cnt = 0
    if sorted_contours == None:
        raise Exception('No contours found, please upload better image - line 41-U')

    # this is be a 4X2 array having the coordinates of the corners
    corner_points = np.zeros((4, 2))
    i = 0
    shape = image.shape
    store_points = []
    # the four corner points that we are interested in are in the ratio of 4 to 20 wrt y dimension of image
    for c in sorted_contours:
        if cv2.contourArea(c) > 0:
            ratio = int(shape[1] / cv2.contourArea(c))
            if ratio > 0:
                store_points.append((ratio, findCentre(c)))

    store = [i[1] for i in store_points[-4:]]
    store = np.array(store)

    corner_points = store.astype(int)
    try:
        cropped_img = four_point_transform(image, corner_points)  # cropped image
    except:
        raise Exception('Please crop the image properly - line 59')
    # print(cropped_img.shape)
    cropped_img = cv2.resize(cropped_img, (714, 474))
    title = "cropped_img"
    show_image(cropped_img, title)

    return cropped_img


def crop_ID_Name(cropped_img):  # crops the enrollment/ID number box out from the image

    # gray it
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    # blur it
    gray = cv2.GaussianBlur(cropped_img, (5, 5), 0)
    # canny edge detection
    edged = cv2.Canny(gray, 30, 35)

    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours) == 0:
        raise Exception('Upload a better image - line 89')

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]
    peri = cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], 0.02 * peri, True)
    ID_number_box = four_point_transform(
        cropped_img, approx.reshape(4, 2))  # cropped image
    x, y, w, h = cv2.boundingRect(approx)
    ID_number_box_corners = [x, y, w, h]
    show_image(ID_number_box, 'Cropped  - line 101')

    return ID_number_box, ID_number_box_corners


def find_centre_points(answer_region):

    gray = cv2.cvtColor(answer_region, cv2.COLOR_BGR2GRAY)

    '''# gray = cv2.erode(gray, (5,5), iterations=5, borderType=cv2.BORDER_CONSTANT)
    # gray = cv2.dilate(gray, (5,5), iterations=5, borderType= cv2.BORDER_CONSTANT)
    #gray = cv2.adaptiveThreshold(gray, 255,)
    #gray_not = cv2.bitwise_not(gray)'''

    gray = cv2.GaussianBlur(gray, (5, 5), 5, sigmaY=5)
    thresh = cv2.threshold(gray, 150, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)

    title = "Thresholded and clear border - line 117"
    show_image(thresh, title)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[:100]

    contours = imutils.grab_contours(contours)

    centre = []
    copy_answer_region = answer_region.copy()

    for c in contours:

        (x, y), radius = cv2.minEnclosingCircle(c)
        radius = int(radius)

        if radius >= 7 and radius <= 10:
            centre.append(findCentre(c))

            cv2.drawContours(copy_answer_region, c, -1, (0, 255, 0), 2)

    show_image(copy_answer_region, title)
    print("Number of responses detected=", len(centre))

    return centre


def calculate_marks(cropped_img, cursor):
    '''
    ->Extract marks from database
    ->find centres of responses
    ->compare
    '''
    try:
        sql = cursor.execute('SELECT X, Y FROM coordinates')
    except:
        raise Exception('Cannot connect to database - line 191')

    answers = []
    for x, y in sql:
        temp = [x, y]
        answers.append(temp)
    print("Answers from database:", answers)
    responses = find_centre_points(cropped_img)
    responses = sort(responses)
    print("Responses without editing:", responses)
    responses = remove_extra_circles(responses)
    score = 0

    for item in range(len(responses)):
        for ans in range(len(answers)):
            if distance(responses[item], answers[ans]) <= 7:
                # print("Matching response:", responses[item])
                score += 1
                print((responses[item], answers[ans], distance(responses[item], answers[ans])))
    aggregate = (score / len(answers)) * 100
    return score, aggregate


def findCentre(c):  # this function returns the centre of each corner point

    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        raise Exception('Answers not marked properly, please check - line 171')
    centre = [cX, cY]

    return centre


def show_image(img, title=1):
    return
    try:
        cv2.imshow('{}'.format(str(title)), img)
    except:
        raise Exception('Image invalid or corrupted')
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def sort(unsorted_list):  # first sort wrt y coordinate then x coordinate
    sorted_list = sorted(unsorted_list, key=lambda x: (x[1], x[0]))

    for ele in range(len(sorted_list) - 1):
        if (sorted_list[ele + 1][1] - sorted_list[ele][1]) <= 2:
            sorted_list[ele + 1][1] = sorted_list[ele][1]

    sorted_list = sorted(unsorted_list, key=lambda x: (x[1], x[0]))

    return sorted_list


def sorting(lst):
    return lst[0]


def remove_extra_circles(responses):  # sort list of responses obtained
    undesired_points = []

    for i in range(len(responses) - 1):

        if responses[i][1] == responses[i + 1][1]:
            # kid has marked 2 answers, now to eliminate all responses for that question
            if responses[i + 1][0] - responses[i][0] <= 65:
                points = [[x, y]
                          for (x, y) in responses if y == responses[i][1]]
                print(points)
                for x1 in range(len(points)):
                    flag = False
                    for x2 in range(x1 + 1, len(points)):
                        if(points[x2][0] - points[x1][0] <= 65):
                            flag = True
                            undesired_points.append(points[x2])
                    if flag:
                        undesired_points.append(points[x1])

    print("undesired Points:")
    print(undesired_points)
    res = []
    [res.append(x) for x in undesired_points if x not in res]
    print("Undesired Points, after removing redundant")
    print(res)
    for k in range(len(res)):
        responses.remove(res[k])

    print("FINAL RESPONSES:")
    print(responses)

    return responses


def calc_enrollment_id(centres, cursor):
    centres.sort(key=sorting)
    temp = []
    if len(centres) < 15:
        raise Exception('Enrollement/Test ID incorrectly marked')
    for lst in centres[:10]:
        y_cor = lst[1]
        lower = y_cor - 4
        upper = y_cor + 4
        try:
            num = cursor.execute(
                'SELECT num FROM enrollment_id WHERE Y >= ? AND Y <= ?', (lower, upper))
        except:
            raise Exception('Cannot connect to database - line 293')
        temp.append(list(num)[0][0])

    enroll_id = int("".join([str(i) for i in temp]))
    temp_lst = []
    for lst in centres[10:]:
        y_cor = lst[1]
        lower = y_cor - 4
        upper = y_cor + 4
        try:
            num = cursor.execute(
                'SELECT num FROM enrollment_id WHERE Y >= ? AND Y <= ?', (lower, upper))
        except:
            raise Exception('Cannot connect to database')
        temp_lst.append(list(num)[0][0])

    test_id = int("".join([str(i) for i in temp_lst]))
    return enroll_id, test_id


def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def analyse_answer_key(cropped_img, cursor, database):
    '''
    This function also stores answers from answer key, into a database, if user doesnt input new answer key, it has to read from database, else it has
    to compute new answer key The output of the code is a list that stores the centres of each answer option, whether newly input or extract
    from database
     '''
    answers = find_centre_points(
        cropped_img)  # answers obtained from centre points
    answers = sort(answers)  # sorts the list and returns
    try:
        cursor.execute('''DELETE FROM coordinates''')
        id = 1
        for x, y in answers:
            cursor.execute(
                '''INSERT INTO coordinates (ID, X, Y) VALUES (?, ?, ?)''', (id, x, y))
            id = id + 1
        database.commit()
    except:
        raise Exception('Can not connect to database')
