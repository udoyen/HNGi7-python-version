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
    lang_count = {
        '.js': 0,
        '.php': 0,
        '.java': 0,
        '.py': 0
    }
    error_file = []
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
            f_path = os.path.abspath('scripts/' + f)
            if file_extension[1] in run_command.keys():
                # Update the language count dict
                lang_count[file_extension[1]] += 1
                # Run the command and get the output
                print('Command: {}'.format(run_command[file_extension[1]]))
                proc = subprocess.run([run_command[file_extension[1]], f_path], stdout=subprocess.PIPE, bufsize=0)
                if proc.returncode is not 0:
                    print('Error in User script')
                    error_file.append(f_path)
                else:
                    print('Output: {}'.format(proc.stdout.decode('utf-8')))
            print('====================================')
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
        print('Error files: {}'.format(error_file))
        print('Total files count: {}'.format(len(files)))
        print('Files processed: {}'.format(len(files) - len(error_file)))
        print('Files not processed: {}'.format(len(error_file)))
        print('Scripts count: {}'.format(lang_count['.js']), 'Java count: {}'.format(lang_count['.java']),
              'Php count: {}'.format(lang_count['.php']), 'Python count: {}'.format(lang_count['.py']))
