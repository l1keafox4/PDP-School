b = None
username = input('Username kiriting >>>>')
password = input('Password kiriting >>>>')
print('Rahmat malumotlar berganizngiz uchun !')

username_confirm = input('Royxatdan otish uchun username kiriting >>>')
password_confirm = input('Royxatdan otish uchun password kiriting >>>')

if username == username_confirm and password == password_confirm:

    print('Siz royxatdan otdingiz')
    print("""Bizning dokonimizga hush kelibsiz
    Bizda bor tavarlar
    1) Coca cola = 10.000
    2) Non 4.000
    3) Lays 16.000
    4) Qurt 20.000 
    5) Saqich 1.000
    6) Rolton 3.000
    7) Suv 2.000
    Siz qaysi birini olmoqchi bolsangiz osha raqamni yozing""")
    balans = int(input('Sizda bor summani kiriting !'))
    print(balans)
    number = input(f'Siz qaysi tovarni tanladingiz. Sizda {balans} som pul bor>>>')

    if number == '1':
        coca = balans - 10000 
        print(f"Siz Coca Colani sotvoldingiz va sizda {coca} pul qoldi")
        # b = input(f"Yana nimadur hoxlaysizmi? Yoq bolsa B yozing>>>")
    # elif b == "B":
    #     print("Yana kelib turing")
    # elif b == '2':
    #     non = coca - 4000
    #     print(f"""Siz Non sotvoldingiz va sizda {non} pul qoldi""")
    if number == '2' and balans >= 4000:
        non = balans - 4000 
        print(f"Siz Non sotvoldingiz va sizda {non} pul qoldi")
    elif number == '3' and balans >= 16000:
        lays = balans - 16000
        print(f"Siz Lays sotvoldingiz va sizda {lays} pul qoldi")
    elif number == '4' and balans >= 20000:
        qurt = balans - 20000
        print(f"""Siz Qurt sotvoldingiz va sizda {qurt} pul qoldi""")
    elif number == '5' and balans >= 1000:
        saqich = balans - 1000
        print(f"Siz Qurt sotvoldingiz va sizda {saqich} pul qoldi")
    elif number == '6' and balans >= 3000:
        rolton = balans - 3000
        print(f"Siz Qurt sotvoldingiz va sizda {rolton} pul qoldi")
    elif number == '7' and balans >= 2000:
        suv = balans - 2000
        print(f"Siz Suv sotvoldingiz va sizda {suv} pul qoldi")
    
elif username != username_confirm or password != password_confirm:
    print(f"Siz yozgan username:{username_confirm} va password:{password_confirm} mana shular xato ekan")
else:
    print('Poxodu sizda puliz kam')
