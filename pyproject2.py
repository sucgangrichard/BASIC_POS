import tkinter as tk
root = tk.Tk()
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, simpledialog
import datetime

root.title("POS SYSTEM")

#=====Windows=====
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    
window_width = 1120
window_height = 550

center_window(root, window_width, window_height)

#=====Button Function=====
def on_button_click(product, price):
    for child in tree.get_children():
        if tree.item(child)["values"][0] == product:
            quantity = tree.item(child)["values"][1] + 1
            total_price = price * quantity
            tree.item(child, values=(product, quantity, f"${total_price:.2f}"))
            update_total_price_label()  # Update the total price label
            return
    tree.insert('', 'end', values=(product, 1, f"${price:.2f}"))
    update_total_price_label()  # Update the total price label

#=====Button=====
# Main container frame
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Frame for the buttons
button_frame = tk.Frame(main_frame, bg="lightblue")  # Colored background
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configure column weights to give equal space to both frames
main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(1, weight=1)

products = [
    ("Apples", 1.20, "apples.png"),
    ("Bananas", 0.80, "apples.png"),
    ("Carrots", 0.60, "apples.png"),
    ("Doughnuts", 1.50, "apples.png"),
    ("Eggs", 2.00, "apples.png"),
    ("Fish", 5.00, "apples.png"),
    ("Grapes", 2.20, "apples.png"),
    ("Honey", 3.25, "apples.png"),
    ("Ice Cream", 4.00, "apples.png")
]
#continue...


# Load images and create buttons
images = []
for i, (product, price, image_file) in enumerate(products):
    original = Image.open(image_file)
    resized = original.resize((50, 50), Image.Resampling.LANCZOS)  # Use LANCZOS resampling for high-quality downsampling
    img = ImageTk.PhotoImage(resized)
    images.append(img)  # Keep a reference to the images
    button_text = f"{product}: ${price:.2f}"
    button = tk.Button(button_frame,
                       image=img,
                       text=button_text,
                       compound="top",
                       command=lambda p=product, pr=price: on_button_click(p, pr))
    button.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
    # Configure button frame grid to expand equally
    button_frame.rowconfigure(i//3, weight=1)
    button_frame.columnconfigure(i%3, weight=1)


#=====Treeview Update Function=====
# Function to update selected product in TreeView
def update_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to update.")
        return

    selected_item = selected[0]
    product_name = tree.item(selected_item)['values'][0]
    current_quantity = tree.item(selected_item)['values'][1]
    price_per_unit = float(tree.item(selected_item)['values'][2].strip('$')) / current_quantity
    new_quantity = simpledialog.askinteger("Update Quantity", f"Enter new quantity for {product_name}:", minvalue=1)
    
    if new_quantity:
        new_total_price = new_quantity * price_per_unit
        tree.item(selected_item, values=(product_name, new_quantity, f"${new_total_price:.2f}"))
        update_total_price_label()  # Update the total price label


#=====Treeview delete Function=====
# Function to delete the selected product from TreeView
def delete_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return

    for item in selected:
        tree.delete(item)
    update_total_price_label()  # Update the total price label

        
#=====TreeView=====
tree_frame = tk.Frame(main_frame, bg="gray")  # Colored background
tree_frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

tree = ttk.Treeview(tree_frame)
tree.grid(row=0, column=0, sticky=tk.NSEW)

# Define columns
tree['columns'] = ('Product_Name', 'Quantity', 'Price')

    # Format our columns
tree.column("#0", width=150, minwidth=25)
tree.column("Product_Name", anchor=tk.W, width=200)
tree.column("Quantity", anchor=tk.W, width=200)
tree.column("Price", anchor=tk.W, width=200)

    # Create Headings
tree.heading("#0", anchor=tk.W)
tree.heading("Product_Name", text="Product_Name", anchor=tk.W)
tree.heading("Quantity", text="Quantity", anchor=tk.W)
tree.heading("Price", text="Price", anchor=tk.W)


#=====Cash Function=====
# Function to calculate total and display balance
def calculate_payment():
    total_amount = 0.0
    for child in tree.get_children():
        # Accumulate the total price from the third column in the TreeView
        item_total = float(tree.item(child)["values"][2].strip('$'))
        total_amount += item_total

    try:
        cash_paid = float(entry1.get())
        balance = cash_paid - total_amount
        messagebox.showinfo("Transaction Complete", f"Total amount: ${total_amount:.2f}\nCash paid: ${cash_paid:.2f}\nChange: ${balance:.2f}")
        label3.config(text=f"${balance:.2f}")  # Update the change label
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid cash amount.")

#=====Total Price Function=====
def update_total_price_label():
    total_amount = 0.0
    for child in tree.get_children():
        total_price = float(tree.item(child)["values"][2].strip('$'))
        total_amount += total_price
    label5.config(text=f"${total_amount:.2f}")  # Update the total price label


#=====Cash Payment=====
cash_frame = tk.Frame(main_frame, bg="green")  # Colored background
cash_frame.grid(row=2, column=0, padx=8, pady=8, sticky="nsew")

label1 = tk.Label(cash_frame, text = 'CASH:')
entry1 = tk.Entry(cash_frame)
button1 = tk.Button(cash_frame, text = 'PAY', command=calculate_payment)
label2 = tk.Label(cash_frame, text = 'CHANGE:')
label3 = tk.Label(cash_frame, text = '0.00')
label4 = tk.Label(cash_frame, text = 'Total Price:')
label5 = tk.Label(cash_frame, text = '$0.00')

label1.grid(row=2, column=0,padx=5, pady=5)
entry1.grid(row=2, column=1,padx=5, pady=5)
button1.grid(row=3, column=1,padx=5, pady=5)
label2.grid(row=4, column=0,padx=5, pady=5)
label3.grid(row=4, column=1,padx=5, pady=5)
label4.grid(row=5, column=1,padx=5, pady=5)
label5.grid(row=5, column=2,padx=5, pady=5)

#=====List Generate receipt Function=====
# Function to generate receipt
def generate_receipt():
    total_amount = 0.0
    listbox.delete(0, tk.END)  # Clear the existing listbox entries
    
    today = datetime.datetime.now().date()  # Get today's date
    listbox.insert(tk.END, f"Date: {today}")
    listbox.insert(tk.END, "")
    
    for child in tree.get_children():
        product_name = tree.item(child)["values"][0]
        quantity = tree.item(child)["values"][1]
        total_price = tree.item(child)["values"][2]
        listbox.insert(tk.END, f"{product_name} x {quantity} - {total_price}")
        total_amount += float(total_price.strip('$'))
    
    listbox.insert(tk.END, "")
    listbox.insert(tk.END, f"Total: ${total_amount:.2f}")
    
    # Assuming cash was paid and change was calculated previously
    try:
        cash_paid = float(entry1.get())
        change = cash_paid - total_amount
        listbox.insert(tk.END, f"Cash Paid: ${cash_paid:.2f}")
        listbox.insert(tk.END, f"Change: ${change:.2f}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid cash amount entered.")

#=====List Print receipt Function=====
# Function to display and print the receipt, then clear the Listbox
def print_receipt():
    if listbox.size() == 0:
        messagebox.showinfo("Empty Receipt", "No receipt to print. Please generate a receipt first.")
        return
    
    receipt_content = "\n".join(listbox.get(0, tk.END))  # Gather all listbox entries into a single string
    messagebox.showinfo("Printing Receipt", receipt_content)  # Display the receipt content in a message box
    
    listbox.delete(0, tk.END)  # Clear the Listbox after displaying
    
#=====List View=====
list_frame = tk.Frame(main_frame, bg="red")  # Colored background
list_frame.grid(row=2, column=1, padx=8, pady=8, sticky="nsew")

 # Create a Listbox widget
listbox = tk.Listbox(list_frame, width=50)
listbox.grid(padx=20, pady=20)

button2 = tk.Button(list_frame, text = 'Generate Receipt', command=generate_receipt)
button2.grid(row=0, column=2,padx=5, pady=5)

button3 = tk.Button(list_frame, text = 'print Receipt', command=print_receipt)
button3.grid(row=0, column=3,padx=5, pady=5)

button4 = tk.Button(list_frame, text = 'Update item', command=update_item)
button4.grid(row=1, column=2,padx=5, pady=5)

button5 = tk.Button(list_frame, text = 'Delete item', command=delete_item)
button5.grid(row=1, column=3,padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

