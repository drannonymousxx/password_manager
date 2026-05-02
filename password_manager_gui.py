import customtkinter as ctk
from password_manager_logic import *

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x650")
root.title("Secure Password Manager 🔐")

current_master_password = None

# ---------------- UTIL ----------------
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# ---------------- CLIPBOARD ----------------
def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    copy_status.configure(text="Copied ✅")

    root.after(10000, clear_clipboard)

def clear_clipboard():
    root.clipboard_clear()
    copy_status.configure(text="Clipboard cleared 🔒")

# ---------------- SETUP ----------------
def show_setup():
    clear_screen()

    ctk.CTkLabel(root, text="Create Master Password", font=("Arial", 20)).pack(pady=20)

    entry = ctk.CTkEntry(root, show="*")
    entry.pack(pady=10)

    def save():
        set_master_password(entry.get())
        show_login()

    ctk.CTkButton(root, text="Save", command=save).pack(pady=10)

# ---------------- LOGIN ----------------
def show_login():
    clear_screen()

    ctk.CTkLabel(root, text="Enter Master Password", font=("Arial", 20)).pack(pady=20)

    entry = ctk.CTkEntry(root, show="*")
    entry.pack(pady=10)

    status = ctk.CTkLabel(root, text="")
    status.pack()

    def login():
        global current_master_password
        if check_master_password(entry.get()):
            current_master_password = entry.get()
            show_main()
        else:
            status.configure(text="Wrong password ❌", text_color="red")

    ctk.CTkButton(root, text="Login", command=login).pack(pady=10)

# ---------------- MAIN ----------------
def show_main():
    clear_screen()

    global copy_status
    copy_button = None

    ctk.CTkLabel(root, text="Password Manager", font=("Arial", 20)).pack(pady=10)

    # -------- INPUTS --------
    site = ctk.CTkEntry(root, placeholder_text="Website")
    site.pack(pady=5)

    username = ctk.CTkEntry(root, placeholder_text="Username")
    username.pack(pady=5)

    password = ctk.CTkEntry(root, placeholder_text="Password", show="*")
    password.pack(pady=5)

    # -------- SHOW / HIDE PASSWORD --------
    def toggle_password():
        if password.cget("show") == "":
            password.configure(show="*")
            toggle_btn.configure(text="👁️ Show")
        else:
            password.configure(show="")
            toggle_btn.configure(text="🙈 Hide")

    toggle_btn = ctk.CTkButton(root, text="👁️ Show", command=toggle_password)
    toggle_btn.pack(pady=5)

    # -------- PASSWORD GENERATOR --------
    gen_length = ctk.CTkEntry(root, placeholder_text="Length (default 12)")
    gen_length.pack(pady=5)

    def generate():
        try:
            length = int(gen_length.get())
        except:
            length = 12

        new_pass = generate_password(length)

        password.delete(0, "end")
        password.insert(0, new_pass)

    ctk.CTkButton(root, text="Generate Password", command=generate).pack(pady=5)

    # -------- COPY GENERATED PASSWORD --------
    def copy_generated():
        copy_to_clipboard(password.get())

    ctk.CTkButton(root, text="Copy Input Password 📋", command=copy_generated).pack(pady=5)

    # -------- RESULT --------
    result = ctk.CTkLabel(root, text="")
    result.pack(pady=10)

    copy_status = ctk.CTkLabel(root, text="")
    copy_status.pack(pady=5)

    # -------- SAVE --------
    def save():
        save_password(current_master_password, site.get(), username.get(), password.get())
        result.configure(text="Saved ✅", text_color="green")

    # -------- SEARCH --------
    def search():
        nonlocal copy_button

        u, p = get_password(current_master_password, site.get())

        if u:
            result.configure(text=f"{u} / {p}", text_color="white")

            if copy_button:
                copy_button.destroy()

            copy_button = ctk.CTkButton(
                root,
                text="Copy Saved Password 📋",
                command=lambda: copy_to_clipboard(p)
            )
            copy_button.pack(pady=5)

        else:
            result.configure(text="Not found ❌", text_color="red")

    ctk.CTkButton(root, text="Save", command=save).pack(pady=5)
    ctk.CTkButton(root, text="Search", command=search).pack(pady=5)

# ---------------- START ----------------
if not is_master_password_set():
    show_setup()
else:
    show_login()

root.mainloop()