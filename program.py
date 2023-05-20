import argparse
import json, yaml, xmltodict

arg_parser = argparse.ArgumentParser(
                    prog='Config Converter',
                    description='Converts config files in xml, json and yml(yaml)')

arg_parser.add_argument('pathFile1', type=argparse.FileType('r'))
arg_parser.add_argument('pathFile2', type=argparse.FileType('w'))
args = arg_parser.parse_args()

file_a = args.pathFile1
file_b = args.pathFile1


def validate(file, file_type):
    match file_type:
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


def json_write(object, object_type):
    match object_type:
        case "yml", "yaml":
            try:
                yaml_data = yaml.safe_load(object)
                json_data = json.dumps(yaml_data)
                return json_data
            except yaml.YAMLError as err:
                print("Error occured while parsing YAML:", err)
        case "xml":
            try:
                xml_data = xmltodict.parse(object)
                json_data = json.dumps(xml_data)
                return json_data
            except Exception as err:
                print("Error occured while parsing XML:", err)


file_a_type = (file_a.name.split(".", 1))[1]
file_b_type = (file_a.name.split(".", 1))[1]

if file_a_type == file_b_type:
    print(file_a.name, "is already in", file_a_type, "file format")
else:
    match file_a_type:
        case "json":
            json_object = json_load(file_a)



    match file_b_type:
        case "json":
            if file_a_type == "yaml" or file_a_type == "yml":
                json_data = json_write(yml_object, file_a_type)
                json_file = open(file_b.name, "w")
                json.dump(json_data, json_file)
                json_file.close()
            elif file_a_type == "xml":
                json_data = json_write(xml_object, file_a_type)
                json_file = open(file_b.name, "w")
                json.dump(json_data, json_file)
                json_file.close()

