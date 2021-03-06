#flask 套件
from flask import Flask,request
#flask 傳輸/解析https 文件套件,以及api建立
from flask_restful import Resource, Api,reqparse
#轉json格式
import json
#匯入pandas 
import pandas as pd
#flask 連接mysql
import pymysql
import datetime 
import MySQLdb
class createNewReview(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            parser.add_argument('toilet_id', type=int)
            parser.add_argument('content', type=str)
            parser.add_argument('rating', type=float)

            #建立args
            args = parser.parse_args()
            #提取參數
            _member_id = args['member_id']
            _toilet_id = args['toilet_id']
            _content = args['content']
            _rating = args['rating']
            #呼叫sp
            cursor.callproc('sp_CreateReview',(_member_id,_toilet_id,_content,_rating))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'Review creation success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000



class getReview(Resource):
    def get(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('toilet_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _toilet_id = args['toilet_id']
            #呼叫sp
            cursor.callproc('sp_getReview',(_toilet_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000     
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','Reviewinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Reviewinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getAvgRating(Resource):
    def get(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('toilet_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _toilet_id = args['toilet_id']
            #呼叫sp
            cursor.callproc('sp_getAverageRating',(_toilet_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000    
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','AvgRating': data[0][0]},204
                else:
                    return {'Message': 'success!!','AvgRating': data[0][0]},200
                    return data[0][0]
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class deleteReview(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('review_id', type=int)

            #建立args
            args = parser.parse_args()
            #提取參數
            _review_id = args['review_id']
            #呼叫sp
            cursor.callproc('sp_DeleteReivew',(_review_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'Review deletion success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000


class updateReview(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('review_id', type=int)
            parser.add_argument('content', type=str)
            parser.add_argument('rating', type=float)
            #建立args
            args = parser.parse_args()
            
            #提取參數
            _review_id = args['review_id']
            _content = args['content']
            _rating = args['rating']

            #呼叫sp
            cursor.callproc('sp_UpdateReview',(_review_id,_content,_rating))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'Review Update success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000


