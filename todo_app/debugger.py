
import logging 

debuglevel = 2
logging.basicConfig(filename='todo.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')

if debuglevel>0: print (f'DEBUG ON - level {debuglevel}')
logging.info(f'DEBUG ON - level {debuglevel}')

def writelog(context, doing, varname, var): 
    if debuglevel > 0: 
        outstring = (f'DEBUG\n  WHERE:    {context} \n  WHAT:     {doing} \n  VARNAME:  {varname} \n  TYPE:     {type(var)} \n  CONTENTS: {var}')
        print(outstring)
        logging.info(outstring)