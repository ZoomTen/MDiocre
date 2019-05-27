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
        print("\nRunning mdiocre.Config test!", file=sys.stderr)

    @classmethod
    def tearDownClass(TestConfig):
        pass

    def setUp(self):
        pass

    def test_load_config_okay(self):
        test = {
                   "vars": {"site-name": "My Homepage",
                            "email-addr": "bobx.x@alicex.x.comx",
                            "hello": "Hello World!"
                           },
                   "modules": ["root","blog","tutorial","page","art"],
                   "use-templates": ["main", "blog", "tutorial", "page", "art"],
                   "no-index": ["page","art"],
                   "source-folder": "Pages/_src",
                   "build-folder": "My Pages/_html",
                   "template-folder": "ShortPages/_templates",
                   }
        c = mdiocre.Config(config=test,logger=mock_log.Debug(False))

    def test_load_config_invalid_var_name(self):
        test = {
                   "vars": {"SiTeNaMe": "My Homepage",
                            "!!!HellO": "bobx.x@alicex.x.comx",
                            "w0RDS": "Hello World!"
                           },
                   "modules": ["root","blog","tutorial","page","art"],
                   "use-templates": ["main", "blog", "tutorial", "page", "art"],
                   "no-index": ["page","art"],
                   "source-folder": "Pages/_src",
                   "build-folder": "My Pages/_html",
                   "template-folder": "ShortPages/_templates",
                   }
        with self.assertRaises(mdiocre.InvalidVarName):
            c = mdiocre.Config(config=test,logger=mock_log.Debug(False))

    def test_load_config_not_okay(self):
        """
        vars and source folder keys missing
        """
        test = {
                   "modules": ["root","blog","tutorial","page","art"],
                   "use-templates": ["main", "blog", "tutorial", "page", "art"],
                   "no-index": ["page","art"],
                   "build-folder": "My Pages/_html",
                   "template-folder": "ShortPages/_templates",
                   }
        with self.assertRaises(mdiocre.ConfigInvalid):
            c = mdiocre.Config(config=test,logger=mock_log.Debug(False))

    def test_load_config_file_okay(self):
        import os
        conf_file = "cfg_test/config.ini"
        if os.path.exists(conf_file):
            c = mdiocre.Config(filename="cfg_test/config.ini",logger=mock_log.Debug(False))
            test = {
                   "vars": {"site-name": "My Homepage",
                            "email-addr": "bobx.x@alicex.x.comx",
                            "hello": "Hello World!"
                           },
                   "modules": ["root","blog","tutorial","page","art"],
                   "use-templates": ["main", "blog", "tutorial", "page", "art"],
                   "no-index": ["page","art"],
                   "source-folder": "Pages/_src",
                   "build-folder": "My Pages/_html",
                   "template-folder": "ShortPages/_templates",
                   }
            self.assertCountEqual(c.config, test)
            #print("\n c.config contains:\n", c.config)
            #print("\n test contains:\n", test)
        else:
            self.fail("required file "+conf_file+" does not exist")

    def test_load_config_file_not_okay(self):
    # this is not a valid config
        import os
        conf_file = "cfg_test/config.invalid.ini"
        if os.path.exists(conf_file):
            with self.assertRaises(mdiocre.ConfigInvalid):
                mdiocre.Config(filename="config.invalid.ini",logger=mock_log.Debug(False))
        else:
            self.fail("required file "+conf_file+" does not exist")

    def test_load_config_file_not_existent(self):
    # no such file
        from random import random
        random_file_name = ""
        for i in range(32):
            random_file_name += chr(97+int(random()*26))
        random_file_name += ".ini"
        print("using random file name: "+random_file_name, file=sys.stderr, end='... ')
        with self.assertRaises(mdiocre.ConfigInvalid):
            mdiocre.Config(filename=random_file_name,logger=mock_log.Debug(False))

class TestWizard(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Wizard test!", file=sys.stderr)

    def setUp(self):
        self.config = mdiocre.Config(filename="wizard/config.ini",logger=mock_log.Debug(False))
        self.wizard = mdiocre.Wizard(config=self.config)

    def test_make_page(self):
        var_list = self.config.config["vars"]
        command = self.wizard.build_page("wizard/src/sub/page1.md", "wizard/template/main.html", var_list)
        expected = """<html>
<head>
<title>My Homepage : Page 1</title>
</head>
<body>
<h1 id="page-1">Page 1</h1>
<p>Date test of 1970-01-01</p>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

</body>
</html>
"""
        self.assertEqual(expected, command)

    def test_list_files_root(self):
        # This will only index the root directory
        compare = ["index.md"]
        command = self.wizard.get_files(root_folder="wizard/src", ext="md", module="root")
        self.assertEqual(compare, command)

    def test_list_files_module_md(self):
        # This will also index subdirectories
        compare = ['anothersub/page1.md', 'anothersub/page2.md',
                   'anothersub/page3.md', 'anothersub2/page1.md',
                   'anothersub2/page2.md', 'anothersub2/page3.md',
                   'page1.md', 'page2.md', 'page3.md']
        command = self.wizard.get_files(root_folder="wizard/src", ext="md", module="sub")
        for i in compare:
            self.assertIn(i, command)

    def test_make_index_sub(self):
        # TODO: Still need to sort this out
        index_string = """This is the index page

* **1601-01-01** - [Page 3](page3.html)
* **1970-01-01** - [Page 1](page1.html)
* **1980-01-01** - [Page 2](page2.html)
* [Emptytemplate.html](anothersub/emptytemplate.html)
* [Emptytemplate.html](anothersub2/emptytemplate.html)
* [Emptytemplate.html](emptytemplate.html)
* [another sub 2: Page 1](anothersub2/page1.html)
* [another sub 2: Page 2](anothersub2/page2.html)
* [another sub 2: Page 3](anothersub2/page3.html)
* [another sub: Page 1](anothersub/page1.html)
* [another sub: Page 2](anothersub/page2.html)
* [another sub: Page 3](anothersub/page3.html)
"""
        index_out = self.wizard.build_index(root_folder="wizard/src", module_name="sub")
        self.assertEqual(index_string, index_out)
    
    def test_make_index_page(self):
            # TODO: Sort out this too
        listing = ["page1.md","page2.md","page3.md"]
        index_string = """* **1601-01-01** - [Page 3](page3.html)
* **1970-01-01** - [Page 1](page1.html)
* **1980-01-01** - [Page 2](page2.html)"""
        index_out = self.wizard.make_index_page(file_list=listing, folder_base="wizard/src/sub", module_name="sub")
        self.assertEqual(index_string, index_out)

    def test_make_index_entry(self):
        index_string = """* **1970-01-01** - [Page 1](page1.html)"""
        mockvars = {"date":"1970-01-01", "title":"Page 1"}
        index_out = self.wizard.make_index_entry(use_vars=mockvars, path="page1.html", name=None)
        self.assertEqual(index_string, index_out)


    def test_make_site_clean_site(self):
        self.wizard.build_site(index_html=True, use_prefix=False)
        self.wizard.clean_site(remove_index_pages=True)

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Utils test!", file=sys.stderr)

    def setUp(self):
        self.vars = {
                    "test":"abc",
                    "foo": "bar",
                    "bar": "foo"
                    }
        self.utils = mdiocre.Utils(logger=mock_log.Debug(False))

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
        # putting the equals sign in between spaces will NOT WORK
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
        text = "Concatenating a variable and a string<!--var2=test,\" set, go\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "abc set, go")

    def test_variable_set_concat_var_str_commaized_inquotes(self):
        text = "Concatenating a variable and a string<!--var2=\"test,\" set, go\"\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "test,\" set, go\"")

    def test_variable_set_concat_var_str_equalssign(self):
        text = "Concatenating a variable and a string<!--var2=test,\" 2 + 2 = 4 quick maths\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "abc 2 + 2 = 4 quick maths")

    def test_variable_set_concat_vars_spaced(self):
        text = "Concatenating two variables<!--var2=test,\" \",test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abc abc")

    def test_variable_set_concat_vars_unspaced(self):
        text = "Concatenating two variables<!--var2=test, test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abcabc")

if __name__ == "__main__":
   print("\n\nSTARTING UNIT TEST\n", file=sys.stderr)
   unittest.main(verbosity=2)
