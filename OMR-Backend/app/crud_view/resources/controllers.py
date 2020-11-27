from flask import request,jsonify
from flask_restplus import Resource, Api
from flask_restplus import reqparse
from PIL import Image
from app import db
import sqlite3
from app import app
from app.models import Student
from .answer_key import main_key
from .scanner import main_omr


database = sqlite3.connect('AnswerKey.db',check_same_thread=False)
cursor = database.cursor()

class OMRREADERView(Resource):
    
    
    def post(self):
        '''
        This is where you'll read the omr sheets and compare them with the answerkey and store
        the results into the database.
        
        '''
        try:
            data=request.files['photo']
            print(data)
            img = Image.open(data.stream)
            img.save("Response.jpeg")
        # main_omr('Response.jpg')
            main_omr('C:\\Users\\Aniruddh\\Desktop\\mobileapp\\OMRBackend\\Response.jpeg',cursor,database)
        
            return jsonify({"args":"Successfully uploaded"})
        except Exception as exp:
            print(exp)
            return exp
            
            
    
    
    def get(self):
        '''
        This is a get request which finally queries all results from the database and appends them to a dictionary
        creating a list of dictionary and sends it back to the frontend so that it can be rendered.
        
        '''
        print("debug 1")
        resarray=[]
        print("debug 2")
        try:
            x = cursor.execute('''SELECT Enrollment_ID, Test_ID, Correct_Answers_Marked, Aggregate_Score FROM Grades''')
            print("debug 3")
        
            for Enrollment_ID,Test_ID,Correct_Answers_Marked,Aggregate_Score in x:
                res={}
                res.update({"Enrollment_ID":Enrollment_ID,"Test_ID":Test_ID,"Grade":Correct_Answers_Marked,"aggr_score":Aggregate_Score})
                resarray.append(res)
            print("debug 4")
            return jsonify(resarray)
        except:
            return jsonify(["No data available"])
            
        


class AnswerKeyReaderView(Resource):
    
    
    def post(self):
        try:
            print("debug 1")
            data=request.files['photo']
            print("debug 2")
            print(data)
            img = Image.open(data.stream)
            img.save("Answer.jpg")
            print("debug 3")
            # main_key('Answer.jpg')
            
            main_key('C:\\Users\\Aniruddh\\Desktop\\mobileapp\\OMRBackend\\Answer.jpg',cursor,database)
            print("debug 4")
        
            return jsonify({"args":"Successfully uploaded"})
        except Exception as exp:
            print(exp)
            return exp
            
    
   
    
