#!/usr/bin/env python

#This script automatically generates plots of SST RMSE over the Pacific for the current and last calendar year
#This script relies on a standard naming convention of daily SST NetCDF files in this directory: /net2/sdu/NMME/oisst/NetCDF/
#This script also relies on the relevent des file 'ecda_v31_ocean.ensm.des' being located in this directory: /home/x1y/gfdl/ecda_operational/sst/ecda_v31_ocean.ensm.des
#This script also relies on the presence of two jnl files, '1head.jnl' and '2body.jnl', in the local directory

import subprocess
import datetime
import os
import os.path

try:
    import pyferret
except ImportError:
    print "You must module load pyferret"
    exit(1)   

def mymain():

	#sets time variables, used in generation of NetCDFs, plots, and file names	

	print 'Please answer the following question to plot SST RMSE over the Pacific for the current and last calendar year...'
	today = raw_input("Enter desired end date (mmyyyy): ")

	date = datetime.datetime.strptime('25' + today, '%d%m%Y')
	month = date.strftime('%m')
	month_abrev = date.strftime('%b')
	month_abrev_low = month_abrev.lower()
	year = date.strftime('%Y')
	year_abrev = date.strftime('%y')
	year_prev = str(int(year)-1)
	year_prev_abrev = year_prev[-2:]
	timeline = str(int(month)+11)

	print 'Generating plots with available data from ', year_prev, '/', year, '...'


	sst_outfile = "sstcm21_oimonthly_" + year + ".nc"
	sst_outfile_prev = "sstcm21_oimonthly_" + year_prev + ".nc"
	sst_outfile_combo = "sstcm21_oimonthly_" + year_prev_abrev + year_abrev + ".nc"

	pyferret.start(quiet=True)
	os.remove("ferret.jnl")

	#the following replaces Xiasong's csh file, and makes one NetCDF file with two years worth of daily SST data averaged monthly

	if os.path.isfile("tmp1.nc"):
		os.remove("tmp1.nc")

	if os.path.isfile(sst_outfile_combo):
		os.remove(sst_outfile_combo)

	if month == "01":
		cmd1 = 'use /net2/sdu/NMME/oisst/NetCDF/sstcm2_daily_' + year_prev_abrev + '0101_' + year_abrev + month + '01.nc'	
	else:
		cmd1 = 'use /net2/sdu/NMME/oisst/NetCDF/sstcm2_daily_' + year_abrev + '0101_' + year_abrev + month + '01.nc'

	cmd2 = 'set memory/size=400'
	cmd3 = 'DEFINE AXIS/T=15-jan-' + year + ':15-' + month_abrev_low + '-' + year + ':1/npoint=' + month + '/UNIT=month tmonth'
	cmd4 = 'let sst_month = temp[gt=tmonth@AVE]'
	cmd5 = 'save/clobber/file=tmp1.nc sst_month'

	(errval, errmsg) = pyferret.run(cmd1)
	(errval, errmsg) = pyferret.run(cmd2)
	(errval, errmsg) = pyferret.run(cmd3)
	(errval, errmsg) = pyferret.run(cmd4)
	(errval, errmsg) = pyferret.run(cmd5)

	d ="."

	child = subprocess.Popen(["ncrename","-v", "SST_MONTH,temp", "tmp1.nc"],cwd=d)
	child.communicate()
	child = subprocess.Popen(["ncrename","-v", "TMONTH,t", "tmp1.nc"],cwd=d)
	child.communicate() 
	child = subprocess.Popen(["ncrename","-d", "TMONTH,t", "tmp1.nc"],cwd=d)
	child.communicate() 
	child = subprocess.Popen(["ncrcat","-O","-v","temp", "tmp1.nc", sst_outfile],cwd=d)
	child.communicate()
   	child = subprocess.Popen(["ncrcat", "/home/x1y/gfdl/ecda_operational/sst/" + sst_outfile_prev, sst_outfile, sst_outfile_combo],cwd=d)
	child.communicate()

	returnCode = child.returncode

	os.remove("tmp1.nc")

	#the following automates the pyferret plot generation and saves a png image file in the local directory

	filename = 'sst_amo_' + month + '_' + year + '.png'

	cmd6 = "go 1head.jnl"
	cmd7 = "use " + sst_outfile_combo
	cmd8 = "let temp2 = temp[d=2, gxy=sst[d=1],gt=sst[d=1]@asn]"
	cmd9 = "let err1 = sst[d=1,z=0,l=1:" + timeline + "] - temp2[d=2,l=1:" + timeline+ "]"
	cmd10 = "go 2body.jnl"
	cmd11 = 'FRAME/FILE=' + filename

	(errval, errmsg) = pyferret.run(cmd6)
	(errval, errmsg) = pyferret.run(cmd7)
	(errval, errmsg) = pyferret.run(cmd8)
	(errval, errmsg) = pyferret.run(cmd9)
	(errval, errmsg) = pyferret.run(cmd10)
	(errval, errmsg) = pyferret.run(cmd11)

	print 'Plot image file for SST RMSE ', year_prev, '/', year, ' is located in the local directory (if data was available) and is named: ', filename
	print 'If no plots generated, please see script comments to find necessary input files.'

if __name__=="__main__":
    mymain()
