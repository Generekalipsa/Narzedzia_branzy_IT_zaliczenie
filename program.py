import argparse

arg_parser = argparse.ArgumentParser(
                    prog='Config Converter',
                    description='Converts config files in xml, json and yml(yaml)')

arg_parser.add_argument('pathFile1', type=open)
arg_parser.add_argument('pathFile2', type=open)
args = arg_parser.parse_args()

