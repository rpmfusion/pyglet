%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pyglet
Version:        1.1.2
Release:        6%{?dist}
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
Requires:       gdk-pixbuf, gtk2, openal 
Requires:       avbin libGL libGLU

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

# Fixes for various permission and EOL encoding problems:
# Everything is reported to upstream:
# http://code.google.com/p/pyglet/issues/detail?id=368
chmod +x tools/*.py
chmod +x examples/*.py
chmod +x examples/soundspace/soundspace.py
sed 's|#!/usr/bin/env python|#|' examples/soundspace/reader.py > reader.py.tmp
touch -r examples/soundspace/reader.py reader.py.tmp
mv -f reader.py.tmp examples/soundspace/reader.py
chmod 644 CHANGELOG NOTICE
sed 's/\r//' NOTICE > NOTICE.tmp
touch -r NOTICE NOTICE.tmp
mv -f NOTICE.tmp NOTICE
chmod -x doc/html/programming_guide/*.py

# Remove the preshipped font (it will use the saved_by_zero.ttf font if 
# larabie-fonts-uncommon is installed)
rm examples/astraea/res/saved_by_zero.ttf
sed "s@\(resource.add_font('saved_by_zero.ttf')\)@try: \1\nexcept: pass@" examples/astraea/astraea.py > astrea.py.tmp
touch -r examples/astraea/astraea.py astrea.py.tmp
mv -f astrea.py.tmp examples/astraea/astraea.py
chmod +x examples/astraea/astraea.py

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
* Tue Feb 03 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-6
- Fix lib-loading-order patch

* Fri Jan 16 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-5
- Add Requires: avbin libGL libGLU

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.1.2-4
- Patch to load the correct (GL*) libraries
- Drop mesa-libGL, mesa-libGLU dependencies

* Mon Dec 01 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> 1.1.2-3
- Updated description.
- Some minor improvements in the SPEC file.

* Sun Nov 23 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> 1.1.2-2
- Removed the extra font dependency (reverting to the default system font).
- Added Requires.

* Sun Nov 23 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> 1.1.2-1
- Initial build.
