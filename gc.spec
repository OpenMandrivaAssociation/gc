%define major 1
%define cordmajor 1
%define gccppmajor 1
%define gctbamajor 1
%define libname %mklibname %{name} %{major}
%define libcord %mklibname cord %{cordmajor}
%define libgccpp %mklibname gccpp %{gccppmajor}
%define libgctba %mklibname gctba %{gctbamajor}
%define devname %mklibname %{name} -d

Summary:	Conservative garbage collector for C
Name:		gc
Version:	8.2.0
Release:	1
License:	BSD
Group:		System/Libraries
Url:		https://www.hboehm.info/%{name}/
Source0:	https://github.com/ivmai/bdwgc/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake

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

%package -n %{libgctba}
Summary:	Conservative garbage collector for C
Group:		System/Libraries
Conflicts:	%{_lib}gc1 < 7.3-0.alpha2.2

%description -n %{libgctba}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files and documentation for Bohem's GC
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcord} = %{version}-%{release}
Requires:	%{libgccpp} = %{version}-%{release}
Requires:	%{libgctba} = %{version}-%{release}

%description -n %{devname}
Header files and documentation needed to develop programs that use Bohem's GC.

%prep
%setup -q

%build
# (tpg) Use -Dwith_libatomic_ops=ON in case the C compiler does not understand C11 intrinsics.
%cmake \
    -Denable_cplusplus=ON      \
    -Denable_large_config=ON   \
    -Denable_parallel_mark=OFF \

%make_build

%check
make test -C build

%install
%make_install -C build

%files -n %{libname}
%{_libdir}/libgc.so.%{major}*

%files -n %{libcord}
%{_libdir}/libcord.so.%{cordmajor}*

%files -n %{libgccpp}
%{_libdir}/libgccpp.so.%{gccppmajor}*

%files -n %{libgctba}
%{_libdir}/libgctba.so.%{gctbamajor}*

%files -n %{devname}
%doc %{_docdir}/%{name}/*
%{_libdir}/*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_includedir}/%{name}*.h
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*
