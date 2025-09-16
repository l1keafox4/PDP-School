# def sum(*args):
#     my_sum = 0
#     for i in args:
#         my_sum+=i
#     print(my_sum)
#     return my_sum
# sum(3,4,5,6,7)



# def box_musa(oltin,kumush,bronza, *args):
#     print("Birinchi o'rin (oltin):",oltin)
#     print("Ikinchi o'rin (kumush):",kumush)
#     print("Uchunchi o'rin (bronza):",bronza)
#     print("")
#     print("Qolgan ishtirokchilar:")
#     for arg in args:
#         print(arg)
        
# box_musa("Jasur va Behruz", "Usmon lox", "Shoxjaxon", "Ibroxim","Ahmad","Mamur", 'Odil')

def ogohlantirish_berish(test_natijalari):

    tartiblangan_natijalar = sorted(enumerate(test_natijalari, start=1), key=lambda x: x[1], reverse=True)
    

    eng_oxirgi_oquvchilar = tartiblangan_natijalar[-3:]
    

    for tartib, (oquvchi, natija) in enumerate(eng_oxirgi_oquvchilar, start=1):
        print(f"{tartib}. {oquvchi}: Natija - {natija}. Ogohlantirish:Harakat qiling")

test_natijalari = [90, 85, 92, 88, 78, 95]


ogohlantirish_berish(test_natijalari)