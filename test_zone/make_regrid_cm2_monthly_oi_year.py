#!/usr/bin/env python

import subprocess
import datetime
import os

try:
    import pyferret
except ImportError:
    print "You must module load pyferret"
    exit(1)   

def mymain():

	#print '.'
	today = raw_input("Enter today's date (mmyyyy): ")

	date = datetime.datetime.strptime('25' + today, '%d%m%Y')
	month = date.strftime('%m')
	month_abrev = date.strftime('%b')
	month_abrev_low = month_abrev.lower()
	year = date.strftime('%Y')
	year_abrev = date.strftime('%y')
	year_prev = str(int(year)-1)
	year_prev_abrev = year_prev[-2:]

	if month == "01":
		print "oh no its january"
		exit(1)

	sst_outfile = "sstcm21_oimonthly_" + year + ".nc"
	sst_outfile_prev = "sstcm21_oimonthly_" + year_prev + ".nc"
	sst_outfile_combo = "sstcm21_oimonthly_" + year_prev_abrev + year_abrev + ".nc"

	pyferret.start(quiet=True)

	cmd1 = 'use /net2/sdu/NMME/oisst/NetCDF/sstcm2_daily_' + year_abrev + '0101_' + year_abrev + month + '01.nc'
	cmd2 = 'set memory/size=400'
	cmd3 = 'DEFINE AXIS/T="15-jan-' + year + '":"15-' + month_abrev_low + '-' + year + '":1/npoint=2/UNIT=month tmonth'
	cmd4 = 'let sst_month = temp[gt=tmonth@AVE]'
	cmd5 = 'save/clobber/file=tmp1.nc sst_month'

	(errval, errmsg) = pyferret.run(cmd1)
	(errval, errmsg) = pyferret.run(cmd2)
	(errval, errmsg) = pyferret.run(cmd3)
	(errval, errmsg) = pyferret.run(cmd4)
	(errval, errmsg) = pyferret.run(cmd5)

	os.remove("ferret.jnl")

	d ="." #it all happens in the local dir
	child = subprocess.Popen(["ncrename","-v", "SST_MONTH,temp", "tmp1.nc"],cwd=d)
	child.communicate()

	child = subprocess.Popen(["ncrename","-v", "TMONTH,t", "tmp1.nc"],cwd=d)
	child.communicate() 

	child = subprocess.Popen(["ncrename","-d", "TMONTH,t", "tmp1.nc"],cwd=d)
	child.communicate() 

	child = subprocess.Popen(["ncrcat","-O","-v","temp", "tmp1.nc", sst_outfile],cwd=d)
	child.communicate()

   	child = subprocess.Popen(["ncrcat", sst_outfile_prev, sst_outfile, sst_outfile_combo],cwd=d)
	child.communicate() 
 
	returnCode = child.returncode

	cmd6 = "cancel data/all"
	(errval, errmsg) = pyferret.run(cmd6)

	cmd7 = "go sst_rms_v3.1_product.jnl"
	(errval, errmsg) = pyferret.run(cmd7)

	os.remove("tmp1.nc")

if __name__=="__main__":
    mymain()



	#ncrename -v SST_MONTH,temp tmp1.nc	###########################VVVVVVVVVVVVVVVVVVVVV
	#ncrename -v TMONTH,t tmp1.nc
	#ncrename -d TMONTH,t tmp1.nc
	
	#ncrcat -O -v temp tmp1.nc ${sst_outfile}

	
	# clean up
	#\rm -f tmp[12].nc        ##################################
