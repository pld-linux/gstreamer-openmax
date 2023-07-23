# TODO:
# - find/wait for OMXIL implementation with OMX_VIDEO_CodingVP8 (requires OpenMAX-IL 1.2 or extension?)
#   OMX_VIDEO_CodingTheora (not available in raw OpenMAX-IL 1.1.2 or 1.2)
# - tizonia >= 0.19.0 as an alternative for bellagio?
#
# Conditional build:
%bcond_without	apidocs		# API documentation

%define		gst_ver		1.22.0
Summary:	GStreamer plug-in that allows communication with OpenMAX IL components
Summary(pl.UTF-8):	Wtyczka GStreamera pozwalająca na komunikację z komponentami OpenMAX IL
Name:		gstreamer-openmax
Version:	1.22.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-omx/gst-omx-%{version}.tar.xz
# Source0-md5:	343d1dc08cce08c47d1e0ea7df18a419
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	glib2-devel >= 1:2.62.0
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-gl-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel
%{?with_apidocs:BuildRequires:	hotdoc}
# currently internal headers used (last bellagio release misses some defines)
#BuildRequires:	libomxil-bellagio-devel
BuildRequires:	meson >= 0.62
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# EGL-devel, OpenGL-GLESv2-devel, xorg-lib-libX11-devel  for examples only
Requires:	glib2 >= 1:2.62.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-gl-libs >= %{gst_ver}
Requires:	libomxil-bellagio
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GstOpenMAX is a GStreamer plug-in that allows communication with
OpenMAX IL components.

OpenMAX IL is an industry standard that provides an abstraction layer
for computer graphics, video, and sound routines.

%description -l pl.UTF-8
GstOpenMAX to wtyczka GStreamera pozwalająca na komunikację z
komponentami OpenMAX IL.

OpenMAX IL to standard przemysłowy zapewniający warstwę abstrakcji dla
funkcji grafiki komputerowej, obrazu i dźwięku komp.

%package apidocs
Summary:	GStreamer OpenMAX API documentation
Summary(pl.UTF-8):	Dokumentacja API wtyczki GStreamera OpenMAX
Group:		Documentation
BuildArch:	noarch

%description apidocs
GStreamer OpenMAX API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API wtyczki GStreamera OpenMAX.

%prep
%setup -q -n gst-omx-%{version}

%build
%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddoc=false} \
	-Dtarget=bellagio

%ninja_build -C build

%if %{with apidocs}
cd build/docs
LC_ALL=C.UTF-8 hotdoc run --conf-file omx-doc.json
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
cp -pr build/docs/omx-doc $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstomx.so
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/gstomx.conf

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-%{gstmver}
%endif
