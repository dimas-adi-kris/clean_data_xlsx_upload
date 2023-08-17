import os,re,glob
import json
import pandas as pd
import numpy as np


from app import app
# from app.models.user import User
# from app.models.add_data import add_new_data
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, url_for, session,Blueprint
import datetime
from werkzeug.utils import secure_filename
from app.helpers import *

excel = Blueprint('excel', __name__)


@excel.route("/result", methods=["POST"])
def result():
    os.makedirs(app.config["EXCEL_UPLOADS"], exist_ok=True)
    if request.files:
        fileUpload = request.files["excel_file"]

        filename = fileUpload.filename
        ext = filename.split('.')[-1]
        # Mendapatkan waktu saat ini
        waktu_sekarang = datetime.datetime.now()
        waktu = waktu_sekarang.strftime("%Y%m%d%H%M%S")
        fileNoExt = filename.split('.')[:-1][0]+'-'+waktu+'-'+''.join(str(v) for v in np.random.randint(3, size=3).tolist())
        filename = fileNoExt+'-ori'+'.'+ext

        fileUpload.save(os.path.join(app.config["EXCEL_UPLOADS"], filename))

        if ext == 'csv':
            df_old = pd.read_csv(os.path.join(app.config["EXCEL_UPLOADS"], filename), dtype=str, keep_default_na=False)
        elif ext in ['xlsx','xls']:
            df_old = pd.read_excel(os.path.join(app.config["EXCEL_UPLOADS"], filename), dtype=str, keep_default_na=False)
        else:
            return render_template("public/index.html",feedback="Format file salah",status='danger')
        df_old = df_old.fillna('')

        old_col = df_old.columns
        col_change = {}
        for col in df_old.columns:
            if is_camel_case(col):
                col_change[col] = ' '.join(camel_case_split(col))
                col_change[col] = ' '.join(remove_special_characters(col_change[col]).split())
        df_old = df_old.rename(columns=col_change)
        # kolomReq = [
        #     'NPWP','Status Kawin','Suami Istri','Kode Pos','Status Pekerjaan','Kebangsaan'
        #     ]
        # for col in kolomReq:
        #     if col not in df_old.columns:
        #         return render_template("public/index.html",feedback="Tidak ada kolom "+col,status='danger') 
        df = df_old.copy()

        column_checked = []
        column_names = find_col(df.columns,'NPWP')
        for column_name in column_names:
            df[column_name] = df[column_name].apply(npwpFormat)
            column_checked.append(column_name)
        try:
            # Cleaning Column name

            df['Status Kawin'] = df['Status Kawin'].apply(setStatusKawin)
            column_checked.append('Status Kawin')
            df['Suami Istri'] = df.apply(suami_istri,axis=1)
            column_checked.append('Suami Istri')
            df['Kode Pos'] = df['Kode Pos'].fillna('0').apply(kodePosConfirm)
            column_checked.append('Kode Pos')
            df['Status Pekerjaan'] = df['Status Pekerjaan'].apply(lambda x: x if len(x)>1 else 'FALSE')
            df['Status Pekerjaan'] = df['Status Pekerjaan'].apply(lambda x: x if x[:1] in ['1','2','3','4'] else 'FALSE')
            column_checked.append('Status Pekerjaan')

            df['Masa Berlaku Identitas'] = '999123123'

            column_names = find_col(df.columns,'telp')
            for column_name in column_names:
                df[column_name] = df[column_name].fillna('').apply(remove_special_characters).str.replace(' ','')
                df[column_name] = df[column_name].apply(cleanPhoneNumber)
                column_checked.append(column_name)


            column_names = find_col(df.columns,'nama')
            for column_name in column_names:
                df[column_name] = uppercase_column(df[column_name])
                df[column_name] = df[column_name].fillna('').apply(remove_special_characters)
                df[column_name] = df[column_name].apply(noNumber)
                column_checked.append(column_name)

            column_names = find_col(df.columns,'kelamin')
            for column_name in column_names:
                df[column_name] = df[column_name].fillna('').apply(gender)
                column_checked.append(column_name)
            
            
            column_names = find_col(df.columns,'kota')
            for column_name in column_names:
                df[column_name] = df[column_name].fillna('').replace({'NULL':''})
                column_checked.append(column_name)

            column_names = find_col(df.columns,'Propinsi')
            for column_name in column_names:
                df[column_name] = df[column_name].fillna('').replace({'NULL':''})
                column_checked.append(column_name)

            column_names = find_col(df.columns,'tanggal')
            for column_name in column_names:
                df[column_name] = df[column_name].fillna('').apply(to_datetime)
                column_checked.append(column_name)
            # column_names = find_col(df.columns,'tgl')
            # for column_name in column_names:
            #     df[column_name] = df[column_name].fillna('').apply(to_datetime)
            del column_names,column_name
            
            df['RT'] = df['RT'].fillna('')
            df['RT'] = df['RT'].apply(onlyNumbersOnStr)
            df['RT'] = df['RT'].apply(format_r)
            column_checked.append('RT')
            df['RW'] = df['RW'].fillna('')
            df['RW'] = df['RW'].apply(onlyNumbersOnStr)
            df['RW'] = df['RW'].apply(format_r)
            column_checked.append('RW')
            df['Pendidikan'] = df['Pendidikan'].fillna('').apply(pendidikan)
            column_checked.append('Pendidikan')
            df['Agama'] = df['Agama'].fillna('').apply(agama)
            column_checked.append('Agama')
            df['Kebangsaan'] = df['Kebangsaan'].apply(update_nationality)
            column_checked.append('Kebangsaan')
            df['No Identitas'] = df['No Identitas'].apply(NIKconfirm)
            column_checked.append('No Identitas')
            df['Kode Dati II CARGCD'] = df.apply(kota,args=[kode_dati],axis=1)
            column_checked.append('Kode Dati II CARGCD')

            df = df.apply(lambda x: x.str.upper())
            c1 = df.where(df.values==df_old.values).notna()

            # false_rows, false_columns = np.where(c1 == False)
            daftar_revisi = []
            for false_row, false_col in zip(*np.where(c1 == False)):
                daftar_revisi.append((c1.columns[false_col], c1.index[false_row],df.iloc[false_row,false_col] , df_old.iloc[false_row, false_col]))

            total_true = c1.to_numpy().sum()
            total_false = c1.size - total_true
            os.makedirs(app.config["EXCEL_UPLOADS"], exist_ok=True)
            if total_false == 0:
                os.makedirs(app.config["EXCEL_UPLOADS"]+'/fix/', exist_ok=True)
                filename_to_save = fileNoExt+'-fix'
                to_xls(df,os.path.join(app.config["EXCEL_UPLOADS"]+'/fix/', filename_to_save+'.xls'))
            else:
                os.makedirs(app.config["EXCEL_UPLOADS"]+'/revisi/', exist_ok=True)
                filename_to_save = fileNoExt+'-full'
                to_xls(df,os.path.join(app.config["EXCEL_UPLOADS"]+'/revisi/', filename_to_save+'.xls'))

                filename_not_valid = fileNoExt+'-not-valid-revisi'
                df_not_valid = df[df[column_checked].apply(lambda x: any([val == '' for val in x]), axis=1)]
                to_xls(df_not_valid,os.path.join(app.config["EXCEL_UPLOADS"]+'/revisi/', filename_not_valid+'.xls'))

                filename_valid = fileNoExt+'-valid-revisi'
                df_valid = df[df[column_checked].apply(lambda x: all(val != '' for val in x), axis=1)]
                to_xls(df_valid,os.path.join(app.config["EXCEL_UPLOADS"]+'/revisi/', filename_valid+'.xls'))

                empty_row_counts = {col: len(df[df[col] == '']) for col in column_checked}
                df.columns = old_col
                with open(os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.json'), 'w+') as f:
                    json.dump(empty_row_counts, f, indent=4)

            





            # df.to_excel(os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.xlsx'), index=False)
            # to_xls(df,os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.xls'))
            # df.to_csv(os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.csv'), index=False)

            return render_template(
                "pages/result/index.html",
                feedback="",
                status='success',
                column=old_col,
                df_upload=df_old.values.tolist(),
                df_processed=df.values.tolist(),
                # filenameXlsx=filename_to_save+'.xlsx',
                filenameXls=filename_to_save+'.xls',
                # filenameCsv=filename_to_save+'.csv',
                # filenameoriginal=fileUpload.filename,
                filenameoriginal=filename,
                daftar_revisi=daftar_revisi,
                total_false=total_false,
                fileNoExt=fileNoExt,
                )
        except Exception as e:
            print(filename,e)
            return render_template(
                "pages/home/index.html",
                )


@excel.route('/daftar-excel/')
@excel.route('/daftar-excel/<status>')
def daftar_excel(status=None):
    daftar_file = glob.glob(app.config["EXCEL_UPLOADS"]+'/*')

    daftar_nama_file_pre = []

    for i in daftar_file:
        hasil  = i.split('.')[1].split('\\')[-1]
        if not hasil.endswith("-ori"):
            daftar_nama_file_pre.append(hasil)
    daftar_nama_file_pre = np.unique(daftar_nama_file_pre)
    daftar_nama_file = []
    if status == "Semua":
        daftar_nama_file = daftar_nama_file_pre
    elif status:
        for nama_file in daftar_nama_file_pre:
            if nama_file.endswith(status):
                daftar_nama_file.append(nama_file)
    else:
        daftar_nama_file = daftar_nama_file_pre

    daftar_nama_file = np.unique(daftar_nama_file)
    if status:
        return render_template("pages/daftar_file/table_daftar_excel.html",daftar_nama_file=daftar_nama_file,status=status)
    return render_template(
        "pages/daftar_file/index.html",
        daftar_nama_file=daftar_nama_file,
        status=status
        )


@excel.route('/daftar-excel/detail-kolom/<filename>')
def detail_kolom(filename):
    
    return render_template(
        "pages/daftar_file/detail_kolom.html",
        # df=df,
        filename=filename
        )