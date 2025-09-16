class Talaba:
    university_name = "CSC Krim"

    def __init__(self, nom):
        self.nom = nom

    @classmethod
    def change_university(cls, new_universitet):
        cls.university_name = new_universitet
        print(f"Universitet nomi o'zgartirildi: {cls.university_name}")

talaba1 = Talaba("Jasur")
print(f"{talaba1.nom} talabasi, {Talaba.university_name} universitetida o'qiydi.")

Talaba.change_university("PDP Universiteti")

print(f"{talaba1.nom} talabasi, {Talaba.university_name} universitetida o'qiydi.")