from PIL import Image
import numpy as np

# Load images
album = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\album cover.png").convert("RGBA")
logo = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\nocean logo.png").convert("RGBA")

# Get dimensions
album_w, album_h = album.size
logo_w, logo_h = logo.size

# Convert to numpy for easier manipulation
logo_array = np.array(logo)

# Make both black background AND dark interior of letters transparent
# Keep only the bright edges/outlines
for y in range(logo_array.shape[0]):
    for x in range(logo_array.shape[1]):
        r, g, b, a = logo_array[y, x]
        # Calculate brightness
        brightness = (int(r) + int(g) + int(b)) / 3
        # If dark (black bg or dark letter interior), make transparent
        if brightness < 100:
            logo_array[y, x] = [0, 0, 0, 0]
        else:
            # Keep the pixel but ensure full opacity
            logo_array[y, x] = [r, g, b, 255]

logo_transparent = Image.fromarray(logo_array)

# Resize logo to fit nicely (about 60% of album width)
target_width = int(album_w * 0.6)
aspect = logo_transparent.height / logo_transparent.width
target_height = int(target_width * aspect)
logo_resized = logo_transparent.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Position centered, slightly below middle (10% down from center)
x = (album_w - target_width) // 2
y = (album_h - target_height) // 2 + int(album_h * 0.10)

# Composite
result = album.copy()
result.paste(logo_resized, (x, y), logo_resized)

# Save
output_path = r"C:\Users\noahs\Desktop\ai experiments\blender\album_cover_final3.png"
result.save(output_path, "PNG")

print(f"Done! Saved to: {output_path}")
