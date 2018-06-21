#!/usr/bin/env /usr/bin/python
import re
import socket
# pip install netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException

AUTHOR='Emilio <ec@ekio.jp>'
DATE='Jun-21-2018'
VERSION='0.2'

def grep_all(pattern, file_path):
    busca = re.compile(pattern)
    with open(file_path, "r") as f:
        return busca.findall(f.read())

def grep_one(pattern, file_path):
    busca = re.compile(pattern)
    with open(file_path, "r") as f:
        return busca.search(f.read())

def login(ip,gu,gp,ju,jp,tu,tp,te,ku,kp,ke):
    device = {'device_type':'cisco_ios_telnet', 'ip':ip, 'username':gu, 'password':gp, 'secret':gp }
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
    except NetMikoAuthenticationException:
        router['username'] = ju
        router['password'] = jp
        router['secret'] = jp
        try:
            net_connect = ConnectHandler(**device)
            net_connect.enable()
        except NetMikoAuthenticationException:
            router['username'] = tu
            router['password'] = tp
            router['secret'] = tp
            try:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
            except NetMikoAuthenticationException:
                router['username'] = tu
                router['password'] = tp
                router['secret'] = te
                try:
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                except NetMikoAuthenticationException:
                    router['username'] = ku
                    router['password'] = kp
                    router['secret'] = ke
                    try:
                        net_connect = ConnectHandler(**device)
                        net_connect.enable()
                    except NetMikoAuthenticationException:
                        print 'ERROR: No credentials valid for device '+ip+' (over telnet)'
                        net_connect = False
    except socket.error:
        router['device_type'] = 'cisco_ios'
        router['username'] = gu
        router['password'] = gp
        router['secret'] = gp
        try:
            net_connect = ConnectHandler(**device)
            net_connect.enable()
        except NetMikoAuthenticationException:
            router['username'] = ju
            router['password'] = jp
            router['secret'] = jp
            try:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
            except NetMikoAuthenticationException:
                router['username'] = tu
                router['password'] = tp
                router['secret'] = tp
                try:
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                except NetMikoAuthenticationException:
                    router['username'] = tu
                    router['password'] = tp
                    router['secret'] = te
                    try:
                        net_connect = ConnectHandler(**device)
                        net_connect.enable()
                    except NetMikoAuthenticationException:
                        router['username'] = ku
                        router['password'] = kp
                        router['secret'] = ke
                        try:
                            net_connect = ConnectHandler(**device)
                            net_connect.enable()
                        except NetMikoAuthenticationException:
                            print 'ERROR: No credentials valid for device '+ip+' (over ssh)'
                            net_connect = False
        except SSHException:
            print 'ERROR: Can\'t connect to '+ip+' on port 23 or 22 (telnet/ssh)'
            net_connect = False
    return net_connect
