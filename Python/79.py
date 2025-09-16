def lox(name):
    def get_lox():
        return f"Salom 😁 {name}"
    
    return get_lox

s = lox("Dulbayib")
print(s())