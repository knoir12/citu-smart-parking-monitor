"""
CIT-U Smart Parking Live Video Feed Dashboard
Author: Jean Roy Lastimosa

Dashboard variant with OpenCV live video frame streaming (BGR-to-RGB conversion
and PIL ImageTk rendering) and YOLOv5 inference launch integration.
"""

import datetime
import subprocess
import sys
from pathlib import Path
from tkinter import StringVar

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / "assets" / "frame0"
ROOT_ASSETS_PATH = OUTPUT_PATH.parent / "assets"

cap = cv2.VideoCapture(0)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def update_datetime():
    """Update the live date and time labels every 1000ms."""
    now = datetime.datetime.now()
    date_str = now.strftime("%m/%d/%y")
    time_str = now.strftime("%I:%M:%S %p")

    label_date.configure(text=date_str)
    label_time.configure(text=time_str)

    window.after(1000, update_datetime)


def update_video(image_container):
    """Read a frame from the OpenCV video capture, convert BGR to RGB, and render on the canvas."""
    ret, frame = cap.read()
    if ret:
        frame_resized = cv2.resize(frame, (571, 321))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        canvas.itemconfig(image_container, image=img_tk)
        canvas.image = img_tk

    window.after(10, lambda: update_video(image_container))


def apply_hover_effect(button):
    def on_enter(event):
        button.configure(border_width=2, border_color="#FFFFFF")

    def on_leave(event):
        button.configure(border_width=0)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def apply_click_effect(button, click_color="#F3E3AB"):
    original_color = button.cget("fg_color")

    def on_click(event):
        button.configure(fg_color=click_color)
        button.after(100, lambda: button.configure(fg_color=original_color))

    button.bind("<Button-1>", on_click)


def run_python_file():
    """Execute YOLOv5 detection script with custom trained weights."""
    python_executable = sys.executable
    python_file_path = OUTPUT_PATH.parent / "yolov5" / "detect.py"
    weights_path = OUTPUT_PATH.parent / "yolov5" / "last.pt"
    subprocess.run([
        python_executable,
        str(python_file_path),
        "--weights", str(weights_path),
        "--view-img",
        "--source", "0"
    ], check=True)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry("830x500")
window.configure(bg="#7D292C")
window.title("The Problem Algo - Live Video Feed")

logo_file = ROOT_ASSETS_PATH / "logo.png"
if logo_file.exists():
    image_icon = ImageTk.PhotoImage(file=str(logo_file))
    window.iconphoto(False, image_icon)

canvas = ctk.CTkCanvas(
    window,
    bg="#7D292C",
    height=500,
    width=830,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = ImageTk.PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(415, 32, image=image_image_1)

image_image_2 = ImageTk.PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(415, 75, image=image_image_2)

image_image_3 = ImageTk.PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(42, 32, image=image_image_3)

original_image_4 = Image.open(relative_to_assets("image_4.png"))
desired_width, desired_height = 571, 321
resized_image_4 = original_image_4.resize((desired_width, desired_height))
resized_image_4_tk = ImageTk.PhotoImage(resized_image_4)
canvas.create_image(510, 280, image=resized_image_4_tk)

image_image_5 = ImageTk.PhotoImage(file=relative_to_assets("image_5.png"))
canvas.create_image(510, 280, image=image_image_5)

image_image_6 = ImageTk.PhotoImage(file=relative_to_assets("image_6.png"))
canvas.create_image(115, 288, image=image_image_6)

label_welcome = ctk.CTkLabel(
    canvas,
    text="Welcome to CIT-U!",
    text_color="#7D292C",
    font=ctk.CTkFont(family="Roboto Mono Bold", size=28),
    bg_color="#FACA25"
)
label_welcome.place(x=84, y=11)

label_date_label = ctk.CTkLabel(
    canvas,
    text="DATE:",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Commissioner Regular", size=12),
    bg_color="#7D5F15",
    height=10
)
label_date_label.place(x=480, y=65)

label_date = ctk.CTkLabel(
    canvas,
    text="MM/DD/YY",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Commissioner Regular", size=12),
    bg_color="#7D5F15",
    height=10
)
label_date.place(x=520, y=65)

label_time_label = ctk.CTkLabel(
    canvas,
    text="TIME:",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Commissioner Regular", size=12),
    bg_color="#7D5F15",
    height=10
)
label_time_label.place(x=680, y=65)

label_time = ctk.CTkLabel(
    canvas,
    text="HH:MM:SS PM",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Commissioner Regular", size=12),
    bg_color="#7D5F15",
    height=10
)
label_time.place(x=720, y=65)

buttons_config = [
    {"text": "GLE Building", "command": lambda: print("GLE Building clicked"), "x": 46, "y": 156},
    {"text": "Near Canteen", "command": lambda: print("Near Canteen clicked"), "x": 46, "y": 212},
    {"text": "JHS Grounds", "command": lambda: print("JHS Grounds clicked"), "x": 46, "y": 268},
    {"text": "RTL Building", "command": lambda: print("RTL Building clicked"), "x": 46, "y": 324},
    {"text": "Allied", "command": lambda: print("Allied clicked"), "x": 46, "y": 380},
]

buttons = []
for config in buttons_config:
    button = ctk.CTkButton(
        master=window,
        text=config["text"],
        command=config["command"],
        width=141,
        height=36,
        fg_color="#FACA25",
        text_color="#7D292C",
        hover_color="#7D292C",
        font=("Average", 15),
        corner_radius=35,
        bg_color="#913609"
    )
    button.place(x=config["x"], y=config["y"])
    apply_hover_effect(button)
    apply_click_effect(button, click_color="#F3E3AB")
    buttons.append(button)

label_slots = ctk.CTkLabel(
    canvas,
    text="Available Slots:",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Roboto Mono SemiBold", size=15)
)
label_slots.place(x=222, y=453)

slots_var = StringVar()
slots_var.set("15")

label_slots_number = ctk.CTkLabel(
    canvas,
    textvariable=slots_var,
    text_color="#FACA25",
    font=ctk.CTkFont(family="Roboto Mono SemiBold", size=18),
)
label_slots_number.place(x=365, y=454)

scan_button = ctk.CTkButton(
    master=window,
    text="Switch Raw Algo",
    command=run_python_file,
    width=100,
    height=36,
    fg_color="#FACA25",
    text_color="#7D292C",
    hover_color="#7D292C",
    font=("Average", 15),
    corner_radius=35,
    bg_color="#7D292C"
)
scan_button.place(x=450, y=453)
apply_hover_effect(scan_button)
apply_click_effect(scan_button, click_color="#F3E3AB")

label_status = ctk.CTkLabel(
    canvas,
    text="Status:",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Roboto Mono SemiBold", size=15)
)
label_status.place(x=670, y=453)

circle_radius = 8
circle_spacing = 20
circle_y = 468


def create_circle(x, y):
    return canvas.create_oval(
        x - circle_radius, y - circle_radius,
        x + circle_radius, y + circle_radius,
        fill="#29DE0C"
    )


circle_items = []
circle_positions = [(788 - i * circle_spacing, circle_y) for i in range(3)]

for x, y in circle_positions:
    circle_item = create_circle(x, y)
    circle_items.append(circle_item)


def update_status_indicator(slots_text):
    print("Updating status indicator with slots:", slots_text)
    slots = int(slots_text.strip())

    if slots == 0:
        color = "#D2042D"
    elif slots < 10:
        color = "orange"
    else:
        color = "#29DE0C"

    for item in circle_items:
        canvas.itemconfig(item, fill=color)


def slots_var_changed(*args):
    update_status_indicator(slots_var.get())


update_status_indicator(slots_var.get())
slots_var.trace_add("write", slots_var_changed)

window.resizable(False, False)
update_datetime()
window.mainloop()
