#!/usr/bin/env python
import re
import socket
# pip install netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException

__author__ = 'Emilio <ec@ekio.jp>'
__date__ = 'Jun-22-2018'
__version__ = '0.3'

def grep_all(pattern, file_path):
    busca = re.compile(pattern)
    with open(file_path, "r") as f:
        return busca.findall(f.read())

def grep_one(pattern, file_path):
    busca = re.compile(pattern)
    with open(file_path, "r") as f:
        return busca.search(f.read())

def find_all(pattern, lista):
    busca = re.compile(pattern)
    listajoined = '\n'.join(lista)
    return busca.findall(listajoined)

def login(ip, gu, gp, ju, jp, tu, tp, te, ku, kp, ke):
    device = {
            'device_type': 'cisco_ios_telnet',
            'ip': ip,
            'username': gu,
            'password': gp,
            'secret': gp
            }
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
    except NetMikoAuthenticationException:
        device['username'] = ju
        device['password'] = jp
        device['secret'] = jp
        try:
            net_connect = ConnectHandler(**device)
            net_connect.enable()
        except NetMikoAuthenticationException:
            device['username'] = tu
            device['password'] = tp
            device['secret'] = tp
            try:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
            except NetMikoAuthenticationException:
                device['username'] = tu
                device['password'] = tp
                device['secret'] = te
                try:
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                except NetMikoAuthenticationException:
                    device['username'] = ku
                    device['password'] = kp
                    device['secret'] = ke
                    try:
                        net_connect = ConnectHandler(**device)
                        net_connect.enable()
                    except NetMikoAuthenticationException:
                        print ('ERROR: No credentials valid for device '
                               + ip + ' (over telnet)')
                        net_connect = False
    except socket.error:
        device['device_type'] = 'cisco_ios'
        device['username'] = gu
        device['password'] = gp
        device['secret'] = gp
        try:
            net_connect = ConnectHandler(**device)
            net_connect.enable()
        except NetMikoAuthenticationException:
            device['username'] = ju
            device['password'] = jp
            device['secret'] = jp
            try:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
            except NetMikoAuthenticationException:
                device['username'] = tu
                device['password'] = tp
                device['secret'] = tp
                try:
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                except NetMikoAuthenticationException:
                    device['username'] = tu
                    device['password'] = tp
                    device['secret'] = te
                    try:
                        net_connect = ConnectHandler(**device)
                        net_connect.enable()
                    except NetMikoAuthenticationException:
                        device['username'] = ku
                        device['password'] = kp
                        device['secret'] = ke
                        try:
                            net_connect = ConnectHandler(**device)
                            net_connect.enable()
                        except NetMikoAuthenticationException:
                            print ('ERROR: No credentials valid for device '
                                   + ip + ' (over ssh)')
                            net_connect = False
        except SSHException:
            print ('ERROR: Can\'t connect to '
                   + ip + ' on port 23 or 22 (telnet/ssh)')
            net_connect = False
    return net_connect
