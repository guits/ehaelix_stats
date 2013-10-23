#!/usr/bin/python

import os
import subprocess
import sys

host = "eno-eh9-b2.mut-8.hosting.enovance.com"

def exec_command_by_ssh(host, command):
	process = subprocess.Popen("ssh %s '%s'" % (host, command), stdout=subprocess.PIPE, stderr=None, shell=True) 
	output = process.communicate()

	return [ line for line in output[0].split("\n") if line != '' ]

def exec_command_on_vz(host, vz_id, command):
#	print "ssh %s \"vzctl exec %s \\\"%s\\\"\"" % (host, vz_id, command)
	process = subprocess.Popen("ssh %s \"vzctl exec %s \\\"%s\\\"\"" % (host, vz_id, command), stdout=subprocess.PIPE, stderr=None, shell=True)
	output = process.communicate()
	return [ line for line in output[0].split("\n") if line != '' ]

def get_vz_list(host):
	vzlist_raw = exec_command_by_ssh(host, "vzlist -a -H -o ctid,hostname,status")
	vzlist = []
	for vz in vzlist_raw:
		vzinfo = vz.split()
		if not vzinfo: continue
		vzlist.append({
			'id': vzinfo[0],
			'hostname': vzinfo[1],
			'status': vzinfo[2],
			'physical_host': host
			})
	return vzlist

def get_cpu_info_vz(vz_id):
	command = "cat /proc/cpuinfo | grep 'cpu MHz'"
	result = exec_command_on_vz(vz['physical_host'], vz_id, command)
	return result
		

vzlist = get_vz_list(host)

for vz in vzlist:
	cpuinfo = get_cpu_info_vz(vz['id'])
	print vz['hostname']
	print cpuinfo