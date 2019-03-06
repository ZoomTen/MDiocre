import os
import re
import configparser as cp
from .logger import Debug
from .exception import *

class Config:
    """ Create a configuration object.

    Parameters:
        filename (str): Load configurations from an `ini` file
            at this path. If set, `self.name` will contain the
            filename specified. Defaults to None.
        config  (dict): An existing configuration
            to be encapsuled in an :py:class:`~mdiocre.Config` object.
            Defaults to None.
        logger (Debug): logger object to use.
            Defaults to a generated Debug object,
            with the extra notes set to `True`.
    Returns:
        Config: A Config object.
    """
    def __init__(self, filename=None, config=None, logger=Debug(True)):
        self.log = logger
        self.name = filename
        self.valid = False
        if config:
            self.validate(config)
        else:
            if type(filename) is str:
                self.load_config(filename)
            else:
                self.config = None

    def load_config(self, filename):
        """
            Loads a configuration from a specified path.
            This will run it through :py:func:`~mdiocre.Config.read_config`
            and then validate it.

        Parameters:
            filename (str): Load configurations from an `ini` file
                at this path. If set, `self.name` will contain the
                filename specified. Defaults to None.
        Returns:
            None
        """
        self.config = self.read_config(filename)
        self.validate(self.config)

    def validate_varname(self, var_name):
        """ Validates a given variable name, according to these rules:
            * Must **only** contain lowercase letters, dashes, underscores, and numbers.
            * That means no capital letters or spaces.

        Parameters:
            var_name (str): Name to validate.
        Returns:
            None
        Raises:
            InvalidVarName: if `var_name` doesn't follow above rules.
        """
        if not (re.search(r"^[a-z\-_0-9]+$", var_name)):
    	    raise InvalidVarName(var_name)

    def read_config(self, config_file):
        """ Reads the configuration from a filename.

        Parameters:
            config_file (str): The configuration file
                to use.
        Returns:
            dict: The configuration dictionary in self.config, if successful.

        Raises:
            ConfigInvalid: if it can't find the file specified by
                `config_file`.
        """
        self.log.header("Trying to read "+config_file+"...", False)

        if os.path.exists(config_file):
            config = cp.ConfigParser()
            config.read(config_file)

            conf_dict = {"vars":{}}
            reqd_opts = ["modules",
                         "use-templates",
                         "source-folder",
                         "build-folder",
                         "template-folder"]
            try:
            # Test required keys
                for require in reqd_opts:
                    config.get("config",require)
            # Get config
                for option in config.options("config"):
                    if option in reqd_opts:
                        assert (config.get("config",option) != ""), "Option \'"+option+"\' is empty!"
                    if option[-7:] == "-folder":
                        cfg_array = config.get("config",option)
                    else:
                        cfg_array = config.get("config",option).replace(" ","").split(",")
                    conf_dict[option] = cfg_array
                if "vars" in config.sections():
                    for option in config.options("vars"):
                        conf_dict["vars"][option] = config.get("vars",option)
            except cp.NoSectionError as e:
                self.log.error("Cannot find section '"+str(e.args[0])+"' in the configuration file!")
                return
            except cp.NoOptionError as e:
                self.log.error("Cannot find option '"+str(e.args[0])+"' in the configuration file!")
                return
            else:
                self.log.header("Successfully read config file!", False)
                return conf_dict
        else:
            raise ConfigInvalid("No such config file: "+config_file)
            return

    def validate(self, config):
        """ Validates a configuration dictionary.

        Parameters:
            config_file (str): The configuration file
                to use.
        Returns:
            dict: The configuration dictionary in self.config, if successful.
            dict: As self.vars, the variable key from self.config.
            bool: In self.valid, set to True if all is OK.

        Raises:
            ConfigInvalid: if `config` is not a :obj:`dict`.
        """
        # Validate config
        if type(config) is not dict:
            raise ConfigInvalid("This is not a valid configuration!")
        else:
            self.log.header("CONFIG CHECK", True)
            self.log.name("Check required keys")
            reqd_opts = ["modules",
                         "use-templates",
                         "source-folder",
                         "build-folder",
                         "template-folder",
                         "vars"]
            for i in reqd_opts:
                try:
                    self.log.log(i+"\t... "+str(config[i]))
                except KeyError as e:
                    raise ConfigInvalid("Can't find key "+i+", fix your configuration!")

            self.log.name("Check extra keys")
            for i in config.keys():
                if i not in reqd_opts:
                    self.log.log(i+"\t... "+str(config[i]))

            self.log.name("Check variable names")
            #try:
            for i in iter(config["vars"].keys()):
                self.validate_varname(i)
                self.log.log(i+"\t... valid")
            #except KeyError as e:
            #    self.log.error("Can't find key 'vars'")
            #    return
            #except InvalidVarName as e:
            #	self.log.log(i+"\t... INVALID")
            #	self.log.error("Illegal variable name "+i+"! Please fix your configuration!")
            #	return
            #else:
            self.config = config
            self.vars = self.config["vars"]
            self.log.header("Configuration check okay!", False)
            self.valid = True
