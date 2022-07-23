from PIL import Image


def compress_image(source_path):
    with Image.open(source_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        destination_path = f"{source_path}_compressed.jpg"
        img.save(
            destination_path,
            "JPEG", optimize=True, quality=80
        )
