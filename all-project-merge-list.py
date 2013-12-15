#!/usr/bin/python

import sys
import os
import commands
import re
import json
import datetime
import uuid

# input parameter : project path, start date, end date
if len(sys.argv) < 4:
    print 'num of parameter wrong ...'
    exit(1)

rootdir = sys.argv[1] if (sys.argv[1][-1] == '/') else sys.argv[1]+'/'
startdate = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
enddate = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%d').date()
jsonall = []
jsonfile = '/tmp/'+str(uuid.uuid4())+'.txt'

def init():
    os.path.exists(jsonfile) and os.remove(jsonfile)

def record_git_log(path):
    command_git = 'cd %s; git log --pretty=format:"%s" --date=short  ' %(path, '%h|%cd|%s')
    git_log_ret = commands.getoutput(command_git).split('\n')
    subpath = path.replace(rootdir, '')
    jsonret = [subpath, git_log_ret]
    jsonall.append(jsonret)

def save_to_file(path):
    file = open(path, 'a')
    try:
        json.dump(jsonall, file)
    except:
        print 'json dump failed'
    finally:
        file.close()

def list_files(path):
    jsondata=[]
    file = open(jsonfile, 'r')
    try:
        jsondata = json.loads(file.read())
    except:
        print 'load json failed'
    finally:
        file.close()
    for data in jsondata:
        print 'project <'+data[0]+'>'
        gitdata = data[1]
        printdata='no'
        for line in gitdata:
            dateobj = datetime.datetime.strptime((line.split('|'))[1], '%Y-%m-%d').date()
            if enddate >= dateobj and dateobj > startdate:
                hashret=(line.split('|'))[0]
                print "\t"+line
                printdata='yes'
        if printdata == 'no':
            print "\tno data ...\n"
        else:
            print "\n"

# traverse root directory
init()
for subroot, dirs, files in os.walk(rootdir):
    skipdir = ['.repo']
    if subroot.replace(rootdir, '') in skipdir:
        continue
    for d in dirs:
        if d == '.git':
            record_git_log(subroot)
            break

save_to_file(jsonfile)

list_files(subroot)

