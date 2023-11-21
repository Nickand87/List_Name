import os
import variables
import time
import re

log = []

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


def process_multiple_sources(u_path, p_path):
    # Takes all unprocessed source files in the "source" folder, processes, then outputs to the "output" folder with
    # the same file names.

    source_file_names = os.listdir(u_path)

    print(u_path)

    for file in range(len(source_file_names)):

        file_name = source_file_names[file]
        print(file_name)

        output_string, source_year = create_file_names(u_path + file_name)
        print(output_string)

        output_file_name = p_path + file_name

        with open(output_file_name, 'x') as txt_file:
            for line in output_string:
                txt_file.write("".join(line) + "\n")

        print(output_file_name)


def rename_set(s_path, p_path, r_path):  # Inputs unprocessed source file to generate a processed source file.

    timestamp = time.strftime("%Y%m%d - %H%M")

    output_string, source_year = create_file_names(s_path)
    print(output_string)

    output_file_name = p_path + source_year + "_" + timestamp + ".txt"

    with open(output_file_name, 'x') as txt_file:
        for line in output_string:
            txt_file.write("".join(line) + "\n")

    print(output_file_name)
    rename_files(r_path, output_file_name)


def create_file_names(u_path):
    # Processes source file, saves processed file as .txt output, then uses this to rename files in output folder
    # until the list ends

    compiled_lines = []
    output_string = []

    source = open(u_path, 'r', errors="surrogateescape")

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

    with open(u_path, encoding="utf8", errors="surrogateescape") as f:
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
    # Takes input string from source files and brakes it apart and reforms it to the proper naming convention for files
    # then returns the processed file name.

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
    # Renames files residing in the "rename" folder to 01.txt...XX.txt
    #

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


def read_source_file(s_file):

    compiled_lines = []

    rename_source = open(s_file, 'r')

    count = 0
    while True:
        count += 1

        line = rename_source.readline()

        if not line:
            break

        compiled_lines.append(line[:-1])

    rename_source.close()

    return compiled_lines


def rename_files(r_path, s_file):
    # Takes source file and renames all files in r_path to all file names contained in name array.
    #

    old_file_names = os.listdir(r_path)
    compiled_lines = read_source_file(s_file)

    log.append("\n*******Renaming Files in Folder*******\n" + r_path + "\n")
    i = 0
    while i < len(compiled_lines):

        log.append(old_file_names[i] + "   to   " + compiled_lines[i] + ".txt")
        #os.rename(r_path + old_file_names[i], r_path + compiled_lines[i] + ".txt")
        i += 1


def iterate_rename(s_path, t_path):

    source_dir = os.listdir(s_path)
    true_dir = os.listdir(t_path)

    print(source_dir)
    print(true_dir)

    for file in range(len(source_dir)):

        s_file = source_dir[file]
        s_file_name = s_file
        s_file = s_file[1:-4]

        if s_file not in true_dir:
            print(s_file + " Folder Not Found")

        else:

            compiled_lines_len = len(read_source_file(s_path + s_file_name))
            p_folder_len = len(os.listdir(t_path + "/" + s_file + "/"))

            if not compiled_lines_len == p_folder_len:

                log.append("\n******* Mismatch of number of files and number of files to be renamed *******")
                log.append("Folder Name     = " + s_file)
                log.append("Number of Names = " + str(compiled_lines_len))
                log.append("Number of Files = " + str(p_folder_len))

            else:
                print(s_file)
                p_folder = t_path + "/" + s_file + "/"
                print(p_folder)
                print(s_path + s_file_name)

                rename_files(p_folder, s_path + s_file_name)


def function_choice(match_choice, r_path, s_path, t_path, u_path, p_path, s_file):

    match match_choice:

        # Processes source file, saves processed file as .txt output, then uses this to rename files in output folder
        # until the list ends
        case 1:

            rename_set(s_file, p_path, r_path)

        # Renames files residing in the "rename" folder to 01.txt...XX.txt
        #
        case 2:

            quick_rename(r_path)

        # Takes all unprocessed source files in the "source" folder, processes, then outputs to the "output" folder with
        # the same file names to create processed source files.
        case 3:

            process_multiple_sources(u_path, p_path)

        case 4:

            iterate_rename(s_path, t_path)


def generate_log(l_path):

    timestamp = time.strftime("%Y%m%d - %H%M")

    output_file_name = l_path + timestamp + ".txt"

    with open(output_file_name, 'x') as txt_file:
        for line in log:
            txt_file.write("".join(line) + "\n")


if __name__ == '__main__':

    home_directory = os.getcwd()

    rename_folder_path = home_directory + "/Names/Rename/"
    source_path = home_directory + "/Names/Source/"
    true_path = home_directory + "/Names/True/"
    unprocessed_path = home_directory + "/Names/Unprocessed/"
    processed_path = home_directory + "/Names/Processed/"
    log_path = home_directory + "/Names/Log/"

    source_file = home_directory + "/Names/Source.txt"

    choice = 4

    function_choice(choice, rename_folder_path, source_path, true_path, unprocessed_path, processed_path, source_file)
    generate_log(log_path)


