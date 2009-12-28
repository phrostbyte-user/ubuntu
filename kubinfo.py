#!/usr/bin/env python

# Import libraries
import subprocess, optparse
from subprocess import Popen, PIPE
from optparse import OptionParser

# Display
display = [
	'os', 
	'hostname',
	'kernel', 
#	'battery',
	'uptime',
	'de', 
	'wm', 
	'packages',
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
color = '\x1b[1;36m' 
color2 = '\x1b[0;36m'
color3 = '\x1b[0;34m'
clear = '\x1b[0m'

# Find running processes.
p1 = Popen(['ps', '-A'], stdout=PIPE).communicate()[0].split('\n')
processes = [process.split()[3] for process in p1 if process]
p1 = None

# Print coloured key with normal value.
def output(key, value):
	output = '%s%s:%s %s' % (color3, key, clear, value)
	list.append(output)

# Screenshot Function
screen = '%s' % options.screenshot

def screenshot():
	subprocess.check_call(['scrot', '-cd5'])

# Operating System Function
def os_display(): 
	arch = Popen(['uname', '-m'], stdout=PIPE).communicate()[0].rstrip('\n')
	distro = Popen(['lsb_release', '-d'], stdout=PIPE).communicate()[0].split()[1::]
	os = '%s %s %s' % (distro[0], distro[1], arch)
	output('OS', os)

# Kernel Function
def kernel_display():
	kernel = Popen(['uname', '-r'], stdout=PIPE).communicate()[0].rstrip('\n')
	output ('Kernel', kernel)

# Kernel Function
def hostname_display():
	hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].rstrip('\n')
	output ('Hostname', hostname)

# Uptime Function
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

# Battery Function [Requires: acpi]
def battery_display(): 
	p1 = Popen(['acpi'], stdout=PIPE).communicate()[0].lstrip()
	battery = p1.split(' ')[3].rstrip('\n')
	output ('Battery', battery)

# Desktop Environment Function 
def de_display():
	dict = {'gnome-session': 'GNOME',
		'ksmserver': 'KDE',
		'xfce-mcs-manager': 'Xfce',
		'xfconfd': 'Xfce 4.6'}
	de = 'None found'
	for key in dict.keys():
		if key in processes: de = dict[key]
	output ('DE', de)

# Window Manager Function
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

# Packages Function
def packages_display():
	p1 = Popen(['dpkg', '--get-selections'], stdout=PIPE)
	p2 = Popen(['wc', '-l'], stdin=p1.stdout, stdout=PIPE)
	packages = p2.communicate()[0].rstrip('\n')
	output ('Packages', packages)

# File System Function
def fs_display(mount=''):
	p1 = Popen(['df', '-Ph',  mount], stdout=PIPE).communicate()[0]
	used = [line for line in p1.split('\n') if line][1]
	used = used.split()[2]
	total = [line for line in p1.split('\n') if line][1]
	total = total.split()[1]
	if mount == '/': mount = '/root'
	fs = mount.rpartition('/')[2].title()
	part = '%s / %s' % (used, total)
   	output (fs, part)

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
list.extend(['']*(13 - len(display)))

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
%s        +++++++++             %s++++++++++       
%s         +++++++++         %s++++++++++++        
%s          +++++++  %s+++++++++++++++++++         
%s           +++++  %s++++++++++++ %s,,,,            
%s             ++  %s++++++++++++ %s++++++           
%s                ++++++++++++ %s++++++++          
%s                  ++++++++++ %s++++++++          
%s                             ++++++++          
%s                              ++++++           
%s """ % (color3, color3, color2, color3, color2, color3, list[0], color, color2, color3, list[1], color, color2, color3, list[2], color, color2, list[3], color, color2, list[4], color, color2, list[5], color, color2, list[6], color2, color, color2, list[7], color2, color, color2, list[8], color2, color, list[9], color2, color, color3, list[10], color2, color, color3, list[11], color, color3, list[12], color, color3, color, color3, color, color3, color, color3, color, color, color3, color, color3, color, color3, color, color, color, clear)

if screen == 'True':
	screenshot()
