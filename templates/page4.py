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

#Title
title_label = ctk.CTkLabel(
    master=main_frame,
    text="✨ ZoroScope ✨",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color ="white"
)
title_label.pack(pady=(20, 5))

subtiltle_label = ctk.CTkLabel(
    master=main_frame,
    text="Discover your stars, style, and self!",
    font=ctk.CTkFont(family='roboto', size=16),
    text_color="lightgray"
)
subtiltle_label.pack(pady=(0, 30))

#image card section
card_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
card_frame.pack(pady=10)
#image
def load_image(path, size, radius=0):
    image = Image.open(path).resize(size).convert("RGBA")

    if radius > 0:
        # Create rounded corner mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)

        # Apply mask
        rounded = ImageOps.fit(image, size, centering=(0.5, 0.5))
        rounded.putalpha(mask)
        image = rounded

    return ImageTk.PhotoImage(image)

img1 = load_image(r"images\lucky color.jpeg", (180, 240), radius=10)
img2 = load_image(r"images\personality.jpeg", (180, 240), radius=10)
img3 = load_image(r"images\birthday countdown.jpeg", (180, 240), radius=10)

#Function to create a card
def create_card(master, image, text):
    frame = ctk.CTkFrame(master=master, fg_color="transparent", corner_radius=10)
    frame.pack(side="left", padx=15)

    img_label = ctk.CTkLabel(master=frame, image=image, text="")
    img_label.pack(padx=10, pady=10)

    button = ctk.CTkButton(
        master=frame,
        text=text,
        fg_color="#D96DF3",
        hover_color="#FF85B3",
        font=ctk.CTkFont(family="Roboto", size=14, weight="bold", slant="italic"),
        width=140,
        corner_radius=5

    )
    button.pack(pady=(10, 15))

# Create Card
create_card(card_frame, img1, "Color Suggestion")
create_card(card_frame, img2, "Personality Matcher")
create_card(card_frame, img3, "Birthday Countdown")

app.mainloop()
