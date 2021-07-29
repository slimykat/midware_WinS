# midware_WinS
midware_WinS is a midware service that can connect Osprey AIPOs and powershell from a remote Windows Server.

## Components
- midware_WinS/
	- **program modules :**
	    - wins_main.py
	    - wins_query.py
	    - wins_UI.py
	    - daemonize.py
	- **config and log file:**
	    - midware.conf
	    - config.json
	    - .midware.log
	- **default output directory:**
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
### 3. Config setting
```json
{
    "winserver": {
        "host": "xxx.xxx.xxx.xxx", 
        "password": "xxx", 
        "user": "xxx", 
        "UI_address": {
            "host": "0.0.0.0", 
            "port": 8882
        }
    }, 
    "winserver_probe": {
        "": ["Name", "CPU"]
    }
}
```
"winserver" entry contains the infomation of the monitored machine. It also defines the address of the program itself.</br>
"winserver_probe" entry defines what information to get from powershell.

	The entry name represent the key word of a process' name you wish to monitor.
		Default value is "", meaning all the available process would be monitored.
		The name could be a full name as well as key word of the process.
	The list in the value determines what kind of data about the process would be aquired.
		Default value is "Name" and "CPU".
		For the whole list of available data, please refer to the [document](https://hackmd.io/@mcnlab538/HJ7JyKTpu#Available-data-about-a-process).

### 4. UI endpoint
Some information and functions can be accessed through a make by Flask:

|Method|URL/endpoint|Description|Form attribute|
|---|---|---|---|
|GET|p:port/show	|show all the available endpoints|	-|
|GET|ip:port/reset 	|set the config to default| -|
|POST|ip:port/update	|update config about a specific process|ProcessName,</br>Targets(can have multiple)|
|POST|ip:port/delete	|delete a process from the list in the config| ProcessName|
|GET|ip:port/namelist 	|get a list of prcess from the monitored machine|-|


