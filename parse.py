import json
import math
import os
from shutil import copyfile
from onshape_client.oas import BTFeatureScriptEvalCall2377
from onshape_client.onshape_url import OnshapeElement
from onshape_client.utility import parse_quantity
from onshape_client import Client
from pint import UnitRegistry

ureg =  UnitRegistry()

msg_str = "message"
val_str = "value"
key_str = "key"

# create global roles using this: https://stackoverflow.com/questions/9698702/how-do-i-create-a-global-role-roles-in-sphinx
# If this grows too much, we'll need to add a global rst as described in the post above.
def parse_quantity(q):
    """Parse an Onshape units definition
    Args:
        q: an Onshape units definition... for instance:
            {
              'typeTag': '',
              'unitToPower': [
                {
                  'key': 'METER',
                  'value': 1
                }
              ],
              'value': 0.0868175271040671
            }
    Returns:
        a string that can be converted to any other unit engine.
    >>> from onshape_client.utility import parse_quantity
    >>> d = {'value': 0.1414213562373095, 'unitToPower': [{'value': 1, 'key': 'METER'}], 'typeTag': ''}
    >>> parse_quantity(d)
    '0.1414213562373095*meter'
    >>> d = {'value': 0.1414213562373095, 'unitToPower': [{'value': 3, 'key': 'MILLIMETER'}], 'typeTag': ''}
    >>> parse_quantity(d)
    '0.1414213562373095*millimeter**3'
    """
    units_s = q[val_str]
    for u in q["unitToPower"]:
        units_s = units_s * ureg(u[key_str].lower()) ** u[val_str]
        try:
            log = math.floor(math.log10(units_s.magnitude))
        except:
            log = 0
        if u[key_str] == 'METER' and u[val_str] == 1:
            if log >= 3:
                units_s = units_s.to(ureg.kilometer)
            elif log >= -2 and log <= -1:
                units_s = units_s.to(ureg.centimeter)
            elif log <= -3:
                units_s = units_s.to(ureg.millimeter)
        elif u[key_str] == 'METER' and u[val_str] == 2:
            if log >= 6:
                units_s = units_s.to(ureg.kilometer**2)
            elif log >= -4 and log <= -1:
                units_s = units_s.to(ureg.centimeter**2)
            elif log <= -5:
                units_s = units_s.to(ureg.millimeter**2)
        elif u[key_str] == 'METER' and u[val_str] == 3:
            log += 3
            if log >= 3:
                units_s = units_s.to(ureg.kiloliter)
            elif log <= -1:
                units_s = units_s.to(ureg.milliliter)
            else:
                units_s = units_s.to(ureg.liter)
    return f'{round(units_s, 2):~}'

def is_fs_type(candidate, type_name):
    """Checks if the a JSON entry is of a specific FeatureScript type.
    Args:
        candidate: decoded JSON object to check the type of
        type_name: string of the FeatureScript Type to check for
    Returns:
        result: True if candidate is of type_name, False otherwise
    >>> import json
    >>> test_json = json.loads('{"type": 2077, "typeName": "BTFSValueMapEntry", "message": {}}')
    >>> is_fs_type(test_json, "BTFSValueMapEntry")
    True
    >>> is_fs_type(test_json, "BTFSValueNumber")
    False
    """
    result = False
    try:
        if isinstance(type_name, str):
            result = type_name == candidate["typeName"]
        elif isinstance(type_name, list):
            result = any(
                [type_name_one == candidate["typeName"] for type_name_one in type_name]
            )
    except Exception:
        result = False
    return result

def copy_to_docs(file_path, base="doc_files"):
    """Copies a file to the current working directory. The new file's path
    will be identical to the old file's path relative to the base path.
    Args:
        file_path: path to the file to be copied
        base: base path to use in creating relative file path of the copy
    Returns:
        none
    """
    file = os.path.basename(file_path)
    dir = os.path.dirname(file_path)
    while os.path.basename(dir) != base:
        file = os.path.basename(dir) + "/" + file
        dir = os.path.dirname(dir)
    try:
        copyfile(file_path, file)
    except IOError as io_err:
        os.makedirs(os.path.dirname(file))
        copyfile(file_path, file)

def parse_variables_from_list(unparsed):
    """Helper function for parse_variables_from_map parses values from a list
    instead of a map.
    Args:
        unparsed: portion of deserialized JSON which has yet to be parsed
    Returns:
        measurement_list: list of parsed values
    """
    measurement_list = []

    for to_parse in unparsed:
        if is_fs_type(to_parse, "BTFSValueWithUnits"):
            measurement_list.append(parse_quantity(to_parse[msg_str]))
        elif is_fs_type(to_parse, ["BTFSValueNumber", "BTFSValueString"]):
            measurement_list.append(to_parse[msg_str][val_str])

    return measurement_list

def merge_index_sections(new_section, old_section):
    """Helper function for merge_indexes which loops through each section and
    combines them.
    Args:
        new_section: section which is being added to if line from old_section is absent
        old_section: section which is pulled from
    Returns:
        none
    >>> new_section = ['test_line', 'test_line2']
    >>> old_section = ['test_line', 'test_line3']
    >>> merge_index_sections(new_section, old_section)
    ['test_line', 'test_line2', 'test_line3']
    """
    for line in old_section:
        if line in new_section:
            continue
        else:
            new_section.append(line)

    return new_section

def find_index_section_limits(filename, section_start=".. toctree::\n",
                              section_end="\n"):
    """Helper function for merge_indexes which loops through the
    file and marks the beginning and end of each section.
    Args:
        filename: path to file to be modified
        section_start: string which marks the start of each section
            Default: '.. toctree::\n'
        section_end: string which marks the end of each section
            Default: '\n'
    Returns:
        lines: list of strings of each line in the file
        section_limits: list of the form [[start1, end1], [start2, end2]]
            which marks the separation between sections
    >>> index = '../../../../test_files/index_lfom.rst'
    >>> _, limits = find_index_section_limits(index)
    >>> limits
    [[18, 26], [27, 32]]
    >>> index = '../../../../test_files/index_lfom_ET.rst'
    >>> _, limits = find_index_section_limits(index)
    >>> limits
    [[18, 26], [27, 33]]
    """
    section_limits = []
    start = 0
    first_newline = True
    index_file = open(filename, "r+")
    lines = index_file.readlines()
    index_file.close()

    for i, line in enumerate(lines):
        if line == section_start:
            start = i
        if line == section_end and start != 0:
            if first_newline:
                first_newline = False
            else:
                end = i
                section_limits.append([start, end])
                start = end = 0
                first_newline = True

    return lines, section_limits

def merge_indexes(new_index, old_index):
    """Merges two indexes by comparing the two files, index.rst and new_index.rst
    section by section and adding pieces which exist in index.rst but are missing
    from new_index.rst . At the end, the one which was added to is maintained as
    index.rst and new_index.rst is deleted.
    Args:
        new_index: path to index file which is being merged from
        old_index: path to existing index file which is being merged into
    Returns:
        none
    >>> old_index = '../../../../test_files/index_lfom.rst'
    >>> new_index = '../../../../test_files/new_index_ET.rst'
    >>> merge_indexes(new_index, old_index)
    >>> index_file = open(old_index, "r+")
    >>> lines = index_file.readlines()
    >>> test_file = open('../../../../test_files/index_lfom_ET.rst')
    >>> test_lines = test_file.readlines()
    >>> test_lines == lines
    True
    """
    old_lines, old_section_limits = find_index_section_limits(old_index)
    new_lines, new_section_limits = find_index_section_limits(new_index)

    for start, end in old_section_limits:
        included = False
        caption = old_lines[start+1]
        for new_start, new_end in new_section_limits:
            if new_lines[new_start+1] == caption:
                new_section = merge_index_sections(new_lines[new_start:new_end], old_lines[start:end])
                del new_lines[new_start:new_end]
                i = new_start
                for line in new_section:
                    new_lines.insert(i, line)
                    i += 1
                included = True
        if not included:
            i = new_end
            new_lines.insert(i, "\n")
            for line in old_lines[start:end]:
                i += 1
                new_lines.insert(i, line)

    old_index_file = open(old_index, "w+")
    old_index_file.write("".join(new_lines))
    old_index_file.close()

    os.remove(new_index)

def find_treatment_section_limits(filename, section_delimiter=".. _heading"):
    """Helper function for merge_treatment_processes which loops through the
    file and marks the beginning and end of each section.
    Args:
        filename: path to file to be modified
        section_delimiter: string which marks the separation between sections
            Default: '.. _heading'
    Returns:
        lines: list of strings of each line in the file
        section_limits: list of the form [[start1, end1], [start2, end2]]
            which marks the separation between sections
    >>> process = '../../../../test_files/Treatment_Process_ET.rst'
    >>> _, limits = find_treatment_section_limits(process)
    >>> limits
    [[0, 14], [15, 20]]
    >>> process = '../../../../test_files/Treatment_Process_ET_Floc.rst'
    >>> _, limits = find_treatment_section_limits(process)
    >>> limits
    [[0, 14], [15, 20], [21, 26]]
    """
    section_limits = []
    start = 0
    file = open(filename, "r+")
    lines = file.readlines()
    file.close()

    for i, line in enumerate(lines):
        if section_delimiter in line:
            end = i - 1
            section_limits.append([start, end])
            start = i

    section_limits.append([start,len(lines)])

    return lines, section_limits

def merge_treatment_processes(new_processes, old_processes):
    """Merges two treatment process descriptions by comparing the two files
    section by section and adding pieces which exist in new_processes but are missing
    from old_processes.
    Args:
        new_processes: path to treatment process file which is being merged from
        old_processes: path to existing treatment process file which is being merged into
    Returns:
        none
    >>> old_processes = '../../../../test_files/Treatment_Process_ET.rst'
    >>> new_processes = '../../../../test_files/Treatment_Process_Floc.rst'
    >>> merge_treatment_processes(new_processes, old_processes)
    >>> file = open(old_processes, "r+")
    >>> lines = file.readlines()
    >>> test_file = open('../../../../test_files/Treatment_Process_ET_Floc.rst')
    >>> test_lines = test_file.readlines()
    >>> test_lines == lines
    True
    """
    old_lines, old_section_limits = find_treatment_section_limits(old_processes)
    new_lines, new_section_limits = find_treatment_section_limits(new_processes)

    for start, end in new_section_limits:
        included = False
        heading = new_lines[start]
        for old_start, old_end in old_section_limits:
            if old_lines[old_start] == heading:
                included = True
        if not included:
            i = old_end
            old_lines.insert(i, "\n")
            for line in new_lines[start:end]:
                i += 1
                old_lines.insert(i, line)

    old_file = open(old_processes, "w+")
    old_file.write("".join(old_lines))
    old_file.close()

def parse_variables_from_map(unparsed, default_key = None):
    """Helper function for parse_attributes which loops through an unparsed map
    that matched one of the desired fields
    Args:
        unparsed: portion of deserialized JSON which has yet to be parsed
        default_key: key for the field. Used to detect special entries like index
    Returns:
        parsed_variables: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
    """
    parsed_variables = {}
    value = None
    templates = []

    if default_key == "template":
        copy_to_docs(unparsed)
        templates.append(unparsed)
        return parsed_variables, templates
    elif default_key == "index":
        if unparsed != "" and unparsed is not None:
            if os.path.exists('index.rst'):
                copyfile(unparsed, 'new_index.rst')
                merge_indexes('new_index.rst', 'index.rst')
            else:
                copyfile(unparsed, 'index.rst')
        return parsed_variables, templates
    elif default_key == "process":
        if unparsed != "" and unparsed is not None:
            file = "Introduction/Treatment_Process.rst"
            file_path = "../doc_files/Introduction/Treatment_Process_" + unparsed + ".rst"
            if os.path.exists(file):
                merge_treatment_processes(file_path, file)
            else:
                try:
                    copyfile(file_path, file)
                except IOError as io_err:
                    os.makedirs(os.path.dirname(file))
                    copyfile(file_path, file)
        return parsed_variables, templates

    if isinstance(unparsed, list):
        for to_parse in unparsed:
            if is_fs_type(to_parse, "BTFSValueMapEntry"):
                key = to_parse[msg_str][key_str][msg_str][val_str]
                candidate_message = to_parse[msg_str][val_str]
                if is_fs_type(candidate_message, "BTFSValueMap"):
                    value, template = parse_variables_from_map(candidate_message[msg_str][val_str])
                    templates.extend(template)
                elif is_fs_type(candidate_message,  "BTFSValueArray"):
                    value = parse_variables_from_list(candidate_message[msg_str][val_str])
                elif is_fs_type(candidate_message, "BTFSValueWithUnits"):
                    value = parse_quantity(candidate_message[msg_str])
                elif is_fs_type(candidate_message, ["BTFSValueNumber", "BTFSValueString"]):
                    value = candidate_message[msg_str][val_str]
                parsed_variables[key] = value
    else:
        parsed_variables[default_key] = unparsed

    return parsed_variables, templates

def parse_attributes(attributes, fields, type_tag="Documenter"):
    """Helper function for get_parsed_measurements which loops through the
    atributes, parsing only the specified fields.
    Args:
        attributes: deserialized JSON object returned by Onshape link
        fields: fields which we are interested in parsing, e.g. 'variables' or 'index'
        type_tag: type from Onshape of the configuration we are parsing for
            Default: 'Documenter'
    Returns:
        measurements: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
    """
    measurements = {}
    templates = []

    for attr in attributes:
        if is_fs_type(attr, "BTFSValueMap"):
            if attr[msg_str]["typeTag"] == type_tag:
                for attr2 in attr[msg_str][val_str]:
                    docs = attr2[msg_str][val_str][msg_str][val_str]
                    for doc in docs:
                        for unparsed in doc[msg_str][val_str]:
                            if is_fs_type(unparsed, "BTFSValueMapEntry"):
                                key = unparsed[msg_str][key_str][msg_str][val_str]
                                for field in fields:
                                    if key == field:
                                        new_measure, new_templates = parse_variables_from_map(unparsed[msg_str][val_str][msg_str][val_str], None)
                                        measurements.update(new_measure)
                                        templates.extend(new_templates)

    for i in range(len(templates)):
        new_template = './' + os.path.basename(os.path.dirname(templates[i])) + \
                       '/' + os.path.basename(templates[i])
        templates[i] = new_template

    return measurements, templates

def get_parsed_measurements(link):
    """Parses the output of the Onshape Documenter feature found in the Onshape
    document at the given url.
    Args:
        link: URL of Onshape document
    Returns:
        measurements: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
    >>> link = 'https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/2990aab7c08553622d0c1402/e/e09d11406e7a9143537efe3a'
    >>> measurements, templates = get_parsed_measurements(link)
    >>> templates
    ['./Entrance_Tank/LFOM.rst', './Entrance_Tank/Tank_Design_Algorithm.rst']
    >>> measurements['W.Et']
    '64.1 cm'
    >>> measurements['N.LfomOrifices']
    [13.0, 3.0, 4.0, 4.0]
    >>> measurements['HL.Lfom']
    '20.0 cm'
    >>> measurements['H.LfomOrifices']
    ['2.22 cm', '7.41 cm', '12.59 cm', '17.78 cm']
    >>> measurements['D.LfomOrifices']
    '4.45 cm'
    >>> measurements['B.LfomRows']
    '5.0 cm'
    """
    script = r"""
        function (context is Context, queries is map)
        {
            return getAttributes(context, {
                "entities" : qEverything(),
            });
        }
        """

    client = Client(
        configuration = {
            "base_url": "https://cad.onshape.com",
            "access_key": "ekAHCj04TtODlvlI9yWj2bjB",
            "secret_key": "sS11vEOD5CavkLVcZshLBgfBlB5aBvnpz6v3oEvC0bN0zxhW"
        }
    )

    element = OnshapeElement(link)

    script_call = BTFeatureScriptEvalCall2377(script=script)
    response = client.part_studios_api.eval_feature_script(
        element.did,
        element.wvm,
        element.wvmid,
        element.eid,
        bt_feature_script_eval_call_2377=script_call,
        _preload_content=False,
    )

    attributes = json.loads(response.data.decode("utf-8"))["result"][msg_str][val_str]
    fields = ["variables", "template", "index", "process"]

    measurements, templates = parse_attributes(attributes, fields)

    return measurements, templates

# from https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
def line_prepender(filename, line):
    """Prepends a file with the given line.
    Args:
        filename: path to file to be modified
        line: string of text to prepend to the file
    Returns:
        none
    """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def make_replace_list(parsed_dict, filename, var_attachment=''):
    """Adds the dictionary of variables which have been parsed to the top of the
    given file.
    Args:
        parsed_dict: dictionary of variables parsed from Onshape document
        filename: path to file to be modified
        var_attachment: string to prepend to all variables, e.g. "LFOM"
            Default: ''
    Returns:
        none
    >>> var_dict = {'test': '3.0 cm'}
    >>> file_path = "../../../../test_files/test_prepend.rst"
    >>> make_replace_list(var_dict, file_path)
    >>> file = open(file_path, "r+")
    >>> lines = file.readlines()
    >>> test_file = open('../../../../test_files/test_prepend_result.rst')
    >>> test_lines = test_file.readlines()
    >>> test_lines == lines
    True
    """
    prefix = '.. |'
    suffix = '| replace:: '

    for var in parsed_dict:
        if type(parsed_dict[var]) == dict:
            make_replace_list(parsed_dict[var], filename, var_attachment + var + "_")
        else:
            line = prefix + var_attachment + str(var) + suffix + str(parsed_dict[var])
            line_prepender(filename, line)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
