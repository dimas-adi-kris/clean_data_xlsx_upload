import os,re
import json
import pandas as pd
import numpy as np

from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
from app.helpers import find_col

with open("./Kode Dati.json",'r') as f:
    kode_dati = pd.DataFrame(json.loads(f.read()))

kode_dati['Kode'] = kode_dati['Kode Dati II'].str.split(':').str[0]
wilayah = kode_dati['Kode Dati II'].str.split(':').str[1].str.strip().str.split('-')
kode_dati['Propinsi'] = wilayah.str[0].str.strip().str.upper()
kode_dati['Kota Kab'] = wilayah.str[1].str.strip().str.upper()


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
            fileNoExt = filename.split('.')[:-1][0]+'-'+''.join(str(v) for v in np.random.randint(10, size=10).tolist())
            filename = fileNoExt+'.'+ext

            fileUpload.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            if ext == 'csv':
                df_old = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], filename),)
            elif ext in ['xlsx','xls']:
                df_old = pd.read_excel(os.path.join(app.config["IMAGE_UPLOADS"], filename), )
            else:
                return render_template("public/index.html",feedback="Format file salah",status='danger')
            df_old = df_old.fillna('')

            old_col = df_old.columns
            
            # Cleaning Column name
            col_change = {}
            for col in df_old.columns:
                if is_camel_case(col):
                    col_change[col] = ' '.join(camel_case_split(col))
                    col_change[col] = ' '.join(remove_special_characters(col_change[col]).split())
            df_old = df_old.rename(columns=col_change)
            kolomReq = [
                'NPWP','Status Kawin','Suami Istri','Kode Pos','Status Pekerjaan','Kebangsaan'
                ]
            for col in kolomReq:
                if col not in df_old.columns:
                    return render_template("public/index.html",feedback="Tidak ada kolom "+col,status='danger') 
            df = df_old.copy()

            npwp_s = find_col(df.columns,'NPWP')
            for npwp in npwp_s:
                df = onlyNumbersOnStr(df,npwp)
                df[npwp] = df[npwp].apply(lambda x:x if len(x)==15 else False)
            del npwp_s,npwp

            df['Status Kawin'] = df['Status Kawin'].astype(str).apply(setStatusKawin)
            df['Suami Istri'] = df.apply(suami_istri,axis=1)
            df['Kode Pos'] = df['Kode Pos'].fillna('0').astype(int).astype(str).apply(kodePosConfirm)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if len(x)>1 else False)
            df['Status Pekerjaan'] = df['Status Pekerjaan'].astype(str).apply(lambda x: x if x[0] in ['1','2','3','4'] else False)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(lambda x: x if x.upper()=='INDONESIA' else False)

            df['Masa Berlaku Identitas'] = '999123123'

            telp_s = find_col(df.columns,'telp')
            for telp in telp_s:
                df[telp] = df[telp].fillna('').astype(str).apply(remove_special_characters)
                df[telp] = df[telp].fillna('').astype(str).apply(cleanPhoneNumber)
            del telp_s,telp


            nama_s = find_col(df.columns,'nama')
            for nama in nama_s:
                df[nama] = uppercase_column(df[nama])
                df[nama] = df[nama].fillna('').astype(str).apply(remove_special_characters)
                df[nama] = df[nama].fillna('').astype(str).apply(noNumber)
            del nama_s,nama

            jen_kel_s = find_col(df.columns,'kelamin')
            for jen_kel in jen_kel_s:
                df[jen_kel] = df[jen_kel].fillna('').astype(str).apply(gender)
            del jen_kel_s,jen_kel

            tgl_s = find_col(df.columns,'tanggal')
            for tgl in tgl_s:
                df[tgl] = df[tgl].fillna('').astype(str).apply(to_datetime)
            del tgl_s,tgl
            tgl_s = find_col(df.columns,'tgl')
            for tgl in tgl_s:
                df[tgl] = df[tgl].fillna('').astype(str).apply(to_datetime)
            del tgl_s,tgl
            
            df['RT'] = df['RT'].fillna('').astype(str)
            df['RW'] = df['RW'].fillna('').astype(str)
            df = onlyNumbersOnStr(df,'RT')
            df = onlyNumbersOnStr(df,'RW')
            df['RT'] = df['RT'].apply(format_r)
            df['RW'] = df['RW'].apply(format_r)
            df['Pendidikan'] = df['Pendidikan'].fillna('').astype(str).apply(pendidikan)
            df['Agama'] = df['Agama'].fillna('').astype(str).apply(agama)
            df['Kebangsaan'] = df['Kebangsaan'].astype(str).apply(update_nationality)
            df['No Identitas'] = df['No Identitas'].astype(str).apply(NIKconfirm)
            df[['Kota','Propinsi']] = df[['Kota','Propinsi']].astype(str)
            df['Kode Dati II CARGCD'] = df.apply(kota,args=[kode_dati],axis=1)

            df = df.apply(lambda x: x.astype(str).str.upper())
            df.columns = old_col
            df.to_excel(os.path.join(app.config["IMAGE_UPLOADS"], fileNoExt+'.xlsx'), index=False)
            

            return render_template(
                "public/index.html",
                feedback="",
                status='success',
                column=old_col,
                df_upload=df_old.values.tolist(),
                df_processed=df.values.tolist(),
                filenamesuccess=fileNoExt+'.xlsx',
                filenameoriginal=fileUpload.filename
                )

def kodePosConfirm(x):
    if len(x) != 5:
        return "Panjang Kode harus 5 angka"
    elif x[-3:] == '000':
        return "3 angka belakang tidak boleh 000"
    else:
        return x



def kota(y, kode_):
    x = str(y['Kota']).strip()
    if (x == '') or (pd.isna(x)) or (x.lower() == 'nan'):
        return ''    
    res = kode_[kode_['Kota Kab'].str.contains(x.upper())]
    
    # kota
    if len(res) == 1:
        return res.iloc[0,0]
    else:
        # Kalo dk langsung ketemu, berarti hasil antara kosong atau ketemu banyak
        # pendekatan berikutnya, kabupaten atau kota. Hanya menerima "Kabupaten" atau "Kota" atau "Kab."
        # Tidak terima "Kab" karena ada "Sukabumi"
        # hasil res akan di filter lagi
        x_kab = y['Kota'].upper()
        if ("KABUPATEN" in x_kab):

            x_kab = x_kab.replace('KABUPATEN','').strip()
            res_k = kode_dati[kode_dati['Kota Kab'] == ('KAB. '+x_kab)]
            if len(res_k) == 1:
                return res_k.iloc[0,0]
        elif 'KAB.' in x_kab:
            x_kab = remove_special_characters(x_kab).replace('KAB','').strip()
            res_k = kode_dati[kode_dati['Kota Kab'] == ('KAB. '+x_kab)]
            if len(res_k) == 1:
                return res_k.iloc[0,0]
        elif 'KOTA' in x_kab:
            x_kab = x_kab.replace('KOTA','').strip()
            res_k = kode_dati[kode_dati['Kota Kab'] == ('KOTA '+x_kab)]
            if len(res_k) == 1:
                    return res_k.iloc[0,0]

        else:
            # Pendekatan propinsi
            # cek apakah x ada di propinsi res
            # diambil dari res
            # pendekatan ini bisa dilakukan kalo res lebih dari 1. 
            # kalo kosong, harus filter ulang
            res_prop = res[res['Kota Kab'].str.contains(y['Propinsi'].upper())]
            if len(res_prop) == 1:
                return res_prop.iloc[0,0]
            res_prop = res[res['Propinsi'].str.contains(y['Propinsi'].upper())]
            if len(res_prop) == 1:
                return res_prop.iloc[0,0]
            
            # pendekatan propinsi, filter ulang
            res_prop = kode_dati[kode_dati['Kota Kab'].str.contains(y['Propinsi'].upper())]
            if len(res_prop) == 1:
                return res_prop.iloc[0,0]
            res_prop = kode_dati[kode_dati['Propinsi'].str.contains(y['Propinsi'].upper())]
            if len(res_prop) == 1:
                return res_prop.iloc[0,0]
            
    return '9999: Di Luar Indonesia'

def suami_istri(row):
    if row['Status Kawin'] == 'K: KAWIN':
        return str(row['Suami Istri']).upper()
    elif row['Status Kawin'] in ['B: BELUM KAWIN','D: CERAI']:
        return 'NULL'
    else:
        return 'False'

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
    x = x.upper()
    if 'INDONESIA' in x:
        return 'I : Indonesia'
    return str(x)


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
    return str(a)

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
    return 'B: BELUM KAWIN' if x.lower()=='belum' else 'K: KAWIN' if x.lower()=='kawin' else 'D: CERAI' if x.lower()=='cerai' else False

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
        x = 'False'
    return str(x)

def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def remove_special_characters(x):
    return re.sub('[^a-zA-Z0-9 \n]', ' ', x)

def gender(x):
    if x.lower() in ['pria', 'p','laki','laki-laki']:
        formatted_gender = 'P : PRIA'
    elif x.lower() in ['wanita', 'w','cewek','perempuan']:
        formatted_gender = 'W : WANITA'
    else:
        formatted_gender = 'False'
    return formatted_gender

def to_datetime(x):
    try:
        return pd.to_datetime(x).strftime('%Y/%m/%d')
    except:
        return x