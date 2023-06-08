import os,re
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
            fileUpload = request.files["excel_file"]
            filename = fileUpload.filename
            fileUpload.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            ext = filename.split('.')[-1]
            fileNoExt = filename.split('.')[:-1][0]
            if ext == 'csv':
                df = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            elif ext in ['xlsx','xls']:
                df = pd.read_excel(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            else:
                return render_template("public/index.html",feedback="Format file salah",status='danger')

            df = onlyNumbersOnStr(df,'NPWP')
            df['NPWP'] = df['NPWP'].apply(lambda x:x if len(x)==15 else False)

            df['Status Kawin'] = df['Status Kawin'].astype(str).apply(setStatusKawin)
            df['KodePos'] = df['KodePos'].fillna(0).astype(int).astype(str).apply(lambda x: x if len(x)==5 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if len(x)>1 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if x[0] in ['1','2','3','4'] else False)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(lambda x: x if x.upper()=='INDONESIA' else False)
            df['Nama'] = uppercase_column(df['Nama'])
            df['Telpon'] = df['Telpon'].fillna('').astype(str).apply(cleanPhoneNumber)
            df['Telpon'] = df['Telpon'].fillna('').astype(str).apply(remove_special_characters)
            df['Nama'] = df['Nama'].fillna('').astype(str).apply(remove_special_characters)
            df['Jen. Kelamin'] = df['Jen. Kelamin'].fillna('').astype(str).apply(gender)
            df['TanggalLahir'] = df['TanggalLahir'].fillna('').astype(str).apply(to_datetime)
            df['RT'] = df['RT'].fillna('').astype(str).apply(format_r)
            df['RW'] = df['RW'].fillna('').astype(str).apply(format_r)
            df['Pendidikan'] = df['Pendidikan'].fillna('').astype(str).apply(pendidikan)
            df['Agama'] = df['Agama'].fillna('').astype(str).apply(agama)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(update_nationality)
            df.to_excel(os.path.join(app.config["IMAGE_UPLOADS"], fileNoExt+'.xlsx'))

            return render_template("public/index.html",feedback="",status='success',filenamesuccess=fileNoExt+'.xlsx')

            return [hists,request.files["excel_file"].filename]
def update_nationality(x):
    if x.upper() == 'INDONESIA':
        return 'I : Indonesia'
    return x


def agama(x):
    if x.lower() == 'islam':
        a = '4: ISLAM'  # Ganti dengan format yang diinginkan
    elif x.lower() == 'hindu':
        a = '1: HINDU'  # Ganti dengan format yang diinginkan
    elif x.lower() == 'budha':
        a = '2: BUDHA'  # Ganti dengan format yang diinginkan
    elif x.lower() == 'protestan':
        a = '3: PROTESTAN'
    elif x.lower() == 'katholik':
        a = '5: KATHOLIK'
    elif x.lower() == 'konghucu':
        a = '7: KONGHUCU'
    else:
        a = False
    return a
def pendidikan(x):
    if x == 'SMA' or x == 'SMP':
        pend = '00: Tanpa Gelar'
    elif x == 'd1':
        pend = '01: Diploma 1'
    elif x == 'd2':
        pend = '02: Diploma 2'
    elif x == 'd3':
        pend = '03: Diploma 3'
    elif x == 's1':
        pend = '04: S-1'
    elif x == 's2':
        pend = '05: S-2'
    elif x == 's3':
        pend = '06: S-3'
    else:
        pend = '99: Lainnya'
    return pend

def format_r(x):
    return x.zfill(3)

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

def remove_special_characters(x):
    return ''.join(e for e in x if e.isalnum())

def gender(x):
    if x.lower() in ['pria', 'p']:
        formatted_gender = 'P : Pria'
    elif x.lower() in ['wanita', 'w']:
        formatted_gender = 'W : Wanita'
    else:
        formatted_gender = gender
    return formatted_gender

def to_datetime(x):
    try:
        return pd.to_datetime(x).strftime('%Y%m%d')
    except:
        return x