%define	major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n %{libname}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Obsoletes:	%{name} < 7.1
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n %{develname}
Summary:	Development files and documentation for Bohem's GC
Group:		Development/C
License: 	BSD
Obsoletes:	%{mklibname gc 1 -d} < 7.1
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Header files and documentation needed to develop programs that use Bohem's GC

%package -n %{staticname}
Summary:	Static libraries for Bohem's GC
Group:		Development/C
License: 	BSD
Obsoletes:	%{mklibname gc 1 -d -s} < 7.1
Provides:	lib%{name}-static-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{staticname}
Static libraries neded to develop programs that use Bohem's GC

%prep
%setup -q -n %{name}-%{ver}

%build
# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
libtoolize --force
autoreconf -i

# or else tkhtml3 won't build on x86-64. the clean way to do this is
# to patch it into the Makefile, but then it doesn't get used for
# mach_dep.lo, and I can't figure out why not - AdamW 2008/12
%ifarch x86_64
export CFLAGS="%{optflags} -fPIC"
%endif

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
rm -rf %{buildroot}

%makeinstall_std

rm -rf %{buildroot}%{_datadir}

install -m644 doc/gc.man -D %{buildroot}%{_mandir}/man3/gc.3

#rm -f %{buildroot}%{_docdir}/gc

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%doc README.QUICK
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%doc doc/*.html
%{_libdir}/*.so
%dir %{_includedir}/gc
%{_includedir}/%{name}/*
%{_includedir}/*h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man?/*

%files -n %{staticname}
%defattr(-, root, root)
%{_libdir}/*.a
