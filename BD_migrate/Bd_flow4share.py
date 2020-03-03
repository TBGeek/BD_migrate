#-*-encoding:utf-8-*-
"""Bd_flow4share.py:主要用于爬取百度迁徙数据."""
__author__      = "LObsangTashi"
from multiprocessing  import Process
import multiprocessing
import akshare as ak
import pandas as pd
import io
import os 
import configparser
import importlib,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
importlib.reload(sys)





def get_data(city,tt,dt):
	migration_area_baidu_df = ak.migration_area_baidu(area=city, indicator=tt, date=dt)
	return migration_area_baidu_df

if __name__ == '__main__':
	param={}
	paramstr = ['month','dayrange','movetype','output']
	config  = configparser.ConfigParser()
	cfgname = 'conf_bdmigration'
	with open(cfgname,'r') as cfgfile:
		config.read_file(cfgfile)		
		for pname in paramstr:
			param[pname] = config.get('param',pname)
	day=param["dayrange"].split(",")
	tt=param["movetype"]
	path=param["output"]
	lst = [param["month"]+"%02d"%i for i in range(int(day[0]),int(day[-1]))] 
	

	df=pd.read_csv("China_citynamelst.csv",header=0)
	for name,group in df.groupby("Pr"):
		newfolder=path+"\\"+name
		if os.path.exists(newfolder):
			pass
		else:
			os.mkdir(newfolder)
		for j in group.values:
			files=newfolder+"\\"+j[-1]
			if os.path.exists(files):
				pass
			else:
				os.mkdir(files)
			for md in lst:
				try:
					df=get_data(j[1],tt,md)
					output_name=md+"_"+tt+".csv"
					outfile=files+"//"+output_name
					df.to_csv(outfile,index=False)
				except:
					continue



		