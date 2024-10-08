from PIL import Image, ImageDraw
import itertools

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
    return count

def set_dimensions(set, gap, empty_set_sidelength):
    if len(set) == 0:
        return (empty_set_sidelength, empty_set_sidelength)
    else:
        height = gap * (2*get_max_level(set)) + empty_set_sidelength # for the centre of the empty set and top and bottom gaps
        width = gap * (2*find_width_of_set(set)-num_empty_in_set(set)-1) + num_empty_in_set(set)*empty_set_sidelength #+2 for the gap between the outer set and its elements
        return (width, height)

def set_dimensions_width_fixed(set, gap, empty_set_sidelength, rectangle_width):
    if len(set) == 0:
        return (empty_set_sidelength, empty_set_sidelength)
    else:
        length_sorted_set = sorted(set, key=lambda x: (-find_width_of_set(x)))
        (max_length,_) = set_dimensions(length_sorted_set[0],gap,empty_set_sidelength)
        
        max_total_elements_width = len(set) * (max_length + gap) + gap
        num_rows = max_total_elements_width // rectangle_width + 1
        height_out = num_rows * (gap * (2*get_max_level(set)) + empty_set_sidelength - gap) + gap
        return (rectangle_width, height_out)

def arrange_elements(set, gap, empty_set_sidelength):
    if len(set) == 0:
        return [(0,0)]
    else:
        offsets = []
        (_, height) = set_dimensions(set, gap, empty_set_sidelength)
        x_offset_sum = gap
        for element in sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x))):
            # Loop gives me the elements of 'set' in order of nesting depth, then length
            (element_width,element_height) = set_dimensions(element, gap, empty_set_sidelength)
            x_offset = x_offset_sum
            y_offset = (height - element_height)//2
            x_offset_sum += gap + element_width
            offsets.append((x_offset,y_offset))
        return offsets     

def arrange_elements_with_horizontal_wrap(set, gap, empty_set_sidelength, rectangle_width):
    if len(set) == 0:
        return [(0,0)]
    else:
        offsets = []
        (_, flat_height) = set_dimensions(set, gap, empty_set_sidelength)
        x_offset_sum = gap
        y_offset_sum = 0
        for element in sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x))):
            # Loop gives me the elements of 'set' in order of nesting depth, then length
            (element_width,element_height) = set_dimensions(element, gap, empty_set_sidelength)
            
            if x_offset_sum + element_width >= rectangle_width - gap:
                x_offset_sum = gap
                x_offset = x_offset_sum
                y_offset_sum += flat_height - gap
                y_offset = y_offset_sum + (flat_height - element_height)//2
                x_offset_sum += gap + element_width
            else:
                x_offset = x_offset_sum
                y_offset = y_offset_sum + (flat_height - element_height)//2
                x_offset_sum += gap + element_width
            offsets.append((x_offset,y_offset))
        return offsets

def draw_sets_no_wrapping(set, position, gap, empty_set_sidelength, radius, stroke_width):
    top_left = position
    dimensions = set_dimensions(set, gap, empty_set_sidelength)
    bottom_right = (top_left[0] + dimensions[0], top_left[1] + dimensions[1])
    
    draw.rounded_rectangle(xy=(top_left,bottom_right), radius=radius, width=stroke_width, outline=0)

    offsets = arrange_elements(set, gap, empty_set_sidelength)
    for i, element in enumerate(sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x)))):
        draw_sets_no_wrapping(element, (position[0] + offsets[i][0],position[1] + offsets[i][1]),
                              gap, empty_set_sidelength, radius, stroke_width)

def draw_sets_horizontal_wrapping(set, position, gap, empty_set_sidelength, rectangle_width, radius, stroke_width):
    offsets = arrange_elements_with_horizontal_wrap(set, gap, empty_set_sidelength,rectangle_width)
    right_extreme = 0
    bottom_extreme = 0
    for i, element in enumerate(sorted(set, key=lambda x: (get_max_level(x), find_width_of_set(x)))):
        draw_sets_no_wrapping(element, (position[0] + offsets[i][0],position[1] + offsets[i][1]),
                                        gap, empty_set_sidelength, radius, stroke_width)
        
        dimensions = set_dimensions(element, gap, empty_set_sidelength)
        bottom_right = (position[0] + offsets[i][0] + dimensions[0], position[1] + offsets[i][1]+ dimensions[1])
        if bottom_right[0] > right_extreme:
            right_extreme = bottom_right[0]
        if bottom_right[1] > bottom_extreme:
            bottom_extreme = bottom_right[1]
        
    bottom_right = (right_extreme + gap, bottom_extreme + gap)
    # Adjust the line below so it just wraps the elements inside
    draw.rounded_rectangle(xy=(position,bottom_right), radius=radius, width=stroke_width, outline=0)
    print(bottom_right)

def draw_poster(gap, empty_set_sidelength, radius, stroke_width):
    


side_length = 100
width = 39998
height = 39104
text_offset = side_length//5
square_offset = side_length // 5
font_size = side_length//10




    



#V5 = GenerateVStage(5)

#V5 = sorted(V5, key=lambda x: (get_max_level(x), find_width_of_set(x)))

empty_set_sidelength = 50
gap = (empty_set_sidelength)*2//5
radius = 6


last_set = frozenset({frozenset({frozenset({frozenset({frozenset()})})}), frozenset({frozenset(), frozenset({frozenset()}), frozenset({frozenset(), frozenset({frozenset()})})}), frozenset({frozenset({frozenset(), frozenset({frozenset()})})}), frozenset({frozenset({frozenset()}), frozenset({frozenset({frozenset()})})}), frozenset({frozenset(), frozenset({frozenset()}), frozenset({frozenset(), frozenset({frozenset()})}), frozenset({frozenset({frozenset()})})}), frozenset({frozenset({frozenset(), frozenset({frozenset()})}), frozenset({frozenset({frozenset()})})}), frozenset({frozenset({frozenset()}), frozenset({frozenset(), frozenset({frozenset()})})}), frozenset({frozenset()}), frozenset({frozenset({frozenset()}), frozenset({frozenset(), frozenset({frozenset()})}), frozenset({frozenset({frozenset()})})}), frozenset({frozenset({frozenset()})}), frozenset({frozenset(), frozenset({frozenset(), frozenset({frozenset()})}), frozenset({frozenset({frozenset()})})}), frozenset(), frozenset({frozenset(), frozenset({frozenset()}), frozenset({frozenset({frozenset()})})}), frozenset({frozenset(), frozenset({frozenset({frozenset()})})}), frozenset({frozenset(), frozenset({frozenset()})}), frozenset({frozenset(), frozenset({frozenset(), frozenset({frozenset()})})})})
print(f"last_set: {last_set}")


width = set_dimensions(last_set, gap, empty_set_sidelength)[0]
height = set_dimensions(last_set, gap, empty_set_sidelength)[1]

image = Image.new("1", (width, height), 1)
draw = ImageDraw.Draw(image)

draw_sets_no_wrapping(last_set, (0,0), gap, empty_set_sidelength, radius, 2)
image.show()