def extract_line_number(line):
    start = line.find(":") + 1
    return int(line[start:])


def extract_package(line):
    end = line.find(":")
    return str(line[:end])


def extract_clazz(package_string):
    parts = package_string.split('.')
    if parts:
        class_name = parts[-1]  # The last part is the class name
        return class_name
    else:
        return None 
