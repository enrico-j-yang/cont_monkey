import datetime
import os
import platform
import shutil
import subprocess
import time
import zipfile
from glob import glob
from optparse import OptionParser

import psutil


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

    error_module = error_info
    error_pos = None

    log_file = open("monkey_log_" + date_time + ".txt")
    for line in log_file:
        if not line.find('ANR') == -1:
            # print line.find('seed=')
            error_pos = line[line.find('/') + len('/'):line.find(')')]
            error_module = line[line.find('in ') + len('in '):line.find(' (')]
            break
    log_file.close()
    if 'error_pos' in dir():
        print('error cause:ANR')

        print('error position:' + error_pos)
        try:
            os.makedirs("ANR")
        except OSError:
            print("ANR exists")

        os.chdir("ANR")
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
    return "ANR/" + error_module + "/" + error_pos + "/" + date_time + "/"


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

    if 'error_pos' in dir():
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
        # os.popen("zip monkey_log_" + date_time + ".zip monkey_log_" + date_time + ".txt")
        f = zipfile.ZipFile("monkey_log_" + date_time + ".zip", 'w', zipfile.ZIP_DEFLATED)
        f.write("monkey_log_" + date_time + ".txt")
        f.close()
        shutil.move("monkey_log_" + date_time + ".zip", log_path)
        os.remove("monkey_log_" + date_time + ".txt")
    else:
        shutil.move("monkey_log_" + date_time + ".txt", log_path)


def pull_log_and_move(log_path):
    print("*****pullLogAndMove*****")
    if os.system(adb_device + " pull /data/system/dropbox/ " + log_path) == 0:
        cur_path = os.getcwd()
        os.chdir(log_path + "dropbox/")
        try:
            os.makedirs("log")
        except OSError:
            print("log exists")

        # os.popen("cp -f *_anr* *_crash* log/")
        for filename in glob("*_anr*"):
            shutil.move(filename, "log/")

        for filename in glob("*_crash*"):
            shutil.move(filename, "log/")
        # for root, dirs, files in os.walk(log_path + "dropbox"):
        #    for file in files:
        #        match_crash_obj = re.search(r'_crash', file, re.M | re.I)
        #        match_anr_obj = re.search(r'_anr', file, re.M | re.I)
        #        if match_anr_obj or match_crash_obj:
        #            print(file)
        #            shutil.move(file, log_path + "log")

        # os.popen("rm *@*")
        for filename in glob("*@*"):
            os.remove(filename)
        # os.popen("cp -f log/* .")
        for filename in glob("log/*"):
            shutil.copy(filename, "./")
        # os.popen("rm -rf log")
        shutil.rmtree("log")
        os.chdir(cur_path)
        if os.system(adb_device + " shell rm -f /data/system/dropbox/*") != 0:
            print("delete /data/system/dropbox/* error")
    if os.system(adb_device + " pull /data/tombstones/ " + log_path) == 0:
        os.system(adb_device + " shell rm -f /data/tombstones/*")

    if os.system(adb_device + " shell /system/bin/screencap -p /sdcard/screenshot.png") == 0:
        if os.system(adb_device + " pull /sdcard/screenshot.png " + log_path) != 0:
            print("get screen shot error")
    else:
        print("get screen shot error")

    file_size = os.path.getsize("main_log_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        # os.popen("zip main_log_" + date_time + ".zip main_log_" + date_time + ".txt")
        f = zipfile.ZipFile("main_log_" + date_time + ".zip", 'w', zipfile.ZIP_DEFLATED)
        f.write("main_log_" + date_time + ".txt")
        f.close()
        # os.popen("mv main_log_" + date_time + ".zip " + log_path)
        shutil.move("main_log_" + date_time + ".zip", log_path)
        # os.popen("rm main_log_" + date_time + ".txt")
        os.remove("main_log_" + date_time + ".txt")
    else:
        shutil.move("main_log_" + date_time + ".txt", log_path)

    file_size = os.path.getsize("event_log_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        # os.popen("zip event_log_" + date_time + ".zip event_log_" + date_time + ".txt")
        f = zipfile.ZipFile("event_log_" + date_time + ".zip", 'w', zipfile.ZIP_DEFLATED)
        f.write("event_log_" + date_time + ".txt")
        f.close()
        # os.popen("mv event_log_" + date_time + ".zip " + log_path)
        shutil.move("event_log_" + date_time + ".zip", log_path)
        # os.popen("rm event_log_" + date_time + ".txt")
        os.remove("event_log_" + date_time + ".txt")
    else:
        # os.popen("mv event_log_" + date_time + ".txt " + log_path)
        shutil.move("event_log_" + date_time + ".txt", log_path)


def dump_state_and_move(log_path):
    print("*****dumpstateAndMove*****")

    file_size = os.path.getsize("dumpstate_" + date_time + ".txt")
    if file_size > 10 * 1024 * 1024:
        # os.system("zip dumpstate_" + date_time + ".zip dumpstate_" + date_time + ".txt")
        f = zipfile.ZipFile("dumpstate_" + date_time + ".zip", 'w', zipfile.ZIP_DEFLATED)
        f.write("dumpstate_" + date_time + ".txt")
        f.close()
        # os.popen("mv dumpstate_" + date_time + ".zip " + log_path)
        shutil.move("dumpstate_" + date_time + ".zip", log_path)
        # os.popen("rm dumpstate_" + date_time + ".txt")
        os.remove("dumpstate_" + date_time + ".txt")
    else:
        # os.popen("mv dumpstate_" + date_time + ".txt " + log_path)
        shutil.move("dumpstate_" + date_time + ".txt", log_path)


if __name__ == "__main__":

    device_sn = '0123456789'
    adb_device = "adb"
    run_time = 1
    event_executed = 0
    event_count = 0
    date_time = None
    random_seed = None

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

    if date_time is None:
        run_time = options.runtime
        print("runTime:" + str(run_time))

    if date_time is None:
        device_sn = options.sn
        if device_sn is not None:
            print("deviceSN:" + device_sn)

        if device_sn is not None:
            adb_device = "adb -s " + device_sn
            print("ADBDevice:" + adb_device)

    if date_time is None:
        if options.seed is not None:
            monkey_seed = "-s " + str(options.seed)
            print("monkeySeed:" + monkey_seed)

    if date_time is not None:
        # process monkey log file only
        print("*****analyse monkey log*****")

        error_type = None
        error_info = None
        log_file = open(options.logfile)
        for line in log_file:
            if not line.find('seed=') == -1:
                # print line.find('seed=')
                random_seed = line[line.find('seed=') + len('seed='):line.find(' count=')]
                print('random seed:' + str(random_seed))

            if not line.find('ANR in') == -1:
                error_type = "ANR"
                error_info = line[line.find('ANR in') + len('ANR in'):len(line)]

            if not line.find('CRASH:') == -1:
                error_type = "CRASH"
                error_info = line[line.find('CRASH: ') + len('CRASH: '):line.find(' (')]

            if not line.find('Events injected: ') == -1:
                # print line.find('Events injected: ')
                event_count = int(line[line.find('Events injected: ') + len('Events injected: '):len(line)])
                print('event count:' + str(event_count))

        log_file.close()

        if error_info is None:
            log_path = normal_cat()
            move_monkey_log(log_path)
        else:
            if error_type is "ANR":
                log_path = anr_cat(error_info)
            elif error_type is "CRASH":
                log_path = crash_cat(error_info)
            elif event_count == 0:
                log_path = unknown_cat()
            else:
                log_path = ""
                print("log path error")
                exit(1)

            move_monkey_log(log_path)

        event_executed = event_executed + event_count
        print('event executed:' + str(event_executed))

    else:
        # run monkey for specified events count
        if 'run_time' not in dir():
            print("runTime is null")
            exit(-1)

        while event_executed < run_time:
            # reboot devices for next run
            print("*****reboot device*****")

            os.system(adb_device + " kill-server")
            os.system(adb_device + " devices")
            os.system(adb_device + " reboot")
            # wait for device connection
            print("*****wait for device*****")

            os.system(adb_device + " wait-for-device")
            os.system(adb_device + " push blacklist.txt /sdcard/")
            # run monkey with a random seed
            if 'monkeySeed' not in dir():
                print("*****run monkey with a random seed*****")

                monkey_seed = ""
            else:
                print("****run monkey with specified seed " + monkey_seed + "*****")

            now = datetime.datetime.now()
            date_time = now.strftime("%Y%m%d-%H%M%S")
            print("dateTime:" + date_time)

            # run logcat in background to generate main log and event log
            m = None
            e = None
            main_log_cmd = adb_device + " logcat *:W>main_log_" + date_time + ".txt"
            event_log_cmd = adb_device + " logcat -b events -v time>event_log_" + date_time + ".txt"
            if platform.system() == "Windows":
                main_log_cmd_list = main_log_cmd.split()
                m = subprocess.Popen(main_log_cmd_list, shell=True)
                event_log_cmd_list = event_log_cmd.split()
                e = subprocess.Popen(event_log_cmd_list, shell=True)
            elif platform.system() == "Darwin":
                m = subprocess.Popen(main_log_cmd, shell=True)
                e = subprocess.Popen(event_log_cmd, shell=True)
            else:
                print("Platform " + platform.system() + " not supported")
                exit(-1)

            # run monkey with specified random seed and key event types distribution
            # --pct-touch 18 --pct-motion 12 --pct-pinchzoom 2 --pct-trackball 0 --pct-nav 30 --pct-majornav 18
            # --pct-syskeys 2 --pct-appswitch 2 --pct-flip 1 --pct-anyevent 15 --throttle 50
            # os.system(ADBDevice+" shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-touch 0
            # --pct-trackball 0 --throttle 50 "+monkeySeed+" -v -v -v "+runTime+" > monkey_log_"+dateTime+".txt")

            para = " shell monkey"
            para += " --pkg-blacklist-file /sdcard/blacklist.txt"
            para += " --pct-majornav 40 --pct-nav 30 --pct-syskeys 20 --throttle 50 --pct-appswitch 5 --pct-anyevent 5"
            if monkey_seed != "":
                para += " -s " + monkey_seed
            para += " -v -v -v " + str(run_time)
            # para += " > monkey_log_" + date_time + ".txt"

            with open("monkey_log_" + date_time + ".txt", 'w') as f:
                if platform.system() == "Windows":
                    monkey_log_cmd_list = para.split()
                    monkey_log_cmd_list[0:0] = [adb_device]
                    monkey_log_process = subprocess.Popen(monkey_log_cmd_list, shell=True, stdout=subprocess.PIPE)
                else:
                    monkey_log_process = subprocess.Popen(adb_device + para, shell=True, stdout=subprocess.PIPE)

                # display progress
                from tqdm import tqdm

                with tqdm(total=run_time) as pbar:
                    pbar.update(event_executed)
                    for line in iter(monkey_log_process.stdout.readline, b''):
                        if not (line.decode("utf-8")).find(":S") == -1:
                            event_count += 1

                            if event_count <= run_time:  # near the end
                                pbar.update(1)
                        f.write(line.decode("utf-8"))

            m.kill()
            e.kill()
            for proc in psutil.process_iter():
                if proc.name() == 'adb.exe' or proc.name() == 'adb':
                    proc.kill()

            # analyse monkey log, figure out error category and pull log to pc
            print("*****analyse monkey log*****")
            time_out = 5
            start_time = time.time()
            current_time = time.time()
            time_out_flag = False
            if current_time - start_time > time_out:
                time_out_flag = True
            while not os.path.exists("monkey_log_" + date_time + ".txt") and not time_out_flag:
                time.sleep(1)
                current_time = time.time()
                if current_time - start_time > time_out:
                    time_out_flag = True

            error_type = None
            error_info = None
            if not time_out_flag:
                log_file = open("monkey_log_" + date_time + ".txt")
                for line in log_file:
                    if not line.find('seed=') == -1:
                        # print line.find('seed=')
                        random_seed = line[line.find('seed=') + len('seed='):line.find(' count=')]
                        print('random seed:' + str(random_seed))

                    if not line.find('Events injected: ') == -1:
                        # print line.find('Events injected: ')
                        event_count = int(line[line.find('Events injected: ') + len('Events injected: '):len(line)])
                        print('event count:' + str(event_count))

                    if not line.find('ANR in') == -1:
                        error_type = "ANR"
                        error_info = line[line.find('ANR in') + len('ANR in'):len(line)]

                    if not line.find('CRASH:') == -1:
                        error_type = "CRASH"
                        error_info = line[line.find('CRASH: ') + len('CRASH: '):line.find(' (')]
                log_file.close()

            if event_count == run_time:
                log_path = normal_cat()
                move_monkey_log(log_path)
                pull_log_and_move(log_path)
            else:
                if error_type is "ANR":
                    log_path = anr_cat(error_info)
                elif error_type is "CRASH":
                    log_path = crash_cat(error_info)
                else:
                    log_path = unknown_cat()

                move_monkey_log(log_path)
                pull_log_and_move(log_path)
                if os.system(adb_device + " shell dumpstate > dumpstate_" + date_time + ".txt") == 0:
                    dump_state_and_move(log_path)

            event_executed = event_executed + event_count
            if event_count < run_time:
                print('event executed:' + str(event_executed))
            else:
                print('event executed:' + str(event_count))
