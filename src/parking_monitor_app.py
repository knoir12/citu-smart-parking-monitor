"""
CIT-U Smart Parking Slot Detection & Monitoring Dashboard
Author: Jean Roy Lastimosa

Main interactive dashboard application built with CustomTkinter and OpenCV.
Features:
- Real-time parking slot occupancy tracking (Slots A-E and 1-9)
- 2D polygon rotational geometry for angled parking bays (-30 degrees)
- Reactive capacity status indicators (Green / Orange / Red)
- Asynchronous YOLOv5 inference subprocess execution and termination
"""

import datetime
import math
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

cap = cv2.VideoCapture(1)


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


def apply_hover_effect(button):
    """Apply a white border highlight when hovering over a button."""
    def on_enter(event):
        button.configure(border_width=2, border_color="#FFFFFF")

    def on_leave(event):
        button.configure(border_width=0)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def apply_click_effect(button, click_color="#F3E3AB"):
    """Apply a brief color flash when clicking a button."""
    original_color = button.cget("fg_color")

    def on_click(event):
        button.configure(fg_color=click_color)
        button.after(100, lambda: button.configure(fg_color=original_color))

    button.bind("<Button-1>", on_click)


# Subprocess handle for external YOLOv5 object detection
process = None


def run_python_file():
    """Launch the external YOLOv5 detection script asynchronously."""
    global process
    if process is None:
        python_executable = sys.executable
        python_file_path = OUTPUT_PATH.parent / "yolov5" / "detect.py"
        weights_path = OUTPUT_PATH.parent / "yolov5" / "last.pt"
        process = subprocess.Popen([
            python_executable,
            str(python_file_path),
            "--weights", str(weights_path),
            "--view-img",
            "--source", "0",
            "--device", "cpu"
        ])
        scan_button.configure(text="Stop Raw Algo", command=stop_python_file)


def stop_python_file():
    """Terminate the running YOLOv5 detection subprocess."""
    global process
    if process is not None:
        process.terminate()
        process = None
        scan_button.configure(text="Switch Raw Algo", command=run_python_file)


# Set the appearance mode and theme of CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry("830x500")
window.configure(bg="#7D292C")
window.title("The Problem Algo - CIT-U Smart Parking Monitor")

logo_file = ROOT_ASSETS_PATH / "logo.png"
if logo_file.exists():
    image_icon = ImageTk.PhotoImage(file=str(logo_file))
    window.iconphoto(False, image_icon)

# Create a CTkCanvas for layout rendering and interactive slot overlays
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

# Load and create background and frame images on the canvas
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

# Header & Date/Time Labels
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

# Campus Zone Navigation Buttons
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

# Available Slots Counter
label_slots = ctk.CTkLabel(
    canvas,
    text="Available Slots:",
    text_color="#FFFFFF",
    font=ctk.CTkFont(family="Roboto Mono SemiBold", size=15)
)
label_slots.place(x=222, y=453)

slots_var = StringVar()
slots_var.set("0")

label_slots_number = ctk.CTkLabel(
    canvas,
    textvariable=slots_var,
    text_color="#FACA25",
    font=ctk.CTkFont(family="Roboto Mono SemiBold", size=18),
)
label_slots_number.place(x=365, y=454)

slots_var.trace_add("write", lambda *args: update_status_indicator(slots_var.get()))

# YOLOv5 Process Toggle Button
scan_button = ctk.CTkButton(
    master=window,
    text="Start Raw Algo",
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

# Status Indicator LEDs
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
    """Update status indicator LEDs based on available slot thresholds."""
    print("Updating status indicator with slots:", slots_text)
    slots = int(slots_text.strip())

    if slots == 0:
        color = "#D2042D"  # Red (Full)
    elif slots <= 7:
        color = "orange"   # Orange (Limited)
    else:
        color = "#29DE0C"  # Lime (Available)

    for item in circle_items:
        canvas.itemconfig(item, fill=color)


# Parking Slot Coordinate & Geometry Definitions (Bays A-E and 1-9)
green_boxes = [
    {"name": "greenbox_A", "x": 632.5, "y": 196, "width": 15, "height": 40, "letter": "A"},
    {"name": "greenbox_B", "x": 657, "y": 196, "width": 15, "height": 40, "letter": "B"},
    {"name": "greenbox_C", "x": 680.5, "y": 196, "width": 15, "height": 40, "letter": "C"},
    {"name": "greenbox_D", "x": 704.5, "y": 196, "width": 15, "height": 40, "letter": "D"},
    {"name": "greenbox_E", "x": 728.3, "y": 196, "width": 15, "height": 40, "letter": "E"},

    {"name": "greenbox_1", "x": 376.5, "y": 294, "width": 15, "height": 40, "number": 1},
    {"name": "greenbox_2", "x": 400.3, "y": 294, "width": 15, "height": 40, "number": 2},
    {"name": "greenbox_3", "x": 424.3, "y": 294, "width": 15, "height": 40, "number": 3},
    {"name": "greenbox_4", "x": 448.3, "y": 294, "width": 15, "height": 40, "number": 4},
    {"name": "greenbox_5", "x": 504.4, "y": 291, "width": 16, "height": 40, "number": 5, "angle": -30},
    {"name": "greenbox_6", "x": 530.9, "y": 289.7, "width": 16, "height": 40, "number": 6, "angle": -30},
    {"name": "greenbox_7", "x": 558.5, "y": 289, "width": 16, "height": 40, "number": 7, "angle": -30},
    {"name": "greenbox_8", "x": 585.6, "y": 289, "width": 16, "height": 40, "number": 8, "angle": -30},
    {"name": "greenbox_9", "x": 613.4, "y": 288.1, "width": 16, "height": 40, "number": 9, "angle": -30}
]

greenbox_items = {}


def rotate_polygon(vertices, angle):
    """Rotate a list of (x, y) polygon vertices around their centroid by angle (in degrees)."""
    cx = sum(x for x, y in vertices) / len(vertices)
    cy = sum(y for x, y in vertices) / len(vertices)
    rotated_vertices = []
    for x, y in vertices:
        tx = x - cx
        ty = y - cy
        rx = tx * math.cos(math.radians(angle)) - ty * math.sin(math.radians(angle))
        ry = tx * math.sin(math.radians(angle)) + ty * math.cos(math.radians(angle))
        rotated_vertices.append((rx + cx, ry + cy))
    return rotated_vertices


for box in green_boxes:
    if "angle" in box:
        rect = canvas.create_polygon(
            rotate_polygon([
                (box["x"], box["y"]),
                (box["x"] + box["width"], box["y"]),
                (box["x"] + box["width"], box["y"] + box["height"]),
                (box["x"], box["y"] + box["height"])
            ], box["angle"]),
            fill="green",
            tags=box["name"],
            outline="black"
        )
    else:
        rect = canvas.create_rectangle(
            box["x"], box["y"],
            box["x"] + box["width"], box["y"] + box["height"],
            fill="green",
            tags=box["name"],
            outline="black"
        )
    text = canvas.create_text(
        box["x"] + box["width"] / 2,
        box["y"] + box["height"] / 2,
        text=box.get("letter", str(box.get("number"))),
        fill="white",
        font=("Arial", 14)
    )
    greenbox_items[box["name"]] = (rect, text)

key_to_greenbox = {
    "a": "greenbox_A",
    "b": "greenbox_B",
    "c": "greenbox_C",
    "d": "greenbox_D",
    "e": "greenbox_E",
    "1": "greenbox_1",
    "2": "greenbox_2",
    "3": "greenbox_3",
    "4": "greenbox_4",
    "5": "greenbox_5",
    "6": "greenbox_6",
    "7": "greenbox_7",
    "8": "greenbox_8",
    "9": "greenbox_9"
}


def hide_greenbox(greenbox_name):
    rect, text = greenbox_items[greenbox_name]
    canvas.itemconfig(rect, state="hidden")
    canvas.itemconfig(text, state="hidden")


for greenbox_name in greenbox_items:
    hide_greenbox(greenbox_name)


def decrement_slots_var():
    current_value = int(slots_var.get())
    new_value = max(current_value - 1, 0)
    slots_var.set(str(new_value))


def increment_slots_var():
    current_value = int(slots_var.get())
    new_value = current_value + 1
    slots_var.set(str(new_value))


def toggle_greenbox(greenbox_name):
    """Toggle visibility of a parking bay overlay and update available slot count."""
    rect, text = greenbox_items[greenbox_name]
    if canvas.itemcget(rect, "state") == "hidden":
        canvas.itemconfig(rect, state="normal")
        canvas.itemconfig(text, state="normal")
        increment_slots_var()
    else:
        canvas.itemconfig(rect, state="hidden")
        canvas.itemconfig(text, state="hidden")
        decrement_slots_var()


def on_key_press(event):
    if event.keysym in key_to_greenbox:
        greenbox_name = key_to_greenbox[event.keysym]
        toggle_greenbox(greenbox_name)


window.bind("<KeyPress>", on_key_press)
window.resizable(False, False)

update_datetime()
window.mainloop()
