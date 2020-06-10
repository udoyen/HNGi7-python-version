import os
import subprocess
import re
from collections import OrderedDict
import json

# regex code
"""
email: ^Hello\sWorld,.*and\s(.*@\w+\.\w+)\.{0,1}$
names: ^Hello\s*World,\s.+is\s*([\w\s-]*)\swith.*
hng id: ^Hello\s*World,\s.+ID\s(HNG-\d{5})
language: ^Hello\s*World,\s.+using\s(\w+)
email = re.match(r"^Hello\sWorld,.*and\s(.*@\w+\.\w+)\.{0,1}$", email)
name = re.match(r"^Hello\s*World,\s.+is\s([\w\s]+)\swith", email)
test = re.match(r"", sample)
print(test.group(1)) if type(test) else print('Failed')
"""

email = "^.+and\s+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+).*$"
names = "^Hello\s*World,\s.+is\s*([\w\s-]*)\swith.*"
hng_id = "^Hello\s*World,\s.+ID\s(HNG-\d{5})"
language = "^Hello\s*World,\s.+using\s(\w+)"
output = "^Hello\sWorld,\s+this\s+is\s+[\w\s-]+with\s+HNGi7\s+ID\s+HNG-\d{5}\s+using\s+\w+\s+for\s+stage\s+2\s+task\s+and\s+[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[\.|\s]*$"

# sample json output
json_data = []

# return value from function
output_results = OrderedDict()


def check_info(test_regex: str, user_output: str) -> str:
    """
    Used to confirm user information
    :param test_regex:
    :param user_output:
    :return (str): string of user information or empty string
    """
    result = re.match(test_regex, user_output)
    if result:
        if test_regex == output:
            return result.group()
        else:
            return result.group(1)
    else:
        return ''


def process_users() -> list:
    """
    Used to process user scripts
    :return (list): Tuple of list of failures and dict of all data
    """
    run_command = {
        '.js': 'node',
        '.py': 'python3',
        '.php': 'php',
        '.java': 'java'
    }
    lang_count = {
        '.js': 0,
        '.php': 0,
        '.java': 0,
        '.py': 0
    }
    error_files = []
    dir_name = os.path.dirname(__file__)
    r_path = os.path.realpath(dir_name + '/scripts')
    target = r_path
    # TODO remove these lines
    print('Dirname: {}'.format(dir_name))
    print('Location: {}'.format(r_path))
    print('Target: {}'.format(target))
    try:
        # Get files in scripts folder
        files = [f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))]
        for f in files:
            # Get file extension
            file_extension = os.path.splitext(f)
            # TODO remove these lines
            # print('====================================')
            # print('File extension: {}'.format(str(file_extension[1])))
            # print('File: {}'.format(f))
            # print('Fullpath to file: {}'.format(os.path.abspath('scripts/' + f)))
            f_path = r_path + '/' + f
            if file_extension[1] in run_command.keys():
                # Update the language count dict
                lang_count[file_extension[1]] += 1
                # Run the command and get the output
                # TODO Remove
                # print('Command: {}'.format(run_command[file_extension[1]]))
                proc = subprocess.run([run_command[file_extension[1]], f_path], stdout=subprocess.PIPE, bufsize=0)
                # change output to string
                proc_str = proc.stdout.decode('utf-8').rstrip("\n")
                # Make sure the out meets the required string format
                if check_info(output, proc_str) == '' and check_info(email, proc_str) == '':
                    print('Error in User script')
                    error_files.append(f_path)
                    # setup the dict result
                    json_data.append(OrderedDict(
                        {
                            'file': f,
                            'output': proc.stdout.decode('utf-8').rstrip("\n"),
                            'email': check_info(email, proc_str),
                            'fullname': check_info(names, proc_str),
                            'HNGId': check_info(hng_id, proc_str),
                            'language': check_info(language, proc_str),
                            'status': 'Fail'
                        }
                    ))
                else:
                    print('Output: {}'.format(proc.stdout.decode('utf-8')), flush=True)
                    # setup the dict result
                    json_data.append(OrderedDict(
                        {
                            'file': f,
                            'output': proc.stdout.decode('utf-8').rstrip("\n"),
                            'email': check_info(email, proc_str),
                            'fullname': check_info(names, proc_str),
                            'HNGId': check_info(hng_id, proc_str),
                            'language': check_info(language, proc_str),
                            'status': 'Pass'
                        }
                    ))
            # TODO remove these line
            # print('====================================')
        return json_data
    except TypeError as t_err:
        print('Error: {}'.format(t_err))
    except ValueError as v_err:
        print('Error: {}'.format(v_err))
    except FileNotFoundError as f_err:
        print('Error: {}'.format(f_err))
    except subprocess.CalledProcessError as sc_err:
        print('Error: {}'.format(sc_err))
    except Exception as e_err:
        print('Error Type: {}, msg: {}'.format(type(e_err), e_err))
    finally:
        # print(for i in json_data)
        print('json_data items: {}'.format(json.dumps(json_data, indent=4)))
        print('Error files: {}'.format(error_files))
        print('Total files count: {}'.format(len(files)))
        print('Files processed: {}'.format(len(files) - len(error_files)))
        print('Files not processed: {}'.format(len(error_files)))
        print('Scripts count: {}'.format(lang_count['.js']), 'Java count: {}'.format(lang_count['.java']),
              'Php count: {}'.format(lang_count['.php']), 'Python count: {}'.format(lang_count['.py']))


if __name__ == '__main__':
    process_users()
