import json, os, sys, atexit, threading
import datetime, time
import logging
from logging.handlers import RotatingFileHandler
import argparse

import wins_query as winsq 
import wins_UI as winsui
from daemonize import daemon


class D(daemon):

    def __init__(self, args):
        logging.debug("MAIN.D.__init__:start_init")
        super(D,self).__init__()
        self.pidfile = args.pidfile
        self.conf_Path = args.config
        self.out_Dir = args.out_Dir

        self.config = {}

        #logging.getLogger().addHandler(logging.StreamHandler()) # write to stderr
        
        try:
            handler = RotatingFileHandler(args.log, maxBytes=24000, backupCount=5)
            logging.getLogger().addHandler(handler) # log file
        except:
            logging.exception("MAIN.D.__init__:cannot_create_logfile")
            sys.exit(0)

        level = logging.WARNING-10*args.v   # logging level
        if args.v:
            logging.info("MAIN.D.__init__:logging_level_change:"+str(level))
        else:
            sys.tracebacklimit = 0
        logging.getLogger().setLevel(level)

        logging.debug("MAIN.D.__init__:complete_init")

    def config_setup(self):
        logging.debug("MAIN.D.config_setup:start_setup")
        try:
            with open(self.conf_Path) as fp:
                self.config = json.load(fp)
            atexit.register(self._config_record) # record the config when exiting
        except Exception as exp:
            logging.error("MAIN.D.config_setup:Failed_to_read_config:{}".format(exp))
            sys.exit(0)

        logging.debug("MAIN.D.config_setup:complete_setup")
    
    def _config_record(self):
        if self.config:
            with open(self.conf_Path, "w") as fp:
                json.dump(self.config,fp, indent=4)

    def run(self):
        logging.debug("MAIN.D.run:start_run")
        # Set up
        self.config_setup()
        if not os.path.isdir(self.out_Dir):
            logging.error("MAIN.D.run:Output_Directory_DNE")
            sys.exit(0)
        winserver = self.config["winserver"]
        winsq.login(host = winserver["host"], user = winserver["user"], password = winserver["password"])
        
        # Start ui thread
        try:
            winsui.app._config = self.config["winserver_probe"] # copy config
            ui = threading.Thread(target=winsui.app.run, kwargs=winserver["UI_address"])
            ui.setDaemon(True)
            ui.start()
        except:
            logging.exception("MAIN.D.run:UI_thread_error")
            sys.exit(1)
        logging.warning("MAIN.D.run:UI_is_now_running")

        # loop runs every 1 minute
        while(True):
            thd = threading.Thread(target=winsq.bulk_query, args=(self.config["winserver_probe"], self.out_Dir))
            try:thd.start()
            except:
                logging.exception("MAIN.D.run:Error_while_query")
                sys.exit(1)
            # timer
            now = datetime.datetime.now()
            delta = datetime.timedelta(minutes=1) - datetime.timedelta(seconds=now.second, microseconds=now.microsecond)
            time.sleep(delta.total_seconds())

if __name__ == "__main__":
    assert (2, 6) <= sys.version_info < (2, 8)
    main_path = os.path.realpath(__file__)
    prj_dir_path = os.path.dirname(main_path)

    parser = argparse.ArgumentParser(description='Connect to powershell on a remote Windows Server.',usage='%(prog)s [-h] [options] {start,stop,restart,daemon}')
    parser.add_argument('command', choices=["start","stop","restart","daemon"],
        help='Commands of this program')
    parser.add_argument("-c","--config", metavar='\b',
        default=os.path.join(prj_dir_path,"midware.conf"), help='change config file path')
    parser.add_argument("-l","--log", metavar='\b',
        default=os.path.join(prj_dir_path,".midware.log"), help='change log file path')
    parser.add_argument("-o","--out_Dir", metavar='\b',
        default=os.path.join(prj_dir_path,"probe/"), help='change output directory path')
    parser.add_argument("-p","--pidfile", metavar='\b',
        default=os.path.join(prj_dir_path,".pidfile"), help='change pidfile path')
    parser.add_argument("-v", action="count", default=0, help='logging level')

    args = parser.parse_args()
    APP = D(args)
    logging.debug("Start_with_command:"+args.command)
    if args.command == "daemon":
        APP.start()
    elif args.command == "restart":
        APP.restart()
    elif args.command == "stop":
        APP.stop()
    elif args.command == "start":
        APP.start(if_daemon=False)