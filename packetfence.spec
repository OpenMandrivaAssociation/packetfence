Name:  packetfence
Summary: PacketFence network registration / worm mitigation system
Version: 3.0.0
Release: %mkrel 3
License: GPL
Group: Monitoring
Source0: http://www.packetfence.org/downloads/PacketFence/src/%{name}-%{version}.tar.gz
URL:	http://www.packetfence.org
BuildArch: noarch
BuildRequires: gettext, httpd, perl-Parse-RecDescent
Requires: chkconfig, coreutils, grep, iproute2, openssl
Requires: libpcap, libxml2, zlib1, zlib1-devel, glibc
Requires: httpd, apache-mod_ssl, php, php-gd, apache-mod_perl
# php-pear-Log required not php-pear, fixes #804
Requires: php-pear-Log
Requires: net-tools
Requires: net-snmp >= 5.3.2.2
Requires: mysql, perl-DBD-mysql
Requires: perl >= 5.8.82
Requires: perl-Apache-Htpasswd
Requires: perl-Bit-Vector
Requires: perl-CGI-Session
Requires: perl-Class-Accessor
Requires: perl-Class-Accessor-Fast-Contained
Requires: perl-Class-Data-Inheritable
Requires: perl-Class-Gomor
Requires: perl-Config-IniFiles >= 2.40
Requires: perl-Data-Phrasebook, perl-Data-Phrasebook-Loader-YAML
Requires: perl-DBI
Requires: perl-File-Tail
Requires: perl-IPC-Cmd
Requires: perl-IPTables-ChainMgr
Requires: perl-IPTables-Parse
Requires: perl-LDAP
Requires: perl(Locale::gettext)
Requires: perl-Log-Log4perl >= 1.11
Requires: perl-Net-Appliance-Session
Requires: perl-Net-Frame, perl-Net-Frame-Simple
Requires: perl-Net-MAC, perl-Net-MAC-Vendor
Requires: perl-Net-Netmask
Requires: perl-Net-Pcap >= 0.16
Requires: perl-Net-SNMP
# for SNMPv3 AES as privacy protocol, fixes #775
Requires: perl-Crypt-Rijndael
Requires: perl-Net-Telnet
Requires: perl-Net-Write
Requires: perl-Parse-Nessus-NBE
Requires: perl-Parse-RecDescent
# TODO: portability for non-x86 is questionnable for Readonly::XS
Requires: perl-Readonly, perl(Readonly::XS)
Requires: perl-Regexp-Common
Requires: rrdtool, perl-rrdtool
Requires: perl-SOAP-Lite
Requires: perl-Template-Toolkit
Requires: perl-Term-ReadKey
Requires: perl-Thread-Pool
Requires: perl-TimeDate
Requires: perl-UNIVERSAL-require
Requires: perl-YAML
Requires: php-jpgraph-packetfence = 2.3.4
Requires: php-ldap
Requires: perl(Try::Tiny)
# Required for Radius auth through captive portal
Requires: perl(Authen::Radius)
# Required for importation feature
Requires: perl(Text::CSV)
Requires: perl(Text::CSV_XS)
# Required for testing
# TODO: I noticed that we provide perl-Test-MockDBI in our repo, maybe we made a poo poo with the deps
BuildRequires: perl(Test::MockModule), perl(Test::MockDBI), perl(Test::Perl::Critic)
BuildRequires: perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::Exception), perl(Test::NoWarnings)


BuildRoot: %_tmppath/%{name}-%{version}-buildroot

%description
PacketFence is an open source network access control (NAC) system.
It can be used to effectively secure networks, from small to very large
heterogeneous networks. PacketFence provides features such
as
* registration of new network devices
* detection of abnormal network activities
* isolation of problematic devices
* remediation through a captive portal
* registration-based and scheduled vulnerability scans.


%package remote-snort-sensor
Group: Monitoring
Requires: perl >= 5.8.0, snort, perl(File::Tail), perl(Config::IniFiles), perl(IO::Socket::SSL), perl(XML::Parser), perl(Crypt::SSLeay)
Requires: perl-SOAP-Lite
Summary: Files needed for sending snort alerts to packetfence

%description remote-snort-sensor
The packetfence-remote-snort-sensor package contains the files needed
for sending snort alerts from a remote snort sensor to a PacketFence
server.


%prep
%setup -q -n pf

%build
# generate pfcmd_pregrammar
/usr/bin/perl -w -e 'use strict; use warnings; use diagnostics; use Parse::RecDescent; use lib "./lib"; use pf::pfcmd::pfcmd; Parse::RecDescent->Precompile($grammar, "pfcmd_pregrammar");'
mv pfcmd_pregrammar.pm lib/pf/pfcmd/

# generate translations
/usr/bin/msgfmt conf/locale/en/LC_MESSAGES/packetfence.po
mv packetfence.mo conf/locale/en/LC_MESSAGES/
/usr/bin/msgfmt conf/locale/es/LC_MESSAGES/packetfence.po
mv packetfence.mo conf/locale/es/LC_MESSAGES/
/usr/bin/msgfmt conf/locale/fr/LC_MESSAGES/packetfence.po
mv packetfence.mo conf/locale/fr/LC_MESSAGES/
/usr/bin/msgfmt conf/locale/it/LC_MESSAGES/packetfence.po
mv packetfence.mo conf/locale/it/LC_MESSAGES/
/usr/bin/msgfmt conf/locale/nl/LC_MESSAGES/packetfence.po
mv packetfence.mo conf/locale/nl/LC_MESSAGES/

%install
rm -rf %{buildroot}
install -D -m0755 packetfence.init %{buildroot}%{_initrddir}/packetfence
install -d %{buildroot}/usr/local/pf
install -d %{buildroot}/usr/local/pf/logs
install -d %{buildroot}/usr/local/pf/var/session
install -d %{buildroot}/usr/local/pf/var/rrd
install -d %{buildroot}/usr/local/pf/addons
cp -r bin %{buildroot}/usr/local/pf/
cp -r addons/802.1X/ %{buildroot}/usr/local/pf/addons/
cp -r addons/captive-portal/ %{buildroot}/usr/local/pf/addons/
cp -r addons/dev-helpers/ %{buildroot}/usr/local/pf/addons/
cp -r addons/freeradius-integration/ %{buildroot}/usr/local/pf/addons/
cp -r addons/high-availability/ %{buildroot}/usr/local/pf/addons/
cp -r addons/integration-testing/ %{buildroot}/usr/local/pf/addons/
cp -r addons/mrtg/ %{buildroot}/usr/local/pf/addons/
cp -r addons/snort/ %{buildroot}/usr/local/pf/addons/
cp addons/*.pl %{buildroot}/usr/local/pf/addons/
cp addons/*.sh %{buildroot}/usr/local/pf/addons/
cp addons/dhcp_dumper %{buildroot}/usr/local/pf/addons/
cp addons/logrotate %{buildroot}/usr/local/pf/addons/
cp -r sbin %{buildroot}/usr/local/pf/
cp -r conf %{buildroot}/usr/local/pf/
#pfdetect_remote
mv addons/pfdetect_remote/initrd/pfdetectd %{buildroot}%{_initrddir}/
mv addons/pfdetect_remote/sbin/pfdetect_remote %{buildroot}/usr/local/pf/sbin
mv addons/pfdetect_remote/conf/pfdetect_remote.conf %{buildroot}/usr/local/pf/conf
rmdir addons/pfdetect_remote/sbin
rmdir addons/pfdetect_remote/initrd
rmdir addons/pfdetect_remote/conf
rmdir addons/pfdetect_remote
#end pfdetect_remote
cp -r ChangeLog %{buildroot}/usr/local/pf/
cp -r configurator.pl %{buildroot}/usr/local/pf/
cp -r COPYING %{buildroot}/usr/local/pf/
cp -r db %{buildroot}/usr/local/pf/
cp -r docs %{buildroot}/usr/local/pf/
cp -r html %{buildroot}/usr/local/pf/
cp -r installer.pl %{buildroot}/usr/local/pf/
cp -r lib %{buildroot}/usr/local/pf/
cp -r NEWS %{buildroot}/usr/local/pf/
cp -r README %{buildroot}/usr/local/pf/
cp -r README.network-devices %{buildroot}/usr/local/pf/
cp -r UPGRADE %{buildroot}/usr/local/pf/

#start create symlinks
curdir=`pwd`

#pf-schema.sql symlink
cd %{buildroot}/usr/local/pf/db
ln -s pf-schema-2.0.0.sql ./pf-schema.sql

cd %{buildroot}/usr/local/pf/conf/templates
if (/usr/sbin/httpd -v | egrep 'Apache/2\.[2-9]\.' > /dev/null)
then
  ln -s httpd.conf.apache22 ./httpd.conf
else
  ln -s httpd.conf.pre_apache22 ./httpd.conf
fi

cd $curdir
#end create symlinks

%pre

if ! /usr/bin/id pf &>/dev/null; then
        /usr/sbin/useradd -r -d "/usr/local/pf" -s /bin/sh -c "PacketFence" -M pf || \
                echo Unexpected error adding user "pf" && exit
fi

#if [ ! `tty | cut -c0-8` = "/dev/tty" ];
#then
#  echo You must be on a directly connected console to install this package!
#  exit
#fi

if [ ! `id -u` = "0" ];
then
  echo You must install this package as root!
  exit
fi

#if [ ! `cat /proc/modules | grep ^ip_tables|cut -f1 -d" "` = "ip_tables" ];
#then
#  echo Required module "ip_tables" does not appear to be loaded - now loading
#  /sbin/modprobe ip_tables
#fi

%pre remote-snort-sensor

if ! /usr/bin/id pf &>/dev/null; then
        /usr/sbin/useradd -r -d "/usr/local/pf" -s /bin/sh -c "PacketFence" -M pf || \
                echo Unexpected error adding user "pf" && exit
fi

%post
echo "Adding PacketFence startup script"
/sbin/chkconfig --add packetfence
for service in snortd httpd snmptrapd
do
  if /sbin/chkconfig --list | grep $service > /dev/null 2>&1; then
    echo "Disabling $service startup script"
    /sbin/chkconfig --del $service > /dev/null 2>&1
  fi
done

#touch /usr/local/pf/conf/dhcpd/dhcpd.leases && chown pf:pf /usr/local/pf/conf/dhcpd/dhcpd.leases

if [ -e /etc/logrotate.d/snort ]; then
  echo Removing /etc/logrotate.d/snort - it kills snort every night
  rm -f /etc/logrotate.d/snort
fi

if [ -d /usr/local/pf/html/user/content/docs ]; then
  echo Removing legacy docs directory
  rm -rf /usr/local/pf/html/user/content/docs
fi

echo Installation complete
#TODO: consider renaming installer.pl to setup.pl?
echo "  * Please cd /usr/local/pf && ./installer.pl to finish installation and configure PF"

%post remote-snort-sensor
echo "Adding PacketFence remote Snort Sensor startup script"
/sbin/chkconfig --add pfdetectd

%preun
if [ $1 -eq 0 ] ; then
        /sbin/service packetfence stop &>/dev/null || :
        /sbin/chkconfig --del packetfence
fi
#rm -f /usr/local/pf/conf/dhcpd/dhcpd.leases

%preun remote-snort-sensor
if [ $1 -eq 0 ] ; then
        /sbin/service pfdetectd stop &>/dev/null || :
        /sbin/chkconfig --del pfdetectd
fi

%postun
if [ $1 -eq 0 ]; then
        /usr/sbin/userdel pf || %logmsg "User \"pf\" could not be deleted."
#       /usr/sbin/groupdel pf || %logmsg "Group \"pf\" could not be deleted."
#else
#       /sbin/service pf condrestart &>/dev/null || :
fi

%postun remote-snort-sensor
if [ $1 -eq 0 ]; then
        /usr/sbin/userdel pf || %logmsg "User \"pf\" could not be deleted."
fi

%files
%defattr(-, pf, pf)
%attr(0755, root, root) %{_initrddir}/packetfence
/usr/local/pf/*
%doc /usr/local/pf/docs/*.odt
%doc /usr/local/pf/docs/fdl-1.2.txt
%doc /usr/local/pf/docs/MIB/Inverse-PacketFence-Notification.mib

# Remote snort sensor file list
%files remote-snort-sensor
%defattr(-, pf, pf)
%attr(0755, root, root) %{_initrddir}/pfdetectd
%dir                    /usr/local/pf
%dir                    /usr/local/pf/conf
%config(noreplace)      /usr/local/pf/conf/pfdetect_remote.conf
%dir                    /usr/local/pf/sbin
%attr(0755, pf, pf)     /usr/local/pf/sbin/pfdetect_remote
%dir                    /usr/local/pf/var

%clean
rm -rf $RPM_BUILD_ROOT
