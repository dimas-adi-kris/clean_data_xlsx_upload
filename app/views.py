import os
import json
import pandas as pd

from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
	return render_template("public/index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    hists = os.listdir(app.config["IMAGE_UPLOADS"])
    print(hists)
    if request.method == "POST":

        if request.files:
            fileUpload = request.files["image"]
            filename = fileUpload.filename
            fileUpload.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            ext = filename.split('.')[-1]
            if ext == 'csv':
                df = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            elif ext in ['xlsx','xls']:
                df = pd.read_excel(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            else:
                return render_template("public/index.html",feedback="Format file salah")

            df = onlyNumbersOnStr(df,'NPWP')
            df['NPWP'] = df['NPWP'].apply(lambda x:x if len(x)==15 else False)

            df['Status Kawin'] = df['Status Kawin'].apply(setStatusKawin)
            df['KodePos'] = df['KodePos'].fillna(0).astype(int).astype(str).apply(lambda x: x if len(x)==5 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if len(x)>1 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if x[0] in ['1','2','3','4'] else False)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(lambda x: x if x.upper()=='INDONESIA' else False)
            df['Nama'] = uppercase_column(df['Nama'])
            df['Telpon'] = df['Telpon'].fillna('').astype(str).apply(cleanPhoneNumber)

            return [hists,request.files["excel_file"].filename]


def setStatusKawin(x):
    return 'B: BELUM KAWIN' if x.lower()=='belum' else 'D: KAWIN' if x.lower()=='kawin' else 'K: CERAI' if x.lower()=='cerai' else False

def onlyNumbersOnStr(df,column):
    df[column] = df[column].astype(str).apply(lambda x:re.sub(r'\D', '', x))
    return df

def uppercase_column(col):
    return col.fillna('').astype(str).str.upper()

def lowercase_column(col):
    return col.fillna('').astype(str).str.lower()

def cleanPhoneNumber(x):
    if x.startswith('08'):
        x = '628' + x[2:]
    elif x.startswith('8'):
        x = '628' + x[1:]
    elif x.startswith('62'):
        x = x
    else:
        x = False
    return x