from difflib import SequenceMatcher
import re,json
import pandas as pd
import datetime


def is_valid_username(username):
    # Username hanya boleh berisi huruf (baik besar maupun kecil), angka, dan underscore
    # Panjang username minimal 3 karakter dan maksimal 20 karakter
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    return re.match(pattern, username) is not None



with open("./Kode Dati.json",'r') as f:
    kode_dati = pd.DataFrame(json.loads(f.read()))

kode_dati['Kode'] = kode_dati['Kode Dati II'].str.split(':').str[0]
wilayah = kode_dati['Kode Dati II'].str.split(':').str[1].str.strip().str.split('-')
kode_dati['Propinsi'] = wilayah.str[0].str.strip().str.upper()
kode_dati['Kota Kab'] = wilayah.str[1].str.strip().str.upper()

df_kode_pos = pd.read_excel('Data_Master_Wilayah.xlsx',dtype=str,na_filter=False)
df_kode_pos = df_kode_pos[df_kode_pos['Kode_pos'] != '']


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_col(columns, key):
    ls_found = []
    for col in columns:
        if key.lower() in col.lower():
            ls_found.append(col)
    return ls_found

def to_xls(df,filename):
    import xlwt 
    # Membuat objek workbook menggunakan xlwt
    workbook = xlwt.Workbook()

    # Membuat sheet di workbook
    sheet = workbook.add_sheet('Sheet1')
    # Menulis nama kolom ke sheet
    for col_idx, col_name in enumerate(df.columns):
        sheet.write(0, col_idx, col_name)
    # Menulis data DataFrame ke sheet
    for row_idx, row_data in enumerate(df.values):
        for col_idx, cell_data in enumerate(row_data):
            sheet.write(row_idx+1, col_idx, cell_data)

    # Menyimpan workbook ke file Excel .xls
    workbook.save(filename)

def kodePosConfirm(x):
    df_ = df_kode_pos[
        (df_kode_pos['Provinsi'].str.contains(x['Propinsi'])) 
    & (df_kode_pos['Kota'].str.contains(x['Kota'])) 
    & (df_kode_pos['Kecamatan'].str.contains(x['Kecamatan'])) 
    & (df_kode_pos['Kelurahan'].str.contains(x['Kelurahan']))
    ].reset_index(drop=True)
    if len(df_) == 0:
        return ''
    elif len(df_) == 1:
        return df_['Kode_pos'][0]
    else:
        return ''
    # if len(x) != 5:
    #     return ""
    # elif x[-3:] == '000':
    #     return ""
    # else:
    #     return x

def npwpFormat(x):
    x = onlyNumbersOnStr(x)
    if len(x) != 15:
        return 'HARUS 15 ANGKA'
    if x[-6:] == '000000':
        return '6 ANGKA TERAKHIR TIDAK BOLEH 000000'
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
            
    return ''

def suami_istri(row):
    if row['Status Kawin'] == 'K: KAWIN':
        return str(row['Suami Istri']).upper()
    elif row['Status Kawin'] in ['B: BELUM KAWIN','D: CERAI']:
        return 'NULL'
    else:
        return ''

def NIKconfirm(x):
    if len(x)!=16:
        return ""
    elif  x[-4:] == '0000':
        return f""
    else:
        return x

def noNumber(x):
    judgement = any(char.isdigit() for char in x)
    return x if not judgement else "FALSE"

def update_nationality(x):
    x = x.upper()
    if 'INDONESIA' in x:
        return 'I : INDONESIA'
    return str(x)


def agama(x):
    if x in ['4: ISLAM','1: HINDU','2: BUDHA','3: PROTESTAN','5: KATHOLIK','7: KONGHUCU']:
        return x
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
    if x in ['00: TANPA GELAR','01: DIPLOMA 1','02: DIPLOMA 2','03: DIPLOMA 3','04: S-1','05: S-2','06: S-3','99: LAINNYA']:
        return x
    if x.upper().split(' ')[0] in ['SMA','SMP','SMAN','SLTA','SLTP','SMK','STM','SMU','SEKOLAH']:
        PEND = '00: TANPA GELAR'
    elif x.upper() in 'D1':
        PEND = '01: DIPLOMA 1'
    elif x.upper() in 'D2':
        PEND = '02: DIPLOMA 2'
    elif x.upper() in ['D3', 'DIII']:
        PEND = '03: DIPLOMA 3'
    elif x.upper() in ['S1','STRATA 1']:
        PEND = '04: S-1'
    elif x.upper() in ['S2','STRATA 2']:
        PEND = '05: S-2'
    elif x.upper() in ['S3','STRATA 3']:
        PEND = '06: S-3'
    else:
        PEND = '99: LAINNYA'
    return PEND

def format_r(x):
    return f"'{x.zfill(3)}"

def setStatusKawin(x):
    if x.upper() in ['B: BELUM KAWIN', 'K: KAWIN','D: CERAI']:
        return x.upper()
    if 'BELUM' in x.upper():
        return 'B: BELUM KAWIN'
    if 'KAWIN' in x.upper():
        return 'K: KAWIN'
    if 'CERAI' in x.upper():
        return 'D: CERAI'
    return ''
    # return 'B: BELUM KAWIN' if x.lower()=='belum' else 'K: KAWIN' if x.lower()=='kawin' else 'D: CERAI' if x.lower()=='cerai' else 'FALSE'

def onlyNumbersOnStr(x):
    count_dot = x.count('.')
    if (count_dot == 1) and (x[-2]=='.'):
        return str(int(x))
    return re.sub(r'\D', '', x)

def uppercase_column(col):
    return col.fillna('').str.upper()

def lowercase_column(col):
    return col.fillna('').str.lower()

def cleanPhoneNumber(x):
    if x.startswith('0'):
        x = "62" + x[1:]
    elif x.startswith('8'):
        x = "628" + x[1:]
    elif x.startswith('62'):
        x = x
    else:
        x = ''
    return str(x)

def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def remove_special_characters(x):
    return re.sub('[^a-zA-Z0-9 \n]', ' ', x)

def gender(x):
    if x.upper() in ['L: LAKI-LAKI','P: PEREMPUAN']:
        return x
    x_splits = x.split(' ')
    for z in x_splits:
        if z.lower() in ['pria', 'p','laki','laki-laki','cowo','cowok']:
            return 'L: LAKI-LAKI'
        elif z.lower() in ['wanita', 'w','cewek','perempuan','cewe','cewek']:
            return 'P: PEREMPUAN'
    return ''

def to_datetime(x):
    try:
        return pd.to_datetime(x).strftime('%Y/%m/%d')
    except:
        return x
