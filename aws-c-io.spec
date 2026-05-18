#
# Conditional build:
%bcond_without	s2n		# s2n-tls support (otherwise ByoCrypto mode, with external context management)
%bcond_with	tests		# unit tests (require networking)
#
Summary:	AWS C IO library
Summary(pl.UTF-8):	Biblioteka AWS C IO
Name:		aws-c-io
Version:	0.26.3
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-c-io/releases
Source0:	https://github.com/awslabs/aws-c-io/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3dfbc1a594e5e92f65506bff23ab83cc
URL:		https://github.com/awslabs/aws-c-io
BuildRequires:	aws-c-cal-devel
BuildRequires:	aws-c-common-devel
BuildRequires:	cmake >= 3.9
BuildRequires:	gcc >= 5:3.2
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_s2n:BuildRequires:	s2n-tls-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# s2n_errno non-function symbol
%define		skip_post_check_so	libaws-c-io.so.*

%description
This is a module for the AWS SDK for C. It handles all IO and TLS work
for application protocols.

aws-c-io is an event driven framework for implementing application
protocols. It is built on top of cross-platform abstractions that
allow you as a developer to think only about the state machine and API
for your protocols. A typical use-case would be to write something
like HTTP on top of asynchronous-io with TLS already baked in. All of
the platform and security concerns are already handled for you.

It is designed to be light-weight, fast, portable, and flexible for
multiple domain use-cases such as: embedded, server, client, and
mobile.

%description -l pl.UTF-8
Ten moduł AWS SDK dla C obsługuje zadania IO (wejścia/wyjścia) oraz
TLS dla protokołów aplikacyjnych.

aws-c-io to sterowany zdarzeniami szkielet do implementowania
protokołów aplikacyjnych. Jest zbudowany w oparciu o wieloplatformowe
abstrakcje, pozwalające programistom myśleć tylko o automacie stanowym
oraz API własnych protokołów. Typowe przypadki użycia to pisanie np.
HTTP w oparciu o asynchroniczne we/wy z podpiętym TLS. Wszystkie
kwestie platformy i bezpieczeństwa są obsługiwane za programistę.

Moduł jest zaprojektowany jako lekki, szybki, przenośny i elastyczny
dla wielu różnych przypadków użycia, takich jak oprogramowanie
wbudowane, serwerowe, klienckie czy przenośne.

%package devel
Summary:	Header files for AWS C IO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AWS C IO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	aws-c-cal-devel
Requires:	aws-c-common-devel
%{?with_s2n:Requires:	s2n-tls-devel}

%description devel
Header files for AWS C IO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AWS C IO.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_s2n:-DBYO_CRYPTO=ON}

# -DUSE_VSOCK=ON ? (requires struct sockaddr_vm)

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%{_libdir}/libaws-c-io.so.1.0.0

%files devel
%defattr(644,root,root,755)
%doc docs/{graphs,images,*.md}
%{_libdir}/libaws-c-io.so
%{_includedir}/aws/io
%{_includedir}/aws/testing/async_stream_tester.h
%{_includedir}/aws/testing/io_testing_channel.h
%{_includedir}/aws/testing/stream_tester.h
%{_libdir}/cmake/aws-c-io
