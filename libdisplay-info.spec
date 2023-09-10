#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	EDID and DisplayID library
Summary(pl.UTF-8):	Biblioteka identyfikatorów EDID i DisplayID
Name:		libdisplay-info
Version:	0.1.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/emersion/libdisplay-info/-/releases
Source0:	https://gitlab.freedesktop.org/emersion/libdisplay-info/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
# Source0-md5:	56e8d2213d2aefd7defaaddfd9cb80e1
URL:		https://gitlab.freedesktop.org/emersion/libdisplay-info
BuildRequires:	hwdata >= 0.362
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	hwdata >= 0.362
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EDID and DisplayID library.

Goals:
- Provide a set of high-level, easy-to-use, opinionated functions as
  well as low-level functions to access detailed information.
- Simplicity and correctness over performance and resource usage.
- Well-tested and fuzzed.

%description -l pl.UTF-8
Biblioteka identyfikatorów EDID i DisplayID.

Cele:
- dostarczenie zestawu wysokopoziomowych, łatwych w użyciu funkcji
  oraz niskopoziomowych funkcji pozwalających na dostęp do
  szczegółowych informacji
- prostota i poprawność ważniejsza niż wydajność i użycie zasobów
- dobre przetestowanie i odporność

%package devel
Summary:	Header files for display-info library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki display-info
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for display-info library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki display-info.

%package static
Summary:	Static display-info library
Summary(pl.UTF-8):	Statyczna biblioteka display-info
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static display-info library.

%description static -l pl.UTF-8
Statyczna biblioteka display-info.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/di-edid-decode
%attr(755,root,root) %{_libdir}/libdisplay-info.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdisplay-info.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdisplay-info.so
%{_includedir}/libdisplay-info
%{_pkgconfigdir}/libdisplay-info.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdisplay-info.a
%endif
