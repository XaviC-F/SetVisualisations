import itertools

def powerset(fset):
    """Generate the powerset of a frozenset."""
    s = list(fset)
    return frozenset(frozenset(comb) for comb in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

INNERMOST_COLOR = 36  # Cyan for innermost empty sets

def frozenset_to_braces(fset, level=0, max_level=None):
    """Convert a frozenset to a string with curly braces and colors based on nesting level."""
    if not isinstance(fset, frozenset):
        return str(fset)

    # Determine max level if not set
    if max_level is None:
        max_level = get_max_level(fset)

    elements = [frozenset_to_braces(element, level+1, max_level) for element in sorted(fset, key=lambda x: (len(frozenset_to_braces(x)), frozenset_to_braces(x)))]
    inner = ", ".join(elements)

    braces = f"{{{" "*(max_level-level)}{inner}{" "*(max_level-level)}}}"
    return braces

def get_max_level(fset):
    """Get the maximum nesting level of a frozenset."""
    if not isinstance(fset, frozenset) or not fset:
        return 0

    max_level = 0
    stack = [(fset, int(1))]  # (current_set, current_level)

    while stack:
        current_set, current_level = stack.pop()
        max_level = max(max_level, current_level)
        for element in current_set:
            if isinstance(element, frozenset):
                stack.append((element, current_level + 1))

    return max_level

def format_outer_set_with_outer_commas(fset):
    """Format the outermost frozenset with commas separating sets at the highest level, sorted by size and lexicographically."""
    elements = sorted(fset, key=lambda x: (len(frozenset_to_braces(x)), frozenset_to_braces(x)))  # Sort by type, size, and then lexicographically
    formatted_elements = []
    for i, element in enumerate(elements):
        inner_repr = frozenset_to_braces(element)
        if i < len(elements) - 1:
            inner_repr += ","  # Add a comma at the end except for the last element
        formatted_elements.append(inner_repr)
    inner_elements = "\n\n  ".join(formatted_elements)
    return f"{{\n  {inner_elements}\n}}"

def GenerateVStage(fset = frozenset(), count = 0):
    if count == 0:
        return fset
    else:
        return GenerateVStage(powerset(fset), count - 1)

print(f"\033[0mV0: {frozenset_to_braces(frozenset())}\033[0m")

print(f"\033[{INNERMOST_COLOR}m{{}}\033[0m")

# for i in range(1, 6):
    # print(f"\nV{i}\n" + format_outer_set_with_outer_commas(GenerateVStage(frozenset(), i)))

filename = "V5_only_nospaces.txt"
# Writing to file
with open((filename), "w") as file:
    for i in range(1, 6):
        print(i)
        file.write(f"\nV{i}\n" + format_outer_set_with_outer_commas(GenerateVStage(frozenset(), i)))