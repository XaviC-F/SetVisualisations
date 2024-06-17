import itertools

def powerset(fset):
    """Generate the powerset of a frozenset."""
    s = list(fset)
    return frozenset(frozenset(comb) for comb in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def frozenset_to_braces(fset, level=0):
    """Convert a frozenset to a string with curly braces and colors based on nesting level."""
    if not isinstance(fset, frozenset):
        return str(fset)

    elements = [frozenset_to_braces(element, level+1) for element in sorted(fset, key=lambda x: (len(frozenset_to_braces(x)), frozenset_to_braces(x)))]
    inner = ",".join(elements)

    braces = f"{{{inner}}}"
    return braces

def format_outer_set_with_outer_commas(fset):
    """Format the outermost frozenset with commas separating sets at the highest level, sorted by size and lexicographically."""
    elements = sorted(fset, key=lambda x: (len(frozenset_to_braces(x)), frozenset_to_braces(x)))  # Sort by type, size, and then lexicographically
    formatted_elements = []
    for i, element in enumerate(elements):
        inner_repr = frozenset_to_braces(element)
        if i < len(elements) - 1:
            inner_repr += ","  # Add a comma at the end except for the last element
        formatted_elements.append(inner_repr)
    inner_elements = "\n".join(formatted_elements)
    return f"{{{inner_elements}}}"

def GenerateVStage(fset = frozenset(), count = 0):
    if count == 0:
        return fset
    else:
        return GenerateVStage(powerset(fset), count - 1)

filename = "V5_only_nospaces.txt"
# Writing to file
with open((filename), "w") as file:
    print("Generating V5 with no spaces...")
    file.write(format_outer_set_with_outer_commas(GenerateVStage(frozenset(), 5)))
    print("Done.")