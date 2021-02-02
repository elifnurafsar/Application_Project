import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select,Table,update, and_
from sqlalchemy import func
from datetime import datetime, date, timedelta

app = Flask(__name__, static_folder="images")
app.secret_key='secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = "b'q\xc2\xdb{XC.\x8e}\xe0[72\x1a\xa7u,J\xedW\x13\xda\xa5\x0c'"
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://ffisjkajvhdpiu:7ebb663aa1dbb1ceb21df24a626fd15ab5142aa8a09f500b27fa83b9a5a413a7@ec2-176-34-123-50.eu-west-1.compute.amazonaws.com:5432/dcqh84alivc9op'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
conn = db.engine.connect()

Kumas = db.Table('kumas', db.metadata, autoload=True, autoload_with=db.engine)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=['GET', 'POST'])
def index():
    image_names = os.listdir('./images')
    return render_template('home.html',image_names = image_names)


@app.route("/deneme", methods=['GET', 'POST'])
def deneme():
    image_names = os.listdir('./images')
    return render_template('deneme.html', image_name=image_names)


@app.route("/filter", methods=[ 'GET','POST'])
def filter():
    return render_template('filter.html')


@app.route("/iletisim", methods=[ 'GET','POST'])
def iletisim():
    return render_template('iletisim.html')


@app.route("/upload/<filename>")
def send_image(filename):
    return send_from_directory("images", filename)


@app.route("/upload", methods=['GET','POST'])
def upload():
    tur_temp = request.form.get('tur')
    desen_temp = request.form.get('desen')
    renk_temp = request.form.get('renk')
    fiyat_temp = request.form.get('fiyat')
    aciklama_temp = request.form.get('aciklama')
    print(fiyat_temp)
    print(desen_temp)
    print(renk_temp)
    print(aciklama_temp)
    print(tur_temp)
    image_variable = 0
    image1 = ""
    image2 = ""
    image3 = ""
    target = os.path.join(APP_ROOT, 'images\\')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        fileName = file.filename
        if image_variable == 0:
            image1 = fileName
            print(image1+"***")
        elif image_variable == 1:
            image2 = fileName
            print(image2+"***")
        elif image_variable == 2:
            image3 = fileName
            print(image3+"***")
        else:
            print("3 images are enough")
        destination = "\\".join([target,fileName])
        print(destination)
        file.save(destination)
        image_variable = image_variable + 1 
    
    values = {1, tur_temp, desen_temp, renk_temp, fiyat_temp, aciklama_temp, image1, image2, image3}
    query = Kumas.insert().values(values)
    conn.execute(query)
    return render_template('upload.html')
