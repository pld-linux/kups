%define qtdir	/usr/X11/
Summary:	A KDE-based printer administration tool for CUPS
Summary(pl):	Interfejs do cupsa
Name:		kups
Version:	1.0
Release:	1
License:	GPL
Group:		Publishing
Source0:	http://prdownloads.sourceforge.net/cups/%{name}-%{version}.tar.gz
URL:		http://sourceforge.net/projects/cups
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	cups >= 1.1, qt >= 2.1, kdelibs, qtcups >= 2.0
BuildRequires:	qtcups-devel >= 2.0
BuildRequires:  docbook-dtd-sgml
BuildRequires:  sgml-tools
BuildRequires:	docbook-style-dsssl
BuildRequires:	sgml-common
BuildRequires:	openjade


%description
A KDE-based frontend for administration of printers running under CUPS
(Common Unix Printing System). One gets a list of all available local
and remote printers, their settings, and their jobs and one can
configure the printers (including head adjustment and colour
calibration for many models), print test pages, kill jobs, install new
printers, and remove undesired ones. The installing of new printers is
done by a wizard which asks for all necessary data and even does
autodetection of the printers.

In addition, there is the "kupsdconf" utility, a KDE based frontend
for setting up all options of the CUPS daemon, defined in the
/etc/cups/cupsd.conf file. So it is easy to choose the users/groups
who are allowed to do printer administration, to restrict
thebroadcasting of printer information to selected machines or
subnets, and so on.

%description devel
This package contains the files needed to compile programs using the
kupsdconf library. This library provides a KDE-based dialog to
configure the options of the CUPS daemon stored in
/etc/cups/cupsd.conf.

%package devel
Summary:        Development files for usage of the kupsdconf library
Group:          Development/C

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%setup -q
touch `find . -type f`
# Clean up "driver/postscript.ppd" and add 1200 dpi and 2400 dpi
# Remove also the CUPS filter line, it is not needed for a PS printer and
# even prevents it from printing images.
perl -pi -e 's!\*Manufacturer:.*"Postscript"!\*Manufacturer:  "POSTSCRIPT"!;' driver/postscript.ppd
perl -pi -e 's!Generic postscript printer!Generic PostScript printer!;' driver/postscript.ppd

%build
# These compiler options are NEEDED otherwise KUPS does not compile
#export MOC=%{_bindir}/moc
export CXXFLAGS="${CXXFLAGS:-%optflags} -DNO_DEBUG -fno-exceptions -fno-check-new"
%configure2_13 --prefix=%{_prefix} --with-install-root=$RPM_BUILD_ROOT \
	--enable-qt2 \
	--with-qt-dir=%{qtdir} \
	--disable-qt-debug \
	--disable-rpath \
	--with-qt-libraries=%{qtdir}
%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# Fix broken link
ln -sf %{_datadir}/doc/HTML/en/common $RPM_BUILD_ROOT%{_datadir}/doc/HTML/en/kups/common

# Link to CUPS test page to avoid having two equal files
rm -f $RPM_BUILD_ROOT%{_datadir}/apps/kups/testprint.ps
ln -s %{_datadir}/cups/data/testprint.ps $RPM_BUILD_ROOT%{_datadir}/apps/kups/testprint.ps

##menus created
install -d $RPM_BUILD_ROOT%{_menudir}

cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/kups
?package(kups): needs=X11 \
section=Configuration/Printing \
title="KUPS - CUPS Administration" \
longtitle="KUPS - Complete administration suite for CUPS" \
command="%{_bindir}/kups" \
icon="%{_iconsdir}/locolor/16x16/apps/kups.png"
?package(kups): needs=X11 \
section=Configuration/Printing \
title="Kupsdonf - CUPS Daemon Configurator" \
longtitle="Graphical environment to configure the CUPS daemon" \
command="%{_bindir}/kdesu %{_bindir}/kupsdconf" \
icon="%{_iconsdir}/locolor/16x16/apps/kups.png"
EOF

gzip -9nf  AUTHORS ChangeLog NEWS README TODO

%post
/sbin/ldconfig
%{update_menus}

%postun
/sbin/ldconfig
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_menudir}/*
%{_datadir}/apps/kups/*
%{_datadir}/cups/model/*
%doc *.gz 
%doc %{_docdir}/HTML/en/kups
%{_iconsdir}/locolor/*/apps/*
%{_iconsdir}/hicolor/*/actions/*
%{_libdir}/libkupsdconf.so.*


%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/*.so
