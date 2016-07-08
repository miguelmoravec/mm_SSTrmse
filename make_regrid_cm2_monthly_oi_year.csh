
foreach year ( 2016 )

set sst_outfile = sstcm21_oimonthly_${year}.nc 
set year2 = ${year}

\rm -f ${sst_outfile} tmp1.nc tmp2.nc

pyferret <<!
!sp dmget /archive/x1y/archive/CM2.1R_ECDA_v4.1_48m1440p_ps2dpuv_ispd/history/ensm/19990101.ocean_month.ensm.nc
!use "/archive/x1y/archive/CM2.1R_ECDA_v4.1_48m1440p_ps2dpuv_ispd/history/ensm/19990101.ocean_month.ensm.nc"
!sp dmget /archive/snz/fms/oda_data/sst/weekly/sstcm2_daily_19490101_20101003.nc
!use "/archive/snz/fms/oda_data/sst/weekly/sstcm2_daily_19490101_20101003.nc"
!use "/archive/nmme/NMME/INPUTS/oisst/sstcm2_daily_150101_150501.nc"
use "/net2/sdu/NMME/oisst/NetCDF/sstcm2_daily_160101_160301.nc"
set memory/size=400
!#let sst1 = sst[d=2,gx=geolon_t[d=1],gy=geolat_t[d=1],t=3-may-2010:3-oct-2010]
!let sst = sst1[d=2,gx=temp[d=1]@ASN,gy=temp[d=1]@ASN]
!let sst = sst1[d=2,gx=temp[d=1],gy=temp[d=1]]
!let sst2 = IF abs(temp[d=1,z=0,l=1]) LT  100 THEN sst1[d=2,gxy=temp[d=1,l=1,z=0]]
!let sst2 = IF abs(sst[d=1,l=1]) LT  100 THEN temp[d=2,gxy=sst[d=1,l=1]]
!define a monthly asix 
DEFINE AXIS/T=15-jan-${year}:15-feb-${year}:1/npoint=2/UNIT=month  tmonth
let sst_month = temp[gt=tmonth@AVE]
!let sst_mask = IF abs(temp[d=1,z=0]) LT  100 THEN 1
!let sst2 = sst1[d=2,gx=temp[d=1,z=0],gy=temp[d=1,z=0]]*sst_mask[gt=sst1[d=2]]
save/clobber/file=tmp1.nc sst_month
exit
!
rm -f ferret*.jnl*

ncrename -v SST_MONTH,temp tmp1.nc
ncrename -v TMONTH,t tmp1.nc

ncrename -d TMONTH,t tmp1.nc

ncrcat -O -v temp tmp1.nc ${sst_outfile}

# clean up
\rm -f tmp[12].nc

end
