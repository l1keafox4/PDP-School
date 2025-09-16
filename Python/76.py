import sqlite3

con = sqlite3.connect("Tgbot1.db")

cur = con.cursor()
    
# cur.execute("""CREATE TABLE IF NOT EXISTS product_prices (
#     product_name TEXT,
#     price INTEGER,
#     link_p TEXT
#     )""")

# cur.executemany("""INSERT INTO product_prices (product_name, price, link_p)
#                     VALUES (?, ?, ?)""",
#                     [
#                         ('Anor', 18000, 'https://gardencells.com/files/original/products/68.jpg'),
#                         ('Shaptoli', 15000, 'https://agri-gator.com.ua/wp-content/uploads/2021/10/nektarin.jpg'),
#                         ('Olma', 15000, 'https://srcyrl.bestplanthormones.com/Content/upload/2019264467/201906051807366069299.jpg'),
#                         ('Nok', 15000, 'https://zira.uz/wp-content/uploads/2018/09/int-fakti-grusha-2.jpg'),
#                         ('Muzqaymoq', 65000, 'https://uzreport.news/fotobank/image/3e23bbac36894a1a4627d7464108240e.jpeg'),
#                         ('Qurt', 82000, 'https://shop.chuztrade.uz/wp-content/uploads/2018/12/9565f4e6d2a4207358f54.jpg'),
#                         ('Qaymoq', 10000, 'https://yukber.uz/image/cache/catalog/smetana-23-700x700.jpg'),
#                         ('Sut', 11000, 'https://yuz.uz/imageproxy/1200x/https://yuz.uz/file/news/918e89a4acbb413819949216503353ab.jpg'),
#                         ('Mol go`shti', 90000, 'https://zamin.uz/uploads/posts/2017-06/1497253009_593d4f6cbe33c.jpg'),
#                         ('Sabzi', 11000, 'https://storage.kun.uz/source/7/SBpc8GysM0sg0bGCTLm4tBn760-w5l6w.jpg'),
#                         ('Bodring', 11000, 'https://www.spot.uz/media/img/2023/11/TfxzIc17010644618077_l.jpg'),
#                         ('Pomidor', 12000, 'https://stat.uz/images/aaacfisj9wtznmregenojdxxt8d2zlc1vp4phnpzdacxirhjtt4kvfbdaiwcno-_p79984.jpg'),
#                         ('Kartoshka', 7000, 'https://www.belta.by/images/storage/news/with_archive/2023/000029_1686923312_572263_big.jpg'),
#                         ('Tovuq go`shti', 80000, 'https://dostavo4ka.uz/upload-file/2021/05/05/2432/c957b80b-43ba-443b-9aba-8b2c5b946541.jpg'),
#                         ('Qo`y go`shti', 70000, 'https://chakchak.uz/uploads/images/tips/7c5dabc875cdcda3.jpg'),
#                         ('Qiyma go`shti', 77000, 'https://dostavo4ka.uz/upload-file/2021/05/05/3386/750x750-0a3e03ed-23e5-4279-8a7b-318421786aeb.jpg'),
#                         ('Marmelad', 75000, 'https://www.zefir.by/upload/iblock/b03/b030f280c5e885afc7725bb2b3da357b.png'),
#                         ('Pechenye', 68000, 'https://www.vkusnyblog.com/wp-content/uploads/2015/02/pechenye-s-shokoladom.jpg'),
#                         ('Cheers', 9000, 'https://dostavo4ka.uz/upload-file/2021/05/05/2608/5e828945-1e92-49b0-8458-b174bd65a162.jpg'),
#                         ('Snickers', 7000, 'https://aquamarket.ua/25109-large_default/snickers-upakovka-40-sht-po-50-g-shokoladnye-batonchiki-snikers.jpg'),
#                         ('Non', 5000, 'https://www.shutterstock.com/image-photo/tandir-non-lepeshka-tarditional-uzbek-260nw-1425851096.jpg')
#                     ])
cur.execute("SELECT link_p FROM product_prices WHERE product_name = ?", ('Anor',))
data = cur.fetchall()
data = list(data)
print(data)