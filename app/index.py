import sys
import subprocess
import os
from shlex import quote as shlex_quote

if __name__ == '__main__':
    run_command = {
        '.js': 'node',
        '.py': 'python3',
        '.php': 'php',
        '.java': 'java'
    }
    target = os.path.abspath('scripts')
    print(target)
    try:
        # Get files in scripts folder
        files = [f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))]
        for f in files:
            # Get file extension
            file_extension = os.path.splitext(f)
            print('====================================')
            print('File extension: {}'.format(str(file_extension[1])))
            print('File: {}'.format(f))
            print('Fullpath to file: {}'.format(os.path.abspath('scripts/' + f)))
            print('====================================')
            f_path = os.path.abspath('scripts/' + f)
            if file_extension[1] in run_command.keys():
                # Run the command and get the output
                print('Command: {}'.format(run_command[file_extension[1]]))
                proc = subprocess.run([run_command[file_extension[1]], f_path],
                                      check=True,
                                      stdout=subprocess.PIPE)
                output = proc.stdout
                print('Output: {}'.format(output))
    except TypeError as t_err:
        print('Error: {}'.format(t_err))
    except ValueError as v_err:
        print('Error: {}'.format(v_err))
    except FileNotFoundError as f_err:
        print('Error: {}'.format(f_err))
    except Exception as e_err:
        print('Error Type: {}, msg: {}'.format(type(e_err), e_err))
