from PIL import Image, ImageDraw

def create_icon(shape, color, size=(64, 64)):
    """
    Create a simple icon with a given shape, color, and size.
    :param shape: 'circle' for sun, 'crescent' for moon
    :param color: Color of the shape
    :param size: Size of the icon (width, height)
    :return: PIL Image object
    """
    icon = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)

    if shape == 'circle':
        # Draw a simple circle for the sun
        draw.ellipse((0, 0, size[0], size[1]), fill=color)
    elif shape == 'crescent':
        # Draw a circle and then overlay a darker circle to create a crescent shape
        draw.ellipse((0, 0, size[0], size[1]), fill=color)
        draw.ellipse((size[0] * -0.2, 0, size[0] * 0.8, size[1]), fill=(0, 0, 0, 0))

    return icon

# Create sun icon (light mode)
sun_icon = create_icon('circle', (255, 215, 0))  # Gold color for sun

# Create moon icon (dark mode)
moon_icon = create_icon('crescent', (169, 169, 169))  # Dark gray for moon

# Save icons
sun_icon_path = "sun_icon.png"
moon_icon_path = "moon_icon.png"

sun_icon.save(sun_icon_path)
moon_icon.save(moon_icon_path)

sun_icon_path, moon_icon_path

