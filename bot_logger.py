from datetime import datetime, date, time

def printLog(module_name, log_msg):
    dt = datetime.now().strftime("%H:%M:%S")
    print('\x1b[33m['+ dt +']\x1b[32m['+module_name+']\x1b[0m: ' + str(log_msg))
