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
        print("using random file name: "+random_file_name, file=sys.stderr)
        with self.assertRaises(mdiocre.ConfigInvalid):
            mdiocre.Config(filename=random_file_name,logger=mock_log.Debug(False))
class TestWizard(unittest.TestCase):
    @classmethod
    def setUpClass(TestConfig):
        print("\nRunning mdiocre.Wizard test!", file=sys.stderr)

    def setUp(self):
        self.config = mdiocre.Config(filename="wizard/config.ini",logger=mock_log.Debug(False))
        self.wizard = mdiocre.Wizard(config=self.config)

    @unittest.skip("todo")
    def test_make_page(self):
        pass

    def test_make_site(self):
        self.wizard.build_site(index_html=True, use_prefix=False)
        # Check for html indexing
        with open("wizard/src/sub/index.md","r") as sub_index:
            o = sub_index.read()
            c = """This is the index page

* [Emptytemplate](emptytemplate.html)
* [Page1.md](page1.html)
* [Page2.md](page2.html)
* [Page3.md](page3.html)
"""
            self.assertEqual(o,c)

    @unittest.skip("todo")
    def test_clean_site(self):
        pass

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
        text = "Concatenating a variable and a string<!--var2=test,\" set=21!\"-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating a variable and a string")
        self.assertEqual(self.vars["var2"], "abc set=21!")

    def test_variable_set_concat_vars_spaced(self):
        text = "Concatenating two variables<!--var2=test,\" \",test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abc abc")

    def test_variable_set_concat_vars_unspaced(self):
        text = "Concatenating two variables<!--var2=test,test-->"
        x = self.utils.process_vars(text, var_list=self.vars, set_var=True)
        self.assertEqual(x,"Concatenating two variables")
        self.assertEqual(self.vars["var2"], "abcabc")


if __name__ == "__main__":
   print("\n\nSTARTING UNIT TEST\n", file=sys.stderr)
   unittest.main(verbosity=2)
