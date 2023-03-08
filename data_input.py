def load_data_from_file(path: str = "cpm/test_data/simple_test.txt", sep: str=";"):
    data = dict()

    with open(path, "r") as f:
        current_header: str = ""
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if line.startswith("STHUNIQUE"):
                    current_header = line
                    data[current_header] = []
                else:
                    data[current_header].append([elem.strip() for elem in line.split(sep)])
    return data