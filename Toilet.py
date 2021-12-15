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
import Review

class createNewToilet(Resource):
    def post(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('name', type=str)
            parser.add_argument('country_id', type=int)
            parser.add_argument('city_id', type=int)
            parser.add_argument('district_id', type=int)
            parser.add_argument('longitude', type=float)
            parser.add_argument('latitude', type=float)
            parser.add_argument('address',type= str)
            #建立args
            args = parser.parse_args()
            #提取參數
            _name = args['name']
            _country_id = args['country_id']
            _city_id = args['city_id']
            _district_id = args['district_id']
            _longitude = args['longitude']
            _latitude = args['latitude']
            _address = args['address']
            #呼叫sp
            cursor.callproc('sp_setNewToilet',(_name,_country_id,_city_id,_district_id,_longitude,_latitude,_address))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close() 
                print(data)       
                return {'Message': 'Toilet creation success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000



class getToiletByLoc(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            parser.add_argument('district_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _district_id = args['district_id']
            #呼叫sp
            cursor.callproc('sp_getToiletByLoc',(_district_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                print(data)
                return {'Message': 'Error!!'},1000 
            else:
                conn.commit()
                conn.close()
                print(data) 
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','Toiletinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Toiletinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000


class getToiletByLongitude(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('longitude', type=float)
            parser.add_argument('latitude', type=float)
            #建立args
            args = parser.parse_args()
            #提取參數
            _longitude = args['longitude']
            _latitude = args['latitude']
            print(_longitude,_latitude)
            #呼叫sp
            cursor.callproc('sp_getToiletByLongitude',(_longitude,_latitude))
            #提取回傳的資料
            data = cursor.fetchall()
            # data_dict = json.load(data[0][0])
            # data_json = json.dumps(data_dict)
            # avgRating = Review.getAvgRating(data_json['toilet_id'])
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                print(data)
                return {'Message': 'Error!!'},1000     
            else:
                conn.commit()
                conn.close()
                print(data) 
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','Toiletinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Toiletinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getToiletByID(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
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
            cursor.callproc('sp_getToiletbyID',(_toilet_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000   
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','Toiletinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Toiletinfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getAllToilet(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            cursor.callproc('sp_getAllToilet')
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000     
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','Toiletinfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','Toiletinfo': data[0][0]},200
 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class deleteToilet(Resource):
    def post(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
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
            cursor.callproc('sp_DeleteToilet',(_toilet_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'Message': 'Toilet deletion success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class updateToilet(Resource):
    def post(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('toilet_id', type=int)
            parser.add_argument('name', type=str)
            parser.add_argument('country_id', type=int)
            parser.add_argument('city_id', type=int)
            parser.add_argument('district_id', type=int)
            parser.add_argument('longitude', type=float)
            parser.add_argument('latitude', type=float)
            parser.add_argument('address',type=str)
            #建立args
            args = parser.parse_args()
            
            #提取參數
            _toilet_id = args['toilet_id']
            _name = args['name']
            _country_id = args['country_id']
            _city_id = args['city_id']
            _district_id = args['district_id']
            _longitude = args['longitude']
            _latitude = args['latitude']
            _address = args['address']
            #呼叫sp
            cursor.callproc('sp_UpdateToilet',(_toilet_id,_name,_country_id,_city_id,_district_id,_longitude,_latitude,_address))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()  
                conn.close()        
                return {'StatusCode':'200','Message': 'Toilet Update success'},200
            else:
                conn.commit()
                conn.close()
                return {'Message': str(data[0])},1000
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getCountry(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('country_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _country_id = args['country_id']
            #呼叫sp
            cursor.callproc('sp_getCountry',(_country_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'StatusCode':'1000','Message': 'Error!!'}     
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','CountryInfo': data[0][0]},204
                else :
                    return {'Message': 'success!!','CountryInfo': data[0][0]},204 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getCity(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('city_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _city_id = args['city_id']
            #呼叫sp
            cursor.callproc('sp_getCity',(_city_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000    
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'Message': 'NO Data Found','CityInfo': data[0][0]},204
                else:
                    return {'Message': 'success!!','CityInfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getDistrict(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
           #建立parser 
            parser = reqparse.RequestParser()
            # Parse the arguments
            parser.add_argument('district_id', type=int)
            #建立args
            args = parser.parse_args()
            #提取參數
            _district_id = args['district_id']
            #呼叫sp
            cursor.callproc('sp_getDistrict',(_district_id,))
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000     
            else:
                conn.commit()
                conn.close()
                if data[0][0] is None :
                    return {'StatusCode':'204','Message': 'NO Data Found','DistrictInfo': data[0][0]}
                else:
                    return {'StatusCode':'200','Message': 'success!!','DistrictInfo': data[0][0]} 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getAllCountry(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getAllCountry')
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000   
            else:
                conn.commit()
                conn.close()
                return {'Message': 'success!!','CountryInfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getAllCity(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getAllCity')
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000    
            else:
                conn.commit()
                conn.close()
                return {'Message': 'success!!','CityInfo': data[0][0]},200 
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'error': str(e)},1000

class getAllDistrict(Resource):
    def get(self):
        conn = pymysql.connect(host="localhost",user="root",password="12345",database="mydb" )
        cursor = conn.cursor()
        try:  
            #呼叫sp
            cursor.callproc('sp_getAllDistrict')
            #提取回傳的資料
            data = cursor.fetchall()
            #判斷回傳結果
            if len(data) == 0:
                conn.commit()
                conn.close()
                return {'Message': 'Error!!'},1000     
            else:
                conn.commit()
                conn.close()
                return {'Message': 'success!!','DistrictInfo': data[0][0]},200
                          
        except Exception as e:
            #顯示錯誤訊息
            conn.rollback()
            return {'StatusCode':'1000','error': str(e)},1000
