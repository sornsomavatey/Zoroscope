import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from PIL import ImageDraw, ImageOps

ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

app = ctk.CTk()
app.geometry("1200x1000")
app.title("ZoroScope")

#Frame
main_frame = ctk.CTkFrame(master=app, fg_color=("#18004F", "#16004B"))
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Sign Up Section
signup_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
signup_frame.pack(pady=30)

signup_title = ctk.CTkLabel(
    master=signup_frame,
    text="🪐 Sign Up to Get Your Horoscope!",
    font=ctk.CTkFont(size=24, weight="bold"),
    text_color="white"
)
signup_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

# Name Entry
name_label = ctk.CTkLabel(signup_frame, text="Name:", text_color="white")
name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
name_entry = ctk.CTkEntry(signup_frame, placeholder_text="Enter your name")
name_entry.grid(row=1, column=1, pady=5, padx=10)

# Password Entry
password_label = ctk.CTkLabel(signup_frame, text="Password:", text_color="white")
password_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Enter your password", show="*")
password_entry.grid(row=2, column=1, pady=5, padx=10)

# Birthday Entry
birthday_label = ctk.CTkLabel(signup_frame, text="Birthday (YYYY-MM-DD):", text_color="white")
birthday_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
birthday_entry = ctk.CTkEntry(signup_frame, placeholder_text="e.g., 2000-08-15")
birthday_entry.grid(row=3, column=1, pady=5, padx=10)

# Sign Up Button
def handle_signup():
    name = name_entry.get()
    password = password_entry.get()
    birthday = birthday_entry.get()
    print(f"Signed up: {name}, {password}, {birthday}")  # Replace with MongoDB insertion later

signup_button = ctk.CTkButton(
    master=signup_frame,
    text="Create Account",
    fg_color="#6E49FF",
    hover_color="#8E66FF",
    corner_radius=6,
    font=ctk.CTkFont(size=14, weight="bold"),
    command=handle_signup
)
signup_button.grid(row=4, column=0, columnspan=2, pady=20)

app.mainloop()