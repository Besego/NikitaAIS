# styles/colors.py

# Pink Shades
TEXT = "#000000"
PINK_LIGHT = "#ADD8E6"  # Light Pink
PINK_MEDIUM = "#87CEEB"  # Hot Pink
PINK_DARK = "#4682B4"  # Medium Violet Red

# Yellow Shades
YELLOW_LIGHT = "#FFFFFF"  # Light Yellow
YELLOW_MEDIUM = "#F0F8FF"  # Yellow
YELLOW_DARK = "#FFD700"  # Gold

# Gradients (Example: Linear gradient from light pink to light yellow)
# Note: Actual gradient implementation depends on the UI framework (e.g., CSS, Tkinter, Kivy, etc.)
# This is a conceptual representation.
PINK_YELLOW_GRADIENT = f"linear-gradient(to right, {PINK_LIGHT}, {YELLOW_LIGHT})"
PINK_GRADIENT = f"linear-gradient(to right, {PINK_LIGHT}, {PINK_DARK})"
YELLOW_GRADIENT = f"linear-gradient(to right, {YELLOW_LIGHT}, {YELLOW_DARK})"


# You might need specific color formats depending on your UI library (e.g., hex, rgb, rgba)
# Example for RGB conversion (if needed):
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# PINK_LIGHT_RGB = hex_to_rgb(PINK_LIGHT)
# YELLOW_LIGHT_RGB = hex_to_rgb(YELLOW_LIGHT)


# Text color
TEXT = "#000000"  # Black, can be changed to a darker blue if needed

# Blue Shades
LIGHT_BLUE = "#ADD8E6"  # Light Blue
MEDIUM_BLUE = "#87CEEB"  # Sky Blue
DARK_BLUE = "#4682B4"  # Steel Blue

# White and Very Light Blue
WHITE = "#FFFFFF"  # White
VERY_LIGHT_BLUE = "#F0F8FF"  # Alice Blue

# Gradients
# Gradient from light blue to white
BLUE_WHITE_GRADIENT = f"linear-gradient(to right, {LIGHT_BLUE}, {WHITE})"
# Gradient from light blue to dark blue
BLUE_GRADIENT = f"linear-gradient(to right, {LIGHT_BLUE}, {DARK_BLUE})"
# Gradient from very light blue to light blue
VERY_LIGHT_BLUE_GRADIENT = f"linear-gradient(to right, {VERY_LIGHT_BLUE}, {LIGHT_BLUE})"


# Function to convert hex to RGB if needed
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
