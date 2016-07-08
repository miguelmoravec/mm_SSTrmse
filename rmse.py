#!/usr/bin/env python

import subprocess
import datetime

try:
    import pyferret
except ImportError:
    print "You must module load pyferret"
    exit(1)

def mymain():

    basedir = '/archive/x1y/FMS/c3/CM2.1_ECDA/CM2.1R_ECDA_v3.1_1960_pfl_auto/gfdl.ncrc3-intel-prod-openmp/history/tmp/'
    filedir = "01.ocean_month.ensm.nc"

    #dirWhereIwantThisToHappen="."
    #child = subprocess.Popen(["", "/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2015.nc", "/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2016.nc"],cwd=dirWhereIwantThisToHappen)
    #child.communicate()

    #dirWhereIwantThisToHappen="."
    #child = subprocess.Popen(["dmget", "/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2015.nc", "/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2016.nc"],cwd=dirWhereIwantThisToHappen)
    #child.communicate()

    d="."
    child = subprocess.Popen(["ncrcat","/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2015.nc", "/home/x1y/gfdl/ecda_operational/sst/sstcm21_oimonthly_2016.nc", "/home/mmm/SSTrmse/sstcm21_oimonthly_1516.nc"],cwd=d)
    child.communicate() 

    returnCode = child.returncode 

    print 'Please answer the following questions to plot SST RMSE over the Pacific for last month...'
    today = raw_input("Specify desired month (mmyyyy): ")
    
    date = datetime.datetime.strptime('25' + today, '%d%m%Y')
    
    month = date.strftime('%m')
    year = date.strftime('%Y')

    print 'Generating plots for months preceeding', month,'/', year, '...'

    pyferret.start(quiet=True)

    count = 0

    while (count < 24):
	
	count = count + 1

    	math = date + datetime.timedelta(days=(-30*count))
    	prev_date =  str(math.strftime('%Y%m'))
        prev_month =  str(math.strftime('%m'))

	dirWhereIwantThisToHappen="."
        child = subprocess.Popen(["dmget", basedir + prev_date + filedir, "/archive/x1y/yxue/realtime/temp.clim.1981_2010.nc"],cwd=dirWhereIwantThisToHappen)
        child.communicate() #this will close the subprocess

        cmd1 ="Use " + basedir + prev_date + filedir
        (errval, errmsg) = pyferret.run(cmd1)

if __name__=="__main__":
    mymain()



