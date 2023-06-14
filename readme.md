# Instalasi

Semua requirement yang ditulis di sini sudah diuji. Jika menggunakan selain yang telah diuji dan terdapat error saat dijalankan, silahkan hubungi


requirement :

| Package | Versi  |
|---------|--------|
| Python  | 3.11   |
| Flask   | 1.1.1  |
| jinja2  | 2.10.3 |
| markupsafe  | 2.0.1 |
| itsdangerous  | 2.0.1 |
| werkzeug  | 2.0.3 |

install Flask, pandas, numpy, dan regex

- pip

```
py -m pip install --user virtualenv
py -m venv flaskpy2
.\flaskpy2\Scripts\activate
pip install flask==1.1.1 jinja2==2.10.3 markupsafe==2.0.1 itsdangerous==2.0.1 werkzeug==2.0.3 
pip install pandas 
pip install numpy 
pip install regex 
pip install openpyxl
pip install xlrd
```

- conda

```
conda install flask -y
conda install pandas -y
conda install numpy -y
conda install regex -y
pip install openpyxl
pip install xlrd
```


# Jalankan
Untuk menjalankan flask, jalankan
```
flask run
```

# v 1.0
- Rilis