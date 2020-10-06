import time

def formattime():
    ctime = time.localtime(time.time())
    wdaylst = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthlst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    wday = wdaylst[ctime.tm_wday]
    month = monthlst[ctime.tm_mon-1]
    minute = ctime.tm_min
    second = ctime.tm_sec
    if minute < 10:
        minute = '0'+str(ctime.tm_min)
    if second < 10:
        second = '0'+str(ctime.tm_sec)
    return str(wday)+' '+str(ctime.tm_mday)+' '+month+' '+str(ctime.tm_year) +' '+str(ctime.tm_hour)+':'+str(minute)+':'+str(second)
