from PIL import Image, ImageDraw

def create_agent_icon(shape, color, size=(64, 64)):
    """
    Create a simple icon for 'New Agent' and 'Delete Agent' actions.
    :param shape: 'plus' for New Agent, 'minus' for Delete Agent
    :param color: Color of the shape
    :param size: Size of the icon (width, height)
    :return: PIL Image object
    """
    icon = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    padding = 20

    if shape == 'plus':
        # Draw a plus sign for the New Agent
        draw.line((size[0]//2, padding, size[0]//2, size[1]-padding), fill=color, width=4)
        draw.line((padding, size[1]//2, size[0]-padding, size[1]//2), fill=color, width=4)
    elif shape == 'minus':
        # Draw a minus sign for the Delete Agent
        draw.line((padding, size[1]//2, size[0]-padding, size[1]//2), fill=color, width=4)

    return icon

# Create New Agent icon
new_agent_icon = create_agent_icon('plus', (0, 128, 0))  # Dark green for New Agent

# Create Delete Agent icon
delete_agent_icon = create_agent_icon('minus', (255, 0, 0))  # Red for Delete Agent

# Save icons
new_agent_icon_path = "agent-config/icons/plus_icon.png"
delete_agent_icon_path = "agent-config/icons/minus_icon.png"

new_agent_icon.save(new_agent_icon_path)
delete_agent_icon.save(delete_agent_icon_path)

new_agent_icon_path, delete_agent_icon_path

