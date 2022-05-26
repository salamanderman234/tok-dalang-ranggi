import mysql.connector
from dotenv import load_dotenv
import os
import string
import random
import datetime

load_dotenv()

db_host = str(os.environ.get("MYSQL_HOST"))
db_user = str(os.environ.get("MYSQL_USER"))
db_passwd = str(os.environ.get("MYSQL_PASSWD"))
db_name = str(os.environ.get("MYSQL_DATABASE"))


def token_generator():
    date = datetime.datetime.now()
    date_string = f"{date.month}{date.day}"
    rand_string = ''.join(random.choice(string.ascii_letters) for i in range(6))

    return f"TK{date_string}{rand_string}"

async def register_toko(nama,pemilik):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = "SELECT id FROM tb_toko WHERE pemilik={}".format(pemilik)
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==0):
            access_token = token_generator()

            query = "INSERT INTO tb_toko(nama_toko,pemilik,token_akses) VALUES (%s,%s,%s)"
            cursor.execute(query,(nama,pemilik,access_token))
            db.commit()

            return f"==** Pesan **==\n(Tok Dalang Kate) : Berhasil mendaftarkan toko ! token akses anda : ||{access_token}|| (jangan sampai tersebar)"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Akun ini sudah memiliki toko yang sudah terdaftar !"
    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"

async def reset_token(pemilik):
    try :
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = "SELECT token_akses FROM tb_toko WHERE pemilik={}".format(pemilik)
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==1):

            access_token = token_generator()
            query = "UPDATE tb_toko SET token_akses=%s WHERE pemilik=%s"
            cursor.execute(query,(access_token,pemilik))
            db.commit()

            return f"==** Pesan **==\n(Tok Dalang Kate) : Token akses berhasil diedit ! token anda yang baru : ||{access_token}|| (jangan sampai tersebar)"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Akun ini tidak terdaftar sebagai toko !"
    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Rose Kate) : Kesalahan internal server"


async def tambah_product(nama,price,stock,deskripsi,access_token):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f'SELECT id FROM tb_toko WHERE token_akses="{access_token}"'
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==1):
            query = "INSERT INTO tb_product(nama_product,price,stock,id_toko,deskripsi) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(query,(nama,price,stock,hasil[0][0],deskripsi))
            db.commit()

            return f"==** Pesan **==\n(Tok Dalang Kate) : Product berhasil ditambahkan ! **/my_product** untuk melihat seluruh product yang sudah anda daftarkan"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Token yang anda masukan salah !"

    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"

async def my_products(access_token):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f'SELECT id FROM tb_toko WHERE token_akses="{access_token}"'
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==1):
            query = "SELECT id,nama_product,price,stock,deskripsi FROM tb_product WHERE id_toko={}".format(hasil[0][0])
            cursor.execute(query)
            hasil = tuple(cursor.fetchall())
            
            if(len(hasil)>0):
                array_hasil = "\n".join([" !! ".join([str(j) for j in i]) for i in hasil])
            else:
                array_hasil = "Tidak ada product"
            return f"==** Product Saya **==\n\n**id** !! **Nama Product** !! **Harga** !! **Stock** !! **Deskripsi Produk**\n{array_hasil}"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Token yang anda masukan salah !"

    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"

async def seluruh_pesanan_toko(access_token):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f'SELECT id FROM tb_toko WHERE token_akses="{access_token}"'
        cursor.execute(query,(access_token))
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==1):
            query = f"SELECT no_pesanan, id_product, user,qty,alamat_penerima, status FROM tb_pesanan WHERE id_toko={hasil[0][0]}"
            cursor.execute(query,(hasil[0][0]))
            hasil = tuple(cursor.fetchall())

            if(len(hasil)>0):
                array_hasil = "\n\n".join([" ".join(["( "+str(j)+" )" for j in i]) for i in hasil])
            else:
                array_hasil = "Tidak ada Pesanan"

            return f"==** Pesanan Toko Saya **==\n\n*format : (**no pesanan**)(**id product**)(**user**)(**qty**)(**alamat penerima**)(**status**)\n\n{array_hasil}"
        else:
            return "Token yang anda masukan salah !"

    except Exception as e:
        print(e)
        return "Kesalahan internal server"

async def update_pesanan(access_token, no_pesanan,status):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f'SELECT id FROM tb_toko WHERE token_akses="{access_token}"'
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)==1):
            query = f'SELECT id_product,qty FROM tb_pesanan WHERE no_pesanan="{no_pesanan}"'
            cursor.execute(query)
            pesanan = tuple(cursor.fetchall())
            if(len(pesanan)==1):
                query = "UPDATE tb_pesanan SET status=%s WHERE id_toko=%s AND no_pesanan=%s"
                cursor.execute(query,(status,hasil[0][0],no_pesanan))
                db.commit()

                if(status == "success"):
                    query = f'SELECT stock FROM tb_product WHERE id={pesanan[0][0]}'
                    cursor.execute(query)
                    stock = tuple(cursor.fetchall())

                    query = "UPDATE tb_product SET stock=%s WHERE id=%s"
                    cursor.execute(query,(stock[0][0]-pesanan[0][1],pesanan[0][0]))
                    db.commit()

                return f"==** Pesan **==\n(Tok Dalang Kate) : Berhasil update transaksi {no_pesanan} ke status {status}"
            else:
                return f"==** Pesan **==\n(Tok Dalang Kate) : Pesanan tidak ditemukan"
                
        else:
            return f"==** Pesan **==\n(Tok Dalang Kate) : Token yang anda masukan salah !"

    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"




#  untuk user

async def seluruh_toko():
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = "SELECT id,nama_toko FROM tb_toko"
        cursor.execute(query)
        hasil = tuple(cursor.fetchall())

        if(len(hasil)>0):
            array_hasil = "\n".join([" ".join(["( "+str(j)+" )" for j in i]) for i in hasil])
        else:
            array_hasil =  "Belum ada toko yang terdaftar"
        return f"==** Seluruh Toko **==\n\n*format : (**id**)(**nama toko**)\n\n{array_hasil}"
        
    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"


async def seluruh_produk_toko(id_toko):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f"SELECT nama_toko FROM tb_toko WHERE id={id_toko}"
        cursor.execute(query)
        toko = tuple(cursor.fetchall())

        if(len(toko)==1):
            query = f"SELECT id,nama_product,price,stock,deskripsi FROM tb_product WHERE id_toko={id_toko}"
            cursor.execute(query)
            hasil = tuple(cursor.fetchall())

            if(len(hasil)>0):
                array_hasil = "\n".join([" ".join(["( "+str(j)+" )" for j in i]) for i in hasil])
            else:
                array_hasil =  "Belum ada product yang terdaftar pada toko ini"
            return f"==** Seluruh Product Toko ({toko[0][0]})**==\n\n*format : (**id product**)(**nama product**)(**harga**)(**stok**)(**deskripsi**)\n\n{array_hasil}"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Toko tidak ditemukan"
        
    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"

async def place_order(user,id_product,qty,alamat):
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_passwd,
            database=db_name
        )
        cursor = db.cursor()

        query = f"SELECT id_toko FROM tb_product WHERE id={id_product}"
        cursor.execute(query)
        toko = tuple(cursor.fetchall())

        if(len(toko)==1):

            query = f"SELECT stock FROM tb_product WHERE id={id_product}"
            cursor.execute(query)
            stock = tuple(cursor.fetchall())

            if(int(qty) <= stock[0][0]):
                date = datetime.datetime.now()
                date_string = f"{date.year}{date.month}"
                rand_string = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
                no_pesanan = f"TR{date_string}{rand_string}"

                query ="INSERT INTO tb_pesanan(no_pesanan,id_product,user,status,id_toko,qty,alamat_penerima) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                values = (no_pesanan,id_product,user,"pending",toko[0][0],qty,alamat)
                cursor.execute(query,values)
                db.commit()

                return f"==** Pesan **==\nTok Dalang Kate : Berhasil menaruh pesanan ! no pesanan anda adalah {no_pesanan}"
            else:
                return f"==** Pesan **==\n(Tok Dalang Kate) : Qty melebihi stock (anda hanya dapat memesan <= {stock[0][0]} untuk barang ini)"
        else:
            return "==** Pesan **==\n(Tok Dalang Kate) : Product Tidak Ditemukan"
        
    except Exception as e:
        print(e)
        return "==** Pesan **==\n(Kak Ros Kate) : Kesalahan internal server"    
