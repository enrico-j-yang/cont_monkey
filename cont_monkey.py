import os
import sys
from optparse import OptionParser
import datetime


def normalCat():
    print "*****normal finish*****"
    try:
        os.makedirs("normal")
    except OSError:
        print "normal exists"
    return "normal/"
    
def unknownCat():
    print "*****unknown reason interruption*****"
    try:
        os.makedirs("unknown")
    except OSError:
        print "unknown exists"
    
    os.chdir("unknown")
    try:
        os.makedirs(dateTime)
    except OSError:
        print "dateTime exists"
    os.chdir("..")
    return "unknown/"+dateTime+"/"
    
def anrCat(errorInfo):
    print "*****error cause:ANR*****"
    
def crashCat(errorInfo):
    print "*****error cause:CRASH*****"
    errorModule = errorInfo
    
    log_file = open("monkey_log_"+dateTime+".txt")
    for line in log_file:
        if not line.find('.java:') == -1:
            #print line.find('seed=')
            errorPos = line[line.find('at ')+len('at '):line.find('(')]
            break
    log_file.close()
    
    if 'errorPos' in dir():
        print 'error cause:CRASH'
        print 'error position:'+errorPos
        try:
            os.makedirs("CRASH")
        except OSError:
            print "CRASH exists"
    
        os.chdir("CRASH")
        try:
            os.makedirs(errorModule)
        except OSError:
            print errorModule+" exists"
    
        os.chdir(errorModule)
        try:
            os.makedirs(errorPos)
        except OSError:
            print errorPos+" exists"
    
        os.chdir(errorPos)
        try:
            os.makedirs(dateTime)
        except OSError:
            print dateTime+" exists"
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
    
    return "CRASH/"+errorModule+"/"+errorPos+"/"+dateTime+"/"
                
def moveMonkeyLog(logPath):
    print "*****moveMonkeyLog*****"
    fileSize = os.path.getsize("monkey_log_"+dateTime+".txt")
    if fileSize > 10*1024*1024:
        os.popen("zip monkey_log_"+dateTime+".zip monkey_log_"+dateTime+".txt")
        os.popen("mv monkey_log_"+dateTime+".zip "+logPath)
        os.popen("rm monkey_log_"+dateTime+".txt")
    else:
        os.popen("mv monkey_log_"+dateTime+".txt "+logPath)
    
def pullLogAndMove(logPath):
    print "*****pullLogAndMove*****"

    os.popen(ADBDevice+" pull /data/system/dropbox/ "+logPath)
    os.popen("cd "+logPath)
    try:
        os.makedirs("log")
    except OSError:
        print "log exists"
    os.popen("cp -f *_anr* *_crash* log/")
    os.popen("rm *@*")
    os.popen("cp -f log/* .")
    os.popen("rm -rf log")
    os.popen("cd -")
    os.popen(ADBDevice+" pull /data/tombstones/ "+logPath)
    os.popen(ADBDevice+" shell rm -f /data/tombstones/*")
    os.popen(ADBDevice+" shell rm -f /data/system/dropbox/*")
    os.popen(ADBDevice+" shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.popen(ADBDevice+" pull /sdcard/screenshot.png "+logPath)
    
    fileSize = os.path.getsize("main_log_"+dateTime+".txt")
    if fileSize > 10*1024*1024:
        os.popen("zip main_log_"+dateTime+".zip main_log_"+dateTime+".txt")
        os.popen("mv main_log_"+dateTime+".zip "+logPath)
        os.popen("rm main_log_"+dateTime+".txt")
    else:
        os.popen("mv main_log_"+dateTime+".txt "+logPath)
        
    fileSize = os.path.getsize("event_log_"+dateTime+".txt")
    if fileSize > 10*1024*1024:
        os.popen("zip event_log_"+dateTime+".zip event_log_"+dateTime+".txt")
        os.popen("mv event_log_"+dateTime+".zip "+logPath)
        os.popen("rm event_log_"+dateTime+".txt")
    else:
        os.popen("mv event_log_"+dateTime+".txt "+logPath)
    
def dumpstateAndMove(logPath):
    print "*****dumpstateAndMove*****"
    fileSize = os.path.getsize("dumpstate_"+dateTime+".txt")
    if fileSize > 10*1024*1024:
        os.popen("zip dumpstate_"+dateTime+".zip dumpstate_"+dateTime+".txt")
        os.popen("mv dumpstate_"+dateTime+".zip "+logPath)
        os.popen("rm dumpstate_"+dateTime+".txt")
    else:
        os.popen("mv dumpstate_"+dateTime+".txt "+logPath)
    
if __name__=="__main__":

    deviceSN = '0123456789'
    ADBDevice="adb"
    runTime=1
    eventExcercuted=0
    
    parser = OptionParser(usage="usage:%prog [optinos]\
    script will run 1 time if no arg found")  
    parser.add_option("-l", "--logfile",
    action = "store",
    type = "string",
    dest = "logfile",
    default = None,
    help="Analyse monkey logfile. Log file name should be monkey_log_yyyymmdd-hhmmss.txt"
    )  
                
    parser.add_option("-r", "--runtime",
    action = "store",
    dest = "runtime",
    type = "int",
    default = 1,
    help = "Specify monkey test event count"
    )
                
    parser.add_option("-n", "--serialnumber",
    action = "store",
    dest = "sn",
    type = "string",
    default = None,
    help = "Specify device serial number for adb"
    )
                
    parser.add_option("-s", "--seed",
    action = "store",
    dest = "seed",
    type = "int",
    default = None,
    help = "Specify monkey test seed"
    )
                
    (options, args) = parser.parse_args()  
    
    if options.logfile!=None:
        if options.logfile.find("monkey_log_")==0:
            dateTime = options.logfile[len("monkey_log_"):options.logfile.find(".txt")]
            print "dateTime:"+dateTime
    
    if not 'dateTime' in dir():
        runTime=options.runtime
        print "runTime:"+str(runTime)
    
    if not 'dateTime' in dir():
        deviceSN = options.sn
        if deviceSN!=None:
            print "deviceSN:"+deviceSN
        
        if deviceSN!=None:
            ADBDevice = "adb -s "+deviceSN
            print "ADBDevice:"+ADBDevice
    
    if not 'dateTime' in dir():
        if options.seed!=None:
            monkeySeed="-s "+str(options.seed)
            print "monkeySeed:"+monkeySeed
            
    if 'dateTime' in dir():
        #process monkey log file only
        print "*****analyse monkey log*****"
        log_file = open(options.logfile)
        for line in log_file:
            if not line.find('seed=') == -1:
                #print line.find('seed=')
                randomSeed = line[line.find('seed=')+len('seed='):line.find(' count=')]
                
            if not line.find('Events injected: ') == -1:
                #print line.find('Events injected: ')
                eventCount = int(line[line.find('Events injected: ')+len('Events injected: '):len(line)])

        log_file.close()
        
        if not 'eventCount' in dir():
            eventCount = 0
            unknownCat()
        
        print 'randomSeed:'+str(randomSeed)
        print 'eventCount:'+str(eventCount)
        eventExcercuted = eventExcercuted + eventCount
        print 'eventExcercuted:'+str(eventExcercuted)
        
        log_file = open("monkey_log_"+dateTime+".txt")
        for line in log_file:
            if not line.find('ANR in') == -1:
                errorInfo = line[line.find('ANR in')+len('ANR in'):len(line)]
                logPath = anrCat(errorInfo)
                moveMonkeyLog(logPath)
                
            if not line.find('CRASH:') == -1:
                errorInfo = line[line.find('CRASH: ')+len('CRASH: '):line.find(' (')]
                print errorInfo
                logPath = crashCat(errorInfo)
                print logPath
                moveMonkeyLog(logPath)
        log_file.close()
        
        if not 'errorInfo'in dir():
            logPath = normalCat()
            moveMonkeyLog(logPath)
        
    else:
        # run monkey for specified events count
        if not 'runTime' in dir():
            print "runTime is null"
            exit

        while eventExcercuted<runTime:
            # set volume to 1 so as to prevent fm annoying sound
            for i in range(1,10):
                os.popen(ADBDevice+" shell input keyevent 25")
    
            os.popen(ADBDevice+" shell input keyevent 24")
    
            # reboot devices for next run
            print "*****reboot device*****"
            os.popen(ADBDevice+" kill-server")
            #os.popen(ADBDevice+" reboot")
            # wait for device connection
            print "*****wait for device*****"
            os.popen(ADBDevice+" wait-for-device")
            os.popen(ADBDevice+" push blacklist.txt /data/")
            # run monkey with a random seed
            if not 'monkeySeed' in dir():
                print "*****run monkey with a random seed*****"
                monkeySeed = ""
            else:
                print "****run monkey with specified seed "+monkeySeed+"*****"

            now = datetime.datetime.now()
            dateTime = now.strftime("%Y%m%d-%H%M%S")
            print "dateTime:"+dateTime
            os.popen("nohup "+ADBDevice+" logcat *:W > main_log_"+dateTime+".txt &")
            os.popen("nohup "+ADBDevice+" logcat -b events -v time > event_log_"+dateTime+".txt &")
            
            #--pct-touch 18 --pct-motion 12 --pct-pinchzoom 2 --pct-trackball 0 --pct-nav 30 --pct-majornav 18 --pct-syskeys 2 --pct-appswitch 2 --pct-flip 1 --pct-anyevent 15 --throttle 50
        #os.popen(ADBDevice+" shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-touch 0 --pct-trackball 0 --throttle 50 "+monkeySeed+" -v -v -v "+runTime+" > monkey_log_"+dateTime+".txt")
            os.popen(ADBDevice+" shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-majornav 40 --pct-nav 30 --pct-syskeys 20 --throttle 50 --pct-appswitch 5 --pct-anyevent 5 "+monkeySeed+" -v -v -v "+str(runTime)+" > monkey_log_"+dateTime+".txt")

            # analyse monkey log, figure out error catagory and pull log to pc
            print "*****analyse monkey log*****"
            log_file = open("monkey_log_"+dateTime+".txt")
            for line in log_file:
                if not line.find('seed=') == -1:
                    #print line.find('seed=')
                    randomSeed = line[line.find('seed=')+len('seed='):line.find(' count=')]
            
                if not line.find('Events injected: ') == -1:
                    #print line.find('Events injected: ')
                    eventCount = int(line[line.find('Events injected: ')+len('Events injected: '):len(line)])

            log_file.close()
            
            if not 'eventCount' in dir():
                eventCount=0
                logPath = unknownCat()
                moveMonkeyLog(logPath)
                pullLogAndMove(logPath)
                os.popen(ADBDevice+" shell dumpstate > dumpstate_"+dateTime+".txt")
                dumpstateAndMove(logPath)
            
            print 'random seed:'+str(randomSeed)
            print 'event count:'+str(eventCount)
            eventExcercuted = eventExcercuted+eventCount
            print 'event exercuted:'+str(eventExcercuted)
            
            log_file = open("monkey_log_"+dateTime+".txt")
            for line in log_file:
                if not line.find('ANR in') == -1:
                    errorInfo = line[line.find('ANR in')+len('ANR in'):len(line)]
                    logPath = anrCat(errorInfo)
                    moveMonkeyLog(logPath)
                    pullLogAndMove(logPath)
                    os.popen(ADBDevice+" shell dumpstate > dumpstate_"+dateTime+".txt")
                    dumpstateAndMove(logPath)
            
                if not line.find('CRASH:') == -1:
                    errorInfo = line[line.find('CRASH: ')+len('CRASH: '):line.find(' (')]
                    logPath = crashCat(errorInfo)
                    moveMonkeyLog(logPath)
                    pullLogAndMove(logPath)
                    os.popen(ADBDevice+" shell dumpstate > dumpstate_"+dateTime+".txt")
                    dumpstateAndMove(logPath)
            log_file.close()
    
            if not 'errorInfo'in dir():
                logPath = normalCat()
                moveMonkeyLog(logPath)
