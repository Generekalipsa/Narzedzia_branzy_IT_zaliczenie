import argparse
import json, yaml, xmltodict

arg_parser = argparse.ArgumentParser(
                    prog='Config Converter',
                    description='Converts config files in xml, json and yml(yaml)')

arg_parser.add_argument('pathFile1', type=argparse.FileType('r'))
arg_parser.add_argument('pathFile2', type=argparse.FileType('w'))
args = arg_parser.parse_args()

file_a = args.pathFile1
file_b = args.pathFile2


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
        case "yml":
            try:
                yaml.safe_load(file)
                return True
            except yaml.YAMLError as err:
                print("Error occured while parsing YAML:", err)
                return False
            finally:
                file.close()
        case "xml":
            try:
                xml_data = file.read()
                xmltodict.parse(xml_data)
                return True
            except Exception as err:
                print("Error occured while parsing XML:", err)
                return False
            finally:
                file.close()


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
        case "yml" | "yaml":
            try:
                json_data = json.dumps(object, indent=2, separators=(", ", ": "))
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


def yml_load(yml_file):
    valid_yml = validate(yml_file, "yml")
    if valid_yml:
        file = open(yml_file.name, "r")
        yml_content = file.read()
        file.close()
        data = yaml.safe_load(yml_content)
        return data
    else:
        return False


def yml_write(object, object_type):
    match object_type:
        case "json":
            try:
                yml_data = yaml.dump(object)
                return yml_data
            except Exception as err:
                print("Error occured while parsing JSON:", err)
        case "xml":
            try:
                xml_data = xmltodict.parse(object)
                yml_data = yaml.dump(xml_data)
                return yml_data
            except Exception as err:
                print("Error occured while parsing XML:", err)


def xml_load(xml_file):
    valid_xml = validate(xml_file, "xml")
    if valid_xml:
        file = open(xml_file.name, "r")
        xml_content = file.read()
        file.close()
        data = xmltodict.parse(xml_content)
        return data
    else:
        return False


file_a_type = (file_a.name.split(".", 1))[1]
file_b_type = (file_b.name.split(".", 1))[1]

if file_a_type == file_b_type:
    print(file_a.name, "is already in", file_a_type, "file format")
else:
    match file_a_type:
        case "json":
            json_object = json_load(file_a)
        case "yml" | "yaml":
            yml_object = yml_load(file_a)
        case "xml":
            xml_object = xml_load(file_a)
        case _:
            json_object = None
            yml_object = None
            xml_object = None


    match file_b_type:
        case "json":
            if file_a_type == "yaml" or file_a_type == "yml":
                json_data = json_write(yml_object, file_a_type)
                json_file = open(file_b.name, "w")
                json_file.write(json_data)
                json_file.close()
            elif file_a_type == "xml":
                json_data = json_write(xml_object, file_a_type)
                json_file = open(file_b.name, "w")
                json_file.write(json_data)
                json_file.close()
        case "yaml" | "yml":
            if file_a_type == "json":
                yml_data = yml_write(json_object, file_a_type)
                yml_file = open(file_b.name, "w")
                yml_file.write(yml_data)
                yml_file.close()
            elif file_a_type == "xml":
                yml_data = yml_write(xml_object, file_a_type)
                yml_file = open(file_b.name, "w")
                yml_file.write(yml_data)
                yml_file.close()
