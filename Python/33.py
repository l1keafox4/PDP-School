class Odam:
    ism = ''
    yil = ''
    yosh = ''
    boyi = ''
    def get_info(self):
        return f'{self.ism} \n{self.yil} \n{self.yosh} \n{self.boyi}'
Odam.ism = 'Behruz'
Odam.yil = 2008
Odam.yosh = 15
Odam.boyi = 172

dostim = Odam()
dostim.ism = 'Jasur'
dostim.yil = 2008
dostim.yosh = 15
dostim.boyi = 172
print(Odam.get_info(Odam))
print('--------------------------------')
print(Odam.get_info(dostim))
    
# malibu.name = "Tesla X model"
# malibu.color = "Black"
# malibu.year = "2022"
# malibu.price = "100000$"


