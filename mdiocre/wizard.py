import sys
import shutil
from os import path as osp
from os import walk as osw
from .utils import Utils
from .config import Config
from .logger import Debug
from .exception import *

class Wizard:
    """
    Sets up the MDiocre procedure class / `wizards`
    for building sites.

    Parameters:
        config (Config): configuration object.
        logger  (Debug): logger object to use
            Defaults to a generated Debug object,
            with the extra notes set to `True`.
    Returns:
        Wizard: A Wizard object.

    Raises:
        ConfigInvalid: When `config` isn't a valid
        :py:class:`~mdiocre.Config` object.
    """
    # image extension support list
    img_support = ["jpg", "jpeg", "png", "gif", "webp"]
    
    def __init__(self, config=None, logger=Debug(True)):
        self.log = logger
        if type(config) is Config:
            self.config = config
        else:
            raise ConfigInvalid("Invalid configuration type!")
        self.tools = Utils(logger=logger)

    def get_files(self, root_folder=None, ext=None, module=None):
        """
        Makes a file list covering a module and its subdirectories. (Except
        the root module)
        
        Parameters:
            root_folder (str): Web root folder.
            module      (str): Module name.
            ext         (str): File extension.
        
        Returns:
            List containing all the file names.
        """
        if type(root_folder) != str:
            raise Exception("No root folder specified")
        if type(ext) != str:
            raise Exception("No file extension specified")
        if type(module) != str:
            raise Exception("No module specified")

        from glob import glob
        import re

        result = []
        if module != "root":
            for walk in osw(osp.join(root_folder, module)):
                for name in walk[2]:
                    if name[-len(ext):].lower() == ext.lower():
                        regex = r'^' + re.escape(module)
                        file_base = re.sub(regex, '', osp.basename(walk[0]))
                        result.append(
                        osp.join(file_base, name)
                        )
            return sorted(result)
        else:
            files =  glob(root_folder + "/*." + ext)
            if ext.lower() != ext:
                files += glob(root_folder + "/*." + ext.lower())
            if ext.upper() != ext:
                files += glob(root_folder + "/*." + ext.upper())
            for a_file in files:
                result.append(osp.basename(a_file))
            return sorted(result)

    def make_index_page(self, file_list=None, PREFIX=False, folder_base=None, module_name=None):
        """
        Create index page, preparing for modularization
        
        Todo:
            Parameter checking.
            Clean this up more. Oh, and implement sorting by
            date or title, reverse or forwards.
            
        Parameters:
            root_folder (str): Web root folder.
            module      (str): Module name.
            ext         (str): File extension.
        
        Returns:
            Formatted index page.
        """
        content = "* "                      # content buffer
        index_contents = []
        # make index of pages
        for i in file_list:
            temp_var_list = {}
            basename = osp.basename(i)
            name = basename
            actual_name = i.replace(".md", ".html").replace(".MD", ".html")

            if PREFIX:
                path = module_name + "/" + actual_name
            else:
                path = actual_name

            self.log.log("Add entry for " + osp.join(folder_base, i))

            # scan files for title and date
            with open(osp.join(folder_base, i), "r") as document:
                scan = document.read()
                self.tools.process_vars(scan,
                                        var_list=temp_var_list,
                                        set_var=True, file_name=i)
            indexer = ""
            if "date" in temp_var_list:
                indexer += "**" + temp_var_list["date"] + "** - "
            if "title" in temp_var_list:
                indexer += "[" + temp_var_list["title"] + "](" + path + ")"
            else:
                indexer += "["
                indexer += " ".join(i.capitalize() for i in name.split("_"))
                indexer += "](" + path + ")"

            index_contents.append(indexer)

        # sort and put
        content += "\n* ".join(sorted(index_contents))
        return content
        
    def build_index(self, root_folder=None, module_name=None, index_html=True, index_md=True, PREFIX=False, vars_list={}):
        # sort_by="date"
        """
        Create index for a single module.
        """
        if type(root_folder) != str:
            raise Exception("No base folder specified")
        if type(module_name) != str:
            raise Exception("No module name specified")
        # ~ if !((sort_by == "date") or (sort_by == "title")):
            # ~ raise Exception("You can only sort between date and title!")

        if module_name != 'root':
            folder_base = osp.join(root_folder, module_name)
        else:
            # Root should already have an index.md
            return

        file_list = []
        if index_md:
            file_list =  self.get_files(root_folder=root_folder, ext="md", module=module_name)
        if index_html:
            file_list += self.get_files(root_folder=root_folder, ext="html", module=module_name)

        # Delist index page if there is one
        if "index.md" in file_list:
            file_list.remove("index.md")

        # Build index
        if (len(file_list) == 0):
            self.log.log("File list empty, making index anyway.")

        if not osp.exists(osp.join(folder_base, "index.template")):
            self.log.warning("Index template does not exist, "
                             "index won't be created.")
        else:
            vars_list["content"] = self.make_index_page(file_list, False, folder_base)

            # create index.md
            template_file = osp.join(folder_base, "index.template")
            with open(template_file, "r") as index_file:
                index_md = self.tools.process_vars(
                                index_file.read(),
                                var_list=vars_list,
                                set_var=False, file_name=template_file)
                self.log.log("Creating index.md entry for " + module_name)
                return index_md

    def build_page(self, source_file=None, template_file=None, vars_list={}):
        """
        Build single html page from a module
        Todo:
        """
        if type(source_file) != str:
            raise Exception("No source file specified")
        if type(template_file) != str:
            raise Exception("No template file specified")

        with open(source_file,"r") as doc:
            document = self.tools.convert_markdown_to_content(
                           doc.read(),
                           var_list=vars_list,
                           file_name=source_file)
            vars_list["content"] = document
            with open(template_file,"r") as x:
                template = x.read()
                document = self.tools.process_vars(template, set_var=True, var_list=vars_list, file_name=template_file)
                document = self.tools.process_vars(document, var_list=vars_list, file_name=template_file)
                return document

    def build_site(self, config=None, exclude=None, index_html=False, move_html=True, use_prefix=True, move_images=True):
        """ Generates a site based on a set configuration, explained in :obj:`Notes`.

            Parameters:
                config                (Config): Configuration object
                exclude       (list, optional): List of modules to be excluded
                    from the build.
                index_html              (bool): Whether or not to index HTML
                    files as well. Defaults to `False`.
                move_html               (bool): Whether or not to copy HTML
                    files to the build directory. Defaults to `True`.
                    **This will also be `True` if `index_html` is also
                    True**, since indexing to an invalid page might not
                    be desirable.
                use_prefix              (bool): Whether or not to include
                    the module's name in the path links. For example,
                    ``module/page.html`` instead of just ``page.html``. This
                    is especially useful if you have a ``<base href=\"...\">``
                    tag on your templates. Defaults to True.

            Returns:
                None, but outputs :obj:`index.html` on the source directory.

            Raises:
                ConfigInvalid: When `config` isn't a valid
                    :py:class:`~mdiocre.Config` object.

            Notes:
                In order for it to successfully build a site, the following
                parameters need to be set in the configuration file:
                    * :obj:`modules`
                    * :obj:`source-folder`
                    * :obj:`build-folder`
                    * :obj:`template-folder`
                    * :obj:`use-templates`

                Optionally, these parameters may also be used:

                    * :obj:`no-index`
                    * :obj:`vars`
                          Not a parameter, but a section defining
                          the variable names and its values. Internally,
                          this will always be used regardless.
"""
        if config is None:
            config = self.config
        if type(config) is not Config:
            raise ConfigInvalid("No configuration to use!")

        if index_html:
            move_html = True

        self.log.header("BUILD START", True)

        cfg      = config.config
        cfg_name = config.name
        self.log.header("Using configuration file: " + cfg_name, False)

        # setup required lists
        modules_list        = cfg["modules"]
        template_list       = cfg["use-templates"]
        vars_list           = cfg["vars"]
        source_base         = osp.realpath(cfg["source-folder"])
        build_base          = osp.realpath(cfg["build-folder"])
        template_base       = osp.realpath(cfg["template-folder"])

        # Index ignore list, has root by default
        index_ignore_list   = ["root"]
        try:
            index_ignore_list += cfg["no-index"]
            self.log.header("Index ignore list: " + str(index_ignore_list), False)
        except KeyError:
            self.log.warning("The 'no-index' option in config is not set, "
                             "continuing...")

        # list excluded modules
        if exclude:
            self.log.header("Excluded modules: " + str(exclude), False)
            if sorted(exclude) == sorted(modules_list):
                self.log.header("All modules excluded.", False)
            for i in exclude:
                try:
                    modules_list.remove(i)
                except Exception:
                    self.log.warning("Can't exclude " + i + ".")
        else:
            self.log.header("No excluded modules.", False)

        # PRE-BUILD
        self.log.header("PRE-BUILD CHECKS", True)

        # check sources
        self.log.name("Checking if source modules dir exists: ")
        for module in modules_list:
            if module == "root":
                self.tools.check_exists(
                                    source_base,
                                    "root sources", strict=True)
            else:
                self.tools.check_exists(
                                    osp.join(source_base, module),
                                    module + " source folder", strict=True)
                                    
        self.log.name("Checking if build modules dir exists: ")
        for module in modules_list:
            if module != "root":
                self.tools.check_exists(
                                    osp.join(build_base, module),
                                    module + " build folder")
                                    
        self.log.name("Checking for index templates: ")
        for module in modules_list:
            # root does not need an index template
            if module != "root":
                self.tools.check_exists(
                              osp.join(source_base, module, "index.template"),
                              "index.template for " + module,
                              create=False)
                              
        # check templates, order doesn't matter
        # templates MUST be in HTML
        try:
            for template in list(set(template_list)):
                self.log.name("Checking if template file exists: " + template)
                self.tools.check_exists(
                                   osp.join(template_base, template + ".html"),
                                   template,
                                   strict=True)
        except FileNotFound as e:
            self.log.error("Can't find template for " + template + " , could not continue.")
            return
            

        # BUILD
        self.log.header("BUILD", True)

        for module in modules_list:
            self.log.name("Build module " + module + "...")

            # Base dirs
            if module == "root":
                source_dir = source_base
                build_dir  = build_base
            else:
                source_dir = osp.join(source_base, module)
                build_dir  = osp.join(build_base, module)

            self.log.name("Make index...")
            if module not in index_ignore_list:
                module_index = self.build_index(root_folder=source_base,
                                                module_name=module,
                                                index_html=index_html,
                                                index_md=True,
                                                PREFIX=use_prefix,
                                                vars_list=vars_list)
                if type(module_index) is str:
                    with open(osp.join(source_dir, "index.md"), "w") as index_out:
                        index_out.write(module_index)
                        self.log.log("Written index to " + osp.join(source_dir, "index.md") + "!")
            else:
                self.log.log(module + " is in index ignore list, skipping!")

            self.log.name("Make pages...")
            # Determine which template to use
            if len(template_list) > 1:
                using_template = modules_list.index(module)
            else:
                using_template = 0
                
            # list pages
            page_list = self.get_files(root_folder=source_base, ext="md", module=module)
            template_name = template_list[using_template]
            use_template = osp.join(template_base, template_name + ".html")
            for name in page_list:
                source_file = osp.join(source_dir, name)
                build_file  = osp.join(build_dir, name.replace(".md",".html").replace(".MD",".html"))
                directory_name = osp.dirname(build_file)
                self.log.log("Building "+name+" with template "+template_name)
                self.tools.check_exists(directory_name, directory_name, quiet=1)
                with open(build_file, "w") as built:
                    doc = self.build_page(source_file=source_file, template_file=use_template, vars_list=vars_list)
                    built.write(doc)
                    self.log.log("Saved to "+build_file+"!")

            if move_html:
                ht_list = self.get_files(root_folder=source_base, ext="html", module=module)
                self.log.name("Copying html files.")
                if (len(ht_list) > 0):
                    for i in ht_list:
                        target = osp.join(source_dir, i)
                        ofile    = osp.join(build_dir, i)
                        self.tools.check_exists(osp.dirname(ofile), osp.dirname(ofile), quiet=1)
                        self.log.log(i+" -> "+ofile)
                        shutil.copyfile(target, ofile)
                else:
                    self.log.log("No html files to copy.")
            
            if move_images:
                im_list  = []
                for i in self.img_support:
                    im_list += self.get_files(root_folder=source_base, ext=i, module=module)
                    
                self.log.name("Copying images.")
                if (len(im_list) > 0):
                    for i in im_list:
                        target = osp.join(source_dir, i)
                        ofile    = osp.join(build_dir, i)
                        self.tools.check_exists(osp.dirname(ofile),osp.dirname(ofile),quiet=1)
                        self.log.log(i+" -> "+ofile)
                        shutil.copyfile(target, ofile)
                else:
                    self.log.log("No image files to copy.")

        self.log.header("Build done!", False)

    def clean_site(self, config=None, exclude=None, remove_index_pages=False, remove_images=True):
        """ Cleans the generated build directories.

            Parameters:
                config                (Config): Configuration object
                exclude       (list, optional): List of modules to be excluded
                    from the cleaning process.

            Returns:
                None, but build directory cleaned.

            Raises:
                ConfigInvalid: When `config` isn't a valid :py:class:`~mdiocre.Config` object.

        """
        if config is None:
            config = self.config
        if type(config) is not Config:
            raise ConfigInvalid("No configuration to use!")
        if not config.valid:
            raise ConfigInvalid("This is an invalid configuration!")

        self.log.header("CLEAN START", True)
        cfg      = config.config
        cfg_name = config.name

        self.log.header("Using configuration file: " + cfg_name, False)

        modules_list = cfg["modules"]
        build_base   = osp.realpath(cfg["build-folder"])
        source_base   = osp.realpath(cfg["source-folder"])

        if exclude:
            self.log.header("Excluded modules: " + str(exclude), False)
            if len(exclude) == len(modules_list):
                self.log.header("All modules excluded.", False)
            for i in exclude:
                try:
                    modules_list.remove(i)
                except Exception:
                    self.log.warning("Can't exclude " + i + ".")
        else:
            self.log.header("No excluded modules.", False)
        for module in modules_list:
            self.log.name("Removing module: " + module)
            mod_dir = osp.join(build_base, module)
            
            if remove_images:
                im_list  = []
                for i in self.img_support:
                    im_list += self.get_files(root_folder=build_base, ext=i, module=module)
                    
                self.log.name("Removing images.")
                if (len(im_list) > 0):
                    for i in im_list:
                        print(i)
                        #self.log.log("Removing " + i)
                        #shutil.rmtree(mod_dir, ignore_errors=True)
                else:
                    self.log.log("No image files to delete.")
                    
            if module != "root":
                try:
                    if self.tools.check_exists(mod_dir, module + " folder", strict=True, quiet=4):
                        self.log.log("Removing " + mod_dir)
                        shutil.rmtree(mod_dir, ignore_errors=True)
                except FileNotFound:
                    self.log.warning(osp.join(cfg["build-folder"], module) + " doesn't exist; no need to clean.")

                if remove_index_pages:
                    from os import remove
                    index_md = osp.join(source_base, module, "index.md")
                    try:
                        if self.tools.check_exists(index_md, "index.md", strict=True, quiet=4):
                            self.log.log("Removing index.md")
                            remove(index_md)
                    except FileNotFound:
                        self.log.warning(index_md + " doesn't exist; no need to clean.")
            else:
                from os import remove
                built_list = self.get_files(root_folder=build_base, ext="html", module=module)
                for html in built_list:
                    target = osp.join(build_base, html)
                    try:
                        if self.tools.check_exists(target, html, strict=True, quiet=4):
                            self.log.log("Removing " + target)
                            remove(target)
                    except FileNotFound:
                        self.log.warning(html + " doesn't exist; no need to clean.")

        self.log.header("Clean done!", False)
