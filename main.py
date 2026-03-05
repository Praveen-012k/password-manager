from tkinter import *
from tkinter import messagebox
from  random import choice,shuffle,randint
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
def password_gen():
    password_letter = [choice(letters) for _ in range(randint(8,10))]
    password_num = [choice(numbers) for _ in range(randint(2,4))]
    password_sym = [choice(symbols) for _ in range(randint(2,4))]
    password_list = password_letter + password_sym + password_num
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_uname_entry.get()
    entered_password = password_entry.get()

    new_data = {website:{
        "Email":email,
        "Password":entered_password
    }}

    if len(website) == 0 or len(entered_password) == 0 :
        messagebox.showwarning(title="Warning",message="Don't leave any spaces empty")
    else:
        is_ok = messagebox.askokcancel(title="Save the details ?", message=f"Website : {website}\n"
                                              f"Email : {email}\n Password : {entered_password}")
        if is_ok:
         try:
             with open("data.json", mode="r") as data_file:
                 data = json.load(data_file)
                 data.update(new_data)

         except FileNotFoundError:
             with open("data.json",mode="w") as data_file:
                 json.dump(new_data,data_file)
         except json.JSONDecodeError:
             if_ok = messagebox.askokcancel(title="Reminder",message=f"There's No Data.\n "
                                                    f" Website : {website}\n"
                                                    f"Email : {email}\n Password : {entered_password} "
                                                    f"if yes click add again ")
             if if_ok :
                 with open("data.json", mode="w") as data_file:
                     json.dump(new_data, data_file, indent=4)

         else:
             with open("data.json", mode="w") as data_file:
                 json.dump(data, data_file, indent=4)
                 website_entry.delete(0, END)
                 password_entry.delete(0, END)
                 website_entry.focus()

# ---------------------------- FINE PASSWORD ------------------------------- #

def search():
    try:
        with open("data.json") as data_file:
            s_data = json.load(data_file)
            data_dict = s_data[website_entry.get()]
    except FileNotFoundError:
        messagebox.showinfo(title="Reminder", message=f"File not found create file with clicking ADD")

    except KeyError:
        messagebox.showinfo(title="Reminder", message=f"There's is no key called {website_entry.get()}")

    except ValueError:
        messagebox.showinfo(title="Reminder", message=f"There's is no key called {website_entry.get()}")

    else:
        messagebox.showinfo(title=f"{website_entry.get()} Data", message=f"Email : {data_dict["Email"]}\n"
                                                                         f"Password : {data_dict["Password"]}")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(height=200,width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo)
canvas.grid(row=0,column=1)

website_entry_l = Label(text="Website Name :")
website_entry_l.grid(row=1,column=0,)

email_uname_l = Label(text="Email/Username :")
email_uname_l.grid(row=2,column=0,)

password_label= Label(text="Password :")
password_label.grid(row=3,column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1,column=1,sticky="EW",)
website_entry.focus()

email_uname_entry = Entry(width=35)
email_uname_entry.grid(row=2,column=1,sticky="EW",columnspan=2)
email_uname_entry.insert(0,"Your Email")

password_entry = Entry(width=21)
password_entry.grid(row=3,column=1,sticky="EW")

password_button = Button(text="Generate Password",command=password_gen)
password_button.grid(row=3,column=2,sticky="EW")

add_button = Button(text="ADD",width=35,command=save)
add_button.grid(row=4,column=1,columnspan=2,sticky="EW")

search_button = Button(text="Search",command=search)
search_button.grid(row=1,column=2,sticky="EW")
window.mainloop()