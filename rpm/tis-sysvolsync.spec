%define _topdir   .
%define buildroot ./builddir
%define sysvolsync_version %(python ../sysvolsync.py -V)

Name:	tis-sysvolsync
Version:    %(python ../sysvolsync.py -V)
Release:	1%{?dist}
Summary:	Sysvol sync for samba4
BuildArch:	x86_64

Group:      System Environment/Daemons
License:	GPL
URL:		https://www.tranquil.it
Source0:	../
Prefix:		/opt

Requires:  python3-requests, python3-lxml, python3-ldap, procps

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description

%install
set -ex

mkdir -p %{buildroot}/opt/tis-sysvolsync/templates/
mkdir -p %{buildroot}/opt/tis-sysvolsync/bin/
mkdir -p %{buildroot}/opt/tis-sysvolsync/data/

mkdir -p %{buildroot}/etc/tis-sysvolsync/

mkdir -p %{buildroot}/usr/lib/systemd/system/

rsync -aP ../../sysvolsync.py  %{buildroot}/opt/tis-sysvolsync/
rsync -aP ../../bin/  %{buildroot}/opt/tis-sysvolsync/bin/
rsync -aP ../../files/tis-sysvol*.service  %{buildroot}/usr/lib/systemd/system/
rsync -aP ../../templates/config.xml.template  %{buildroot}/opt/tis-sysvolsync/templates/

%files

%attr(755,root,root)/opt/tis-sysvolsync/
%attr(755,root,root)/opt/tis-sysvolsync/sysvolsync.py
%attr(755,root,root)/opt/tis-sysvolsync/bin/syncthing
%attr(755,root,root)/etc/tis-sysvolsync/
%attr(755,root,root)/opt/tis-sysvolsync/data/
%attr(755,root,root)/usr/lib/systemd/system/

%pre


%post
[ -f /opt/tis-sysvolsync/data/config.xml ] || cp /opt/tis-sysvolsync/templates/config.xml.template /opt/tis-sysvolsync/data/config.xml
