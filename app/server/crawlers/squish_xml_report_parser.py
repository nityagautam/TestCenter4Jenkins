#===================================================================
# @author:  nityanarayan44@live.com
# @written: 09 December 2021
# @desc:    Squish XML report crawlers (gives out the dict/json data)
#===================================================================
# use:> python3 <script_name.py> squish_xml_file.xml
# < returns the dict/json data

from collections import defaultdict
import xml.etree.ElementTree as ET
import json, re

# Squish XML Parser Class
# --------------------------
class SquishXMLParser:
    # Attributes
    xml_file = None
    output = None

    # Constructor
    def __init__(self, file) -> None:
        if file and 'xml' in file.split('.')[-1]:
            self.xml_file = file
            print('>>> XML file extension validation; Passed !')
        else:
            print(f'\n>>> Looks like, Invalid file passed;\n FILE:: {file}  \n Please use: python3 <script>.py <your_squish_xml_file>.xml \n')

    def __read_xml(self):
        with open(self.xml_file, mode='r', encoding='utf-8') as fp:
            return fp.read()
        
    def handleNamespaceInTag(self, tag) -> str:
        pattern = re.compile(r'(\{[a-zA-Z\.\/:\d]*\}[^a-zA-Z]*)')
        if pattern.search(tag):
            result = re.sub(r'(\{[a-zA-Z\.\/:\d]*\}[^a-zA-Z]*)', '', str(tag))
            return result
        else:
            return tag

    def xml2dict(self, t) -> dict:
        """
            @param: t as root node from parsed xml
            @return dict
        """
        d = {self.handleNamespaceInTag(t.tag): {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.xml2dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            #d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
            d = {self.handleNamespaceInTag(t.tag): {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            #d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
            d[self.handleNamespaceInTag(t.tag)].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    #d[t.tag]['#text'] = text.replace("\\", "/")
                    d[self.handleNamespaceInTag(t.tag)]['#text'] = text.replace("\\", "/")
            else:
                #d[t.tag] = text.replace("\\", "/")
                d[self.handleNamespaceInTag(t.tag)] = text.replace("\\", "/")
        return d

    # Initializer
    def initialize(self):
        # Parse now
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # Start the conversion and return the dict
        return self.xml2dict(root)


# ---------------------------------
# Class for html file generator
# ---------------------------------
class HTMLGenerator:
    def __init__(self, dict_data) -> None:
        self.data = dict_data
        self.html_output = ''

    def generate(self, output_file_name):
        # iterate over json/dict object
        # for k, v in self.data.items():
        #     print(f'{k} >>> {v} \n\n')
        
        # DEBUG: HTML DATA GETTING READY
        #print(f'START TIME:: {0 if type(self.data["SquishReport"]["test"]) is dict else self.data["SquishReport"]["test"]["prolog"]["@time"]}')
        #print(f'END TIME:: {self.data["SquishReport"]["test"]["epilog"]["@time"]}')
        #print(f'Total Suites:: {1 if type(self.data["SquishReport"]["test"]) is dict else len(self.data["SquishReport"]["test"])}')
        
        # For testcase count
        testcases = 0
        for key, value in self.data.items():
            print(type(value))
            if type(value["test"]) is dict:
                testcases += len(value["test"]["test"]) if type(value["test"]) is dict else [1 if type(v["test"]) is dict else len(v["test"]) for k,v in value["test"].items()]
            else:
                print(value["test"])
                testcases += len([v["test"] for v in value["test"]])
        print(f'Total testcases:: {testcases}')

        # For suite names
        # testsuites = []
        # for key, value in self.data.items():
        #     testcases += value["test"]["prolog"]["name"] if type(value["test"]) is dict else [names["prolog"]["name"] for k, names in value["test"].items()]
        # print(f'Total testcases:: {testsuites}')

        

        # Return the text
        return self.html_output


# --------------------------
# For CLI Execution
# --------------------------
if __name__ == "__main__":
    #initiate the squish xml file crawlers
    #dict_output = SquishXMLParser('C:\\Users\\mishra.ashutosh\\Downloads\\TC1\\2020-04-07T16-40-13+0530\\results.xml').initialize()
    #print(">>> For XML file, dict/json has been generated: \n\n", json.dumps(dict_output) )
    #html_output = HTMLGenerator(dict_data=dict_output).generate(output_file_name='index.html')
    #print(">>> Generated HTML: \n\n", html_output )
    dict_output = SquishXMLParser('./results.xml')
    html_output = HTMLGenerator(dict_data=dict_output).generate(output_file_name='index.html')
    