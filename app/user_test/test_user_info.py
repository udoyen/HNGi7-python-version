import unittest
from schema import Schema, And, Use, Or, Regex
import re
from ..index import check_info, process_users

email_test = r"Hello World, this is Idowu Toluwani with HNGi7 ID HNG-04337 " \
             r"using CSharp for stage 2 task and email toluwanieaidowu@gmail.com ."
name_fail = r"Hello World, this is with HNGi7 ID HNG-050709 using PHP for stage " \
            r"2 task and amusaabiodun88@gmail.com"
fail_sample = r"Hello World, this is Fagoroye George-Ayomide with " \
              r"HNGi7 ID HNG-05#@4 using python for stage 2 task and fagoroyeayomidegmail.com"
sample = r"Hello World, this is Oke George-Kehinde with HNGi7 ID " \
         r"HNG-05678 using Javascript for stage 2 task and okekehinde@gmail.com"
email = r"^.+and\s+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)[\.|\s]*$"
names = r"^Hello\s*World,\sthis\s+is\s+([\w\s-]*)\s+with.*"
hng_id = r"^Hello\s*World,\s.+ID\s(HNG-\d{5})"
language = r"^Hello\s*World,\s.+using\s(\w+)"
main_output = r"^Hello\sWorld,\s+this\s+is\s+[\w\s-]+with\s+HNGi7\s+ID\s+HNG-\d{5}" \
              r"\s+using\s+\w+\s+for\s+stage\s+2\s+task\s+and\s+[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[\.|\s]*$"
main = r"Hello World, this is Idowu Toluwani with HNGi7 ID HNG-04337 " \
       r"using CSharp for stage 2 task and email toluwanieaidowu@gmail.com ."
main2 = r"Hello World, this is Onwuka Chidumga with HNGi7 ID HNG-06529 " \
        r"using javascript for stage 2 task and my email is kelvinonwuka8@gmail.com"
main3 = r"\n\nHello World, this is Gabriel Ifgoa with HNGi7 ID 02808 using " \
        r"PHP for stage 2 task and gabrielifoga@yahoo.com"
name_checker = r"Hello World, this is Idris Olubisi with HNGi7 ID " \
               r"HNG-01329 using javascript for stage 2 task and heedris2olubisi@gmail.com"
run_command = {
    '.js': 'node',
    '.py': 'python3',
    '.php': 'php',
    '.java': 'java'
}
schema = Schema([{
    'file': str,
    'output': lambda n: re.match(main_output, n, flags=re.I) or str,
    'email': lambda n: re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[.|\s]*$', n,
                                flags=re.I) or n == '',
    'fullname': str,
    'HNGId': lambda n: re.match(r'^HNG-\d{5}', n) or n == '',
    'language': str,
    'status': lambda n: n == 'Pass' or n == 'Fail'
}])


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_process_users(self):
        ls = process_users()
        validated = schema.validate(ls[:200])
        self.assertIsInstance(ls, list)
        self.assertIsInstance(ls[0], dict)
        self.assertTrue(validated)

    def test_main_pass(self):
        result = check_info(main_output, sample)
        self.assertEqual(result, sample)

    def test_main_fail(self):
        result = check_info(main_output, main2)
        self.assertEqual(result, '')

    def test_main_for_leading_newlines(self):
        result = check_info(main_output, main3)
        self.assertEqual(result, '')

    def test_email(self):
        result = check_info(email, sample)
        self.assertEqual(result, 'okekehinde@gmail.com')

    def test_names(self):
        result = check_info(names, sample)
        self.assertEqual(result, 'Oke George-Kehinde')

    def test_hng_id(self):
        result = check_info(hng_id, sample)
        self.assertEqual(result, 'HNG-05678')

    def test_language(self):
        result = check_info(language, sample)
        self.assertEqual(result, 'Javascript')

    def test_email_fail(self):
        result = check_info(email, fail_sample)
        self.assertEqual(result, '')

    def test_hng_id_fail(self):
        result = check_info(hng_id, fail_sample)
        self.assertEqual(result, '')

    def test_name_fail(self):
        result = check_info(names, name_fail)
        self.assertEqual(result, '')

    def test_another_email_fail(self):
        result = check_info(email, email_test)
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
