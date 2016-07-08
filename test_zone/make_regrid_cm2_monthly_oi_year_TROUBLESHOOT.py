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

	os.remove("ferret.jnl")

	d ="." #it all happens in the local dir

	child = subprocess.Popen(["csh", "make_regrid_cm2_monthly_oi_year.csh"],cwd=d)
	child.communicate() 

   	child = subprocess.Popen(["ncrcat", sst_outfile_prev, sst_outfile, sst_outfile_combo],cwd=d)
	child.communicate() 
 
	returnCode = child.returncode

	cmd6 = "cancel data/all"
	(errval, errmsg) = pyferret.run(cmd6)

	cmd7 = "go sst_rms_v3.1_product.jnl"
	(errval, errmsg) = pyferret.run(cmd7)


if __name__=="__main__":
    mymain()



	#ncrename -v SST_MONTH,temp tmp1.nc	###########################VVVVVVVVVVVVVVVVVVVVV
	#ncrename -v TMONTH,t tmp1.nc
	#ncrename -d TMONTH,t tmp1.nc
	
	#ncrcat -O -v temp tmp1.nc ${sst_outfile}

	
	# clean up
	#\rm -f tmp[12].nc        ##################################
