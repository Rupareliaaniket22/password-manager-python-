from tkinter import *
import random
from tkinter import simpledialog, messagebox
import json
import pyperclip

Background = "#1F1F1F"
label_fg = "#FFFFFF"
entry_bg = "#444444"
entry_fg = "#FFFFFF"
entry_border = "#333333"
button_bg = "#2484E4"
slogan_color = "#FFFFFF"
generated_password = ""


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    global generated_password
    generated_password = ""
    for _ in range(random.randint(10, 16)):
        generated_password += chr(random.randint(33, 126))
    password_input.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def store_password():
    global generated_password
    site_name = site_name_input.get()
    email_username = email_username_input.get()
    added_pass = password_input.get()
    old_data = {}
    if len(added_pass) == 0:
        added_pass = generated_password

    if len(site_name) == 0 or len(email_username) == 0:
        messagebox.showerror(message="you have left fields empty please fill it")
    else:
        user_answer = messagebox.askyesno("Confirmation", f"These are the details provided \n {site_name}\n"
                                                          f"{email_username}\n{added_pass}\n do you want save it?")
        if user_answer:
            data = {
                site_name: {
                    "email": email_username,
                    "password": added_pass
                }
            }
            try:
                with open("password.json", 'r') as fi:
                    old_data = json.load(fi)
            except FileNotFoundError:
                with open("password.json", 'w') as fi:
                    json.dump(data, fi, indent=4)
            else:
                old_data.update(data)
                with open("password.json", 'w') as data_file:
                    json.dump(old_data, data_file, indent=4)
            finally:
                site_name_input.delete(0, END)
                email_username_input.delete(0, END)
                password_input.delete(0, END)


def search():
    site_name=site_name_input.get()
    try:
        with open("password.json", 'r') as data_file:
            data = json.load(data_file)
            try:
                details=data[site_name]
                email=details["email"]
                password=details["password"]

            except KeyError:
                messagebox.showerror(message="data not found")
            else:
                messagebox.showerror(message=f"email : {email}\n password : {password}")
    except FileNotFoundError:
        messagebox.showerror(message="record not found")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
window.config(pady=50, padx=50, bg=Background)

# canvas for logo
canvas = Canvas(width=200, height=200, highlightthickness=0, bg=Background)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1, padx=20, pady=5)

frame_search = Frame(window)
frame_pass = Frame(window)
# ---------------------------------------label----------------------------------------------------

# slogan
slogan = Label(text="Your Passkey to Privacy", font="Arial", fg=slogan_color, bg=Background)
slogan.grid(row=1, column=1, pady=5)

# site_name_label
site_name_label = Label(text="Website", font="Arial", fg=label_fg, bg=Background)
site_name_label.grid(row=2, column=0)

# email/username_label
email_username_label = Label(text="Email/Username", font="Arial", fg=label_fg, bg=Background)
email_username_label.grid(row=3, column=0, )

# password_label
password_label = Label(text="Password", font="Arial", fg=label_fg, bg=Background)
password_label.grid(row=4, column=0)

# ---------------------------------------Entry----------------------------------------------------
# site_name_input
site_name_input = Entry(frame_search, width=18, bg=entry_bg, fg=entry_fg)
site_name_input.pack(side="left")

# email/username_input
email_username_input = Entry(width=32, bg=entry_bg, fg=entry_fg)
email_username_input.grid(row=3, column=1, pady=3)

# password_input
password_input = Entry(frame_pass, width=18, bg=entry_bg, fg=entry_fg)
password_input.pack(side="left")

# ---------------------------------------Button----------------------------------------------------
# searchButton
searchbutton = Button(frame_search, text="Search", font="Arial,12", width=10, bg=Background, highlightthickness=0,command=search)
searchbutton.pack(side="right")
frame_search.grid(row=2, column=1, pady=3)

# password_generator_button
password_generator_button = Button(frame_pass, text="Generate", font="Arial,12", width=10, bg=button_bg,
                                   command=generate_password)
password_generator_button.pack(side="right")
frame_pass.grid(row=4, column=1, pady=3)

# Add
add_button = Button(text="Add", font="Arial", width=33, bg=button_bg, command=store_password)
add_button.grid(row=5, column=1)

window.mainloop()
