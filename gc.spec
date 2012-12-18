%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s

%define prever	alpha2
Summary:	Conservative garbage collector for C
Name:		gc
Version:	7.3
Release:	%mkrel 0.%{prever}.1
License:	BSD
Group:		System/Libraries
URL:		http://www.hpl.hp.com/personal/Hans_Boehm/%{name}/
Source0:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}%{prever}.tar.gz
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
