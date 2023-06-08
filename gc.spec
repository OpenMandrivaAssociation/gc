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
Version:	8.2.4
Release:	1
License:	BSD
Group:		System/Libraries
Url:		https://www.hboehm.info/%{name}/
Source0:	https://github.com/ivmai/bdwgc/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	cmake

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
Summary:	Development files and documentation for Boehm's GC
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcord} = %{version}-%{release}
Requires:	%{libgccpp} = %{version}-%{release}
Requires:	%{libgctba} = %{version}-%{release}

%description -n %{devname}
Header files and documentation needed to develop programs that use Boehm's GC.

%prep
%autosetup -p1

%build
# (tpg) Use -Dwith_libatomic_ops=ON in case the C compiler does not understand GCC atomic intrinsics.
%cmake \
    -Denable_cplusplus=ON      \
    -Denable_large_config=ON   \

%make_build

%check
make test -C build

%install
%make_install -C build

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

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
%doc %{_mandir}/man?/*
