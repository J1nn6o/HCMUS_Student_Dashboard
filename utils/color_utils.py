def lighten_color(color_str, alpha=0.2):
    """Làm sáng một màu RGBA bằng cách điều chỉnh alpha."""
    rgba_values = color_str.strip("rgba()").split(",")
    if len(rgba_values) < 3:
        raise ValueError(f"Invalid color format: {color_str}")
    return f"rgba({rgba_values[0]}, {rgba_values[1]}, {rgba_values[2]}, {alpha})"
