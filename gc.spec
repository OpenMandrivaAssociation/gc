%define major 1
%define cordmajor 1
%define gccppmajor 1
%define libname %mklibname %{name} %{major}
%define libcord %mklibname cord %{cordmajor}
%define libgccpp %mklibname gccpp %{gccppmajor}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -d -s
%ifarch %{armx} %{riscv}
%define _disable_lto 1
%endif

Summary:	Conservative garbage collector for C
Name:		gc
Version:	8.0.4
Release:	7
License:	BSD
Group:		System/Libraries
Url:		http://www.hpl.hp.com/personal/Hans_Boehm/%{name}/
Source0:	https://github.com/ivmai/bdwgc/releases/download/v%{version}/%{name}-%{version}.tar.gz
%ifarch %{riscv}
Patch0:		0000-Fix-undefined-reference-to-__data_start-linker-error.patch
%endif

%description
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n %{libname}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Boehm's GC is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

%package -n %{libcord}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Conflicts:	%{_lib}gc1 < 7.3-0.alpha2.2

%description -n %{libcord}
This package contains a shared library for %{name}.

%package -n %{libgccpp}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Conflicts:	%{_lib}gc1 < 7.3-0.alpha2.2

%description -n %{libgccpp}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files and documentation for Bohem's GC
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcord} = %{version}-%{release}
Requires:	%{libgccpp} = %{version}-%{release}
%rename %{static}

%description -n %{devname}
Header files and documentation needed to develop programs that use Bohem's GC.

%prep
%autosetup -p1
%config_update

%build
# (tpg) use with-libatomic-ops=yes in case of C compiler does not understand C11 intrinsics
export CPPFLAGS="$CPPFLAGS -DUSE_GET_STACKBASE_FOR_MAIN"
%configure \
    --disable-dependency-tracking \
    --enable-cplusplus \
    --disable-static \
    --enable-large-config \
    --with-libatomic-ops=none \
    --disable-parallel-mark \
    --enable-threads=posix

%make_build

%check
make check

%install
%make_install

rm -rf %{buildroot}%{_datadir}

install -m644 doc/gc.man -D %{buildroot}%{_mandir}/man3/gc.3

%files -n %{libname}
%{_libdir}/libgc.so.%{major}*

%files -n %{libcord}
%{_libdir}/libcord.so.%{cordmajor}*

%files -n %{libgccpp}
%{_libdir}/libgccpp.so.%{gccppmajor}*

%files -n %{devname}
%doc README.QUICK doc/*
%{_libdir}/*.so
%dir %{_includedir}/gc
%{_includedir}/%{name}/*
%{_includedir}/*h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man?/*
