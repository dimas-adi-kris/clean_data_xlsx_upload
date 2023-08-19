# Instalasi

Semua requirement yang ditulis di sini sudah diuji. Sangat mungkin terjadi jika terdapat perbedaan versi yang tidak terlalu signifikan tetapi proyek masih tetap dapat dijalankan. Namun sangat disarankan untuk sebisa mungkin mencocokkan versi yang digunakan. Jika menggunakan selain yang telah diuji dan terdapat error saat dijalankan, silahkan melapor

Sebelum melakukan instalasi, pastikan perangkat telah dipasang python. Untuk memeriksanya, buka command prompt/powershell/terminal kemudian jalankan `python --version`. Jika belum terinstall, silahkan download dan install melalui website resmi [python](https://python.org) atau menggunakan [anaconda](https://anaconda.org/) untuk melanjutkan proses instalasi

requirement :

| Package | Versi  |
|---------|--------|
| [Python](#python_head)  | 3.11   |
| [Flask](#flask_head)    | 1.1.1  |
| [Jinja2](#jinja2_head)  | 2.10.3 |
| [NumPy](#numpy_head)  | 1.24.3 |
| [Pandas](#pandas_head)  | 2.0.2 |
| [OpenPyXl](#openpyxl_head)  | 3.1.2 |
| [Xlrd](#xlrd_head)  | 2.0.1 |
| [Regex](#regex_head)  | 2023.6.3 |
| [markupsafe](#markupsafe_head)  | 2.0.1 |
| [itsdangerous](#itsdangerous_head)  | 2.0.1 |
| [werkzeug](#werkzeug_head)  | 2.0.3 |

install Flask, pandas, numpy, dan regex

# BUAT ENVIRONMENT PYTHON BARU
- pip

```
py -m pip install --user virtualenv
py -m venv flaskpy2
```


# AKTIFKAS ENVIRONMENT
## Untuk powershell
```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\flaskpy2\Scripts\activate.ps1
```
## Untuk command prompt
```bash
.\flaskpy2\Scripts\activate
```
## Untuk linux terminal
```bash
source /flaskpy2/bin/activate
```

# INSTAL LIBRARY YANG AKAN DIGUNAKAN

```BASH
pip install flask==1.1.1 jinja2==2.10.3 markupsafe==2.0.1 itsdangerous==2.0.1 werkzeug==2.0.3 
pip install pandas 
pip install numpy 
pip install regex 
pip install openpyxl
pip install xlrd
pip install xlwt

pip install ordereduuid

pip install --upgrade firebase-admin

```

<!-- - conda

```
conda install flask -y
conda install pandas -y
conda install numpy -y
conda install regex -y
pip install openpyxl
pip install xlrd
``` -->


# JALANKAN SERVER FLASK
Untuk menjalankan flask, jalankan
```
flask run
```

Untuk menghentikan program flask, tekan kombinasi tombol `Ctrl+C` pada terminal/cmd/powershell

# Deskripsi

## Penjelasan syntax Instalasi
Perintah `py -m pip install --user virtualenv` secara khusus menginstal package "virtualenv" secara lokal di dalam direktori pengguna, yang memungkinkan pengguna untuk membuat dan mengelola lingkungan virtual Python terisolasi yang dapat digunakan untuk memisahkan dependensi dan proyek Python secara independen. 

Perintah `py -m venv flaskpy2` digunakan untuk membuat lingkungan virtual Python dengan nama "flaskpy2" menggunakan modul venv yang disertakan dalam instalasi Python.

Dengan menjalankan perintah ini, sebuah lingkungan virtual dengan nama "flaskpy2" akan dibuat. Lingkungan virtual ini akan berisi salinan lokal dari interpreter Python, pustaka standar, dan pip yang terisolasi dari instalasi Python sistem global. Lingkungan virtual ini dapat digunakan untuk mengisolasi dependensi dan proyek Python spesifik dalam lingkungan yang terpisah, memungkinkan pengembangan dan pengujian yang lebih terkontrol dan mudah dikelola

- PowerShell

Perintah `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` digunakan untuk mengatur kebijakan eksekusi skrip PowerShell di level pengguna saat ini menjadi "RemoteSigned". Kebijakan ini memungkinkan eksekusi skrip PowerShell lokal dan memerlukan tanda tangan digital pada skrip yang diunduh dari sumber eksternal sebelum dapat dieksekusi.

Perintah `.\flaskpy2\Scripts\activate.ps1` digunakan untuk mengaktifkan lingkungan virtual "flaskpy2" yang sebelumnya dibuat. Ini menjalankan skrip "activate.ps1" yang ada di dalam direktori "flaskpy2\Scripts". Skrip tersebut mengatur variabel lingkungan dan jalur untuk mengarahkan pengguna ke lingkungan virtual yang aktif. Dengan menjalankan perintah ini, lingkungan virtual "flaskpy2" akan diaktifkan, dan semua perintah Python yang dieksekusi akan menggunakan interpreter dan dependensi yang terkait dengan lingkungan tersebut.

- Command Prompt

Pada command prompt, pengguna dapat langsung mengeksekusi `.\flaskpy2\Scripts\activate` untuk mengaktifkan lingkungan virtual seperti yang dilakukan powershell. command prompt tidak perlu mengatur `ExecutionPolicy` untuk mengaktifkan lingkungan virtual

- Linux Terminal

Perintah `source /flaskpy2/bin/activate` adalah perintah yang digunakan untuk mengaktifkan lingkungan virtual "flaskpy2" di sistem berbasis Unix atau Linux.

Dengan menjalankan perintah ini, skrip "activate" yang ada di dalam direktori "/flaskpy2/bin" akan dijalankan. Skrip tersebut akan mengatur variabel lingkungan dan jalur agar mengarahkan pengguna ke lingkungan virtual yang aktif. Setelah menjalankan perintah ini, lingkungan virtual "flaskpy2" akan diaktifkan, dan semua perintah Python yang dieksekusi akan menggunakan interpreter dan dependensi yang terkait dengan lingkungan tersebut. Perintah ini berguna ketika ingin beralih ke lingkungan virtual yang ada sebelumnya untuk menjalankan atau menguji proyek Flask yang terkait.


## Penjelasan Package yg digunakan

### <a name="python_head"></a> Python
Python adalah bahasa pemrograman tingkat tinggi yang serbaguna dan mudah dipelajari. Python dapat digunakan sebagai Pengembangan Perangkat Lunak, Automasi Tugas, Analisis Data dan Ilmu Data, Kecerdasan Buatan (Artificial Intelligence), Pengembangan Game, dan Web Development

Python populer di kalangan pengembang karena sintaksnya yang mudah dipelajari, dukungan komunitas yang besar, dan tersedianya banyak pustaka dan alat yang siap pakai. Python juga dapat diintegrasikan dengan bahasa lain, seperti C/C++, Java, dan lainnya, memungkinkan penggunaan Python dalam skenario yang beragam.

### <a name="flask_head"></a> Flask 
Flask adalah sebuah framework web yang ringan dan fleksibel untuk bahasa pemrograman Python. Kegunaan Flask adalah memudahkan pengembang dalam membangun aplikasi web dengan Python. Dengan Flask, Anda dapat membuat halaman web, mengelola rute URL, memproses formulir, berinteraksi dengan basis data, dan lainnya. Flask memberikan kerangka kerja yang minimalis namun kuat untuk membangun aplikasi web dengan cepat. Flask juga cocok untuk membangun RESTful API, mengembangkan mikroservis, dan skenario pengembangan yang fleksibel.

### <a name="jinja2_head"></a> Jinja2
Jinja2 adalah mesin template Python yang digunakan untuk memisahkan logika aplikasi dari tampilan. Kegunaannya adalah memungkinkan pengembang untuk membuat template yang terstruktur dan mudah dipelihara. Jinja2 menyediakan sintaks untuk mengatur variabel, kondisi, loop, dan blok pada tampilan. Ini membantu dalam pemisahan logika dan tampilan, meningkatkan keamanan dengan pembersihan karakter berbahaya, dan mendukung konsep pewarisan template. Jinja2 juga merupakan mesin template yang digunakan dalam framework Flask.

### <a name="numpy_head"></a> NumPy
NumPy adalah pustaka Python untuk komputasi numerik. Kegunaannya adalah menyediakan struktur data array multidimensi dan operasi matematika yang cepat. Dengan NumPy, Anda dapat melakukan manipulasi dan analisis data numerik secara efisien. NumPy juga digunakan dalam pengolahan gambar, pengolahan sinyal, serta menjadi dasar bagi banyak pustaka dan alat di ekosistem Python, seperti pandas.

### <a name="pandas_head"></a> Pandas
Pandas adalah pustaka Python untuk manipulasi dan analisis data. Kegunaannya adalah menyediakan struktur data seperti Series dan DataFrame untuk menyimpan data dalam format tabular. Pandas memungkinkan manipulasi data, membersihkan data, membaca dan menulis data dari berbagai format, serta melakukan analisis statistik dan time series. Pustaka ini sangat berguna dalam pengolahan data dan analisis data karena ekspresi yang sederhana dan intuitif.

### <a name="openpyxl_head"></a> OpenPyXl
Openpyxl adalah pustaka Python yang digunakan untuk membaca, menulis, dan memanipulasi file Excel (.xlsx). Kegunaannya adalah memungkinkan pengguna untuk mengakses data yang ada dalam file Excel menggunakan kode Python. Openpyxl diperlukan oleh Pandas karena Pandas menggunakan openpyxl sebagai salah satu metode untuk membaca dan menulis data dari file Excel. Dengan menggunakan openpyxl sebagai backend, Pandas dapat mengimpor data dari file Excel dan mengubahnya menjadi struktur data Pandas, seperti DataFrame. Ini memungkinkan pengguna Pandas untuk melakukan manipulasi data, analisis, dan visualisasi yang lebih lanjut menggunakan data yang berasal dari file Excel. Dengan demikian, openpyxl menjadi penting dalam ekosistem Pandas karena menyediakan konektivitas antara Pandas dan file Excel.

### <a name="xlrd_head"></a> Xlrd
Xlrd adalah pustaka Python yang digunakan untuk membaca data dari file Excel (.xls). Kegunaannya adalah memungkinkan pengguna untuk mengambil data dari file Excel, seperti nilai sel, format sel, dan informasi lainnya. Xlrd diperlukan oleh Pandas karena Pandas menggunakan xlrd sebagai salah satu metode untuk membaca data dari file Excel lama (.xls). Dengan menggunakan xlrd, Pandas dapat mengimpor data dari file Excel dan mengubahnya menjadi struktur data Pandas, seperti DataFrame. Ini memungkinkan pengguna Pandas untuk melakukan manipulasi data, analisis, dan visualisasi yang lebih lanjut menggunakan data yang berasal dari file Excel lama. Dengan demikian, xlrd menjadi penting dalam ekosistem Pandas karena memberikan konektivitas antara Pandas dan file Excel lama (.xls).

### <a name="regex_head"></a> Regex
Regex (Regular Expression) adalah sebuah notasi atau pola yang digunakan untuk mencocokkan dan memanipulasi teks berdasarkan pola tertentu. Regex digunakan untuk pencocokan pola string yang fleksibel dan kompleks, memungkinkan pengguna untuk melakukan pencarian, pemfilteran, penggantian, dan validasi string berdasarkan pola yang didefinisikan. Regex digunakan dalam berbagai bahasa pemrograman dan aplikasi untuk melakukan operasi teks yang kompleks, seperti validasi format email, pencarian kata kunci dalam teks, ekstraksi data dari string, dan banyak lagi. Regex merupakan alat yang sangat kuat dalam pemrosesan teks dan memungkinkan pengguna untuk melakukan manipulasi string dengan cara yang lebih efisien dan efektif.

### <a name="markupsafe_head"></a> MarkupSafe
MarkupSafe adalah pustaka Python yang digunakan untuk menjamin keamanan dalam memanipulasi dan menghasilkan kode HTML, XML, dan teks lainnya. Kegunaannya adalah melindungi aplikasi dari serangan injeksi skrip lintas situs (XSS) dengan memberikan escape dan enkoding yang tepat pada data yang akan ditampilkan dalam format markup. Dengan menggunakan MarkupSafe, pengembang dapat dengan aman memasukkan data pengguna ke dalam tampilan aplikasi tanpa khawatir terhadap potensi serangan keamanan. Pustaka ini berperan penting dalam menjaga keamanan aplikasi web yang menggunakan markup untuk menampilkan konten kepada pengguna

### <a name="itsdangerous_head"></a> MarkupSafe
Itsdangerous adalah pustaka Python yang digunakan untuk menghasilkan dan memverifikasi tanda tangan digital yang aman. Kegunaannya adalah untuk mengamankan data sensitif seperti token otentikasi, cookie, atau URL agar tidak dapat dipalsukan atau dimanipulasi oleh pihak yang tidak berwenang. Dengan menggunakan itsdangerous, pengembang dapat memastikan bahwa data yang dikirimkan antara aplikasi dan pengguna tidak akan rusak atau diganti tanpa sepengetahuan atau izin yang sah. Pustaka ini sering digunakan dalam pengembangan aplikasi web untuk mengimplementasikan fitur keamanan seperti autentikasi, otorisasi, pengaturan sesi, dan tanda tangan data yang sensitif.


### <a name="werkzeug_head"></a> werkzeug
Werkzeug adalah pustaka Python yang digunakan sebagai utilitas web untuk membangun aplikasi web yang kuat dan fleksibel. Kegunaannya adalah menyediakan beragam alat dan fungsi yang dibutuhkan dalam pengembangan aplikasi web, seperti routing URL, penanganan permintaan dan respons HTTP, pengelolaan cookie, serta utilitas lainnya yang mendukung pembangunan web dengan Python. Werkzeug juga menyediakan server pengembangan bawaan yang memungkinkan pengembang untuk dengan mudah menjalankan dan menguji aplikasi web secara lokal. Pustaka ini digunakan oleh framework Flask, sehingga merupakan komponen penting dalam pengembangan aplikasi web menggunakan Flask. Werkzeug memudahkan pengembang untuk membangun aplikasi web yang efisien, terstruktur, dan aman dengan Python.








# v 1.0
- Rilis





# jpy
```
py -m venv jupyter
.\jupyter\Scripts\activate
pip install notebook werkzeug ordereduuid firebase-admin
jupyter notebook

```