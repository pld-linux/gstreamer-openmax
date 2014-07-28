# TODO: find/wait for OMXIL implementation with OMX_VIDEO_CodingVP8, OMX_VIDEO_CodingTheora
# (not available in raw OpenMAX-IL 1.1.2)
%include	/usr/lib/rpm/macros.gstreamer
Summary:	GStreamer plug-in that allows communication with OpenMAX IL components
Summary(pl.UTF-8):	Wtyczka GStreamera pozwalająca na komunikację z komponentami OpenMAX IL
Name:		gstreamer-openmax
Version:	1.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gst-omx/gst-omx-%{version}.tar.xz
# Source0-md5:	d24e8c0153c35dfefee3e26b1c2c35f8
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	gstreamer-devel >= 1.2.2
# gstreamer-gl
BuildRequires:	gstreamer-plugins-bad-devel >= 1.4.0
BuildRequires:	gtk-doc >= 1.3
#BuildRequires:	libomxil-bellagio-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.32
Requires:	gstreamer >= 1.2.2
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
# NOTE: force internal OMX IL headers for now, bellagio doesn't provide OMX_VERSION_*
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
