%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s

Summary:	Conservative garbage collector for C
Name:		gc
%define	ver	7.2
Version:	%{ver}c
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://www.hpl.hp.com/personal/Hans_Boehm/%{name}/
Source0:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz
BuildRequires:	libatomic_ops-devel

%description
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n	%{libname}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Obsoletes:	%{name} < 7.1
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n	%{devname}
Summary:	Development files and documentation for Bohem's GC
Group:		Development/C
License: 	BSD
Obsoletes:	%{mklibname gc 1 -d} < 7.1
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Header files and documentation needed to develop programs that use Bohem's GC

%package -n	%{static}
Summary:	Static libraries for Bohem's GC
Group:		Development/C
License: 	BSD
Obsoletes:	%{mklibname gc 1 -d -s} < 7.1
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n	%{static}
Static libraries neded to develop programs that use Bohem's GC

%prep
%setup -q -n %{name}-%{ver}
# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
libtoolize --force
autoreconf -i

%build
%configure2_5x \
    --disable-dependency-tracking \
    --enable-cplusplus \
%ifarch %{ix86}
    --enable-parallel-mark \
%endif
    --enable-threads=pthreads
        
%make

%check
make check

%install
%makeinstall_std

rm -rf %{buildroot}%{_datadir}

install -m644 doc/gc.man -D %{buildroot}%{_mandir}/man3/gc.3

%files -n %{libname}
%doc README.QUICK
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc doc/*.html
%{_libdir}/*.so
%dir %{_includedir}/gc
%{_includedir}/%{name}/*
%{_includedir}/*h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man?/*

%files -n %{static}
%{_libdir}/*.a


%changelog
* Thu Jun 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.2c-1
+ Revision: 807442
- make static package require devel package, not library package
- make provides for devel & static package lib neutral
- move autoreconf & libtoolize to %%prep
- don't manually add -fPIC to %%optflags on x86_64, it's now part of default
  %optflags for x86_64
- cleanups
- new version

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 7.1-8
+ Revision: 664810
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 7.1-7mdv2011.0
+ Revision: 605440
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 7.1-6mdv2010.1
+ Revision: 522708
- rebuilt for 2010.1

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 7.1-5mdv2010.0
+ Revision: 448322
- fix mips support, "nice" regression from 6.8 (from Arnaud Patard)

* Sat Jul 18 2009 Anssi Hannula <anssi@mandriva.org> 7.1-4mdv2010.0
+ Revision: 396975
- fix build failure due to duplicate headers in the same install command
  (duplicate-headers-install.patch, from Mika Laitio)

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 7.1-3mdv2009.1
+ Revision: 310348
- better comment
- build with -fPIC on x86-64 (tkhtml3 build fails without)

* Fri Sep 26 2008 Oden Eriksson <oeriksson@mandriva.com> 7.1-2mdv2009.0
+ Revision: 288616
- rebuild

* Fri Jul 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 7.1-1mdv2009.0
+ Revision: 231792
- rename
- update to new version 7.1
- new library policy
- spec file clean

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 0:6.8-2mdv2008.1
+ Revision: 150564
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu May 17 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0:6.8-1mdv2008.0
+ Revision: 27627
- Updated to 6.8.
- Minor identation fixes.

