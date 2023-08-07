# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 19:38:20 2023

@author: WELCOME
"""

import os
import dill
import pandas as pd
from flask import Flask,render_template,request
import psycopg2 as sql

def create_app(test_config=None):
    # create and configure the app
    conn=sql.connect(database='test1',user='postgres',password='root',host='127.0.0.1',port='5432')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def main():
        return render_template("login.html",msg='')

    @app.route('/login',methods=['POST'])
    def login():
        ulist= [i for i in (request.form.values())]
        uname = str(ulist[0])
        password = str(ulist[1])
        q='select username,password from logindet where username=\'{}\''.format(uname)
        df = pd.read_sql_query(q, conn)
        if(not(df.empty)):
            if(df.iloc[0,0]==uname and df.iloc[0,1]==password):
                return render_template('index.html')
        return render_template('login.html',msg='Invalid credentials')

    @app.route('/signup',methods=['post'])
    def signup():
        silist = [i for i in (request.form.values())]
        Suname=str(silist[0])
        Spass = str(silist[1])
        Scpass = str(silist[2])
        if(Spass==Scpass):
            q='insert into logindet values(\'{}\',\'{}\')'.format(Suname,Spass)
            cur = conn.cursor()
            cur.execute(q)
            conn.commit()
            return render_template('login.html')

        else:
            return render_template('login.html',msg2='Confirm Password doesn\'t match the entered password')




    @app.route("/predict", methods=['post'])
    def pred():
        model = dill.load(open('model.pkl','rb'))
        features = [i for i in (request.form.values())]
        pred = model.content_recommender(str(features[0]))
        print(pred)
        return render_template("success.html",data1=features[0],data=pred)
        
    @app.route("/exit", methods=['POST'])
    def exit1():
        return render_template("login.html",msg='')
    @app.route('/home',methods=['POST'])
    def home():
        return render_template('index.html')
    return app
