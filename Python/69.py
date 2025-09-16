import yaml

def oqibOlibQaytar(fayl_nomi):
    with open(fayl_nomi, 'r') as f:
        malumotlar = yaml.safe_load(f)
    return malumotlar

if __name__ == "__main__":
    fayl_nomi = "shaxsiy.yaml"
    malumotlar = oqibOlibQaytar(fayl_nomi)
    print(malumotlar)