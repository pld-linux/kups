%define qtdir	/usr/X11/
Summary:	A KDE-based printer administration tool for CUPS
Summary(pl.UTF-8):   Oparte na KDE narzędzie administracyjne do cupsa
Name:		kups
Version:	1.0
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/cups/%{name}-%{version}.tar.gz
# Source0-md5:	6988ed0e755335e819587bb73537c3da
URL:		http://sourceforge.net/projects/cups/
BuildRequires:	docbook-dtd-sgml
BuildRequires:	docbook-style-dsssl
BuildRequires:	openjade
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sgml-common
BuildRequires:	sgml-tools
BuildRequires:	qtcups-devel >= 2.0
Requires:	cups >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
who are allowed to do printer administration, to restrict the
broadcasting of printer information to selected machines or subnets,
and so on.

%description -l pl.UTF-8
Oparty na KDE interfejs do administrowania drukarkami działającymi
poprzez CUPS (Common Unix Printing System). Podaje listę dostępnych
lokalnie i zdalnie drukarek, ich ustawienia oraz zadania, pozwalając
skonfigurować drukarki (w tym ustawienie głowicy i kalibrację kolorów
w wielu modelach), wydrukować stronę testową, usuwać zadania, dodawać
i usuwać drukarki. Do instalowania nowych drukarek służy wizard, który
pyta o potrzebne dane i próbuje automatycznie wykryć drukarki.

Ponadto dołączone jest narzędzie kupsdconf, będące interfejsem KDE do
ustawiania opcji demona CUPS, zdefiniowanych w pliku
/etc/cups/cupsd.conf. Pozwala łatwo wybrać użytkowników i grupy mające
prawo do administrowania drukarkami, ograniczyć do wybranych maszyn
lub podsieci rozgłaszanie informacji o drukarkach itp.

%package devel
Summary:	Development files for usage of the kupsdconf library
Summary(pl.UTF-8):   Pliki dla programistów używających biblioteki kupsdconf
Group:		Development/Libraries

%description devel
This package contains the files needed to compile programs using the
kupsdconf library. This library provides a KDE-based dialog to
configure the options of the CUPS daemon stored in
/etc/cups/cupsd.conf.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do kompilacji programów używających
biblioteki kupsdconf. Biblioteka ta udostępnia okienko dialogowe KDE z
opcjami do konfiguracji demona CUPS z pliku /etc/cups/cupsd.conf.

%prep
%setup -q
touch `find . -type f`
# Clean up "driver/postscript.ppd" and add 1200 dpi and 2400 dpi
# Remove also the CUPS filter line, it is not needed for a PS printer and
# even prevents it from printing images.
%{__perl} -pi -e 's!\*Manufacturer:.*"Postscript"!\*Manufacturer:  "POSTSCRIPT"!;' driver/postscript.ppd
%{__perl} -pi -e 's!Generic postscript printer!Generic PostScript printer!;' driver/postscript.ppd

%build
# These compiler options are NEEDED otherwise KUPS does not compile
CXXFLAGS="%{rpmcflags} %{!?debug:-DNO_DEBUG} -fno-exceptions -fno-check-new"
%configure2_13 \
	--with-install-root=$RPM_BUILD_ROOT \
	--enable-qt2 \
	--with-qt-dir=%{qtdir} \
	--disable-qt-debug \
	--disable-rpath \
	--with-qt-libraries=%{qtdir}

%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libkupsdconf.so.*
%{_datadir}/apps/kups/*
%doc AUTHORS ChangeLog NEWS README TODO
%doc %{_kdedocdir}/en/kups
%{_pixmapsdir}/locolor/*/apps/*
%{_pixmapsdir}/hicolor/*/actions/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*.h
