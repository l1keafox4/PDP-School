username = input('Username kiriting >>>>')
password = input('Password kiriting >>>>')
print('Rahmat malumotlar berganizngiz uchun !')

username_confirm = input('Royxatdan otish uchun username kiriting >>>')
password_confirm = input('Royxatdan otish uchun password kiriting >>>')

if username == username_confirm and password == password_confirm:
    print('Siz royxatdan otdingiz')
    
elif username != username_confirm or password != password_confirm:
    print(f"Siz yozgan username:{username_confirm} va password:{password_confirm} mana shular xato ekan")