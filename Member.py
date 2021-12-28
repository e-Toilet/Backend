#flask 套件
from flask import Flask,request
#flask 傳輸/解析https 文件套件,以及api建立
from flask_restful import Resource, Api,reqparse, abort
#轉json格式
import json
#匯入pandas 
import pandas as pd
#flask 連接mysql
import pymysql
import datetime 
import MySQLdb

class Signin(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            #建立args
            args = parser.parse_args()
            #提取參數
            _email = args['email']
            _password = args['password']
            _last_login_time = datetime.datetime.now()
            #呼叫sp
            cursor.callproc('sp_Login',(_email,_password,_last_login_time))
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
                    return {'Message': 'NO Data Found','Memberinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Memberinfo':data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class Register(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('name', type=str)
            #建立args
            args = parser.parse_args()
            #提取參數
            _email = args['email']
            _password = args['password']
            _name = args['name']
            _last_login_time = datetime.datetime.now()
            _status = 1 # 0 刪除 1 普通 2 管理員
            #呼叫sp
            cursor.callproc('sp_setNewMember',(_email,_name,_password,_last_login_time,_status))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'User creation success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                # return abort(1000, str(data[0]))
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getMemberInfo(Resource):
    def get(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _member_id = args['member_id']
            #呼叫sp
            cursor.callproc('sp_getMemberinfo',(_member_id,))
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
                    return {'Message': 'NO Data Found','Memberinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Memberinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)}, 1000

class getAllMember(Resource):
    def get(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getAllMember')
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
                return {'Message': 'success!!','Memberinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getMemberReviewCount(Resource):
    def get(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _member_id = args['member_id']
            #呼叫sp
            cursor.callproc('sp_getMemberReviewCount',(_member_id,))
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
                    return {'Message': 'NO Data Found','Review_count': data[0][0]},204
                else:
                    return {'Message': 'success!!','Review_count':data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class updateMemberInfo(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('name', type=str)
            #建立args
            args = parser.parse_args()
            #提取參數
            _email = args['email']
            _password = args['password']
            _name = args['name']
            _member_id = args['member_id']
            #呼叫sp
            cursor.callproc('sp_UpdateMemberinfo',(_member_id,_email,_name,_password))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'UserInfo Update success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class updateMemberStatus(Resource):
    def post(self):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            parser.add_argument('status', type=int)
            #建立args
            args = parser.parse_args()
            #print(args)
            #提取參數
            _member_id = args['member_id']
            _status = args['status']
            #呼叫sp
            cursor.callproc('sp_UpdateMemberStatus',(_member_id,_status))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'UserStatus Update success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

def Info (member_id):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getMemberinfo',(member_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'}   
            else:
                conn.commit()
                conn.close()
                return data[0][0] 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)}

def CountR(member_id):
        conn = MySQLdb.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getMemberReviewCount',(member_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            cursor.close()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'}   
            else:
                conn.commit()
                conn.close()
                return data[0][0]
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)}

class getMemberAllInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('member_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _member_id = args['member_id']
            #print(_member_id)
            info = Info(_member_id)
            count = CountR(_member_id)
            if info[0][0] is None or count[0][0] is None :
                    return {'Message': 'NO Data Found', 'Memberinfo':info, 'count' : count},204
            else:
                return {'Message': 'success' , 'Memberinfo':info, 'count' : count},200
        except Exception as e:
            #顯示錯誤訊息
            return {'error': str(e)},1000
    

