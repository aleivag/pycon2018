#!/bin/bash

#set -e

rm -rf /home/terry/

pacman -Syy
pacman -Su --noconfirm
pacman  --noconfirm -S cython ipython python-pip python-wheel vim git debootstrap pandoc

pip install pypandoc Pygments

# lets install debian in the background
systemd-run --unit install-debian.service /usr/bin/debootstrap --include "dbus,vim" unstable /var/lib/machines/debian

# install pystemd
git clone https://github.com/facebookincubator/pystemd /usr/src/pystemd &&
cd /usr/src/pystemd &&
rm -rf dist/* &&
python setup.py bdist_wheel &&
pip install dist/* || /bin/true

mkdir -p /usr/share/venvs.conf

cat <<EOT > /usr/share/venvs.conf/pyvenv-wo-site-packages.cfg
home = /usr/bin
include-system-site-packages = false
version = 3.6.5
EOT

cat <<EOT > /usr/share/venvs.conf/pyvenv-w-site-packages.cfg
home = /usr/bin
include-system-site-packages = true
version = 3.6.5
EOT

cat <<EOT >> /home/vagrant/.bashrc

test -e /var/lib/machines/debian/etc/os-release ||  systemctl -q is-active install-debian.service ||\
    sudo systemd-run --unit install-debian.service /usr/bin/debootstrap --include "dbus,vim" unstable /var/lib/machines/debian || /bin/true

test -z "\${INVOCATION_ID}" && sudo tmux

EOT


cat <<EOT >> /root/.bashrc

cd /srv/pycon

EOT