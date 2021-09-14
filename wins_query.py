import json, os, logging, csv, sys, datetime, threading
import winrm

_session = ""
_Host = ""
_User = "Administrator"
_Password = ""

def query(Name, TargetObject = []):
    if (not _session):
        logging.error("please log in")
    r = _session.run_ps("Get-Process *" + Name + "* | Format-list " + ",".join(TargetObject))
    if r.std_err :
        logging.warning("wins_query.query:"+r.std_err)
    
    # empty result
    if not r.std_out: 
        return ""

    # remove header
    return r
    
def login(host="", user = "", password=""):
    
    # write to global variable if given any
    global _Host, _User, _Password, _session
    if host :
        _Host = host
    if not _Host:
        logging.error("wins_query.login:Missing_Host")
        sys.exit(0)
    if user:
        _User = user
    if password:
        _Password = password

    # build session with the given variables
    try:
        _session = winrm.Session(_Host, auth=(_User, _Password))
    except Exception as exp:
        logging.warning("wins_query.login:Login_failed:{}".format(exp))
        sys.exit(1)
"""
def extend_lifetime():
    #NYI
    query(life_rpc)

"""
def bulk_query(c, outpath):
    # extract from config
    
    probe = c.copy() # copy to prevent collision operation
    if not outpath.endswith("/"):
        outpath += "/"

    # record the query time (AKA "current time")
    t = datetime.datetime.now()
    now = t.strftime("%Y%m%d_%H_%M")

    logging.debug("Start_query")
    # bulk query for each target
    with open(outpath + "winserver_probe@" + now +".csv", "a+") as fp:
        writer = csv.writer(fp)
        payload = []
        for keyword, ObjList in probe.items():
            for line in query(keyword, TargetObject = ObjList):
                if (line):
                    for obj, value in list(zip(ObjList,line.split())):
                        payload.append([value, obj, keyword, _Host , now])
        writer.writerows(payload)

    # record query time in logging level "info"
    t2 = datetime.datetime.now()
    spent = (t2-t).total_seconds()
    logging.info("wins_query.bulk_query:Query_time_spent:"+str(spent)+"s")

def get_namelist():
    List = query("",TargetObject = ["Name"]) # will return a list of names
    return [l.replace(" ","") for l in List][:-3]

##################################################
# the following functions are used for dev ->
##################################################
"""
def hostid_get(host_name_list):
    id_jsonrpc = {**_prot, **{
        "method":"host.get", 
        "params":{
            "output":["hostid","name"],
            "filter":{ "host": host_name_list }
    }}}
    return query(id_jsonrpc)

def itemlist_get(host_name=None, host_id=None, filter_dict={}):
    itemlist_jsonrpc = {**_prot, **{
        "method": "item.get",
        "params":{
            "hostids": host_id,
            "host":host_name,
            "filter": filter_dict,
            "output":["itemids","name","value_type","host","host_id"]
    }}}
    return query(itemlist_jsonrpc)

def item_get(item_id):
    item_jsonrpc = {**_prot, **{
        "method": "item.get",
        "params":{
            "itemids": item_id,
            "output":"extend"
    }}}
    return query(item_jsonrpc)

def itemid_get(item_name, host_name):
    attr_get_jsonrpc = {**_prot, **{
        "method": "item.get",
        "params":{
            "filter": {"name":item_name},
            "host": host_name,
            "output":["itemids","name","value_type", "hostid"]
    }}}
    return query(attr_get_jsonrpc)

def item_attr_get(itemid):
    attr_get_jsonrpc = {**_prot, **{
        "method": "item.get",
        "params":{
            "itemids":itemid,
            #"selectApplications":["name"],
            "output":["itemids","name","value_type"]
    }}}
    return query(attr_get_jsonrpc)
"""
if __name__ == "__main__":
    print("usage : ")
    print("login(host=ip, user=Name, password=...) -> query(Name,TargetObject)")


