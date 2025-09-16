import tkinter as tk

def add_digit(digit):
    value = calc.get()
    if value[0] == '0':
        value = value[1:]
    calc.delete(0,tk.END)
    calc.insert(0,value+digit)
    

def add_operation(operation):
    value = calc.get()
    if value[-1] in '-+/*':
        value = value[:-1]
    calc.delete(0,tk.END)
    calc.insert(0,value+operation)    
    
def calculate():
    value = calc.get()
    calc.delete(0,tk.END)
    calc.insert(0,eval(value)) 
    
def m_d_b(digit):
        return tk.Button(text=digit, bd = 5, font=('Arial', 13), command = lambda : add_digit(digit))
    
def m_o_b(oper):
        return tk.Button(text=oper, bd = 5, font=('Arial', 13), fg='orange', command = lambda : add_operation(oper))
    
  
def m_c_b(oper):
        return tk.Button(text=oper, bd = 5, font=('Arial', 13), fg='orange', command=calculate)
def m_del_b(oper):
        return tk.Button(text=oper, bd = 5, font=('Arial', 13), fg='orange', command = lambda : add_digit(oper))
    
root = tk.Tk()
root.geometry("240x270+100+200")
root['bg'] = '#ff5900'
root.title('Calculator')

calc = tk.Entry(root, justify=tk.RIGHT, font=('Arial', 15), width=15)
calc.insert(0,'0',)
calc.grid(row=0, column=0, columnspan=4, stick='we', padx=5)

m_d_b("1").grid(row=1, column=0, stick='wens', padx=5, pady=5)
m_d_b("2").grid(row=1, column=1, stick='wens', padx=5, pady=5)
m_d_b("3").grid(row=1, column=2, stick='wens', padx=5, pady=5)
m_d_b("4").grid(row=2, column=0, stick='wens', padx=5, pady=5)
m_d_b("5").grid(row=2, column=1, stick='wens', padx=5, pady=5)
m_d_b("6").grid(row=2, column=2, stick='wens', padx=5, pady=5)
m_d_b("7").grid(row=3, column=0, stick='wens', padx=5, pady=5)
m_d_b("8").grid(row=3, column=1, stick='wens', padx=5, pady=5)
m_d_b("9").grid(row=3, column=2, stick='wens', padx=5, pady=5)
m_d_b("0").grid(row=4, column=0, stick='wens', padx=5, pady=5)

m_o_b('+').grid(row=1, column=3, stick='wens', padx=5, pady=5)
m_o_b('-').grid(row=2, column=3, stick='wens', padx=5, pady=5)
m_o_b('/').grid(row=3, column=3, stick='wens', padx=5, pady=5)
m_o_b('*').grid(row=4, column=3, stick='wens', padx=5, pady=5)

m_c_b('=').grid(row=4, column=2, stick='wens', padx=5, pady=5)
m_c_b('c').grid(row=4, column=1, stick='wens', padx=5, pady=5)

root.grid_columnconfigure(0,minsize=60)
root.grid_columnconfigure(1,minsize=60)
root.grid_columnconfigure(2,minsize=60)
root.grid_columnconfigure(3,minsize=60)

root.grid_rowconfigure(1,minsize=60)
root.grid_rowconfigure(2,minsize=60)
root.grid_rowconfigure(3,minsize=60)
root.grid_rowconfigure(4,minsize=60)

root.mainloop()