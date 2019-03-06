import sys
import shutil
from os import path as osp
from os import walk as osw
from .utils import Utils
from .config import Config
from .logger import Debug
from .exception import *

# TODO: Dev routine to build individual pages


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
        ConfigInvalid: When `config` isn't a valid :py:class:`~mdiocre.Config` object.
    """
    def __init__(self, config=None, logger=Debug(True)):
        self.log = logger
        if type(config) is Config:
           self.config = config
        else:
           raise ConfigInvalid("Invalid configuration type!")
        self.tools = Utils(logger=logger)

    def build_index(self, config, folder_base=None):
        """
        Todo:
           Make this function. Move
           the index generation part of
           :py:func:`build_site` here
        """
        if type(folder_base) != str:
            self.log.error("No base folder specified")
        if config == None:
           config = self.config
        if type(config) is not Config:
           raise ConfigInvalid("No configuration to use!")

    def build_page(self, config):
        """
        Todo:
           Make this function. Maybe move
           the page generation part of
           :py:func:`build_site` here?
        """
        pass

    def build_site(self, config=None, exclude=None, index_html=False, move_html=True, use_prefix=True):
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
        if config == None:
           config = self.config
        if type(config) is not Config:
           raise ConfigInvalid("No configuration to use!")

        if index_html:
            move_html = True

        from glob import glob

        self.log.header("BUILD START", True)

        cfg      = config.config
        cfg_name = config.name

        self.log.header("Using configuration file: "+cfg_name,False)

        # setup lists
        # (Required)
        modules_list        = cfg["modules"]
        template_list       = cfg["use-templates"]
        vars_list           = cfg["vars"]
        source_base         = osp.realpath(cfg["source-folder"])
        build_base          = osp.realpath(cfg["build-folder"])
        template_base       = osp.realpath(cfg["template-folder"])

        # (Optional)
        index_ignore_list   = ["root"]
        try:
            index_ignore_list += cfg["no-index"]
            self.log.header("Index ignore list: "+str(index_ignore_list), False)
        except KeyError:
            self.log.warning("The 'no-index' option in config is not set, continuing...")

        # setup base dirs


        # set html link prefix, useful with html baseurl or whatever it's called
        PREFIX = use_prefix

        # list excluded modules
        if exclude:
            self.log.header("Excluded modules: "+str(exclude),False)
            if len(exclude) == len(modules_list):
                self.log.header("All modules excluded.",False)
            for i in exclude:
                try:
                    modules_list.remove(i)
                except Exception:
                    self.log.warning("Can't exclude "+i+".")
        else:
            self.log.header("No excluded modules.",False)

        # pre-build process
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
                                    osp.join(source_base,module),
                                    module+" source folder", strict=True)
        # TODO: check whether this needs a strict param.

        self.log.name("Checking if build modules dir exists: ")
        for module in modules_list:
            if module != "root":
                self.tools.check_exists(
                                    osp.join(build_base,module),
                                    module+" build folder")

        self.log.name("Checking for index templates: ")
        for module in modules_list:
        # root does not need an index template
            if module != "root":
                self.tools.check_exists(
                              osp.join(source_base,module,"index.template"),
                              module+" index.template",
                              create=False)

        # check templates, order doesn't matter
        try:
            for template in list(set(template_list)):
                self.log.name("Checking if template file exists: "+template)
                self.tools.check_exists(
                                   osp.join(template_base,template+".html"),
                                   template,
                                   strict=True)
        except FileNotFound as e:
            self.log.error("Can't find template for "+template+" , could not continue.")
            return

        # build process
        self.log.header("BUILD", True)
        for module in modules_list:
        # init dirs
            if module == "root":
                source_dir = source_base
                build_dir  = build_base
            else:
                source_dir = osp.join(source_base, module)
                build_dir  = osp.join(build_base, module)

        # list files
            md_list = []
            if module != "root":
                for walk in osw(source_dir):
                    for name in walk[2]:
                        if name[-3:].lower() == ".md":
                            md_list.append(
                                osp.join(osp.basename(walk[0]).replace(module,""),name))
            else:
                md_list = glob(source_dir+"/*.md")+glob(source_dir+"/*.MD")

            # uhh wtf
            if index_html or move_html:
                #if module != "root":
                #    for walk in osw(source_dir):
                #        for name in walk[2]:
                #            if name[-5:].lower() == ".html":
                #                ht_list.append(
                #                    osp.join(osp.basename(walk[0]).replace(module,""),name))
                #else:
                ht_list = glob(source_dir+"/*.html")+glob(source_dir+"/*.HTML")

            # caveat: html files can only be indexed if there is a single markdown page

        # delist index page if there is one
        # except for root
            if module != "root":
                if "index.md" in md_list:
                    md_list.remove("index.md")
            #if source_dir+"/index.html" in md_list:
            #    ht_list.remove(source_dir+"/index.html")

        # build module
            self.log.name("Building module "+module+".")
            content = "\n"                                  # init content buffer

            if module in index_ignore_list:
        # INDEX IGNORED
                if (len(md_list) == 0):
                    self.log.log("File list empty and module ignored, skipping.")
                else:
                    self.log.log("Module in index ignore list. Skipping.")
            else:
        # INDEXED
                if (len(md_list) == 0):
                    self.log.log("File list empty, making index anyway.")
                if not osp.exists(osp.join(source_dir,"index.template")):
                    self.log.warning("Index template for module "+module+" does not exist, index won't be created.")
                else:
                    self.log.log("Making index...")
                    content = "* "
                    index_contents = []
            # make index of pages (markdown)
                    for i in md_list:
                        temp_var_list = {}
                        basename = osp.basename(i)
                        name = basename
                        actual_name = i.replace(".md",".html").replace(".MD",".html")
                        if PREFIX:
                            path = module+"/"+actual_name
                        else:
                            path = actual_name
                        self.log.log("Add entry for "+name)
                # scan files for title and date
                        with open(osp.join(source_dir,i),"r") as file:
                            self.tools.process_vars(
                                           file.read(),
                                           var_list=temp_var_list,
                                           set_var=True, file_name=i)
                        indexer = ""
                        if "date" in temp_var_list:
                            indexer += "**"+temp_var_list["date"]+"** - "
                        if "title" in temp_var_list:
                            indexer += "["+temp_var_list["title"]+"]("+path+")"
                        else:
                            indexer += "["+" ".join(i.capitalize() for i in name.split("_"))+"]("+path+")"
                        index_contents.append(indexer)

            # make index of pages (html)
                    if index_html:
                        for i in ht_list:
                            temp_var_list = {}
                            basename = osp.basename(i)
                            name = basename.replace(".html","")
                            if PREFIX:
                                path = module+"/"+basename
                            else:
                                path = basename
                            self.log.log("Add entry for "+name)
                # scan files for title and date
                            with open(osp.join(source_dir,i),"r") as file:
                                self.tools.process_vars(
                                           file.read(),
                                           var_list=temp_var_list,
                                           set_var=True, file_name=i)
                            indexer = ""
                            if "date" in temp_var_list:
                                indexer += "**"+temp_var_list["date"]+"** - "
                            if "title" in temp_var_list:
                                indexer += "["+temp_var_list["title"]+"]("+path+")"
                            else:
                                indexer += "["+" ".join(i.capitalize() for i in name.split("_"))+"]("+path+")"
                            index_contents.append(indexer)

            # sort and put
                    content += "\n* ".join(sorted(index_contents))
                    vars_list["content"] = content

            # create index.md
                    template_file = osp.join(source_dir,"index.template")
                    with open(template_file,"r") as index_file:
                        index_md = self.tools.process_vars(
                                      index_file.read(),
                                      var_list=vars_list,
                                      set_var=False, file_name=template_file)
                        self.log.log("Creating index.md entry for "+module)
                        with open(osp.join(source_dir,"index.md"),"w") as f:
                            f.write(index_md)
                            md_list.append("index.md")

            # build html pages
            for i in md_list:
                # init
                if module == "root":
                    i = osp.basename(i)

                vars_list["content"],vars_list["title"],vars_list["date"] = "","",""
                name = i.replace(".md",".html")

                # template settings
                if len(template_list) > 1:
                    using_template = modules_list.index(module)
                else:
                    using_template = 0

                # build pages
                self.log.log("Building "+name+" with template "+template_list[using_template])

                with open(osp.join(source_dir,i),"r") as doc:
                    document = self.tools.convert_markdown_to_content(
                               doc.read(),
                               var_list=vars_list,
                               file_name=i)
                vars_list["content"] = document
                cur_template = osp.join(template_base, template_list[using_template]+".html")
                with open(cur_template,"r") as x:
                    template = x.read()
                    document = self.tools.process_vars(template, set_var=True, var_list=vars_list, file_name=cur_template)
                    document = self.tools.process_vars(document, var_list=vars_list, file_name=cur_template)

                directory_name = osp.join(build_dir, osp.dirname(name))
                self.tools.check_exists(directory_name, directory_name, quiet=1)
                with open(osp.join(build_dir, name), "w") as output:
                    output.write(document)
            if move_html:
                self.log.name("Copying html files.")
                if (len(ht_list) > 0):

                    for i in ht_list:
                        basename = osp.basename(i)
                        ofile    = osp.join(build_dir, basename)
                        self.log.log(i+" -> "+ofile)
                        shutil.copyfile(i, ofile)
                else:
                    self.log.log("No html files to copy.")

        self.log.header("Build done!",False)

    def clean_site(self, config=None, exclude=None):
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
        if config == None:
           config = self.config
        if type(config) is not Config:
           raise ConfigInvalid("No configuration to use!")

        if not config.valid:
           raise ConfigInvalid("This is an invalid configuration!")

        self.log.header("CLEAN START", True)
        cfg      = config.config
        cfg_name = config.name

        self.log.header("Using configuration file: "+cfg_name,False)

        modules_list = cfg["modules"]
        build_base   = osp.realpath(cfg["build-folder"])

        if exclude:
            self.log.header("Excluded modules: "+str(exclude),False)
            if len(exclude) == len(modules_list):
                self.log.header("All modules excluded.",False)
            for i in exclude:
                try:
                    modules_list.remove(i)
                except Exception:
                    self.log.warning("Can't exclude "+i+".")
        else:
            self.log.header("No excluded modules.",False)

        for module in modules_list:
            self.log.name("Removing module: "+module)
            mod_dir = osp.join(build_base,module)
            if module != "root":
                try:
                    if self.tools.check_exists(mod_dir, module+" folder", strict=True, quiet=4):
                        self.log.log("Removing "+mod_dir)
                        shutil.rmtree(mod_dir, ignore_errors=True)
                except FileNotFound:
                    self.log.warning(osp.join(cfg["build-folder"],module)+" doesn't exist; no need to clean.")
            else:
                from glob import glob
                from os import remove
                built_list = glob(build_base+"/*.html")
                for html in built_list:
                    try:
                        if self.tools.check_exists(html, html, strict=True, quiet=4):
                            self.log.log("Removing "+html)
                            remove(html)
                    except FileNotFound:
                        self.log.warning(html+" doesn't exist; no need to clean.")

        self.log.header("Clean done!",False)
