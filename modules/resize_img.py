from PIL import Image, ImageTk

def resize_image(img_path, target_width, target_height):
    img = Image.open(img_path)
    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)
