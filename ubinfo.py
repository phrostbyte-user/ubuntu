#!/usr/bin/env python

import subprocess, optparse
from subprocess import Popen, PIPE
from optparse import OptionParser
import re

display = [
	'os', 
	'hostname',
	'kernel', 
#	'battery',
	'uptime',
	'de', 
	'wm', 
	'packages',
	'gpu',
	'cpu',
	'ram',
#	'fs:/boot', 
#	'fs:/home',
#	'fs:/MOUNT/POINT
	'fs:/' ]

# Array containing Values
list = []

# Options
if __name__=='__main__':
	parser = OptionParser(usage='%prog [-s, --screenshot]', description='To customize the data displayed, edit the file directly and look for the display array. Note: It can only allow up to 13 fields.')
	parser.add_option('-s', '--screenshot',
		action='store_true', dest='screenshot', help='take a screenshot')
	(options, args) = parser.parse_args()

# Define colors		
color = '\x1b[1;33m' 
color2 = '\x1b[0;33m'
color3 = '\x1b[0;31m'
clear = '\x1b[0m'

# Find running processes.
p1 = Popen(['ps', '-A'], stdout=PIPE).communicate()[0].split('\n')
processes = [process.split()[3] for process in p1 if process]
p1 = None

# Find info from uname -a
uname = Popen(['uname', '-a'], stdout=PIPE).communicate()[0].split()

# Print coloured key with normal value.
def output(key, value):
	output = '%s%s:%s %s' % (color3, key, clear, value)
	list.append(output)

# Screenshot Function
screen = '%s' % options.screenshot

def screenshot():
	subprocess.check_call(['scrot', '-cd5'])

def os_display(): 
	os = Popen(['lsb_release', '-d'], stdout=PIPE).communicate()[0].split()[1::]
	output('OS', '%s %s' % (os[0], os[1]))

def kernel_display():
	output ('Kernel', '%s (%s)' % (uname[2], uname[11]))
	
def hostname_display():
	output ('Hostname', '%s' % uname[1])

def uptime_display():
	fuptime = int(open('/proc/uptime').read().split('.')[0])
	day = int(fuptime / 86400)
	fuptime = fuptime % 86400
	hour = int(fuptime / 3600)
	fuptime = fuptime % 3600
	minute = int(fuptime / 60)
	uptime = ''
	if day == 1:
		uptime += '%d day, ' % day
	if day > 1:
		uptime += '%d days, ' % day
	uptime += '%d:%02d' % (hour, minute)
	output('Uptime', uptime)

# requires acpi
def battery_display(): 
	p1 = Popen(['acpi'], stdout=PIPE).communicate()[0].lstrip()
	battery = p1.split(' ')[3].rstrip('\n')
	output ('Battery', battery)

def de_display():
	dict = {'gnome-session': 'GNOME',
		'ksmserver': 'KDE',
		'xfce-mcs-manager': 'Xfce',
		'xfconfd': 'Xfce 4.6'}
	de = 'None found'
	for key in dict.keys():
		if key in processes: de = dict[key]
	output ('DE', de)

def wm_display():
        dict = {'awesome': 'Awesome',
		'beryl': 'Beryl',
		'blackbox': 'Blackbox',
		'compiz': 'Compiz',
		'dwm': 'DWM',
		'enlightenment': 'Enlightenment',
		'fluxbox': 'Fluxbox',
		'fvwm': 'FVWM',
		'icewm': 'icewm',
		'kwin': 'kwin',
		'metacity': 'Metacity',
		'openbox': 'Openbox',
		'wmaker': 'Window Maker',
		'xfwm4': 'Xfwm',
		'xmonad': 'Xmonad'}  
        wm = 'None found'
        for key in dict.keys():
		if key in processes: wm = dict[key]
        output ('WM', wm)

def packages_display():
	p1 = Popen(['dpkg', '--get-selections'], stdout=PIPE)
	p2 = Popen(['wc', '-l'], stdin=p1.stdout, stdout=PIPE)
	packages = p2.communicate()[0].rstrip('\n')
	output ('Packages', packages)

def fs_display(mount=''):
	p1 = Popen(['df', '-TPh',  mount], stdout=PIPE).communicate()[0]
	used = [line for line in p1.split('\n') if line][1]
	used = used.split()[3]
	total = [line for line in p1.split('\n') if line][1]
	total = total.split()[2]
	type = [line for line in p1.split('\n') if line][1]
	type = type.split()[1]
	if mount == '/': mount = '/root'
	fs = mount.rpartition('/')[2].title() + " FS"
	part = '%s / %s (%s)' % (used, total, type)
   	output (fs, part)

def gpu_display():
	gpu = Popen('lspci', stdout=PIPE).communicate()[0].split('\n')
	expr = re.compile('VGA')
	# use regexp 'expr' to filter results, [1::] removes space in string
	output ('GPU', ''.join(filter(expr.search, gpu)).split(':')[2][1::])

def cpu_display():
	cpuinfo = open('/proc/cpuinfo')
	cpu = set(cpuinfo.read().split('\n'))
	cpuinfo.close()
	expr = re.compile('model n')
	output ('CPU', ''.join(filter(expr.search, cpu)).split(':')[1][1::])

def ram_display():
	raminfo = Popen(['free', '-m'], stdout=PIPE).communicate()[0].split('\n')
	ram = ''.join(filter(re.compile('M').search, raminfo)).split()
	used = int(ram[2]) - int(ram[5]) - int(ram[6])
	cache = int(ram[5]) + int(ram[6])
	output ('RAM', '%s MB / %s MB (%s MB cache)' % (used, ram[1], cache))
	
# Run functions found in 'display' array.
for x in display:
	call = [arg for arg in x.split(':') if arg]
	funcname=call[0] + '_display'
	func=locals()[funcname]
	if len(call) > 1:
		func(arg)
	else:
		func()

# Array containing values.
list.extend(['']*(15 - len(display)))

###### Result #######   
print """
%s                              ++++++           
%s                             ++++++++          
%s                  ++++++++++ %s++++++++          
%s                ++++++++++++ %s++++++++          %s
%s             ++  %s++++++++++++ %s++++++           %s
%s           +++++  %s++++++++++++ %s^^^^            %s
%s          +++++++  %s+++++++++++++++++++         %s
%s         +++++++++          %s+++++++++++        %s
%s        ++++++++++            %s++++++++++       %s
%s        ++++++++               %s++++++++++      %s
%s  ++++++ %s++++++                 %s++++++++++     %s
%s ++++++++ %s+++++                  %s+++++++++     %s
%s +++++++++ %s++++                                %s
%s ++++++++ %s+++++                  %s+++++++++     %s
%s  ++++++ %s++++++                 %s++++++++++     %s
%s        ++++++++               %s++++++++++      %s
%s        +++++++++             %s++++++++++       %s
%s         +++++++++         %s++++++++++++        %s
%s          +++++++  %s+++++++++++++++++++         
%s           +++++  %s++++++++++++ %s,,,,            
%s             ++  %s++++++++++++ %s++++++           
%s                ++++++++++++ %s++++++++          
%s                  ++++++++++ %s++++++++          
%s                             ++++++++          
%s                              ++++++           
%s """ % (color3, color3, color2, color3, color2, color3, list[0], color, color2, color3, list[1], color, color2, color3, list[2], color, color2, list[3], color, color2, list[4], color, color2, list[5], color, color2, list[6], color2, color, color2, list[7], color2, color, color2, list[8], color2, color, list[9], color2, color, color3, list[10], color2, color, color3, list[11], color, color3, list[12], color, list[13], color3, list[14], color, color3, color, color3, color, color3, color, color, color3, color, color3, color, color3, color, color, color, clear)

if screen == 'True':
	screenshot()
