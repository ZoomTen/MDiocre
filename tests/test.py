import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import mdiocre
import unittest
import mock_log

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Config test!")
        with open("config.test.ini", "w") as c:
            c.write("""[config]
modules         = root, blog, tutorial, page, art
use-templates   = main, blog, tutorial, page, art
no-index        = page, art
source-folder   = Pages/_src
build-folder    = My Pages/_html
template-folder = ShortPages/_templates

[vars]
site-name       = My Homepage
email-addr      = bobx.x@alicex.x.comx
hello           = Hello World!""")
        print("config.test.ini has been created in the test directory.")
        with open("config.invalid.ini", "w") as c:
            c.write("""[config]
modules         = 
use-templates   = """)
        print("config.invalid.ini has been created in the test directory.")
    
    @classmethod
    def tearDownClass(TestConfig):
        import os
        os.remove("config.test.ini")
        print("Removing config.test.ini.")
        os.remove("config.invalid.ini")
        print("Removing config.invalid.ini.")
    
    def setUp(self):
        pass
    
    @unittest.skip("todo")
    def test_load_config(self):
        pass
    
    def test_load_config_file_okay(self):
        c = mdiocre.Config(filename="config.test.ini",logger=mock_log.Debug(False))
        test = {
               "vars": {"site-name": "My Homepage",
                        "email-addr": "bobx.x@alicex.x.comx",
                        "hello": "Hello World!"
                       },
               "modules": ["root","blog","tutorial","page","art"],
               "use-templates": ["main", "blog", "tutorial", "page", "art"],
               "no-index": ["page","art"],
               "source-folder": ["Pages/_src"],
               "build-folder": ["My Pages/_html"],
               "template-folder": ["ShortPages/_templates"],
               }
        
        for key in test.keys():
            with self.subTest(key=key):
                if key == "use-templates":
                    pass
                else:
                    self.assertEqual(c.config[key], test[key])
        
        #print("\n c.config contains:\n", c.config)
        #print("\n test contains:\n", test)
    
    def test_load_config_file_not_okay(self):
        with self.assertRaises(AssertionError):
            mdiocre.Config(filename="config.invalid.ini",logger=mock_log.Debug(False))

class TestWizard(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Wizard test!")
    
    def setUp(self):
        pass
    
    @unittest.skip("todo")
    def test_make_page(self):
        pass
    
    @unittest.skip("todo")
    def test_make_site(self):
        pass
    
    @unittest.skip("todo")
    def test_clean_site(self):
        pass

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Utils test!")
    
    def setUp(self):
        self.vars = {
                    "test":"abc",
                    "foo": "bar",
                    "bar": "foo"
                    }
        self.utils = mdiocre.Utils(logger=mock_log.Debug(False))
    
    @unittest.skip("todo")
    def test_file_exists(self):
        pass
    
    @unittest.skip("todo")
    def test_file_does_not_exist_create(self):
        pass
    
    @unittest.skip("todo")
    def test_file_does_not_exist_nocreate(self):
        pass
    
    @unittest.skip("todo")
    def test_directory_exists(self):
        pass
    
    @unittest.skip("todo")
    def test_directory_does_not_exist_create(self):
        pass
    
    @unittest.skip("todo")
    def test_directory_does_not_exist_nocreate(self):
        pass
        
    def test_variable_put_single(self):
        text = "Hello from <!--var:test--> world"
        proc = self.utils.process_vars(text, var_list=self.vars)
        self.assertEqual(proc, "Hello from abc world")
    
    def test_variable_put_multiple(self):
        text = "<!--var:test-->ing... <!--var:bar--><!--var:foo--> is <!--var:foo--> <!--var:bar-->"
        proc = self.utils.process_vars(text, var_list=self.vars)
        self.assertEqual(proc, "abcing... foobar is bar foo")

    def test_variable_set_assign_string(self):
        text = "Directly setting variable to string<!--var1=\"set\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Directly setting variable to string")
        self.assertEqual(self.vars["var1"], "set")

    def test_variable_set_assign_var(self):
        text = "Directly assigning a variable to another<!--var3=test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Directly assigning a variable to another")
        self.assertEqual(self.vars["var3"], "abc")
        
    def test_variable_set_concat_var_str(self):
        text = "Concatenating a variable and a string<!--var2=test,\" set\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "abc set")
        
    
    def test_variable_set_concat_var_str_commaized(self):
        text = "Concatenating a variable and a string<!--var2=test,\" set\, go\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "abc set, go")
    
    def test_variable_set_concat_vars_spaced(self):
        text = "Concatenating two variables<!--var2=test, test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abc abc")
    
    def test_variable_set_concat_vars_unspaced(self):
        text = "Concatenating two variables<!--var2=test,test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abcabc")


if __name__ == "__main__":
   print("\n\nSTARTING UNIT TEST\n")
   unittest.main(verbosity=2)
