from mendeleev import element

INPUT_FILE = "elements.txt"
OUTPUT_FILE = "elements_extra.txt"

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

        el = element(symbol)

        period = el.period
        group = el.group_id   # mendeleev uses group_id

        new_line = f"{symbol} {atomic_number} {name} {mass} {period} {group}"
        output.append(new_line)

        element()

    #with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        #f.write("\n".join(output))

    #print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()