#!/bin/python3
import os
import shutil
import sys
import argparse as ap
import mdiocre

VERSION = [0, 2, 0, "2019.03.07"]

class Parse(ap.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def create_objects(args):
    """
    Parameters:
        args (Namespace): passed from ArgumentParser
    """
    global log
    global config
    global wizard
    if type(args.logfile) is str:
       log     = mdiocre.Debug(debug=args.detail, file_name=os.path.realpath(args.logfile))
    else:
       log     = mdiocre.Debug(debug=args.detail, file_name=None)
    config     = mdiocre.Config(args.site_config, logger=log)
    wizard     = mdiocre.Wizard(config=config, logger=log)

def build_site(args):
    if type(args.exclude) is str:
        excludes = list(i.replace(" ","") for i in args.exclude.split(","))
    else:
        excludes = None
    wizard.build_site(exclude=excludes,
                      index_html=args.include_html,
                      move_html=args.copy_html,
                      use_prefix=args.use_prefix)

def clean_site(args):
    if type(args.exclude) is str:
        excludes = list(i.replace(" ","") for i in args.exclude.split(","))
    else:
        excludes = None
    wizard.clean_site(exclude=excludes, remove_index_pages=args.clean_index)

def none_mode(args):
    print("\nPlease specify a command to use!\nAvailable commands are:\n\tbuild\n\tclean")
    print("\nCurrently displaying set command line arguments:\n")
    print("="*10 + " GENERAL " + "="*10)
    print("Detail   (-d) :",args.detail)
    print("App  Config   (-c) :",args.config)
    print("Site Config   (-c) :",args.site_config)
    print("Log file (-l) :",args.logfile)

def main():
    # Default options

    loaded_opts = {"mdiocre": {"detail":False, "config":"config.ini", "logfile":None},\
                 "build":   {"include-html":False, "copy-html":False, "build-exclude":None, "use-prefix":True},\
                 "clean":   {"clean-exclude":None, "clean-index":True}}

    main_opts = loaded_opts["mdiocre"]
    build_opts = loaded_opts["build"]
    clean_opts = loaded_opts["clean"]

    # program parser
    p = Parse(prog="mdiocre",
              description = "Automated static website building tool using the"
                            " Markdown format."
             )
    p.add_argument(
                      "-v", "--version",
                      help="Display the version number",
                      action="version",
                      version="%(prog)s "
                              +str(VERSION[0])+"."
                              +str(VERSION[1])+"."
                              +str(VERSION[2])+", "
                              +"released "+VERSION[3]
                      )
    p.add_argument('-C', '--config',
                       help='use custom app configuration file')
    p.add_argument('-c', '--site-config',
                       help='use custom site configuration file')
    p.add_argument('-d', '--detail',
                       action='store_true',
                       help='display actions performed in more detail')
    p.add_argument('-l', '--logfile',
                       help='log action messages to a file in the root directory')
    

    p_subs  = p.add_subparsers()

    p_build = p_subs.add_parser(
                  "build",
                  description="Build the website"
                              " and its modules.",
                  help="build website")
    p_build.add_argument(
                "-x", "--exclude",
                help="exclude building these modules : "
                     "list of modules separated by commas")
    p_build.add_argument(
                "-i", "--include-html",
                action="store_true",
                help="Include HTML files in the index. This will also copy the indexed html into the build directory!"
                )
    p_build.add_argument(
                "-c", "--copy-html",
                action="store_true",
                help="Copy any HTML file present in the source directories to the respective build directories."
                )
    p_build.add_argument(
                "-p", "--use-prefix",
                action="store_true",
                help="Use module prefixes in built files"
                )
    
    p_clean = p_subs.add_parser(
                  "clean",
                  help="clean built site")
    p_clean.add_argument(
                "-x", "--exclude",
                help="only clean these modules : "
                "list of modules separated by spaces")
    p_clean.add_argument(
                "-i", "--clean-index",
                action="store_true",
                help="Also clean index.md files"
                )

    p.set_defaults(config="mdiocre.ini", mode=None, run=none_mode)
    p_build.set_defaults(run=build_site, mode="building")
    p_clean.set_defaults(run=clean_site, mode="cleaning")
    
    # print help if invokes without commands
    if len(sys.argv)==1:
        p.print_help(sys.stderr)
        sys.exit(1)
    
    o = p.parse_args() # parse cmdline options
    
    import configparser as cp
    config = cp.ConfigParser()
    config.read(o.config)
    # uh what
    try: loaded_opts["mdiocre"]["detail"]  = config.getboolean("mdiocre", "detail")
    except Exception: pass
    try: loaded_opts["mdiocre"]["config"]  =        config.get("mdiocre", "config")
    except Exception: pass
    try: loaded_opts["mdiocre"]["logfile"] =        config.get("mdiocre", "logfile")
    except Exception: pass

    try: loaded_opts["build"]["include-html"]  = config.getboolean("build", "include-html")
    except Exception: pass
    try: loaded_opts["build"]["copy-html"]     = config.getboolean("build", "copy-html")
    except Exception: pass
    try: loaded_opts["build"]["build-exclude"] = config.get("build", "build-exclude")
    except Exception: pass
    try: loaded_opts["build"]["use-prefix"]    = config.getboolean("build", "use-prefix")
    except Exception: pass

    try: loaded_opts["clean"]["clean-exclude"]  = config.get("clean", "clean-exclude")
    except Exception: pass
    try: loaded_opts["clean"]["clean-index"]  = config.getboolean("clean", "clean-index")
    except Exception: pass
    
    main_opts = loaded_opts["mdiocre"]
    build_opts = loaded_opts["build"]
    clean_opts = loaded_opts["clean"]
    
    p.set_defaults(config="mdiocre.ini",
                   site_config=main_opts["config"],
                   detail=main_opts["detail"],
                   logfile=main_opts["logfile"], mode=None, run=none_mode)
    p_build.set_defaults(exclude=build_opts["build-exclude"],
                         include_html=build_opts["include-html"],
                         copy_html=build_opts["copy-html"],
                         use_prefix=build_opts["use-prefix"],run=build_site, mode="building")
    p_clean.set_defaults(exclude=clean_opts["clean-exclude"],
                         clean_index=clean_opts["clean-index"],run=clean_site, mode="cleaning")

    o = p.parse_args() # parse cmdline options
    
    #print("o contains", str(o))
    #print("loaded opts contains", str(loaded_opts))
    #exit()
    
    create_objects(o)

    try:
        create_objects(o)
    except mdiocre.exception.ConfigInvalid as e:
        print(e.__str__()+"\nPlease select a correct config file by using mdiocre -c")
        return
    except Exception as e:
        print("ERROR INITIALIZING!\n"+e.__str__())
        return

    if o.mode:
        log.header("\nMDiocre version "+str(VERSION[0])+"."
                              +str(VERSION[1])+"."
                              +str(VERSION[2])+" starting in "+o.mode+" mode!",False)
    try:
         o.run(o)
    except Exception as e:
        log.error(e.__str__())
        log.error("An error occured, quitting...")

if __name__ == '__main__':
    main()
