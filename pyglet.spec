%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pyglet
Version:        1.1.4
Release:        1%{?dist}
Summary:        A cross-platform windowing and multimedia library for Python
Group:          Development/Libraries
License:        BSD
URL:            http://www.pyglet.org/
Source0:        http://pyglet.googlecode.com/files/%{name}-%{version}.tar.gz
#This patch makes sure that the library loader uses the find_library() facility of 
#ctypes.utils so that the library path is taken from the linker. Normally, pyglet would 
#try to load "libx.so" (which is of -devel type) when the library "x" is called and 
#this would make pyglet fail in certain cases. For instance, when pyglet requests the 
#GL library, it may try to load libGL.so from mesa-libGL-devel, which is not desired.
Patch0:         pyglet-lib-loading-order.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel

Requires:       avbin
Requires:       gdk-pixbuf
Requires:       gtk2
Requires:       libGL
Requires:       libGLU
Requires:       openal 

%description
Pyglet provides an object-oriented programming interface for developing
games and other visually-rich applications for Windows, Mac OS X and
Linux. Pyglet loads images, sound, music and video in almost any format 
and can optionally use AVbin to play back audio formats such as MP3, 
OGG/Vorbis and WMA, and video formats such as DivX, MPEG-2, H.264, WMV
and Xvid.

%package examples
Summary: Examples for pyglet module
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description examples
Pyglet provides an object-oriented programming interface for developing
games and other visually-rich applications for Windows, Mac OS X and
Linux. Pyglet loads images, sound, music and video in almost any format 
and can optionally use AVbin to play back audio formats such as MP3, 
OGG/Vorbis and WMA, and video formats such as DivX, MPEG-2, H.264, WMV
and Xvid. This package provides example scripts for pyglet usage.

%package doc
Summary: API documentation of pyglet
Group: Documentation

%description doc
Pyglet provides an object-oriented programming interface for developing
games and other visually-rich applications for Windows, Mac OS X and
Linux. Pyglet loads images, sound, music and video in almost any format 
and can optionally use AVbin to play back audio formats such as MP3, 
OGG/Vorbis and WMA, and video formats such as DivX, MPEG-2, H.264, WMV
and Xvid. This package provides API documentation of pyglet.

%prep

%setup -q

%patch0 -p2 -b .loading.order

for i in doc/html/*/*.py; do
    sed -i '\|/usr/bin/env python|d' $i
    chmod -x $i
done

%build
echo "Nothing to build."


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
install -dm 755  $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -a examples/* $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -a tools/*    $RPM_BUILD_ROOT/%{_datadir}/%{name}

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE NOTICE README 
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{name}

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/*

%files examples
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/%{name}

%changelog
* Thu Feb 04 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.4-1
- update to 1.1.4

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.3-1
- update to 1.1.3

* Tue Feb 03 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-6
- Fix lib-loading-order patch

* Fri Jan 16 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-5
- Add Requires: avbin libGL libGLU

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-4
- Patch to load the correct (GL*) libraries
- Drop mesa-libGL, mesa-libGLU dependencies

* Mon Dec 01 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-3
- Updated description.
- Some minor improvements in the SPEC file.

* Sun Nov 23 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-2
- Removed the extra font dependency (reverting to the default system font).
- Added Requires.

* Sun Nov 23 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-1
- Initial build.
