#!/appl/splunk/bin/python
# -*- coding: utf-8 -*-
import os
import sys # for early exit
import maxminddb

import splunk.Intersplunk
import re

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

################################################################################
# OPTIONS
# ip=<ipfield> # use this field as the field with the urls. defaults to src_ip
# lang=<sprache>
# nomm # do not create the prefix 'mm_'
# debug # used for testing this python script


################################################################################
# ERRORCODS

################################################################################
# SETUP LOGGER

def setup_logging():
  """ initialize the logging handler """
  logger = logging.getLogger('splunk.maxmind')
  #SPLUNK_HOME = os.environ['SPLUNK_HOME']
  LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
  LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
  LOGGING_STANZA_NAME = 'python'
  LOGGING_FILE_NAME = "maxmind.log"
  BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
  LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
  splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
  splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
  logger.addHandler(splunk_log_handler)
  splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
  return logger


################################################################################
# METHODS, FUNCTIONS

################################################################################
# MAIN

def main():

  ################
  ## SET VARIABLES
  fldip = "src_ip"
  results = splunk.Intersplunk.readResults(None, None, True)
  keywords,kvs = splunk.Intersplunk.getKeywordsAndOptions()
  DEBUG = False
  MMPRE = "mm_"
  LANGLIST = ['ru','fr','en','pt-BR','zh-CN','de','ja','es']
  LANG = "de"
  DATABASE = SPLUNK_HOME+"etc/apps/SplunkDataenrichment/lookups/GeoLite2-City.mmdb"


  ##################
  ## CHECK VARIABLES

  # used for testing new features
  if "debug" in keywords:
    DEBUG=True
    logger.debug("ID="+ID+" DEBUGMODE=True")

  if "nomm" in keywords:
    MMPRE = ""
    logger.info("ID="+ID+" nomm=true");

  if "ip" in kvs:
    fldip = kvs["ip"]
    logger.debug("ID="+ID+" IPFIELD="+fldip)

  if "lang" in kvs:
    if not kvs["lang"] in LANGLIST:
      logger.error("ID="+ID+" ERROR=\"Lang not found\" lang=\""+kvs['lang']+"\"")
      sys.exit("ERROR: Sprache nicht bekannt! Bitte nutze eines von: "+str(LANGLIST))
    else:
      LANG = kvs["lang"]
      logger.debug("ID="+ID+" LANGUAGE="+LANG)


  ##############
  ## OPEN READER

  reader = maxminddb.open_database(DATABASE,maxminddb.MODE_FILE);


  #############################
  #############################
  ## ITERATE THROUGH EACH EVENT

  for res in results:
    try:
      ip = res[fldip]
      data = reader.get(ip)

      if "country" in data and "names" in data['country'] and LANG in data['country']['names']:
        country_name = data['country']['names'][LANG]
        res[MMPRE+"country"] = country_name

      if "country" in data and "iso_code" in data['country']:
        country_code = data['country']['iso_code']
        res[MMPRE+"country_code"] = country_code

      if "continent" in data and "names" in data['continent']:
        continent_name = data['continent']['names'][LANG]
        res[MMPRE+"continent"] = continent_name

      if "continent" in data and "code" in data['continent']:
        continent_code = data['continent']['code']
        res[MMPRE+"continent_code"] = continent_code

      if "registered_country" in data and "iso_code" in data['registered_country']:
        registered_country_iso_code = data['registered_country']['iso_code']
        res[MMPRE+"registered_country_iso_code"] = registered_country_iso_code

      if "registered_country" in data and "names" in data['registered_country'] and LANG in data['registered_country']['names']:
        registered_country_name = data['registered_country']['names'][LANG]
        res[MMPRE+"registered_country_name"] = registered_country_name

      if "location" in data and "latitude" in data['location']:
        latitude = data['location']['latitude']
        res[MMPRE+"latitude"] = latitude

      if "location" in data and "longitude" in data['location']:
        longitude = data['location']['longitude']
        res[MMPRE+"longitude"] = longitude
      
  
    except:
      pass

  reader.close
  splunk.Intersplunk.outputResults(results)


if __name__ == "__main__":
  SPLUNK_HOME = "/appl/splunk/"
  PYTHONPATH = "/appl/splunk/lib/python27.zip:/appl/splunk/lib/python2.7:/appl/splunk/lib/python2.7/plat-sunos5:/appl/splunk/lib/python2.7/lib-tk:/appl/splunk/lib/python2.7/lib-old:/appl/splunk/lib/python2.7/lib-dynload:/appl/splunk/lib/python2.7/site-packages"
  logger = setup_logging()
  tstart = datetime.now()
  ID = str(tstart.year)+str(tstart.month)+str(tstart.day)+str(tstart.hour)+str(tstart.minute)+str(tstart.second)+str(tstart.microsecond)
  logger.debug("NEWRUN ############### ID="+ID)
  main()
  tend = datetime.now()
  period = tend - tstart
  logger.info("ID="+ID+" STATE=FINISHED SUCCESS=true durationmicrosec="+str(period.microseconds))
