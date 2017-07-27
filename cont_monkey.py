import datetime
import os
from optparse import OptionParser


def normal_cat():
    print("*****normal finish*****")

    try:
        os.makedirs("normal")
    except OSError:
        print("normal exists")

    return "normal/"


def unknown_cat():
    print("*****unknown reason interruption*****")

    try:
        os.makedirs("unknown")
    except OSError:
        print("unknown exists")

    os.chdir("unknown")
    try:
        os.makedirs(date_time)
    except OSError:
        print("dateTime exists")

    os.chdir("..")
    return "unknown/" + date_time + "/"


def anr_cat(error_info):
    print("*****error cause:ANR*****")


def crash_cat(error_info):
    print("*****error cause:CRASH*****")

    error_module = error_info
    error_pos = None

    log_file = open("monkey_log_" + date_time + ".txt")
    for line in log_file:
        if not line.find('.java:') == -1:
            # print line.find('seed=')
            error_pos = line[line.find('at ') + len('at '):line.find('(')]
            break
    log_file.close()

    if 'errorPos' in dir():
        print('error cause:CRASH')

        print('error position:' + error_pos)

        try:
            os.makedirs("CRASH")
        except OSError:
            print("CRASH exists")

        os.chdir("CRASH")
        try:
            os.makedirs(error_module)
        except OSError:
            print(error_module + " exists")

        os.chdir(error_module)
        try:
            os.makedirs(error_pos)
        except OSError:
            print(error_pos + " exists")

        os.chdir(error_pos)
        try:
            os.makedirs(date_time)
        except OSError:
            print(date_time + " exists")

        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    return "CRASH/" + error_module + "/" + error_pos + "/" + date_time + "/"


def move_monkey_log(log_path):
    print("*****moveMonkeyLog*****")

    file_size = os.path.getsize("monkey_log_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        os.popen("zip monkey_log_" + date_time + ".zip monkey_log_" + date_time + ".txt")
        os.popen("mv monkey_log_" + date_time + ".zip " + log_path)
        os.popen("rm monkey_log_" + date_time + ".txt")
    else:
        os.popen("mv monkey_log_" + date_time + ".txt " + log_path)


def pull_log_and_move(log_path):
    print("*****pullLogAndMove*****")

    os.popen(adb_device + " pull /data/system/dropbox/ " + log_path)
    os.popen("cd " + log_path)
    try:
        os.makedirs("log")
    except OSError:
        print("log exists")

    os.popen("cp -f *_anr* *_crash* log/")
    os.popen("rm *@*")
    os.popen("cp -f log/* .")
    os.popen("rm -rf log")
    os.popen("cd -")
    os.popen(adb_device + " pull /data/tombstones/ " + log_path)
    os.popen(adb_device + " shell rm -f /data/tombstones/*")
    os.popen(adb_device + " shell rm -f /data/system/dropbox/*")
    os.popen(adb_device + " shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.popen(adb_device + " pull /sdcard/screenshot.png " + log_path)

    file_size = os.path.getsize("main_log_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        os.popen("zip main_log_" + date_time + ".zip main_log_" + date_time + ".txt")
        os.popen("mv main_log_" + date_time + ".zip " + log_path)
        os.popen("rm main_log_" + date_time + ".txt")
    else:
        os.popen("mv main_log_" + date_time + ".txt " + logPath)

    file_size = os.path.getsize("event_log_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        os.popen("zip event_log_" + date_time + ".zip event_log_" + date_time + ".txt")
        os.popen("mv event_log_" + date_time + ".zip " + logPath)
        os.popen("rm event_log_" + date_time + ".txt")
    else:
        os.popen("mv event_log_" + date_time + ".txt " + logPath)


def dump_state_and_move(log_path):
    print("*****dumpstateAndMove*****")

    file_size = os.path.getsize("dumpstate_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        os.popen("zip dumpstate_" + date_time + ".zip dumpstate_" + date_time + ".txt")
        os.popen("mv dumpstate_" + date_time + ".zip " + log_path)
        os.popen("rm dumpstate_" + date_time + ".txt")
    else:
        os.popen("mv dumpstate_" + date_time + ".txt " + log_path)


if __name__ == "__main__":

    device_sn = '0123456789'
    adb_device = "adb"
    run_time = 1
    event_executed = 0

    parser = OptionParser(usage="usage:%prog [optinos]\
    script will run 1 time if no arg found")
    parser.add_option("-l", "--logfile",
                      action="store",
                      type="string",
                      dest="logfile",
                      default=None,
                      help="Analyse monkey logfile. Log file name should be monkey_log_yyyymmdd-hhmmss.txt"
                      )

    parser.add_option("-r", "--runtime",
                      action="store",
                      dest="runtime",
                      type="int",
                      default=1,
                      help="Specify monkey test event count"
                      )

    parser.add_option("-n", "--serialnumber",
                      action="store",
                      dest="sn",
                      type="string",
                      default=None,
                      help="Specify device serial number for adb"
                      )

    parser.add_option("-s", "--seed",
                      action="store",
                      dest="seed",
                      type="int",
                      default=None,
                      help="Specify monkey test seed"
                      )

    (options, args) = parser.parse_args()

    if options.logfile is not None:
        if options.logfile.find("monkey_log_") == 0:
            date_time = options.logfile[len("monkey_log_"):options.logfile.find(".txt")]
            print("dateTime:" + date_time)

    if 'date_time' not in dir():
        run_time = options.runtime
        print("runTime:" + str(run_time))

    if 'date_time' not in dir():
        device_sn = options.sn
        if device_sn is not None:
            print("deviceSN:" + device_sn)

        if device_sn is not None:
            adb_device = "adb -s " + device_sn
            print("ADBDevice:" + adb_device)

    if 'date_time' not in dir():
        if options.seed is not None:
            monkey_seed = "-s " + str(options.seed)
            print("monkeySeed:" + monkey_seed)

    if 'date_time' in dir():
        # process monkey log file only
        print("*****analyse monkey log*****")

        log_file = open(options.logfile)
        for line in log_file:
            if not line.find('seed=') == -1:
                # print line.find('seed=')
                random_seed = line[line.find('seed=') + len('seed='):line.find(' count=')]
                print('randomSeed:' + str(random_seed))

            if not line.find('Events injected: ') == -1:
                # print line.find('Events injected: ')
                event_count = int(line[line.find('Events injected: ') + len('Events injected: '):len(line)])
                print('eventCount:' + str(event_count))
                event_executed = event_executed + event_count
                print('eventExecuted:' + str(event_executed))

        log_file.close()

        if 'event_count' not in dir():
            event_count = 0
            unknown_cat()

        log_file = open("monkey_log_" + date_time + ".txt")
        for line in log_file:
            if not line.find('ANR in') == -1:
                error_info = line[line.find('ANR in') + len('ANR in'):len(line)]
                log_path = anr_cat(error_info)
                move_monkey_log(log_path)

            if not line.find('CRASH:') == -1:
                error_info = line[line.find('CRASH: ') + len('CRASH: '):line.find(' (')]
                print(error_info)

                log_path = crash_cat(error_info)
                print(log_path)

                move_monkey_log(log_path)
        log_file.close()

        if 'error_info' not in dir():
            logPath = normal_cat()
            move_monkey_log(log_path)

    else:
        # run monkey for specified events count
        if 'run_time' not in dir():
            print("runTime is null")
            exit(-1)

        while event_executed < run_time:
            # set volume to 1 so as to prevent fm annoying sound
            for i in range(1, 10):
                os.popen(adb_device + " shell input keyevent 25")

            os.popen(adb_device + " shell input keyevent 24")

            # reboot devices for next run
            print("*****reboot device*****")

            os.popen(adb_device + " kill-server")
            # os.popen(ADBDevice+" reboot")
            # wait for device connection
            print("*****wait for device*****")

            os.popen(adb_device + " wait-for-device")
            os.popen(adb_device + " push blacklist.txt /data/")
            # run monkey with a random seed
            if 'monkeySeed' not in dir():
                print("*****run monkey with a random seed*****")

                monkey_seed = ""
            else:
                print("****run monkey with specified seed " + monkey_seed + "*****")

            now = datetime.datetime.now()
            date_time = now.strftime("%Y%m%d-%H%M%S")
            print("dateTime:" + date_time)

            os.popen("nohup " + adb_device + " logcat *:W > main_log_" + date_time + ".txt &")
            os.popen("nohup " + adb_device + " logcat -b events -v time > event_log_" + date_time + ".txt &")

            # --pct-touch 18 --pct-motion 12 --pct-pinchzoom 2 --pct-trackball 0 --pct-nav 30 --pct-majornav 18 --pct-syskeys 2 --pct-appswitch 2 --pct-flip 1 --pct-anyevent 15 --throttle 50
            # os.popen(ADBDevice+" shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-touch 0 --pct-trackball 0 --throttle 50 "+monkeySeed+" -v -v -v "+runTime+" > monkey_log_"+dateTime+".txt")
            os.popen(
                adb_device + " shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-majornav 40 --pct-nav 30 --pct-syskeys 20 --throttle 50 --pct-appswitch 5 --pct-anyevent 5 " + monkey_seed + " -v -v -v " + str(
                    run_time) + " > monkey_log_" + date_time + ".txt")

            # analyse monkey log, figure out error catagory and pull log to pc
            print("*****analyse monkey log*****")

            log_file = open("monkey_log_" + date_time + ".txt")
            for line in log_file:
                if not line.find('seed=') == -1:
                    # print line.find('seed=')
                    random_seed = line[line.find('seed=') + len('seed='):line.find(' count=')]

                if not line.find('Events injected: ') == -1:
                    # print line.find('Events injected: ')
                    event_count = int(line[line.find('Events injected: ') + len('Events injected: '):len(line)])

            log_file.close()

            if 'event_count' not in dir():
                event_count = 0
                log_path = unknown_cat()
                move_monkey_log(log_path)
                pull_log_and_move(log_path)
                os.popen(adb_device + " shell dumpstate > dumpstate_" + date_time + ".txt")
                dump_state_and_move(log_path)

            print('random seed:' + str(random_seed))

            print('event count:' + str(event_count))

            event_executed = event_executed + event_count
            print('event exercuted:' + str(event_executed))

            log_file = open("monkey_log_" + date_time + ".txt")
            for line in log_file:
                if not line.find('ANR in') == -1:
                    error_info = line[line.find('ANR in') + len('ANR in'):len(line)]
                    log_path = anr_cat(error_info)
                    move_monkey_log(log_path)
                    pull_log_and_move(log_path)
                    os.popen(adb_device + " shell dumpstate > dumpstate_" + date_time + ".txt")
                    dump_state_and_move(log_path)

                if not line.find('CRASH:') == -1:
                    error_info = line[line.find('CRASH: ') + len('CRASH: '):line.find(' (')]
                    log_path = crash_cat(error_info)
                    move_monkey_log(log_path)
                    pull_log_and_move(log_path)
                    os.popen(adb_device + " shell dumpstate > dumpstate_" + date_time + ".txt")
                    dump_state_and_move(log_path)
            log_file.close()

            if 'error_info' not in dir():
                log_path = normal_cat()
                move_monkey_log(log_path)
