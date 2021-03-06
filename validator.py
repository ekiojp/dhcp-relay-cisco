#!/usr/bin/env /usr/bin/python
import re
import sys
import getpass
import socket
import threading
from Queue import Queue
# pip install pyping
import pyping
# pip install netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
# git clone https://github.com/ekiojp/dhcp-relay-cisco/common.py
from common import login
from common import grep_all

__author__ = 'Emilio <ec@ekio.jp>'
__date__ = 'Jul-5-2018'
__version__ = '0.4'

def device_session(IP,scope,gu,gp,ju,jp,tu,tp,te,ku,kp,ke,output_q):
    output_dict = {}
    net_connect = login(IP,gu,gp,ju,jp,tu,tp,te,ku,kp,ke)
    if net_connect:
        prompt = re.sub('[>|#]', '', net_connect.find_prompt())
        shint = net_connect.send_command('show ip interface brief | i ' + IP).split('\n')
        if len(shint) > 1:
            for x in range(len(shint)):
                if shint[x].split()[1] == IP:
                    shrunint = net_connect.send_command('show run interface '
                                                        + shint[x].split()[0]
                                                        + ' | i helper-address|dhcp relay address')
                    if re.search('helper-address', shrunint):
                        output = ',IOS,' + prompt + ',' + IP + ',' + shint[x].split()[0]
                        + ',None,None,None\n'
                    elif re.search('dhcp relay address', shrunint):
                        output = ',NX,' + prompt + ',' + IP + ',' + shint[x].split()[0]
                        + ',None,None,None\n'
                    else:
                        output = ',None,' + prompt + ',' + IP + ',' + shint[x].split()[0]
                        + ',None,None,None\n'
        else:
            shstb = net_connect.send_command('show standby brief | i ' + IP)
            if 'Invalid' not in shstb:
                m = re.search('.* ' + IP, shstb)
                if m:
                    regex = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                    peerip = re.search(regex, shstb).group()
                    peer_connect = login(peerip,
                                         gu,
                                         gp,
                                         ju,
                                         jp,
                                         tu,
                                         tp,
                                         te,
                                         ku,
                                         kp,
                                         ke
                                        )
                    if peer_connect:
                        peer_prompt = re.sub('[>|#]', '', peer_connect.find_prompt())
                        shint = peer_connect.send_command('show ip interface brief | i ' + peerip).split('\n')
                        if len(shint) == 1:
                            peerint = shint[0].split()[0]
                        else:
                            peerint = 'None'
                        peer_connect.disconnect()
                    else:
                        peer_prompot = 'None,None,None'
                    output = (',IOS,' + prompt + ',' + IP + ',' + m.group().split()[0] + ','
                              + peer_prompt + ',' + peerip + ',' + peerint + '\n')
            else:
                shhsrp = net_connect.send_command('show hsrp brief | i ' + IP)
                m = re.search('.* ' + IP, shhsrp)
                if m:
                    regex = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                    peerip = re.search(regex, shhsrp).group()
                    peer_connect = login(peerip,
                                         gu,
                                         gp,
                                         ju,
                                         jp,
                                         tu,
                                         tp,
                                         te,
                                         ku,
                                         kp,
                                         ke
                                        )
                    if peer_connect:
                        peer_prompt = re.sub('[>|#]', '' , peer_connect.find_prompt())
                        shint = peer_connect.send_command('show ip interface brief | i ' + peerip).split('\n')
                        if len(shint) == 1:
                            peerint = shint[0].split()[0]
                        else:
                            peerint = 'None'
                        peer_connect.disconnect()
                    else:
                        peer_prompt = 'None,None,None'
                    output = (',NX,' + prompt + ',' + IP + ',' + m.group().split()[0]
                              + ',' + peer_prompt + ',' + peerip + ',' + peerint + '\n')

        net_connect.disconnect()
    else:
        output = ',NA,NA,'+IP+',NA,NA,NA,NA\n'

    output_dict[scope] = output
    output_q.put(output_dict)


if __name__ == "__main__":

    if len(sys.argv) <= 2:
        print 'Author: ' + __author__
        print 'Date: ' + __date__
        print 'Version: ' + __version__
        print '\nUsage: ' + sys.argv[0] + ' <dhcp-dump> <scope-list>'
        print ('\n<dhcp-dump> input file with Windows DHCP'
               + ' dump format (after cleaner.py)')
        print ('<scope-list> CSV output format: '
               + '<Scope>,<IOS/NX/None>,<ACT_hostname>,<ACT_IP>,'
               + '<ACT_Intf>,<STB_hostname>,<STB_IP>,<STB_Intf>\n')
        sys.exit(0)

    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]
    salida = open(OUTPUT,'w')

    scopelist=[]
    with open(INPUT,'r') as sfile:
        for line in sfile:
            if line not in ['\n', '\r\n']:
                scopelist.append(line.split()[1])
    mm = set(scopelist)
    scopelist = list(mm)

    gu = raw_input('First TACACS Username: ')
    gp = getpass.getpass('First TACACS Password: ')
    ju = raw_input('Second TACACS Username: ')
    jp = getpass.getpass('Second TACACS Password: ')
    tu = raw_input('Third Local Username: ')
    tp = getpass.getpass('Third Local Password: ')
    te = getpass.getpass('Third Local Enable: ')
    ku = raw_input('Fourth Local Username: ')
    kp = getpass.getpass('Fourth Local Password: ')
    ke = getpass.getpass('Fourth Local Enable: ')

    output_q = Queue()

    for x in range(len(scopelist)):
        regex = 'Scope ' + scopelist[x] + ' set optionvalue 3 IPADDRESS .*'
        aver = grep_all(regex, INPUT)
        if len(aver) == 1:
            IP = re.sub('"','',aver[0].split()[6])
            response = pyping.ping(IP,count=1)
            if response.ret_code == 0:
                my_thread = threading.Thread(target=device_session,
                                             args=(IP,
                                                   scopelist[x],
                                                   gu,
                                                   gp,
                                                   ju,
                                                   jp,
                                                   tu,
                                                   tp,
                                                   te,
                                                   ku,
                                                   kp,
                                                   ke,
                                                   output_q)
                                            )
                my_thread.start()
            else:
                print (
                    'ERROR: Scope ' + scopelist[x]
                    + ' can\'t ping scope gateway (' + IP + ')'
                )
                salida.write(scopelist[x]+',NotPing,,,,,,\n')
        elif len(aver) > 1:
            print (
                'ERROR: Scope ' + scopelist[x]
                + ' have too many gateways'
            )
            salida.write(scopelist[x]+',ManyGateway,,,,,,\n')
        else:
            print 'ERROR: Scope ' + scopelist[x] + ' doesn\'t have a gateway'
            salida.write(scopelist[x]+',NoGateway,,,,,,\n')

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            salida.write(k+val)

    salida.close()
