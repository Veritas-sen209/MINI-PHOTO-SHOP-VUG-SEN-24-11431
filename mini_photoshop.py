from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

current_image = None
original_image = None
display_image = None

def open_image():
    global current_image, original_image
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if path:
        current_image = cv2.imread(path)
        if current_image is None:
            print("Error: Could not read image. Please check file.")
            return
        original_image = current_image.copy()
        show_image(current_image)

def show_image(img):
    global display_image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.thumbnail((600, 450))
    display_image = ImageTk.PhotoImage(img)
    canvas.config(width=display_image.width(), height=display_image.height())
    canvas.create_image(0, 0, anchor=NW, image=display_image)

def reset_image():
    global current_image, original_image
    if original_image is not None:
        current_image = original_image.copy()
        show_image(current_image)

def save_image():
    global current_image
    if current_image is not None:
        path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if path:
            cv2.imwrite(path, current_image)

def apply_gray():
    global current_image
    if current_image is not None:
        gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        current_image = gray
        show_image(current_image)

def apply_blur():
    global current_image
    if current_image is not None:
        blur = cv2.GaussianBlur(current_image, (15, 15), 0)
        current_image = blur
        show_image(current_image)

def apply_sharpen():
    global current_image
    if current_image is not None:
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        sharpened = cv2.filter2D(current_image, -1, kernel)
        current_image = sharpened
        show_image(current_image)

def apply_edge():
    global current_image
    if current_image is not None:
        edges = cv2.Canny(current_image, 100, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        current_image = edges
        show_image(current_image)

def adjust_brightness(value):
    global current_image, original_image
    if original_image is not None:
        brightness = int(value)
        hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = v.astype(np.int16)
        v = np.clip(v + brightness, 0, 255)
        v = v.astype(np.uint8)
        final = cv2.merge((h, s, v))
        final = cv2.cvtColor(final, cv2.COLOR_HSV2BGR)
        current_image = final
        show_image(final)

root = Tk()
root.title("Mini Photoshop - Modern UI")
root.geometry("900x500")
root.config(bg="#f0f0f0")

canvas_frame = Frame(root, bg="white", bd=2, relief=RIDGE)
canvas_frame.place(x=20, y=20, width=620, height=460)
canvas = Canvas(canvas_frame, bg="lightgray")
canvas.pack(fill=BOTH, expand=True)

panel = Frame(root, bg="#2c3e50")
panel.place(x=660, y=20, width=220, height=460)

Label(panel, text="Mini Photoshop", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

Button(panel, text="Open Image", command=open_image, width=20, bg="#27ae60", fg="white").pack(pady=5)
Button(panel, text="Reset", command=reset_image, width=20, bg="#e67e22", fg="white").pack(pady=5)
Button(panel, text="Save Image", command=save_image, width=20, bg="#2980b9", fg="white").pack(pady=5)

Label(panel, text="Filters", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
Button(panel, text="Grayscale", command=apply_gray, width=20).pack(pady=3)
Button(panel, text="Blur", command=apply_blur, width=20).pack(pady=3)
Button(panel, text="Sharpen", command=apply_sharpen, width=20).pack(pady=3)
Button(panel, text="Edge Detect", command=apply_edge, width=20).pack(pady=3)

Label(panel, text="Brightness", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
brightness_slider = Scale(panel, from_=-100, to=100, orient=HORIZONTAL, command=adjust_brightness, length=180)
brightness_slider.pack(pady=5)

root.mainloop()
