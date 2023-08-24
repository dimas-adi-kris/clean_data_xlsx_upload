import os, re, glob
import json
import pandas as pd
import numpy as np


from app import app

# from app.models.user import User
# from app.models.add_data import add_new_data
from flask import (
    render_template,
    request,
    redirect,
    jsonify,
    make_response,
    send_file,
    send_from_directory,
    abort,
    url_for,
    session,
    Blueprint,
    flash,
)
import datetime
from werkzeug.utils import secure_filename
from app.helpers import *
import app.models.ActivityModel as Activity

excel = Blueprint("excel", __name__)


@excel.route("/result", methods=["POST"])
def result():
    os.makedirs(app.config["EXCEL_UPLOADS"], exist_ok=True)
    if request.files:
        fileUpload = request.files["excel_file"]

        filename = fileUpload.filename
        ext = filename.split(".")[-1]
        # Mendapatkan waktu saat ini
        waktu_sekarang = datetime.datetime.now()
        waktu = waktu_sekarang.strftime("%Y%m%d%H%M%S")
        fileNoExt = (
            filename.split(".")[:-1][0]
            + "-"
            + waktu
            + "-"
            + "".join(str(v) for v in np.random.randint(3, size=3).tolist())
        )
        filename = fileNoExt + "-ori" + "." + ext

        fileUpload.save(os.path.join(app.config["EXCEL_UPLOADS"], filename))

        if ext == "csv":
            df_old = pd.read_csv(
                os.path.join(app.config["EXCEL_UPLOADS"], filename),
                dtype=str,
                keep_default_na=False,
            )
        elif ext in ["xlsx", "xls"]:
            df_old = pd.read_excel(
                os.path.join(app.config["EXCEL_UPLOADS"], filename),
                dtype=str,
                keep_default_na=False,
            )
        else:
            return render_template(
                "public/index.html", feedback="Format file salah", status="danger"
            )
        df_old = df_old.fillna("")

        old_col = df_old.columns
        col_change = {}
        for col in df_old.columns:
            if is_camel_case(col):
                col_change[col] = " ".join(camel_case_split(col))
                col_change[col] = " ".join(
                    remove_special_characters(col_change[col]).split()
                )
        df_old = df_old.rename(columns=col_change)
        df = df_old.copy()

        column_checked = []
        column_names = find_col(df.columns, "NPWP")
        for column_name in column_names:
            df[column_name] = df[column_name].apply(npwpFormat)
            column_checked.append(column_name)
        try:
            # Cleaning Column name

            df["Nama"] = df["Nama"].fillna("").apply(remove_special_characters)
            df["Nama"] = df["Nama"].apply(uppercase)
            df["Nama"] = df["Nama"].apply(no_double_space)
            df["Nama"] = df["Nama"].apply(max_char, max_char=40)
            column_checked.append("Nama")

            column_names = find_col(df.columns, "kelamin")
            for column_name in column_names:
                df[column_name] = df[column_name].apply(gender)
                column_checked.append(column_name)

            df["Kebangsaan"] = df["Kebangsaan"].apply(update_nationality)
            column_checked.append("Kebangsaan")

            df["Tempat Lahir"] = df["Tempat Lahir"].apply(max_char, max_char=29)
            df["Tempat Lahir"] = df["Tempat Lahir"].apply(uppercase)
            column_checked.append("Tempat Lahir")

            column_names = find_col(df.columns, "tanggal")
            for column_name in column_names:
                df[column_name] = df[column_name].fillna("").apply(to_datetime)
                column_checked.append(column_name)

            df["No Identitas"] = df["No Identitas"].apply(NIKconfirm)
            column_checked.append("No Identitas")

            df["Nama Ibu Kandung Wali"] = df["Nama Ibu Kandung Wali"].apply(
                remove_special_characters
            )
            df["Nama Ibu Kandung Wali"] = df["Nama Ibu Kandung Wali"].apply(uppercase)
            df["Nama Ibu Kandung Wali"] = df["Nama Ibu Kandung Wali"].apply(
                no_double_space
            )
            df["Nama Ibu Kandung Wali"] = df["Nama Ibu Kandung Wali"].apply(
                max_char, max_char=25
            )
            column_checked.append("Nama Ibu Kandung Wali")

            df["Status Kawin"] = df["Status Kawin"].apply(setStatusKawin)
            column_checked.append("Status Kawin")

            df["Agama"] = df["Agama"].fillna("").apply(agama)
            column_checked.append("Agama")

            df["Pendidikan"] = df["Pendidikan"].fillna("").apply(pendidikan)
            column_checked.append("Pendidikan")

            column_names = find_col(df.columns, "alamat")
            for column_name in column_names:
                df[column_name] = df[column_name].apply(uppercase)
                df[column_name] = df[column_name].apply(remove_special_characters)
                df[column_name] = df[column_name].apply(no_double_space)
                df[column_name] = df[column_name].apply(max_char, max_char=40)
                column_checked.append(column_name)

            df["RT"] = df["RT"].fillna("")
            df["RT"] = df["RT"].apply(onlyNumbersOnStr)
            df["RT"] = df["RT"].apply(format_r)
            column_checked.append("RT")
            df["RW"] = df["RW"].fillna("")
            df["RW"] = df["RW"].apply(onlyNumbersOnStr)
            df["RW"] = df["RW"].apply(format_r)
            column_checked.append("RW")

            column_names = find_col(df.columns, "kelurahan")
            for column_name in column_names:
                df[column_name] = df[column_name].fillna("").replace({"NULL": ""})
                df[column_name] = df[column_name].apply(uppercase)
                df[column_name] = df[column_name].apply(remove_special_characters)
                df[column_name] = df[column_name].apply(no_double_space)
                df[column_name] = df[column_name].apply(max_char, max_char=50)
                column_checked.append(column_name)

            column_names = find_col(df.columns, "kecamatan")
            for column_name in column_names:
                df[column_name] = df[column_name].fillna("").replace({"NULL": ""})
                df[column_name] = df[column_name].apply(uppercase)
                df[column_name] = df[column_name].apply(remove_special_characters)
                df[column_name] = df[column_name].apply(no_double_space)
                df[column_name] = df[column_name].apply(max_char, max_char=50)
                column_checked.append(column_name)

            column_names = find_col(df.columns, "kota")
            for column_name in column_names:
                df[column_name] = df[column_name].fillna("").replace({"NULL": ""})
                df[column_name] = df[column_name].apply(uppercase)
                df[column_name] = df[column_name].apply(remove_special_characters)
                df[column_name] = df[column_name].apply(no_double_space)
                df[column_name] = df[column_name].apply(max_char, max_char=29)
                column_checked.append(column_name)

            column_names = find_col(df.columns, "propinsi")
            for column_name in column_names:
                df[column_name] = df[column_name].fillna("").replace({"NULL": ""})
                df[column_name] = df[column_name].apply(uppercase)
                df[column_name] = df[column_name].apply(remove_special_characters)
                df[column_name] = df[column_name].apply(no_double_space)
                df[column_name] = df[column_name].apply(max_char, max_char=15)
                column_checked.append(column_name)

            column_names = find_col(df.columns, "Pos")
            for column_name in column_names:
                df[column_name] = df.apply(kodePosConfirm, axis=1)
                column_checked.append(column_name)

            # status rumah skipped

            column_names = find_col(df.columns, "telp")
            for column_name in column_names:
                df[column_name] = (
                    df[column_name]
                    .fillna("")
                    .apply(remove_special_characters)
                    .str.replace(" ", "")
                )
                df[column_name] = df[column_name].apply(cleanPhoneNumber)
                column_checked.append(column_name)

            # Pekerjaan / Bidang Usaha skipped

            # Kode profesi skipped

            df["Status Pekerjaan"] = df["Status Pekerjaan"].apply(
                lambda x: x if len(x) > 1 else "FALSE"
            )
            df["Status Pekerjaan"] = df["Status Pekerjaan"].apply(
                lambda x: x if x[:1] in ["1", "2", "3", "4"] else "FALSE"
            )
            column_checked.append("Status Pekerjaan")

            df["Nama Instansi"] = (
                df["Nama Instansi"].fillna("").apply(remove_special_characters)
            )
            df["Nama Instansi"] = df["Nama Instansi"].apply(uppercase)
            df["Nama Instansi"] = df["Nama Instansi"].apply(no_double_space)
            df["Nama Instansi"] = df["Nama Instansi"].apply(max_char, max_char=40)

            # df['Alamat Instansi'] = df['Alamat Instansi'].fillna("").apply(remove_special_characters)
            df["Alamat Instansi"] = df["Alamat Instansi"].apply(uppercase)
            df["Alamat Instansi"] = df["Alamat Instansi"].apply(no_double_space)
            df["Alamat Instansi"] = df["Alamat Instansi"].apply(max_char, max_char=40)

            # Kode pos sudah di clear di atas

            df["Suami Istri"] = df.apply(suami_istri, axis=1)
            df["Suami Istri"] = df["Suami Istri"].apply(uppercase)
            df["Suami Istri"] = df["Suami Istri"].apply(remove_special_characters)
            df["Suami Istri"] = df["Suami Istri"].apply(no_double_space)
            df["Suami Istri"] = df["Suami Istri"].apply(max_char, max_char=40)
            column_checked.append("Suami Istri")

            df["Nama Pihak Yang Dapat Dihubungi"] = df[
                "Nama Pihak Yang Dapat Dihubungi"
            ].apply(uppercase)
            df["Nama Pihak Yang Dapat Dihubungi"] = df[
                "Nama Pihak Yang Dapat Dihubungi"
            ].apply(remove_special_characters)
            df["Nama Pihak Yang Dapat Dihubungi"] = df[
                "Nama Pihak Yang Dapat Dihubungi"
            ].apply(no_double_space)
            df["Nama Pihak Yang Dapat Dihubungi"] = df[
                "Nama Pihak Yang Dapat Dihubungi"
            ].apply(max_char, max_char=40)
            column_checked.append("Nama Pihak Yang Dapat Dihubungi")

            # hubungan skipped

            # alamat sudah di clear di atas
            # kota sudah di clear di atas
            # propinsi sudah di clear di atas

            df["Masa Berlaku Identitas"] = "999123123"

            del column_names, column_name
            df["Kode Dati II CARGCD"] = df.apply(kota, args=[kode_dati], axis=1)
            column_checked.append("Kode Dati II CARGCD")

            df = df.apply(lambda x: x.str.upper())
            c1 = df.where(df.values == df_old.values).notna()

            # false_rows, false_columns = np.where(c1 == False)
            daftar_revisi = []
            for false_row, false_col in zip(*np.where(c1 == False)):
                daftar_revisi.append(
                    (
                        c1.columns[false_col],
                        c1.index[false_row],
                        df.iloc[false_row, false_col],
                        df_old.iloc[false_row, false_col],
                    )
                )

            total_true = c1.to_numpy().sum()
            total_false = c1.size - total_true
            os.makedirs(app.config["EXCEL_UPLOADS"], exist_ok=True)
            if total_false == 0:
                os.makedirs(app.config["EXCEL_UPLOADS"] + "/fix/", exist_ok=True)
                filename_to_save = fileNoExt + "-fix"
                to_xls(
                    df,
                    os.path.join(
                        app.config["EXCEL_UPLOADS"] + "/fix/", filename_to_save + ".xls"
                    ),
                )
            else:
                os.makedirs(app.config["EXCEL_UPLOADS"] + "/revisi/", exist_ok=True)
                filename_to_save = fileNoExt + "-full"
                to_xls(
                    df,
                    os.path.join(
                        app.config["EXCEL_UPLOADS"] + "/revisi/",
                        filename_to_save + ".xls",
                    ),
                )

                filename_not_valid = fileNoExt + "-not-valid-revisi"
                df_not_valid = df[
                    df[column_checked].apply(
                        lambda x: any([val == "" for val in x]), axis=1
                    )
                ]
                to_xls(
                    df_not_valid,
                    os.path.join(
                        app.config["EXCEL_UPLOADS"] + "/revisi/",
                        filename_not_valid + ".xls",
                    ),
                )

                filename_valid = fileNoExt + "-valid-revisi"
                df_valid = df[
                    df[column_checked].apply(
                        lambda x: all(val != "" for val in x), axis=1
                    )
                ]
                to_xls(
                    df_valid,
                    os.path.join(
                        app.config["EXCEL_UPLOADS"] + "/revisi/",
                        filename_valid + ".xls",
                    ),
                )

                empty_row_counts = {
                    col: len(df[df[col] == ""]) for col in column_checked
                }
                df.columns = old_col
                with open(
                    os.path.join(
                        app.config["EXCEL_UPLOADS"] + "/revisi/",
                        filename_to_save + ".json",
                    ),
                    "w+",
                ) as f:
                    json.dump(empty_row_counts, f, indent=4)

            # df.to_excel(os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.xlsx'), index=False)
            # to_xls(df,os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.xls'))
            # df.to_csv(os.path.join(app.config["EXCEL_UPLOADS"], filename_to_save+'.csv'), index=False)
            if not app.config["AUTHOR"]:
                if app.config["AUTHOR"] != "Dimas":
                    Activity.add_activity(
                        session["username"],
                        f'Username {session["username"]} mengunggah file {filename}',
                    )
            return render_template(
                "pages/result/index.html",
                feedback="",
                status="success",
                column=old_col,
                df_upload=df_old.values.tolist(),
                df_processed=df.values.tolist(),
                # filenameXlsx=filename_to_save+'.xlsx',
                filenameXls=filename_to_save + ".xls",
                # filenameCsv=filename_to_save+'.csv',
                # filenameoriginal=fileUpload.filename,
                filenameoriginal=filename,
                daftar_revisi=daftar_revisi,
                total_false=total_false,
                fileNoExt=fileNoExt,
            )
        except Exception as e:
            print(filename, e)
            if session["role"] == "admin":
                flash(f"Terjadi kesalahan, silahkan coba lagi. Error : {e}", "danger")
            else:
                flash("Terjadi kesalahan, silahkan coba lagi", "danger")
            return render_template(
                "pages/home/index.html",
            )


@excel.route("/daftar-excel/")
@excel.route("/daftar-excel/<status>")
def daftar_excel(status=None):
    paths = glob.glob(app.config["EXCEL_UPLOADS"] + "/*/*.xls")
    path_dict = {}
    if (status == "Semua") or (status == None) or (status == ""):
        for path in paths:
            if "fix" in path:
                no_ext = path.split(".")[-2].split("\\")[-1]
                path_dict[no_ext] = "fix"
            else:
                no_ext = path.split(".")[-2].split("\\")[-1]
                if no_ext[-5:] == "-full":
                    no_ext = no_ext[:-5]
                elif no_ext[-17:] == "-not-valid-revisi":
                    no_ext = no_ext[:-17]
                elif no_ext[-13:] == "-valid-revisi":
                    no_ext = no_ext[:-13]
                path_dict[no_ext] = "revisi"
    elif status == "revisi":
        for path in paths:
            if "revisi" in path:
                no_ext = path.split(".")[-2].split("\\")[-1]
                if no_ext[-5:] == "-full":
                    no_ext = no_ext[:-5]
                elif no_ext[-17:] == "-not-valid-revisi":
                    no_ext = no_ext[:-17]
                elif no_ext[-13:] == "-valid-revisi":
                    no_ext = no_ext[:-13]
                path_dict[no_ext] = "revisi"
    elif status == "fix":
        for path in paths:
            if "fix" in path:
                no_ext = path.split(".")[-2].split("\\")[-1]
                path_dict[no_ext] = "fix"
    if status:
        return render_template(
            "pages/daftar_file/table_daftar_excel.html",
            daftar_nama_file=list(path_dict.keys()),
            path_dict=path_dict,
            status=status,
        )
    return render_template(
        "pages/daftar_file/index.html",
        daftar_nama_file=list(path_dict.keys()),
        path_dict=path_dict,
        status=status,
    )


@excel.route("/daftar-excel/detail-kolom/<filename>")
def detail_kolom(filename):
    with open(
        os.path.join(
            app.config["EXCEL_UPLOADS"] + "/revisi/" + filename + "-full.json"
        ),
        "r",
    ) as f:
        empty_row_counts = json.load(f)
    return render_template(
        "pages/daftar_file/detail_kolom.html",
        empty_row_counts=empty_row_counts,
        data_key=list(empty_row_counts.keys()),
        filename=filename,
    )
