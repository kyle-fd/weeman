#
# shell.py - the weeman main shell
#
# This file if part of weeman project
#
# See 'LICENSE' file for copying 
#

import sys
import os
from core.complete import complete
from core.complete import array 
from core.config import __version__
from core.config import __codename__
from core.misc import printt
from core.misc import print_help
from core.misc import print_help_option
from core.config import url
from core.config import action_url
from core.config import port
from core.config import user_agent
from core.config import html_file
from core.config import quiet_mode
from core.config import say
from core.httpd import weeman

# Prompt
PROMPT_P = "( weeman ) : "

def print_startup():
    """
        Print the startup banner
    """
    print("\033[H\033[J") # Clear the screen
    print("\033[01;31m")
    sys.stdout.write(open("core/logo.txt", "r").read()[:-1])
    print("\033[00m") 
    sys.stdout.write("\033[01;37m\t\t     (%s-%s)\n\033[00m" %(__version__,  __codename__))
    print("\033[01;37m\t<><><><><><><><><><<><><><><><><><><>\033[00m")
    print("\t\'%s\'" %say)
    print("\033[01;37m\t<><><><><><><><><><<><><><><><><><><>\n\033[00m")

def shell_noint(options):
    global url
    global port
    global action_url
    global user_agent
    global html_file

    url = options.url
    action_url = options.action_url
    port = int(options.port)
    user_agent = options.user_agent
    html_file = options.html_file

    try:
        print_startup()
        s = weeman(url,port)
        s.clone()
        s.serve()

    except KeyboardInterrupt:
        s = weeman(url,port)
        s.cleanup()
        print("\nInterrupt ...")
    except IndexError:
        if prompt[0] == "help" or prompt[0] == "?":
            print_help()
        else:
            printt(3, "Error: please provide option for \'%s\'." %prompt[0])
    except Exception as e:
        printt(3, "Error: (%s)" %(str(e)))

def shell():
    """
        The shell, parse command line args,
        and set variables.
    """
    global url
    global port
    global action_url
    global user_agent
    global html_file

    print_startup()
    complete(array)

    if os.path.exists("history.log"):
        if  os.stat("history.log").st_size == 0:
            history = open("history.log", "w")
        else:
            history = open("history.log", "a")
    else:
        history = open("history.log", "w")

    while True:
        try:
            an = raw_input(PROMPT_P)
            prompt = an.split()
            if not prompt:
                print("Error: What? try help.")
            elif prompt[0] == ";" or prompt[0] == "clear":
                print("\033[H\033[J")
            elif prompt[0] == "q" or prompt[0] == "quit":
                printt(2,"bye bye!")
                break;
            elif prompt[0] == "help" or prompt[0] == "?":
                if prompt[1]:
                    print_help_option(str(prompt[1]))
                else:
                    print_help()
            elif prompt[0] == "show":
                l = 20
                sys.stdout.write("\033[01;37m\t")
                print("-" * l)
                print("\turl        : %s " %url)
                print("\tport       : %d " %(port))
                print("\taction_url : %s " %(action_url))
                print("\tuser_agent : %s " %(user_agent))
                print("\thtml_file  : %s " %(html_file))
                sys.stdout.write("\t")
                print("-" * l)
                sys.stdout.write("\033[01;00m")
            elif prompt[0] == "set":
                if prompt[1] == "port":
                    port = int(prompt[2])
                    ## Check if port == 80 and not running as root
                    if port == 80 and os.getuid() != 0:
                        printt(2, "Permission denied, to bind port 80, you need to run weeman as root.");
                    history.write("port = %s\n" %port)
                if prompt[1] == "url":
                    url = str(prompt[2])
                    history.write("url = %s\n" %url)
                if prompt[1] == "action_url":
                    action_url = str(prompt[2])
                    history.write("action_url = %s\n" %action_url)
                if prompt[1] == "user_agent":
                    prompt.pop(0)
                    u = str()
                    for x in prompt:
                        u+=" "+x
                    user_agent = str(u.replace("user_agent", ""))
                    history.write("user_agent = %s\n" %user_agent)
                if prompt[1] == "html_file":
                    html_file = str(prompt[2])
            elif prompt[0] == "run" or prompt[0] == "r":
                if not url:
                    printt(3, "Error: \'url\' Can't be \'None\', please use \'set\'.")
                elif not action_url:
                    printt(3, "Error: \'action_url\' Can't be \'None\', please use \'set\'.")
                else:
                    # Here we start the server (:
                    s = weeman(url,port)
                    s.clone()
                    s.serve()
            elif prompt[0] == "banner" or prompt[0] == "b":
                print_startup()
            else:
                print("Error: \'%s\' What? try help." %prompt[0])

        except KeyboardInterrupt:
            s = weeman(url,port)
            s.cleanup()
            print("\nInterrupt ...")
        except IndexError:
            if prompt[0] == "help" or prompt[0] == "?":
                print_help()
            else:
                printt(3, "Error: please provide option for \'%s\'." %prompt[0])
        except Exception as e:
            printt(3, "Error: (%s)" %(str(e)))
