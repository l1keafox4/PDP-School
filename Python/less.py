from tkinter import * 
from speedtest import Stest

def test():
    down = Stest().download()
    upl = Stest().upload()
    down_speed = round(down / (10**6), 2)
    upl_speed = round(upl / (10**6), 2)
    
    label.config(text="SKOROST ZAGRUSKI:\n"+ str(down_speed)+ "Mbps")
    label1.config(text="SKOROST OTDACHI:\n"+ str(upl_speed)+ "Mbps")
root = Tk()

root.title("SpeedTest")
root.geometry("300x400")

button = Button(root, text="OHIO", font=40, command=test)
button.pack(side=BOTTOM, pady=40, padx=10)
label = Label(root, text="SKOROST ZAGRUSKI:\n-", font=35)
label.pack(pady=(50,0))
label1 = Label(root, text="SKOROST OTDACHI:\n-", font=35)
label1.pack(pady=(10,0))

root.mainloop()
