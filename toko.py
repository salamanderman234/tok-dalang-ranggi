# from distutils import command2
from cgitb import reset
from unittest.mock import AsyncMagicMixin
import discord
from discord.ext import commands
import re
import database


class Toko(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("**Selamat datang di sistem toko Kampoeng Durian Runtuh !**\nketik **/help** untuk melihat command yang dapat dijalankan")
            break
    
    @commands.command()
    async def information(self,ctx):
        text = "== **Selamat Datang di Bot Toko Kampoeng Durian Runtuh** ==\n\n**Perintah Untuk Toko :**\n\
**/register** <nama toko> *(bungkus dalam petik jika ada spasi) = mendaftarkan akun sebagai toko baru\n\
**/reset_token** = membuat token baru\n\
**/add_product** <nama product> <harga> <stok> <deskripsi> <token akses> *(bungkus dalam petik jika ada spasi) = mendaftarkan product baru\n \
**/my_products** <token akses> = melihat seluruh product yang dimiliki\n \
**/my_toko_orders** <token akses> = melihat seluruh pesanan yang dimiliki oleh toko\n \
**/verify_order** <no pesanan> <token akses> = mengubah status pesanan menjadi berhasil\n \
**/cancel_order** <no pesanan> <token akses> = mengubah status pesanan menjadi cancel\n\n \
**Perintah Untuk Pembeli :**\n\
**/toko** = melihat seluruh toko\n \
**/toko_product** <id toko> = melihat seluruh product yang dimiliki oleh sebuah toko\n \
**/order** <id product> <kuantitas> <alamat pengiriman> = menaruh pesanan baru\n\n\
note :\nToken akses diperlukan sebagai identitas toko dan diperlukan untuk menjalankan seluruh perintah yang berkaitan dengan toko. Token hanya dapat dibuat kembali oleh akun yang digunakan untuk mendaftar sebagai toko."
        await ctx.send(text)

    @commands.command()
    async def register(self,ctx,*args):
        try:
            if(len(args)>=1):
                name = " ".join(args)
                user_id = ctx.author.id
                result = await database.register_toko(name,user_id)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate ): Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")
        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")

    @commands.command()
    async def reset_token(self,ctx):
        try:
            user_id = ctx.author.id
            result = await database.reset_token(user_id)
            await ctx.send(result)
        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    @commands.command()
    async def add_product(self,ctx,*args):
        try:
            if(len(args)==5):

                name = args[0]
                price = args[1]
                stock = args[2]
                description = args[3]
                access_token = args[4]

                result = await database.tambah_product(name,price,stock,description,access_token)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    @commands.command()
    async def my_products(self,ctx,*args):
        try:
            if(len(args)==1):
                access_token = args[0]
                result = await database.my_products(access_token)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    @commands.command()
    async def my_toko_orders(self,ctx,*args):
        try:
            if(len(args)==1):
                access_token = args[0]
                result = await database.seluruh_pesanan_toko(access_token)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    @commands.command()
    async def toko(self,ctx):
        try:
            result = await database.seluruh_toko()
            await ctx.send(result)

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    
    @commands.command()
    async def toko_product(self,ctx,*args):
        try:
            if(len(args)==1):
                id_toko = args[0]
                result = await database.seluruh_produk_toko(id_toko)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")


    @commands.command()
    async def order(self,ctx,*args):
        try:
            if(len(args)==3):
                user = ctx.author.id
                id_product = args[0]
                qty = args[1]
                alamat = args[2]

                result = await database.place_order(user,id_product,qty,alamat)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")

    @commands.command()
    async def verify_order(self,ctx,*args):
        try:
            if(len(args)==2):
                no_order = args[0]
                access_token = args[1]
                status = "success"
                result = await database.update_pesanan(access_token,no_order,status)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")
    
    @commands.command()
    async def cancel_order(self,ctx,*args):
        try:
            if(len(args)==2):
                no_order = args[0]
                access_token = args[1]
                status = "cancelled"
                result = await database.update_pesanan(access_token,no_order,status)
                await ctx.send(result)
            else:
                await ctx.send("==** Pesan **==\n(Tok Dalang Kate) : Argumen tidak sesuai ! **/info** untuk menampilkan detail perintah")

        except Exception as e:
            print(e)
            await ctx.send("==** Error **==\n(Kak Ros Kate) : Terjadi kesalahan !")

def setup(client):
    client.add_cog(Toko(client))
