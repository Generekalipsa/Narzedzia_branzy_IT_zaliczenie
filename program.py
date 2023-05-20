import argparse
import json

arg_parser = argparse.ArgumentParser(
                    prog='Config Converter',
                    description='Converts config files in xml, json and yml(yaml)')

arg_parser.add_argument('pathFile1', type=argparse.FileType('r'))
# arg_parser.add_argument('pathFile2', type=open)
args = arg_parser.parse_args()

file_a = args.pathFile1
# file_b = args.pathFile1


def validate(file, f_type):
    match f_type:
        case "json":
            try:
                json.load(file)
            except ValueError as err:
                print("JSON syntax is invalid")
                print("Details:", err)
                return False
            except FileNotFoundError:
                print("Can't find file:", file.name)
                return False
            finally:
                file.close()
            return True


def json_load(json_file):
    valid_json = validate(json_file, "json")
    if valid_json:
        file = open(json_file.name)
        data = json.load(file)
        file.close()
        return data
    else:
        return False


file_a_type = (file_a.name.split(".", 1))[1]
# file_b_type = (file_a.name.split(".", 1))[1]

match file_a_type:
    case "json":
        json_object = json_load(file_a)
