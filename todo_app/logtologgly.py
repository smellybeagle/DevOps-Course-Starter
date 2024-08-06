import logging,logging.config
import os,time
from loggly.handlers import HTTPSHandler
from logging import Formatter



logger = logging.getLogger('loginfo.log')

debuglevel=logger.setLevel=os.getenv('LOG_LEVEL')
#Formatter.converter= time.gmtime


def num_in_words(no):
    if(no=='NOTSET'):
        return 1
    elif(no=='DEBUG'):
        return 2
    elif(no=='INFO'):
        return 3
    elif(no=='WARNING'):
        return 4
    elif(no=='ERROR'):
        return 5
    elif(no=='CRITICAL'):
        return 6
    else:
        return 2
        
loglevel=num_in_words(debuglevel)
#loglevel=2     

if loglevel> 0: print (f'LOGGING ON - level {debuglevel}')
logging.info(f'LOGGING ON - level {debuglevel}')

token = os.getenv('LOGGLY_TOKEN')
args=('https://logs-01.loggly.com/inputs/[{token}]/tag/todo-app/','POST')

def logtologgly(context,doing,varname,var):
    if loglevel>0:
        outstring = (f'TODO-APP\n WHERE: {context} \n WHAT: {doing} \n VARNAME: {varname} TYPE: \n {type(var)} \n CONTENTS: {var}')
        print(outstring)
        logging.info(outstring)
    if token is not None:
        handler = HTTPSHandler(args)
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )