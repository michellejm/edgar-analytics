import csv
import os
import datetime
import collections

timekeeper=[]
timedict=collections.defaultdict(list)
ipdict={}

outfile="output/sessionization.txt"
w=csv.writer(open(os.path.join(os.pardir, outfile), "w"))

inactivityfile = 'input/inactivity_period.txt'
fi=open(os.path.join(os.pardir, inactivityfile),'r').read()
mynum=int(fi)
timeout = datetime.timedelta(seconds=mynum)

#read the file line by line
def readfile(filename):
    with open(filename) as f:
        for entry in csv.DictReader(f):
            yield entry
            
infile = 'input/log.csv'
iterrow = iter(readfile(os.path.join(os.pardir, infile)))
for row in iterrow:
    ipname=row['ip']
    mytime=row['date']+" "+row['time']
    rqst_time=datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S")
    timedict[rqst_time].append(ipname)
    if rqst_time not in timekeeper:
        timekeeper.append(rqst_time)
    if ipname not in ipdict:
        ipdict[ipname]=[rqst_time, mytime]
    docdict={k:collections.Counter(v) for k,v in timedict.items()}
    #if the request time minus the first entry of the timekeeper is greater than the timeout, 
    #we need to check if all of the ipaddresses have been active in the past 2 seconds.
    if (rqst_time - timekeeper[0]) > timeout: 
        #get the ipaddresses that were active in the earliest second
        tk0=timekeeper[0]
        tkearly = timedict[tk0]
        #get those that were active in the later seconds
        try:
            for n in range(mynum+1)[1:]:
                tklate = timedict[timekeeper[n]]
                tklate+=tklate
        except:
            tklate=timedict[timekeeper[0]]
            
        #set of all ipaddresses seen in earliest second
        earlyips=set(tkearly)
        
        #set of all ipaddresses seen in later second
        lateips =set(tklate)
        #ipaddresses that only appeared in the earliest second, but not in the later ones
        diff = earlyips.difference(lateips)
        #for the ipaddresses only in the early set, count the number of times each ipaddress made a call 
        for ip in diff:
            #calculate number of seconds have elapsed
            iptime = (rqst_time-ipdict[ip][0]).total_seconds()
            start = ipdict[ip][1]
            t = ipdict[ip][0]
            end = rqst_time
            v=0
            while t < end:
                v+=docdict[t][ip]
                t+= datetime.timedelta(seconds=1)
            w.writerow([ip, start, mytime, iptime, v])
        #remove the oldest second
        del timekeeper[0] 
    else:
        pass
    
