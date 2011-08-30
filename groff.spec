%{!?with_x:%define with_x 1}

Summary: A document formatting system
Name:	groff
Version: 1.18.1.4
Release: 21%{?dist}
License: GPLv2 and GFDL
Group: Applications/Publishing
URL: http://groff.ffii.org
Source0: ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
Source3: mandocj.tar.gz
Source4: man-pages-ja-GNU_groff-20000115.tar.gz
Source6: hyphen.cs
Source7: nroff
Patch1: groff-1.16-safer.patch
Patch3: groff_1.18.1-15.diff
Patch4: groff-1.18-info.patch
Patch6: groff-1.18-pfbtops_cpp.patch
Patch7: groff-1.18-gzip.patch
Patch9: groff-1.18.1-fixminus.patch
Patch11: groff-1.18.1-8bit.patch
Patch12: groff-1.18.1-korean.patch
Patch13: groff-1.18.1-gzext.patch
#Patch14: groff-xlibs.patch
Patch15: groff-1.18.1-fix15.patch
Patch16: groff-1.18.1-devutf8.patch
#Patch17: groff-1.18.1.3-revision.patch
Patch18: groff-1.18.1.1-do_char.patch
#Patch19: groff-1.18.1.1-grn.patch
#Patch20: groff-1.18.1.1-tempfile.patch
#Patch21: groff-1.18.1.1-gcc41.patch
#Patch22: groff-1.18.1.1-bigendian.patch
Patch23: groff-1.18.1.1-spacefix.patch
Patch24: groff-1.18.1.4-sectmp.patch
Patch25: groff-1.18.1.4-grofferpath.patch
Patch26: groff-1.18.1.4-gcc4.3.0.patch
Patch27: groff-1.18.1.4-big-endian.patch
Patch28: groff-1.18.1.4-segv-get_breakpoints.patch
Patch29: groff-1.18.1.4-abrt-make_node-hypen.patch
 
Requires: mktemp
Requires: /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts: groff-tools = %version
Provides: nroff-i18n = %version
BuildRequires: byacc zlib-devel texinfo

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-gxditview package.

%package perl
Summary: Parts of the groff formatting system that require Perl
Group: Applications/Publishing
Requires: %{name} = %{version}-%{release}

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the
troff-to-ps print filter.

%if %{with_x}
%package gxditview
Summary: An X previewer for groff text processor output
Group: Applications/Publishing
BuildRequires: imake xorg-x11-proto-devel libX11-devel libXaw-devel
BuildRequires: libXt-devel libXpm-devel libXext-devel
Requires: %{name} = %{version}-%{release}

%description gxditview
Gxditview displays the groff text processor's output on an X Window
System display.
%endif

%prep
%setup -q -a 4
%patch1 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1 -b .gzext
#%patch14 -p1
%patch15 -p1 -b .fix9
%patch16 -p1 -b .devutf8
#%patch17 -p1 -b .revision
%patch18 -p1 -b .do_char
#%patch19 -p1 -b .grn
#%patch20 -p1 -b .tempfile
#%patch21 -p1 -b .gcc41
#%patch22 -p1 -b .bigendian
%patch23 -p1 -b .spacefix
%patch24 -p1 -b .sectmp
%patch25 -p1 -b .grofferpath
%patch26 -p1 -b .gcc43
%patch27 -p1 -b .big-endian
%patch28 -p1 -b .segv-get_breakpoints
%patch29 -p1 -b .abrt-make_node-hypen

for i in contrib/mm/{groff_mm,groff_mmse,mmroff}.man \
		src/devices/grolbp/grolbp.man; do
	iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
#PATH=$PATH:%{_prefix}/X11R6/bin
#autoconf
%configure --enable-multibyte
# no html docs
make make_html=
(cd doc && makeinfo groff.texinfo)
%if %{with_x}
cd src/xditview
xmkmf && make %{?_smp_mflags}
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
#PATH=$PATH:%{_prefix}/X11R6/bin
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
# 1) no html docs
# 2) the list could be shorter if configure parameters were not expanded;
#    %%configure should be fixed!
make install make_html= make_install_html= \
			manroot=${RPM_BUILD_ROOT}%{_mandir} \
			bindir=%{buildroot}%{_bindir} \
			mandir=%{buildroot}%{_mandir} \
			prefix=%{buildroot}/usr \
			exec_prefix=%{buildroot}/usr \
			sbindir=%{buildroot}%{_exec_prefix}/sbin \
			sysconfdir=%{buildroot}/etc \
			datadir=%{buildroot}/usr/share \
			infodir=%{buildroot}/%{_prefix}/info \
			sysconfdir=%{buildroot}/etc \
			includedir=%{buildroot}/usr/include \
			libdir=%{buildroot}/%{_libdir} \
			libexecdir=%{buildroot}/usr/libexec \
			localstatedir=%{buildroot}/var \
			sharedstatedir=%{buildroot}/usr/com \
			infodir=%{buildroot}/usr/share/info
			
#install -m 644 doc/groff.info* ${RPM_BUILD_ROOT}/%{_infodir}
%if %{with_x}
cd src/xditview
make install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
%endif

for file in {s,mse,m}.tmac; do
	ln -s $file ${RPM_BUILD_ROOT}%{_datadir}/groff/%{version}/tmac/g$file
done
for file in g{{n,t}roff,tbl,pic,{,n}eqn,refer,{look,indx}bib} {g,z}soelim; do
	ln -s ${file#?} ${RPM_BUILD_ROOT}%{_bindir}/$file
	ln -s {${file#?},${RPM_BUILD_ROOT}%{_mandir}/man1/$file}.1.gz
done

ln -s devnippon ${RPM_BUILD_ROOT}%{_datadir}/groff/%{version}/font/devkorean

cat debian/mandoc.local >> ${RPM_BUILD_ROOT}%{_datadir}/groff/site-tmac/mdoc.local
cat debian/mandoc.local >> ${RPM_BUILD_ROOT}%{_datadir}/groff/site-tmac/man.local

find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l | \
	sed "/afmtodit/d;/mdoc\.samples/d;/mmroff/d;/gxditview/d
		s|${RPM_BUILD_ROOT}||g; s|\.[0-9]|\.*|g" > groff-files

install -pm 644 %SOURCE6 $RPM_BUILD_ROOT%{_datadir}/groff/%version/tmac/hyphen.cs

install -pm 755 %SOURCE7 $RPM_BUILD_ROOT%{_bindir}/nroff

ln -sf doc.tmac $RPM_BUILD_ROOT%{_datadir}/groff/%version/tmac/docj.tmac
# installed, but not packaged in rpm
mkdir -p $RPM_BUILD_ROOT%{_datadir}/groff/%{version}/groffer/
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devps/generate/symbol.sed
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devdvi/generate/CompileFonts
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devps/generate/afmname
chmod 755 $RPM_BUILD_ROOT%{_libdir}/groff/groffer/version.sh
mv $RPM_BUILD_ROOT%{_libdir}/groff/groffer/* $RPM_BUILD_ROOT/%{_datadir}/groff/%{version}/groffer/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/groff $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT/%{_prefix}/lib/X11/app-defaults
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff/groffer
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff/site-tmac
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/groff.gz %{_infodir}/dir;
exit 0

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/groff.gz %{_infodir}/dir
fi
exit 0

%files -f groff-files
%defattr(-,root,root,-)
%doc	BUG-REPORT NEWS PROBLEMS README TODO VERSION
%doc	doc/meintro.me doc/meref.me doc/pic.ms
%{_datadir}/groff
%{_infodir}/groff*

%files perl
%defattr(-,root,root,-)
%{_bindir}/mmroff
%{_bindir}/afmtodit
%{_mandir}/man1/afmtodit.*
%{_mandir}/man1/mmroff*

%if %{with_x}
%files gxditview
%defattr(-,root,root,-)
%{_bindir}/gxditview
%{_datadir}/X11/app-defaults/GXditview
%endif

%changelog
* Tue Jun 29 2010 Jan Vcelak <jvcelak@redhat.com> 1.18.1.4-21
- Fixes SIGSEGV in get_breakpoint, SIGABRT in make_node (#608794).

* Tue Jun 15 2010 Jan Vcelak <jvcelak@redhat.com> 1.18.1.4-20
- fixes grotty segfault on big endian archs when parsing multibyte characters
  bz #601874

* Fri Mar 19 2010 Jan Vcelak <jvcelak@redhat.com> - 1.18.1.4-19
- Fix subpackage dependencies
- grog moved to the main package

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.18.1.4-18.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> - 1.18.1.14-16
- Fixed wrong symlinking of man pages into %%{_bindir} after simplifying

* Mon Sep 29 2008 Stepan Kasal <skasal@redhat.com> - 1.18.1.14-15
- Replace groff-1.18-nohtml.patch by a code in spec file
- fix groff-1.18-gzip.patch to apply cleanly
- simplify the code for symlinking in %%install

* Wed Mar 26 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-14
- 175459 warning goes on stderr

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.18.1.4-13
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-12
- rewrite nroff for using -Tencoding with main support of utf8
- Resolves: rhbz#251064

* Thu Jan  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-11
- fix for gcc4.3.0

* Mon Oct  8 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-10
- path for groffer wasn't set correctly #89210

* Mon Sep 17 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-9
- fix license

* Tue Sep 11 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-8
- another change in spec for review

* Thu Aug 16 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-7
- rebuild
- another encoding are print correct with nroff
- Resolves: rhbz#251064

* Mon Jul  2 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-5
- Resolves: rhbz#245934

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-4
- merge review
- rhbz#225859 review

* Mon Jan 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-2
- changes in spec, remove patches groff-1.18.1.1-bigendian.patch, groff-xlibs.patch
 
* Mon Oct 23 2006 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-1
- new version from upstream - update groffer

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-11.1
- rebuild

* Wed Apr 26 2006 Adam Jackson <ajackson@redhat.com> - 1.18.1.1-11
- Rebuild for updated imake build rules.

* Thu Feb 16 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-10
- use mktemp for temporary files in pic2graph and eqn2graph scripts

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.2
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-9
- remove gxditview from groff package (#179684)
- remove obsolete "--enable-japanese" configure option

* Fri Jan 12 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-8
- fix segfault in grotty on 64-bit big endian machines (#176904)
- fix assertion failure on abort message (#141912)
- attempt to fix a space problem with several european languages (#137728)

* Fri Jan 06 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-7
- require X dependencies only for gxditview (#177118)
- work if bash's noclobber is on (#127492)

* Thu Jan 05 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-6
- add BuildRequires imake and update dependencies for modular X
- spec cleanup
- fix compilation with gcc-4.1.0

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-5
- Convert also mmroff.1 to UTF-8

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-4
- Convert man pages to UTF-8

* Tue Oct 19 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-3
- fixed groffer scripte security problem (#136314)

* Thu Sep 16 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-2
- fixed DoCharacter calls in xditview (#110812)
- fixed fclose called once too often (#132690): thanks to Ulrich Drepper for
  the bug hunting

* Tue Jun 29 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-1
- new version 1.18.1.1 (fixed groffer script)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-35
- fixed build prereq and requires

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-34
- new debian groff patch: groff_1.18.1-15.diff
- new fix for debian patch: groff-1.18.1-fix15.patch
- fixed width in devutf8 font M: groff-1.18.1-devutf8.patch
- removed iconv patch

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-33
- fixed nroff script: convert output to locale charmap

* Wed Feb 25 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-32
- fixed nroff script input (#116596)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Adrian Havill <havill@redhat.com>
- provide I18N version of nroff that accepts --legacy parameter
  (used by man-1.5m2-2)

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- fixed missing BuildRequires (#110574)

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling this without XFree86

* Wed Aug  6 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28.2
- new devutf8 font description
- use -Tutf8 for ru_*.UTF-8 in nroff.sh
- fixes #88618 (ru_RU man pages in cambridge are using UTF-8, now)

* Fri Jun 13 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28
- rebuild (debian-9)

* Tue Jun 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-27
- going back to 1.18.1-4 from debian (the newer versions did not work properly)
- fixed nroff.sh for ru_RU.(!UTF-8)

* Mon May 19 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-26
- fix input and output handler for 1.18.1-9 to be compatible with 1.18.1-4

* Tue Apr 29 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-9 from debian

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-8 from debian: use latin1 instead of C locale

* Sun Mar 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-7 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 1.18.1-21
- groff-xlibs.patch to fix ppc64 builds

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-20
- Make the iconv patch a little less broken (bug #84132).

* Tue Feb 11 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-19
- added new iconv patch

* Tue Feb 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- disable the iconv patch, this will go into a wrapper within the man rpm

* Mon Feb 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-17
- fixed source of gzipped files

* Mon Feb 10 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add Korean support from ynakai@redhat.com, #83933

* Sun Feb 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove automatic conversion for ru_* and cz_*
- add 8bit patch
- update to 1.18.1-4 debian patch
- disable Patch8: groff-1.18.1-multichar.patch for now
- add ugly patch within the iconv patch to partly fix display of russian
  man-pages with "-Tnippon"

* Thu Feb  6 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-11
- Unbreak EUC-JP (bug #83608).

* Mon Feb  3 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-10
- fixed missing minus
- added iconv conversion script

* Fri Jan 31 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-9
- Fix UTF-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- also add hyphen changes to man.local in addition to mdoc.local

* Tue Jan 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- really include mdoc.local changes from debian

* Sat Jan 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix #81401, maybe also #57410

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add more documentation #80729

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- hot fix for devascii8 breakage

* Sun Dec 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-2 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Mon Nov 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- use newest debian patch on top of it

* Mon Nov 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add gzip decompression patch

* Sat Nov 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- apply groff_1.18-7 from debian
- remove some not-packaged files
- rm old printfilters completely

* Fri Oct 04 2002 Elliot Lee <sopwith@redhat.com> 1.18-7
- Patch7 - move pfbtops to CCPROGDIRS (it needs to link to C++ stuff)

* Sat Aug 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for #72924

* Mon Aug 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove README.A4  #65920

* Sun Aug 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- use info files as installed by groff package
- completely disable older printconf stuff

* Thu Aug  8 2002 Yukihiro Nakai <ynakai@redhat.com>
- link docj.tmac to doc.tmac #57560

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de>
- update to 1.18
- mmroff(7) is now mmroff(1)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com>
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq install-info and add post/preun for info files

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add info files #64667

* Fri Feb 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild in new environment

* Sun Feb 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-16
- patch4 is already included in that

* Thu Jan 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- disable printconf support, but do not yet delete it from the source rpm

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- check string input

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add URL tag

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-13

* Thu Dec 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-12

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 1.17.2-3
- Added symlink from soelim to zsoelim, fixing bug (#51037)

* Tue Aug 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fixes security bug #50494

* Sun Aug 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.17.2
- strerror patch is not needed anymore
- apply newest debian patch

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Tue Apr 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not change groff to use /etc/papersize. Deleted the changes
  in the debian patch.

* Fri Mar 30 2001 Trond Eivind GlomsrĹd <teg@redhat.com>
- Add hyphen.cs - file generated as described in Czech how-to, 6.7

* Wed Mar 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- updated to newest debian patch to get nippon/ascii8 support
  better working

* Fri Feb  9 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switch to printconf filtration rules

* Tue Jan 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change app-defaults to /usr/X11R6/lib/X11/app-defaults/
  and do not mark it as config file

* Thu Dec 14 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch from RHL7J

* Fri Aug  4 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to bug-fix release 1.16.1

* Fri Jul 28 2000 Tim Waugh <twaugh@redhat.com>
- Install troff-to-ps.fpi in /usr/lib/rhs-printfilters (#13634).

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with gcc-2.96-41.

* Mon Jul 17 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to fix miscompilation manifesting in alpha build of tcltk.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- move mmroff to -perl

* Wed Jun  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build
- FHS
- 1.16

* Sun May 14 2000 Jeff Johnson <jbj@redhat.com>
- install tmac.mse (FWIW tmac.se looks broken) to fix dangling symlink (#10757).
- add README.A4, how to set up for A4 paper (#8276).
- add other documents to package.

* Thu Mar  2 2000 Jeff Johnson <jbj@redhat.com>
- permit sourcing on regular files within cwd tree (unless -U specified).

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- fix incorrectly installed tmac.m file (#8362).

* Mon Feb  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- check if build system is sane again

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary
- man pages are compressed. This is ugly.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- put the binaries actually in the package *oops*

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- split perl components into separate subpackage

* Wed Dec 29 1999 Bill Nottingham <notting@redhat.com>
- update to 1.15

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)
* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1 patch for xditview (#992)

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- fix makefiles to work with bash2

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use g++ for C++ code

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- manhattan and buildroot

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- made xdefaults file a config file

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- split perl components into separate subpackage

* Tue Oct 21 1997 Michael Fulbright <msf@redhat.com>
- updated to 1.11a
- added safe troff-to-ps.fpi

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- removed troff-to-ps.fpi for security reasons.

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

