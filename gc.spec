%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	libcord %mklibname cord %{major}
%define	libgccpp %mklibname gccpp %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s

Summary:	Conservative garbage collector for C
Name:		gc
Version:	7.4.0
Release:	5
License:	BSD
Group:		System/Libraries
Url:		http://www.hpl.hp.com/personal/Hans_Boehm/%{name}/
Source0:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(atomic_ops)

%description
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n	%{libname}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n	%{libcord}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Conflicts:	%{_lib}gc1 < 7.3-0.alpha2.2

%description -n	%{libcord}
This package contains a shared library for %{name}.

%package -n	%{libgccpp}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Conflicts:	%{_lib}gc1 < 7.3-0.alpha2.2

%description -n	%{libgccpp}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development files and documentation for Bohem's GC
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcord} = %{version}-%{release}
Requires:	%{libgccpp} = %{version}-%{release}

%description -n %{devname}
Header files and documentation needed to develop programs that use Bohem's GC

%package -n	%{static}
Summary:	Static libraries for Bohem's GC
Group:		Development/C
%define		build_ada		0
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n	%{static}
Static libraries needed to develop programs that use Bohem's GC

%prep
%setup -qn %{name}-%{version}
%apply_patches
# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
libtoolize --force
autoreconf -i

%build
%configure2_5x \
	--disable-dependency-tracking \
	--enable-cplusplus \
	--enable-static \
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
%{_libdir}/libgc.so.%{major}*

%files -n %{libcord}
%{_libdir}/libcord.so.%{major}*

%files -n %{libgccpp}
%{_libdir}/libgccpp.so.%{major}*

%files -n %{devname}
%doc README.QUICK doc/*.html
%{_libdir}/*.so
%dir %{_includedir}/gc
%{_includedir}/%{name}/*
%{_includedir}/*h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man?/*

%files -n %{static}
%{_libdir}/*.a

