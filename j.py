from PIL import Image, ImageDraw, ImageFont

# Define constants
cell_size = 100
width = 15 * cell_size
height = 5 * cell_size
square_size = cell_size // 4

# Create a new image with white background
image = Image.new("L", (width, height), 255)
draw = ImageDraw.Draw(image)

def get_max_level(fset):
    """Get the maximum nesting level of a frozenset."""
    if not isinstance(fset, frozenset) or not fset:
        return 0
    return max((get_max_level(subset) for subset in fset), default=0) + 1

def draw_set(fset, position, level):
    """Draw a frozenset at a specific position with a given level of nesting."""
    if not isinstance(fset, frozenset):
        return position

    x, y = position
    width = square_size * (2 ** level)
    height = square_size * (2 ** level)

    draw.rectangle([x, y, x + width, y + height], outline=0)
    
    sub_x = x + square_size
    for subset in sorted(fset, key=lambda x: get_max_level(x), reverse=True):
        sub_y = y + square_size
        sub_x, sub_y = draw_set(subset, (sub_x, sub_y), level - 1)
        sub_x += square_size * 2

    return x + width, y + height

# Example sets to draw
sets = [
    frozenset(),
    frozenset([frozenset()]),
    frozenset([frozenset(), frozenset([frozenset()])]),
    frozenset([frozenset([frozenset()]), frozenset([frozenset()]), frozenset([frozenset()])]),
    frozenset([
        frozenset([frozenset([frozenset()])]), 
        frozenset([frozenset([frozenset()]), frozenset([frozenset()])]),
        frozenset([frozenset([frozenset()]), frozenset([frozenset()]), frozenset([frozenset()])])
    ]),
]

# Draw each set with increasing complexity
y_offset = 0
for level, fset in enumerate(sets):
    draw.text((10, y_offset + 10), f"V_{level}", fill=0)
    draw_set(fset, (50, y_offset), get_max_level(fset))
    y_offset += cell_size

# Save or show the image
image.show()
