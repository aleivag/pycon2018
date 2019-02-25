#!/usr/bin/env python

import os
import socket
import shlex
import sys

import subprocess

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter


import pystemd
import pystemd.run

stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr

from IPython.terminal.embed import InteractiveShellEmbed

display_banner = f"""
Welcome to pycon interactive shell for python {sys.version}.
"""

os.environ['EDITOR']='vim'

def _epd(cmd):
    shell.magic("%clear")
    print('>>>', highlight(cmd, PythonLexer(), TerminalFormatter()), '\n')
    exec(cmd)
    return cmd

def unit_status(unit):
    shell.magic("%clear")
    if isinstance(unit, pystemd.systemd1.Unit):
        unit = unit.Unit.Names[0].decode()
    cmd = f'systemctl status {unit} --no-pager'
    print(f'[shell] {cmd}\n')
    subprocess.call(shlex.split(cmd))

def unit_stop(unit):
    shell.magic("%clear")
    if isinstance(unit, pystemd.systemd1.Unit):
        unit = unit.Unit.Names[0].decode()
    cmd = f'systemctl stop {unit}'
    print(f'[shell] {cmd}\n')
    subprocess.call(shlex.split(cmd))



def unit_clean(unit='mys.service'):
    unit_stop(unit)
    subprocess.call(shlex.split('systemctl reset-failed'))

status_unit = unit_status
stop_unit = unit_stop
clean_unit = unit_clean

def echo_pycon():
    return _epd(
        """pystemd.run(['/bin/echo', 'hi PYCON!!!'], stdout=sys.stdout)"""
    )

def bash_pycon():
    return _epd(
        """pystemd.run(
    ['/bin/bash'],
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
)"""
    )

def home_system_protect_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        'ProtectHome': 'true',
        'ProtectSystem': 'strict',
    }
)""")


def directories_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        
        'ReadOnlyDirectories': ['/root'],
        'InaccessibleDirectories': ['/home'],
        'ReadWriteDirectories': ['/var/log'],
        
        'PrivateTmp': True,
        'TemporaryFileSystem': [('/var/cache/mys', '')],
        
        'BindPaths': [('/srv/pycon', '/var/cache/mys/lib/', False, 0)],
        'BindReadOnlyPaths': [('/usr/bin/python', '/var/cache/mys/bin/python', False, 0)],
        
    }
)""")


def venv_pycon():
    return _epd("""pystemd.run(
    ['/var/cache/mys/bin/python', '-c', 'import six; print(six.__file__); input()'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={

        'TemporaryFileSystem': [('/var/cache/mys', '')],

        'BindReadOnlyPaths': [
            ('/usr/bin/python', '/var/cache/mys/bin/python', False, 0),
            ('/lib/python3.6/site-packages/six.py', '/var/cache/mys/lib/python3.6/site-packages/six.py', False, 0),
            ('/usr/share/venvs.conf/pyvenv-wo-site-packages.cfg', '/var/cache/mys/pyvenv.cfg', False, 0)
        ],
    }
)""")


def private_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={

        'PrivateNetwork': True,
        'PrivateDevices': True,
    }
)""")


def dynamic_user_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        'DynamicUser': True,
    }
)""")


def ip_user_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        'IPAddressDeny': [(socket.AF_INET, (0,0,0,0), 0)], # 0.0.0.0/0
        'IPAddressAllow': [(socket.AF_INET, (8,8,8,8), 32)], # 8.8.8.8/32
    }
)""")


def cgroup_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        'CPUQuota': 0.2,
        'MemoryMax': 1024*1024*10,
        'TasksMax': 5,
    }
)""")


def chroot_pycon():
    return _epd("""pystemd.run(
    ['/bin/bash'], 
    stdin=sys.stdin, stdout=sys.stdout, 
    wait=True, pty=True, 
    name='mys.service',
    extra={
        'RootDirectory': '/var/lib/machines/debian',
        
        'MountAPIVFS': True,
    }
)""")


def exit():
    shell.magic("%clear")
    print('we are done!!!')
    shell.exiter()


PAST_MENU = []

MENU = [

    home_system_protect_pycon,

    directories_pycon,

    ip_user_pycon,

    cgroup_pycon,
    chroot_pycon,

    exit,
]


def n():
    "Next element in the MENU"
    PAST_MENU.append(MENU.pop(0))
    return PAST_MENU[-1]()

def p():
    """Previous element in the menu"""
    MENU.insert(0, PAST_MENU.pop())
    return MENU[0]()


def r():
    shell.magic("%clear")
    shell.magic("%rep")


for k in pystemd.systemd1.unit_signatures.KNOWN_UNIT_SIGNATURES:
    k = k.decode()
    exec(f'{k}="{k}"')


if __name__ == '__main__':

    shell = InteractiveShellEmbed()
    clean_unit()
    shell.show_banner(display_banner)
    shell.magic("%autocall 2")
    shell.magic("%clear")
    shell.mainloop()
