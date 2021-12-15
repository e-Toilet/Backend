#gevent 用來部署sever
from gevent.pywsgi import WSGIServer # Imports the WSGIServer
from gevent import monkey; 
import gevent
monkey.patch_all() 

#new
import json

#flask套件
from flask import Flask
from flask_restful import Resource, Api,reqparse

#waitress windows 的guicorn
from waitress import serve
import api

#api套件
import Member
import Toilet
import Review

#解決CORS傳輸協議問題
from flask_cors import CORS
#import threading
#flask api 啟動
app = Flask(__name__)
api = Api(app)

#Member
api.add_resource(Member.Signin, '/Signin')#登入get
api.add_resource(Member.Register, '/Register')#註冊get
api.add_resource(Member.getMemberInfo, '/getMemberInfo')
api.add_resource(Member.getAllMember, '/getAllMember')
api.add_resource(Member.updateMemberInfo, '/updateMemberInfo')
api.add_resource(Member.updateMemberStatus, '/updateMemberStatus')
api.add_resource(Member.getMemberReviewCount, '/getMemberReviewCount')
api.add_resource(Member.getMemberAllInfo,'/getMemberAllInfo')

#Toilet
api.add_resource(Toilet.getCity, '/getCity')
api.add_resource(Toilet.getCountry, '/getCountry')
api.add_resource(Toilet.getDistrict, '/getDistrict')
api.add_resource(Toilet.getAllToilet, '/getAllToilet')
api.add_resource(Toilet.deleteToilet, '/deleteToilet')
api.add_resource(Toilet.updateToilet, '/updateToilet')
api.add_resource(Toilet.getToiletByID, '/getToiletByID')
api.add_resource(Toilet.getToiletByLoc, '/getToiletByLoc')
api.add_resource(Toilet.createNewToilet, '/createNewToilet')
api.add_resource(Toilet.getToiletByLongitude, '/getToiletByLongtitude')

#開始頁面叫這三個?
api.add_resource(Toilet.getAllCity, '/getAllCity')
api.add_resource(Toilet.getAllCountry, '/getAllCountry')
api.add_resource(Toilet.getAllDistrict, '/getAllDistrict')

#Review
api.add_resource(Review.getReview, '/getReview')
api.add_resource(Review.getAvgRating, '/getAvgRating')
api.add_resource(Review.deleteReview, '/deleteReview')
api.add_resource(Review.updateReview, '/updateReview')
api.add_resource(Review.CreateNewReview, '/CreateNewReview')


#主程式
if __name__ == '__main__':
    CORS(app)#避免CORS通訊協定
    
    #使用app.run()會有 WARNING: This is a development server. Do not use it in a production deployment. 
    #bundle.crt 是把certificate.crt 和 ca_bundle.crt 合併 certificate 上 ca_bundle 下

    #new
    listenner = gevent.server._tcp_listener(('140.115.87.117', 8090), backlog= 500, reuse_addr= True)
    #listenner = gevent.server._tcp_listener(('etoilet.ddns.net', 8090), backlog= 500, reuse_addr= True)
    
    #server = WSGIServer(listenner, app, keyfile='private.key', certfile='bundle.crt')
    server = WSGIServer(listenner, app)
    server.serve_forever()
    
    


    
