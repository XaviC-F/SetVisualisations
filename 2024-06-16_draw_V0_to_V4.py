from PIL import Image, ImageDraw
import itertools

side_length = 100
width = 22*side_length
height = 5*side_length
text_offset = side_length//5
square_offset = side_length // 5
font_size = side_length//10

image = Image.new("RGB", (width, height),(255,255,255))
draw = ImageDraw.Draw(image)

'''
Represent an image as a list of rectangles
    i.e. a list of coordinate pairs, where the first coordinate is the top-left corner, and the second the bottom-right corner

I need:
- A method to give the dimensions of a set's rectangle based on its elements
- A method to arrange a set's elements within itself. This can be done without knowing the elements' exact elements
    - Should use internal coordinates relative to set's top-left corner to place elements

Both of these take a set and a value for the gap between two rectangles
'''

def powerset(fset):
    """Generate the powerset of a frozenset."""
    s = list(fset)
    return frozenset(frozenset(comb) for comb in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def GenerateVStage(count = 0, fset = frozenset()):
    if count == 0:
        return fset
    else:
        return GenerateVStage(count - 1, powerset(fset))

def get_max_level(fset):
    """Get the maximum nesting level of a frozenset."""
    if not isinstance(fset, frozenset):
        return 0

    max_level = 0
    stack = [(fset, int(0))]  # (current_set, current_level)

    while stack:
        current_set, current_level = stack.pop()
        max_level = max(max_level, current_level)
        for element in current_set:
            if isinstance(element, frozenset):
                stack.append((element, current_level + 1))

    return max_level

def find_width_of_set(fset):
    if not isinstance(fset, frozenset) or len(fset) == 0:
        return 1
    width = 0
    for element in fset:
        width += find_width_of_set(element)
    return width + 1  # Add 1 for the current level

def num_empty_in_set(fset):
    if not isinstance(fset, frozenset) or len(fset) == 0:
        return 1
    count = 0
    for element in fset:
        count += num_empty_in_set(element)
    print("Num empty in set:", count)
    return count

def set_dimensions(set, gap):
    if len(set) == 0:
        return (empty_set_sidelength, empty_set_sidelength)
    else:
        height = gap * (2*get_max_level(set)) + empty_set_sidelength # for the centre of the empty set
        width = gap * (2*find_width_of_set(set)-num_empty_in_set(set)-1) + num_empty_in_set(set)*empty_set_sidelength #+2 for the gap between the outer set and its elements
        print(f"Set: {set}; Width: {width}; Height: {height}")
        return (width, height)

def arrange_elements(set, gap):
    if len(set) == 0:
        return [(0,0)]
    else:
        offsets = []
        (width, height) = set_dimensions(set, gap)
        x_offset_sum = gap
        for element in sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x))):
            # Loop gives me the elements of 'set' in order of nesting depth, then length
            (element_width,element_height) = set_dimensions(element, gap)
            print((element_width,element_height))
            x_offset = x_offset_sum
            y_offset = (height - element_height)//2
            x_offset_sum += gap + element_width
            offsets.append((x_offset,y_offset))
        return offsets     

def draw_sets_no_wrapping(set, position, gap, radius, width):
    top_left = position
    dimensions = set_dimensions(set, gap)
    bottom_right = (top_left[0] + dimensions[0], top_left[1] + dimensions[1])
    
    draw.rounded_rectangle(xy=(top_left,bottom_right), radius=radius, width=width, outline=0)

    offsets = arrange_elements(set, gap)
    for i, element in enumerate(sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x)))):
        draw_sets_no_wrapping(element, (position[0] + offsets[i][0],position[1] + offsets[i][1]), gap, radius, width)

empty_set_sidelength = 20
gap = (empty_set_sidelength)*2//5
radius = 2




for i in range(5):
    draw.text((10,5*i*empty_set_sidelength+2),f"L{i}",font_size=25,fill=(0,0,0))
    draw_sets_no_wrapping(GenerateVStage(i), (50,5*i*empty_set_sidelength+5), gap, radius, 2)

image.show()