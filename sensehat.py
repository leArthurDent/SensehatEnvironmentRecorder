#Copyright (C) 2017  Sascha Manier (SaschaManier@posteo.de)
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation version 3 of the License.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program. If not, see http://www.gnu.org/licenses/.

from sense_hat import SenseHat
import time
import os.path
import subprocess
import dropbox

sense=SenseHat()

def writeintolog(log):
    logtime = time.localtime()
    printlogtime = time.strftime("%H:%M", logtime)
    logdir = "/home/pi/Documents/Sensehat/log/"
    logname = time.strftime("%Y%m%d", logtime) + "_log.txt"
    logpath = logdir + logname
    if os.path.isfile(logpath):
        try:
            logfile = open(logpath, mode = "a")
            print(printlogtime, "\t", log, file=logfile)
        finally:
            logfile.close()

    else:
        try:
            logfile = open(logpath, mode = "w")
            print(printlogtime, "\t", log, file=logfile)
        finally:
            logfile.close()

def readdata():
    t = time.localtime()
    mtime = t.tm_hour*60 + t.tm_min
    try:
        temperature = sense.temperature
    except:
        log = "Failed to read temperature"
        writeintolog(log)

    try:
        pressure = sense.pressure
    except:
        log = "Failed to read pressure"
        writeintolog(log)

    try:
        humidity = sense.humidity
    except:
        log = "Failed to read humidity"
        writeintolog(log)
        
    data = str(mtime) + "," + str(temperature) + "," + str(pressure) + "," + str(humidity)
    return data

def writedata(data, fpath):
    try:
        f = open(fpath, mode = "w")
        print("time,temperature,pressure,humidity", end = "\n", file = f)
        print(data, end = '\n',file = f)
        log = "Wrote data into file"
        writeintolog(log)
    except:
        log = "Failed to write data into file"
        writeintolog(log)
    finally:
        f.close()

def appenddata(data, fpath):
        try:
            f = open(fpath, mode = "a")
            print(data, end = '\n',file = f)
            log = "Wrote data into file"
            writeintolog(log)
        except:
            log = "Failed to write data into file"
            writeintolog(log)
        finally:
            f.close()

def processdata():
    try:
        subprocess.call(["Rscript","/home/pi/Sensehat/sensehat.R"])
        log = "Called sensehat.R to generate Graphs"
        writeintolog(log)
    except:
        log = "Failed to called sensehat.R"
        writeintolog(log)

def uploaddata(tup):
    try:
        updir = "/home/pi/Sensehat/graphs/"
        upname = time.strftime("%Y%m%d", tup) + ".pdf"
        uppath = updir + upname
        f = open(uppath, "rb")
        log = dbc.put_file(upname, f)
        writeintolog(log)
    except:
        log = "Failed to Upload Graphs"
        writeintolog(log)
    finally:
        f.close()
    
log = "Started sensehat.py"
writeintolog(log)
       
try:
    dbc=dropbox.client.DropboxClient("DOPBOX TOKENCODE")
    
except:
    log = "Failed to connect to Dropbox"
    writeintolog(log)

log = "Connected with Dropbox"
writeintolog(log)

log = dbc.account_info()
writeintolog(log)

localt = time.localtime()
fdir = "/home/pi/Sensehat/data/"
fname = time.strftime("%Y%m%d", localt) + ".csv"
fpath = fdir + fname

if os.path.isfile(fpath):
    data = readdata()
    appenddata(data, fpath)
else:
    data = readdata()
    writedata(data, fpath)

time.sleep(60)

while(1):
    t = time.time()
    twrite = time.localtime(t)
    fname = time.strftime("%Y%m%d", twrite) + ".csv"
    fpath = fdir + "/" + fname
    tup = time.localtime(t-86400)

    if os.path.isfile(fpath):
        data=readdata()
        appenddata(data, fpath)

    else:
        data=readdata()
        writedata(data, fpath)
        processdata()
        uploaddata(tup)
        
    time.sleep(60)
