import os
import argparse
import json, yaml, xmltodict


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


def json_write(obj, obj_type):
    match obj_type:
        case "yml" | "yaml":
            try:
                json_data = json.dumps(obj, indent=2, separators=(", ", ": "))
                return json_data
            except yaml.YAMLError as err:
                print("Error occured while parsing YAML:", err)
        case "xml":
            try:
                xml_data = xmltodict.parse(obj)
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


def yml_write(obj, obj_type):
    match obj_type:
        case "json":
            try:
                yml_data = yaml.dump(obj)
                return yml_data
            except Exception as err:
                print("Error occured while parsing JSON:", err)
        case "xml":
            try:
                xml_data = xmltodict.parse(obj)
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


def xml_write(obj, obj_type):
    match obj_type:
        case "json":
            try:
                json_data = json.dumps(obj)
                json_data = "[" + json_data + "]"
                json_data = json.loads(json_data)
                xml_data = xmltodict.unparse({'root': json_data}, pretty=True)
                return xml_data
            except Exception as err:
                print("Error occured while parsing JSON:", err)
        case "yml" | "yaml":
            try:
                yml_data = yaml.safe_dump(obj)
                xml_data = xmltodict.unparse({'root': yml_data}, pretty=True)
                return xml_data
            except Exception as err:
                print("Error occured while parsing YAML:", err)


arg_parser = argparse.ArgumentParser(
                    prog='Config Converter',
                    description='Converts config files in xml, json and yml(yaml)')
arg_parser.add_argument('pathFile1')
arg_parser.add_argument('pathFile2')
args = arg_parser.parse_args()
file_a_path = args.pathFile1
file_b_path = args.pathFile2
with open(file_a_path, "r") as file_a:
    file_a_type = (file_a.name.split(".", 1))[1]

if os.path.exists(file_b_path):
    with open(file_b_path, "r") as file_b:
        file_b_type = (file_b.name.split(".", 1))[1]
        file_b_exists = True
else:
    with open(file_b_path, "w") as file_b:
        file_b_type = (file_b.name.split(".", 1))[1]
        file_b_exists = False

if file_b_exists:
    if (file_a_type == "yaml" or file_a_type == "yml") and (file_b_type == "yaml" or file_b_type == "yml"):
        print(file_a.name, "is already in yaml file format")
    elif file_a_type == file_b_type:
        print(file_a.name, "is already in", file_a_type, "file format")
else:
    file_a = open(file_a_path, "r")
    match file_a_type:
        case "json":
            json_obj = json_load(file_a)
        case "yml" | "yaml":
            yml_obj = yml_load(file_a)
        case "xml":
            xml_obj = xml_load(file_a)
        case _:
            json_obj = None
            yml_obj = None
            xml_obj = None
    file_a.close()

    file_b = open(file_b_path, "w")
    match file_b_type:
        case "json":
            if file_a_type == "yaml" or file_a_type == "yml":
                json_data = json_write(yml_obj, file_a_type)
                json_file = open(file_b.name, "w")
                json_file.write(json_data)
                json_file.close()
            elif file_a_type == "xml":
                json_data = json_write(xml_obj, file_a_type)
                json_file = open(file_b.name, "w")
                json_file.write(json_data)
                json_file.close()
        case "yaml" | "yml":
            if file_a_type == "json":
                yml_data = yml_write(json_obj, file_a_type)
                yml_file = open(file_b.name, "w")
                yml_file.write(yml_data)
                yml_file.close()
            elif file_a_type == "xml":
                yml_data = yml_write(xml_obj, file_a_type)
                yml_file = open(file_b.name, "w")
                yml_file.write(yml_data)
                yml_file.close()
        case "xml":
            if file_a_type == "json":
                xml_data = xml_write(json_obj, file_a_type)
                xml_file = open(file_b.name, "w")
                xml_file.write(xml_data)
                xml_file.close()
            elif file_a_type == "yml" or file_a_type == "yaml":
                xml_data = xml_write(yml_obj, file_a_type)
                xml_file = open(file_b.name, "w")
                xml_file.write(xml_data)
                xml_file.close()
    file_b.close()