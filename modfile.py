from mendeleev import element

INPUT_FILE = "elements.txt"
OUTPUT_FILE = "elements_extra.txt"

def get_element_type(el):
    # try common string attributes first
    for attr in ("chemical_series", "series", "category"):
        val = getattr(el, attr, None)
        if isinstance(val, str) and val:
            return val

    # boolean flag checks (use getattr to be robust across mendeleev versions)
    checks = [
        ("is_alkali_metal", "alkali metal"),
        ("is_alkali", "alkali metal"),
        ("is_alkaline_earth_metal", "alkaline earth metal"),
        ("is_alkaline", "alkaline earth metal"),
        ("is_transition_metal", "transition metal"),
        ("is_post_transition_metal", "post-transition metal"),
        ("is_metalloid", "metalloid"),
        ("is_halogen", "halogen"),
        ("is_noble_gas", "noble_gas"),
        ("is_lanthanoid", "lanthanoid"),
        ("is_actinoid", "actinoid"),
        ("is_nonmetal", "nonmetal"),
        ("is_metal", "metal"),
    ]
    for attr, label in checks:
        if getattr(el, attr, False):
            return label

    # fallback to block if available
    block = getattr(el, "block", None)
    if block:
        return f"{block}-block"

    return "unknown"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = []

    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue

        symbol = parts[0]
        atomic_number = int(parts[1])
        name = parts[2]
        mass = parts[3]

        try:
            el = element(symbol)
        except Exception:
            period = group = "?"
            element_type = "unknown"
        else:
            period = getattr(el, "period", "?")
            group = getattr(el, "group_id", getattr(el, "group", "?"))
            element_type = get_element_type(el)

        # normalize element type: replace spaces with underscores
        element_type = (element_type or "unknown").replace(" ", "_")

        new_line = f"{symbol} {atomic_number} {name} {mass} {period} {group} {element_type}"
        output.append(new_line)


    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()