# TODO:
# - find/wait for OMXIL implementation with OMX_VIDEO_CodingVP8 (requires OpenMAX-IL 1.2 or extension?)
#   OMX_VIDEO_CodingTheora (not available in raw OpenMAX-IL 1.1.2 or 1.2)
# - tizonia as an alternative for bellagio?
%define		gst_ver		1.16.2
Summary:	GStreamer plug-in that allows communication with OpenMAX IL components
Summary(pl.UTF-8):	Wtyczka GStreamera pozwalająca na komunikację z komponentami OpenMAX IL
Name:		gstreamer-openmax
Version:	1.16.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-omx/gst-omx-%{version}.tar.xz
# Source0-md5:	6362786d2b6cce34de08c86b7847f782
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-gl-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk-doc >= 1.3
# currently internal headers used (last bellagio release misses some defines)
#BuildRequires:	libomxil-bellagio-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# EGL-devel, OpenGL-GLESv2-devel, xorg-lib-libX11-devel  for examples only
Requires:	glib2 >= 1:2.40.0
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

%prep
%setup -q -n gst-omx-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
# NOTE: force internal OMX IL headers for now, bellagio doesn't provide OMX_VERSION_* (OMX IL 1.2 required?)
%configure \
	ac_cv_header_OMX_Core_h=no \
	--disable-silent-rules \
	--disable-static \
	--with-omx-target=bellagio
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstomx.so
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/gstomx.conf
