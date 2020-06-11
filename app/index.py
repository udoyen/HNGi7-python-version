import os
import subprocess
import re
from collections import OrderedDict
import json
import itertools
from flask import Flask, render_template, make_response, request, jsonify

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

app = Flask(__name__)


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
    dir_name = os.path.dirname(__file__)
    r_path = os.path.realpath(dir_name + '/scripts')
    target = r_path
    counter = itertools.count(0)
    try:
        # Get files in scripts folder
        files = [f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))]
        for f in files:
            # Get file extension
            file_extension = os.path.splitext(f)
            lang_count[file_extension[1]] += 1
            # TODO remove these lines
            # print('File extension: {}'.format(str(file_extension[1])))
            # print('File: {}'.format(f))
            # print('Fullpath to file: {}'.format(os.path.abspath('scripts/' + f)))
            f_path = r_path + '/' + f
            proc_str = [subprocess.run([run_command[file_extension[1]], f_path], stdout=subprocess.PIPE,
                                       bufsize=0).stdout.decode('utf-8').replace('\n', '').rstrip() if file_extension[
                                                                                                           1] in run_command.keys() else 'Nothing']
            print('Output Str: {}'.format(proc_str[0]), flush=True)
            # Unpack the list of dict created earlier
            # and append them to the json_data list
            json_data.append(*[OrderedDict({
                'file': f,
                'output': proc_str[0],
                'email': check_info(email, proc_str[0]),
                'fullname': check_info(names, proc_str[0]),
                'HNGId': check_info(hng_id, proc_str[0]),
                'language': check_info(language, proc_str[0]),
                'status': 'Fail'
            }) if check_info(output, proc_str[0]) == '' or check_info(email, proc_str[0]) == '' else
                               OrderedDict({
                                   'file': f,
                                   'output': proc_str[0],
                                   'email': check_info(email, proc_str[0]),
                                   'fullname': check_info(names, proc_str[0]),
                                   'HNGId': check_info(hng_id, proc_str[0]),
                                   'language': check_info(language, proc_str[0]),
                                   'status': 'Pass'
                               })])
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
        error_files = [next(counter, i) for i in json_data if i['status'] == 'Fail']
        print('json_data items: {}'.format(json.dumps(json_data, indent=4)))
        print('Files processed: {}'.format(len(files)), 'Script Success: {}'.format(len(files) - error_files[-1]),
              'Script Fails: {}'.format(error_files[-1]), sep='\n')
        print('JavaScripts count: {}'.format(lang_count['.js']), 'Java count: {}'.format(lang_count['.java']),
              'Php count: {}'.format(lang_count['.php']), 'Python count: {}'.format(lang_count['.py']))
    return json_data


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """
    Landing page function
    :return:
    """
    if 'json' in request.args:
        data = process_users()
        return jsonify(message=data)
    else:
        return render_template('index.html')


@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(render_template("400.html"), 400)


@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(render_template("500.html"), 500)


if __name__ == '__main__':
    app.run(debug=True)
