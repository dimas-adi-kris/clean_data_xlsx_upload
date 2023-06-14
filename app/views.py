import os,re
import json
import pandas as pd
import numpy as np

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
    if request.method == "POST":

        if request.files:
            fileUpload = request.files["excel_file"]

            filename = fileUpload.filename
            ext = filename.split('.')[-1]
            fileNoExt = filename.split('.')[:-1][0]+'-'+''.join(str(v) for v in np.random.randint(1, [3, 5, 10]).tolist())
            filename = fileNoExt+'.'+ext

            fileUpload.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            if ext == 'csv':
                df_old = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], filename),)
            elif ext in ['xlsx','xls']:
                df_old = pd.read_excel(os.path.join(app.config["IMAGE_UPLOADS"], filename), )
            else:
                return render_template("public/index.html",feedback="Format file salah",status='danger')
            df_old = df_old.fillna('')
            kolomReq = [
                'NPWP','Status Kawin','KodePos','Status Pekerjaan',
            'Kebangsaan']
            df = df_old.copy()
            df = onlyNumbersOnStr(df,'NPWP')
            df['NPWP'] = df['NPWP'].apply(lambda x:x if len(x)==15 else False)

            df['Status Kawin'] = df['Status Kawin'].astype(str).apply(setStatusKawin)
            df['KodePos'] = df['KodePos'].replace({'':0}).astype(int).astype(str).apply(lambda x: x if len(x)==5 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if len(x)>1 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if x[0] in ['1','2','3','4'] else False)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(lambda x: x if x.upper()=='INDONESIA' else False)
            df['Nama'] = uppercase_column(df['Nama'])
            df['Telpon'] = df['Telpon'].fillna('').astype(str).apply(remove_special_characters)
            df['Telpon'] = df['Telpon'].fillna('').astype(str).apply(cleanPhoneNumber)
            df['TelpHP(62000000000000)'] = df['TelpHP(62000000000000)'].fillna('').astype(str).apply(remove_special_characters)
            df['TelpHP(62000000000000)'] = df['TelpHP(62000000000000)'].fillna('').astype(str).apply(cleanPhoneNumber)
            df['Nama'] = df['Nama'].fillna('').astype(str).apply(remove_special_characters)
            df['Jen. Kelamin'] = df['Jen. Kelamin'].fillna('').astype(str).apply(gender)
            df['TanggalLahir'] = df['TanggalLahir'].fillna('').astype(str).apply(to_datetime)
            df['Nama Pihak Yang Dapat Dihubungi'] = df['Nama Pihak Yang Dapat Dihubungi'].fillna('').astype(str).apply(noNumber)
            
            df['RT'] = df['RT'].fillna('').astype(str)
            df['RW'] = df['RW'].fillna('').astype(str)
            df = onlyNumbersOnStr(df,'RT')
            df = onlyNumbersOnStr(df,'RW')
            df['RT'] = df['RT'].apply(format_r)
            df['RW'] = df['RW'].apply(format_r)
            df['Pendidikan'] = df['Pendidikan'].fillna('').astype(str).apply(pendidikan)
            df['Agama'] = df['Agama'].fillna('').astype(str).apply(agama)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(update_nationality)
            df['NoIdentitas'] = df['NoIdentitas'].astype(str).apply(NIKconfirm)
            df.to_excel(os.path.join(app.config["IMAGE_UPLOADS"], fileNoExt+'.xlsx'), index=False)
            

            return render_template(
                "public/index.html",
                feedback="",
                status='success',
                column=df_old.columns,
                df_upload=df_old.values.tolist(),
                df_processed=df.values.tolist(),
                filenamesuccess=fileNoExt+'.xlsx',
                filenameoriginal=fileUpload.filename
                )

def NIKconfirm(x):
    if len(x)!=16:
        return "Panjang NIK harus 16 angka"
    elif  x[-4:] == '0000':
        return f"4 angka belakang NIK tidak boleh 0000"
    else:
        return x

def noNumber(x):
    judgement = any(char.isdigit() for char in x)
    return x if not judgement else ""

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
        a = x
    return a
def pendidikan(x):
    if x.upper().split(' ')[0] in ['SMA','SMP','SMAN','SLTA','SLTP','SMK','STM','SMU','SEKOLAH']:
        pend = '00: Tanpa Gelar'
    elif x.upper() in 'D1':
        pend = '01: Diploma 1'
    elif x.upper() in 'D2':
        pend = '02: Diploma 2'
    elif x.upper() in ['D3', 'DIII']:
        pend = '03: Diploma 3'
    elif x.upper() in ['S1','STRATA 1']:
        pend = '04: S-1'
    elif x.upper() in ['S2','STRATA 2']:
        pend = '05: S-2'
    elif x.upper() in ['S3','STRATA 3']:
        pend = '06: S-3'
    else:
        pend = '99: Lainnya'
    return pend

def format_r(x):
    return f"'{x.zfill(3)}"

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
    if x.startswith('0'):
        x = "'62" + x[1:]
    elif x.startswith('8'):
        x = "'628" + x[1:]
    elif x.startswith('62'):
        x = x
    else:
        x = False
    return x

def remove_special_characters(x):
    return ''.join(e for e in x if e.isalnum())

def gender(x):
    if x.lower() in ['pria', 'p','laki','laki-laki']:
        formatted_gender = 'P : Pria'
    elif x.lower() in ['wanita', 'w','cewek','perempuan']:
        formatted_gender = 'W : Wanita'
    else:
        formatted_gender = False
    return formatted_gender

def to_datetime(x):
    try:
        return pd.to_datetime(x).strftime('%Y/%m/%d')
    except:
        return x