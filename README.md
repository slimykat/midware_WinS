# midware_WinS

## Components
- midware_WinS/
**program modules :**
    - wins_main.py
    - wins_query.py
    - wins_UI.py
    - daemonize.py
**config and log file:**
    - midware.conf
    - config.json
    - .midware.log
**default output directory:**
    - probe/

## Usage

### 1. starting the service
midware_WinS is designed to run under python 2 envirionment:
```python
assert((2, 6) <= sys.version_info < (2, 8))
```
Additional required package(s):
```shell
$ pip install winrm;
```
How to run this program:
```shell
$ python wins_main.py -h
usage: wins_main.py [-h] [options] {start,stop,restart,daemon}

Connect to powershell on a remote Windows Server.

positional arguments:
  {start,stop,restart,daemon}
                        Commands of this program

optional arguments:
  -h, --help            show this help message and exit
  -c, --config     	 	change config file path
  -l, --log         	change log file path
  -o, --out_Dir     	change output directory path
  -p, --pidfile     	change pidfile path
  -v                    logging level
```

### 2. Systemd instruction
Sample config:
```.service=
# put this file in the fallowing path
# /usr/lib/systemd/system/Wins-midware.service
[Unit]
Description=Midware between Windows server and AIOPs

[Service]
ExecStart=/root/midware_Wins/Wins_main.py -o /root/midware_Wins/probe start
Restart=on-abnormal
RestartSec=3min

[Install]
WantedBy=multi-user.target
```
A better option then letting the program run in background on its own.</br>
Running as a systemd service has several benefits, including :
1. auto-load at boot-up
2. auto-restart
3. log handling

### 3. endpoint UI

    "winserver midware UI:\n"+
    "   index:\n"+
    "[GET]      1. ip:port/show\n"+
    "[GET]      2. ip:port/init\n"+
    "[POST]     3. ip:port/update\n"+
    "[POST]     4. ip:port/delete\n"+
    "[GET]      5. ip:port/namelist"


