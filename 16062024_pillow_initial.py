from PIL import Image, ImageDraw
import itertools

def draw_set_as_squares(draw, x, y, size, fset, level, max_level, colors):
    if not isinstance(fset, frozenset) or len(fset) == 0:
        color = colors[level % len(colors)]
        draw.rectangle([x, y, (x + size)*level, (y + size)*level], outline=color, width=1)
        return

    elements = sorted(fset, key=lambda x: (len(str(x)), str(x)))
    n = len(elements)
    sub_size = size / (n + 1)  # Adjust size based on the number of elements

    for i, element in enumerate(elements):
        sub_x = x + (i + 1) * sub_size
        sub_y = y + sub_size
        draw_set_as_squares(draw, sub_x, sub_y, sub_size, element, level + 1, max_level, colors)

    color = colors[level % len(colors)]
    draw.rectangle([x, y, x + size, y + size], outline=color, width=1)

def create_von_neumann_image(levels, image_size):
    max_level = levels - 1
    colors = ["black"] * (max_level + 1)  # Use different colors for each level if needed
    image_height = image_size // levels
    image = Image.new("RGB", (image_size, image_height * levels), "white")
    draw = ImageDraw.Draw(image)

    for level in range(levels):
        fset = GenerateVStage(frozenset(), level)
        size = 50 * (level + 1)  # Fixed size for the empty set and increasing size for larger sets
        x = 10
        y = level * 100 + 10
        draw_set_as_squares(draw, x, y, size, fset, 0, max_level, colors)

    image.show()

def GenerateVStage(fset=frozenset(), count=0):
    if count == 0:
        return fset
    else:
        return GenerateVStage(powerset(fset), count - 1)

def powerset(fset):
    """Generate the powerset of a frozenset."""
    s = list(fset)
    return frozenset(frozenset(comb) for comb in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

# Create and display the image
create_von_neumann_image(levels=5, image_size=800)