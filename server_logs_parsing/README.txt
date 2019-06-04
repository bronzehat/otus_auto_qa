This is short instruction for server_log_parsing utility.
Commandline options to run utility (no slashes in path's end or file's beginning):

    cd <utility directory in which test_parsed.py is located>
    pytest -s -v --dir (nothing or path to directory with file) --file (nothing or filename)

or you can not go to utility's directory and run it from any directory, just adding path to test_parser.py in the end:

    pytest -s -v --dir (nothing or path to directory with file) --file (nothing or filename) <path to test_parser.py>

How you can use command line otions:

    if --dir is not set, but --file is set      ==> parses --file in current directory
    if --dir is set, but --file is not set      ==> parses all files in --dir
    if --dir is set and --file is set           ==> parses --file in --dir
    if --dir is not set, and --file is not set  ==> throws an exception and sends you to read this file
    (if you have come here after it, say "cheeeeze")

utility running commands examples:

    pytest -s -v --dir G:\Prog\Coder\OTUS_Autotests\otus_auto_qa\server_logs_parsing\logs_to_parse

    pytest -s -v --file access.log

The result json-file is log_parse.json - you can open it by text editor or by browser.
