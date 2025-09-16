import tkinter as tk
from tkinter import PhotoImage

my_magazine = {
    'non': {
        'price': 4000,
        'quantity': 0,
        'image_filename': 'non.png'
    },
    'anor': {
        'price': 45000,
        'quantity': 0,
        'image_filename': 'anor.png'
    },
    'shaftoli': {
        'price': 25000,
        'quantity': 0,
        'image_filename': 'shaftoli.png'
    }
}

def calculate_total_price():
    total_price = 0
    shopping_list = []

    for item, item_data in my_magazine.items():
        quantity = item_data['quantity']
        total_price += quantity * item_data['price']

        if quantity > 0:
            shopping_list.append(f'{item}: {quantity} шт.')

    result_label.config(text=f'Total payment: {total_price} so\'m')

    shopping_text.delete(1.0, tk.END)
    for item in shopping_list:
        shopping_text.insert(tk.END, item + '\n')

def increase_quantity(item):
    my_magazine[item]['quantity'] += 1
    calculate_total_price()

def decrease_quantity(item):
    if my_magazine[item]['quantity'] > 0:
        my_magazine[item]['quantity'] -= 1
        calculate_total_price()

root = tk.Tk()
root.title("Magazine Sales")
root.geometry('1920x1080')

item_buttons = {}
item_labels = {}
# item_images = {}

for item, item_data in my_magazine.items():
    item_buttons[item] = {
        'plus': tk.Button(root, text="+", command=lambda item=item: increase_quantity(item)),
        'minus': tk.Button(root, text="-", command=lambda item=item: decrease_quantity(item))
    }

    item_labels[item] = tk.Label(root, text=f'{item}: {item_data["price"]} so\'m')
    # item_images[item] = PhotoImage(file=f"images/{item_data['image_filename']}")

    if item == 'non':
        x, y = 0, 0
    elif item == 'anor':
        x, y = 0, 150
    elif item == 'shaftoli':
        x, y = 0, 300

    item_buttons[item]['plus'].place(x=45 + x, y=125 + y)
    item_buttons[item]['minus'].place(x=65 + x, y=125 + y)
    item_labels[item].place(x=150 + x, y=50 + y)

    # image_label = tk.Label(root, image=item_images[item])
    # image_label.place(x=x, y=y)

result_label = tk.Label(root, text="")
result_label.place(x=830, y=300)

calculate_button = tk.Button(root, text="Calculate Total Price", command=calculate_total_price)
calculate_button.place(x=50, y=450)

shopping_text = tk.Text(root, height=10, width=30)
shopping_text.place(x=800, y=100)

root.mainloop()