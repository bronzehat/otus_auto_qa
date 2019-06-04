This is short instruction for server_log_parsing utility.
There are 2 ways to run it:
1) with python's pytest module
2) with python's argparse module

Common for each method:

    How you can use command line otions:
        if --dir is not set, but --file is set      ==> parses --file in current directory
        if --dir is set, but --file is not set      ==> parses all files in --dir
        if --dir is set and --file is set           ==> parses --file in --dir
        if --dir is not set, and --file is not set  ==> throws an exception and sends you to read this file
        (if you have come here after it, say "cheeeeze")


Below are the instructions for each of given methods.
************************************************************************************************************************

1) pytest
    Commandline options to run utility (no slashes in path's end or file's beginning):

        cd <utility directory in which test_parsed.py is located>
        pytest -s -v --dir (nothing or path to directory with file) --file (nothing or filename)

    or you can not go to utility's directory and run it from any directory, just adding path to test_parser.py in the end:

        pytest -s -v --dir (nothing or path to directory with file) --file (nothing or filename) <path to test_parser.py>

    utility running commands examples:

        pytest -s -v --dir G:\Prog\Coder\OTUS_Autotests\otus_auto_qa\server_logs_parsing\logs_to_parse

        pytest -s -v --file access.log

    The result json-file is a separate file for each parsed logfile,
    it's named as "log_parse_<TIMESTAMP_OF_FILE'S_LAST_STRING>.json",
    you can open it by text editor or by browser.

***********************************************************************************************************************

2) argparse

    - add Python installed directory (for me it's C:\Users\<user>\AppData\Local\Programs\Python\Python36\)
      in "Path" environment variable
    or
    - go to the directory in which Python is installed
      (you can move the test_logparse_with_argparse.py in that directory and run it from any directory

    utility running commands examples:

      test_logparse_with_argparse.py --dir G:\Prog\Coder\OTUS_Autotests\otus_auto_qa\server_logs_parsing\logs_to_parse

      (use <path_to_test_logparse_with_argparse.py> instead of test_logparse_with_argparse.py if you're not in the
      directory where this file is, and if Python installation directory isn't in Path variable)

    The result json-file is log_parse.json - you can open it by text editor or by browser.

***********************************************************************************************************************