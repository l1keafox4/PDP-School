login = input('Login kiriting >>>>')
a = 'admin'
ha = 'ha'

if login == a:
    print("Xush kelibsiz,Admin.")
    p = input("Foydalanuvchilarni ro'yxatini ko'rasizmi?")
    print('Xech kim yoq')
  
elif login != a:
    print(f"Xush kelibsiz,{login}")
    print("Iltimoz 2 ta son kiriting⇊⇊")
    son1=input("1-son>>>")
    son2=input("2-son>>>")

if son1 == son2:
    print('Sonlar teng')
    manbat1=int(input("Endi istalgan son kiriting>>>"))
elif son1 != son2:
    print('Sonlar teng emas')
    manbat1=int(input("Endi istalgan son kiriting>>>"))
if manbat1 > 0:
    print('Musbat son')
    ildiz1 = manbat1 ** 0.5
    print(f"{manbat1} soningizni ildizi>>> {ildiz1}")

if manbat1<0:
    print('Manfiy son')
    manbat2=int(input('Endi musbat son kiriting>>>'))

if manbat2 < 0:
    print('LOX')

if  manbat2>0:
    print('Musbat son')
    ildiz2 = manbat2 ** (0.5)
    print(f"{manbat2} soningizni ildizi>>> {ildiz2}")

