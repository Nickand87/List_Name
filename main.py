import os
import variables
import time
import re

_surrogates = re.compile(r"[\uDC80-\uDCFF]")


def detect_decoding_errors_line(l, _s=_surrogates.finditer):
    """Return decoding errors in a line of text

    Works with text lines decoded with the surrogateescape
    error handler.

    Returns a list of (pos, byte) tuples

    """
    # DC80 - DCFF encode bad bytes 80-FF
    return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
            for m in _s(l)]


def process_multiple_sources(s_path, o_path):

    source_file_names = os.listdir(s_path)

    print(s_path)

    for file in range(len(source_file_names)):

        file_name = source_file_names[file]
        print(file_name)

        output_string, source_year = create_file_names(s_path + file_name)
        print(output_string)

        output_file_name = o_path + file_name

        with open(output_file_name, 'x') as txt_file:
            for line in output_string:
                txt_file.write("".join(line) + "\n")

        print(output_file_name)


def rename_set(s_path, o_path, r_path):

    timestamp = time.strftime("%Y%m%d - %H%M")

    output_string, source_year = create_file_names(s_path)
    print(output_string)

    output_file_name = o_path + source_year + "_" + timestamp + ".txt"

    with open(output_file_name, 'x') as txt_file:
        for line in output_string:
            txt_file.write("".join(line) + "\n")

    print(output_file_name)
    rename_files(r_path, o_path, output_file_name)


def create_file_names(s_path):

    compiled_lines = []
    output_string = []

    source = open(s_path, 'r', errors="surrogateescape")

    source_year = source.readline()
    source_year = variables.year[source_year[:-1]]

    count = 0
    while True:
        count += 1

        line = source.readline()

        if not line:
            break

        compiled_lines.append(line)

    source.close()

    with open(s_path, encoding="utf8", errors="surrogateescape") as f:
        for i, line in enumerate(f, 1):
            errors = detect_decoding_errors_line(line)
            if errors:
                print(f"Found errors on line {i}:")
                for (col, b) in errors:
                    print(f" {col + 1:2d}: {b[0]:02x}")

    match source_year:
        case "2006":

            i = 0
            while i < len(compiled_lines):
                if not compiled_lines[i].find("2006") == -1:
                    output_string.append(new_file_name(compiled_lines[i], "2006"))
                i += 1

        case "2023":

            i = 0
            while i < len(compiled_lines):
                if not compiled_lines[i].find("2023") == -1:
                    combined_lines = compiled_lines[i - 1] + " " + compiled_lines[i]
                    output_string.append(new_file_name(combined_lines, "2023"))
                i += 1

        case _:
            print("Hello")

    return output_string, source_year


def new_file_name(string, year):

    split_name = string.split()

    by_index = split_name.index('by')
    year_index = split_name.index(year)

    i = 0
    event_name = str()
    while i < by_index:

        if i == 0:
            event_name = str.capitalize(split_name[i])

        else:
            event_name = event_name + ' ' + str.capitalize(split_name[i])

        i += 1

    intermediate_creator_name = split_name[by_index + 1]

    if not (split_name[by_index + 2]) == (split_name[year_index - 2]):

        i = by_index + 2
        while i < (year_index - 2):

            intermediate_creator_name = intermediate_creator_name + "_" + split_name[i]

            i += 1

    creator_split = list(intermediate_creator_name)
    creator_name = str.capitalize(creator_split[0])

    i = 1
    while i < len(creator_split):

        if creator_split[i - 1] == "_":

            creator_name = creator_name + str.capitalize(creator_split[i])

        else:

            creator_name = creator_name + creator_split[i]

        i += 1

    date = split_name[year_index - 2] + '.' + variables.month[
        split_name[year_index - 1]] + '.' + split_name[year_index].partition('.')[0]

    new_name = date + " - " + creator_name + " - " + event_name

    return new_name


def quick_rename(r_path):

    old_file_names = os.listdir(r_path)
    print(old_file_names)

    i = 0
    for file in range(len(old_file_names)):

        i += 1
        if i < 10:
            number = "0" + str(i)
        else:
            number = str(i)

        os.rename(r_path + old_file_names[file], r_path + number + ".txt")


def rename_files(r_path, o_path, f_name):

    old_file_names = os.listdir(r_path)
    compiled_lines = []

    rename_source = open(f_name, 'r')

    count = 0
    while True:
        count += 1

        line = rename_source.readline()

        if not line:
            break

        compiled_lines.append(line[:-1])

    rename_source.close()

    print(old_file_names)
    print(compiled_lines)

    i = 0
    while i < len(compiled_lines):

        print(r_path + old_file_names[i] + " to " + r_path + compiled_lines[i] + ".txt")
        os.rename(r_path + old_file_names[i], r_path + compiled_lines[i] + ".txt")
        i += 1


def function_choice(match_choice, d_path, r_path, s_path, o_path):

    match match_choice:

        case 1:

            rename_set(s_path, o_path, r_path)

        case 2:

            quick_rename(r_path)

        case 3:

            process_multiple_sources(d_path + "Source//", o_path)


if __name__ == '__main__':

    directory_path = "C://Users//be05naa//PycharmProjects//List_Name//Names//"
    rename_folder_path = "C://Users//be05naa//PycharmProjects//List_Name//Names//Rename//"
    source_path = "C://Users//be05naa//PycharmProjects//List_Name//Names//Source.txt"
    output_path = "C://Users//be05naa//PycharmProjects//List_Name//Names//Output//"

    choice = 3

    function_choice(choice, directory_path, rename_folder_path, source_path, output_path)



