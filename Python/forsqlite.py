import sqlite3

product_prices = {
    'Anor': {'price': 18000, 'link_p': "https://gardencells.com/files/original/products/68.jpg", "how_much": 100},
    'Shaptoli': {'price': 15000, 'link_p': "https://agri-gator.com.ua/wp-content/uploads/2021/10/nektarin.jpg", "how_much": 100},
    'Olma': {'price': 15000, 'link_p': "https://srcyrl.bestplanthormones.com/Content/upload/2019264467/201906051807366069299.jpg", "how_much": 100},
    'Nok': {'price': 15000, 'link_p': "https://zira.uz/wp-content/uploads/2018/09/int-fakti-grusha-2.jpg", "how_much": 100},
    'Muzqaymoq': {'price': 65000, 'link_p': "https://uzreport.news/fotobank/image/3e23bbac36894a1a4627d7464108240e.jpeg", "how_much": 100},
    'Qurt': {'price': 82000, 'link_p': "https://shop.chuztrade.uz/wp-content/uploads/2018/12/9565f4e6d2a4207358f54.jpg", "how_much": 100},
    'Qaymoq': {'price': 10000, 'link_p': "https://yukber.uz/image/cache/catalog/smetana-23-700x700.jpg", "how_much": 100},
    'Sut': {'price': 11000, 'link_p': "https://yuz.uz/imageproxy/1200x/https://yuz.uz/file/news/918e89a4acbb413819949216503353ab.jpg", "how_much": 100},
    'Mol go`shti': {'price': 90000, 'link_p': "https://zamin.uz/uploads/posts/2017-06/1497253009_593d4f6cbe33c.jpg", "how_much": 100},
    "Sabzi": {'price': 11000, 'link_p': "https://storage.kun.uz/source/7/SBpc8GysM0sg0bGCTLm4tBn760-w5l6w.jpg", "how_much": 100},
    "Bodring": {'price': 11000, 'link_p': "https://www.spot.uz/media/img/2023/11/TfxzIc17010644618077_l.jpg", "how_much": 100},
    "Pomidor": {'price': 12000, 'link_p': "https://stat.uz/images/aaacfisj9wtznmregenojdxxt8d2zlc1vp4phnpzdacxirhjtt4kvfbdaiwcno-_p79984.jpg", "how_much": 100},
    "Kartoshka": {'price': 7000, 'link_p': "https://www.belta.by/images/storage/news/with_archive/2023/000029_1686923312_572263_big.jpg", "how_much": 100},
    'Tovuq go`shti': {'price': 80000, 'link_p': "https://dostavo4ka.uz/upload-file/2021/05/05/2432/c957b80b-43ba-443b-9aba-8b2c5b946541.jpg", "how_much": 100},
    'Qo`y go`shti': {'price': 70000, 'link_p': "https://chakchak.uz/uploads/images/tips/7c5dabc875cdcda3.jpg", "how_much": 100},
    'Qiyma go`shti': {'price': 77000, 'link_p': "https://dostavo4ka.uz/upload-file/2021/05/05/3386/750x750-0a3e03ed-23e5-4279-8a7b-318421786aeb.jpg", "how_much": 100},
    'Marmelad': {'price': 75000, 'link_p': "https://www.zefir.by/upload/iblock/b03/b030f280c5e885afc7725bb2b3da357b.png", "how_much": 100},
    'Pechenye': {'price': 68000, 'link_p': "https://www.vkusnyblog.com/wp-content/uploads/2015/02/pechenye-s-shokoladom.jpg", "how_much": 100},
    'Cheers': {'price': 9000, 'link_p': "https://dostavo4ka.uz/upload-file/2021/05/05/2608/5e828945-1e92-49b0-8458-b174bd65a162.jpg", "how_much": 100},
    'Snickers': {'price': 7000, 'link_p': "https://aquamarket.ua/25109-large_default/snickers-upakovka-40-sht-po-50-g-shokoladnye-batonchiki-snikers.jpg", "how_much": 100},
    'Non': {'price': 5000, 'link_p': "https://www.shutterstock.com/image-photo/tandir-non-lepeshka-tarditional-uzbek-260nw-1425851096.jpg", "how_much": 100}
}

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the table
cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

# for product, details in product_prices.items():
#     product_name = product
#     price = details['price']
#     link_p = details['link_p']
#     peaces = details['how_much']
#     cursor.execute("INSERT INTO product_prices (product_name, price, link_p, peaces) VALUES (?, ?, ?, ?)", (product_name, price, link_p, peaces))

# # Commit changes and close the connection
conn.commit()
conn.close()