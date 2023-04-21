import netCDF4 as nc
import pandas as pd
import numpy as np
import os
import sys

input_args=sys.argv
print(input_args[1],flush=True)
min_time=input_args[1]
max_time=input_args[2]

tm=np.zeros(120)
sst = "../ncdata/SST_3daily.nc"
ds = nc.Dataset(sst)
lat = ds["latitude"][:].data
lon = ds["longitude"][:].data
yearday = ds["yearday"][:].data
temp = ds["SST"][:].data
opt=[33.0,-3.0,1.0,5.0,9.0,13.0,17.0,21.0,25.0,29.0]
sizes=[3]*10+[4.5]*10+[6.6]*10+[9.8]*10+[14]*10
print("Temp done",flush=True)

folder_location="/nobackup1/stephdut/GUD_20151027/run15_151_grazsame3_temperature_new_pared_nomort2"
path3d=[]
for i in range(1,121):
    p=11544+(i-1)*24
    a=os.path.join(folder_location,"3DAILY","3d.00000"+str(p)+".nc")
    path3d.append(a)


## create tracer array
nmt = [str(curr+60) for curr in range(1,40)] + ["0"+str(curr) for curr in ["a","b","c","d","e","f","g","h","i","j","k"]]

tm=[]
abund_category=[]
biomass=[]
day=[]
cocco_type=[]
opt_temps=[]
sst=[]
latitudes=[]
longitudes=[]

pd.DataFrame({"Abundance_Category":abund_category,
                            "Biomass":biomass,
                            "Day":day,
                            "Coccolithophore_Type":cocco_type,
                            "Optimum_Temp":opt_temps,
                            "ESD":[],
                            "SST":sst,
                            "Latitude":latitudes,
                            "Longitude":longitudes}).to_csv("coccolithophore_data_output_step_w_"+str(min_time) + "_" + str(max_time) + ".csv")

for i in range(int(min_time),int(max_time)): # day of year (3-daily)
    time_data = nc.Dataset(path3d[i])
    t = time_data["T"][:].data
    tm.append(int(t[0]/3600.0/24.0-1442.0))
    for types in range(0,50): # coccolithophore types
        nm_curr=nmt[types]
        #p_file=nc.Dataset(path3d[i])
        p_temp=time_data["TRAC"+nm_curr][:].data
        print("Type",types,"Time",i,flush=True)
        curr_df = pd.DataFrame()
        counter=0
        for y in range(len(lat)):
            latitude=lat[y]
            for x in range(len(lon)):
                longitude=lon[x]
                tm.append(int(t[0]/3600.0/24.0-1442.0))
                if p_temp[0,0,y,x] > 0.01:
                    abund_category = "Present"
                else:
                    abund_category = "Absent"
                if p_temp[0,0,y,x] > 0:
                    curr_df = pd.concat([curr_df,pd.DataFrame({"Abundance_Category":abund_category,
                                                          "Biomass":p_temp[0,0,y,x],
                                                          "Day":yearday[i],
                                                          "Coccolithophore_Type":types,
                                                          "Optimum_Temp":opt[types%10],
                                                          "ESD":sizes[types],
                                                          "SST":temp[i,y,x],
                                                          "Latitude":latitude,
                                                          "Longitude":longitude},index=[counter])])
                counter=counter+1
                
        curr_df.to_csv("coccolithophore_data_output_step_w_"+str(min_time) + "_" + str(max_time) + ".csv",mode="a", index=False, header=False)
                    
