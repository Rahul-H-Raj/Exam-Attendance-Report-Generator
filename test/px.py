# Given pixel colors
pixel_colors = [
    (147, 181, 227),
    (170, 205, 239),
    (162, 196, 239),
    (132, 165, 210),
    (107, 145, 187),
    (107, 141, 187),
    (114, 148, 201),
    (116, 153, 205),
    (120, 154, 207),
    (77, 111, 157),
    (81, 117, 165),
    (86, 119, 169),
    (85, 118, 168),
    (80, 115, 155),
    (86, 120, 166),
    (102, 133, 178),
    (118, 147, 192)
]

# Initialize min and max values for each channel
min_b, min_g, min_r = 255, 255, 255
max_b, max_g, max_r = 0, 0, 0

# Iterate through pixel colors to find min and max values
for color in pixel_colors:
    b, g, r = color
    min_b = min(min_b, b)
    min_g = min(min_g, g)
    min_r = min(min_r, r)
    max_b = max(max_b, b)
    max_g = max(max_g, g)
    max_r = max(max_r, r)

# Print the range of BGR values
print(f"Blue Range: {min_b} - {max_b}")
print(f"Green Range: {min_g} - {max_g}")
print(f"Red Range: {min_r} - {max_r}")
