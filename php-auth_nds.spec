%define realname Auth NDS
%define modname auth_nds
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A21_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	2.2.6
Release:	32
Group:		Development/PHP
License:	GPL
URL:		ftp://platan.vc.cvut.cz/pub/linux/ncpfs/
Source0:	php-%{modname}-%{version}.tar.gz
Patch0:		php-auth_nds-2.2.6-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ncpfs-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a dynamic shared object (DSO) that adds Auth NDS support to PHP.

%prep

%setup -q -n php-%{modname}-%{version}

%patch0 -p0

# small hack
#cat >> config.h << EOF
#define HAVE_DLFCN_H 1
#define COMPILE_DL_AUTH_NDS 1
#define NCPFS_VERSION "%{version}"
#EOF

%build

%{_usrsrc}/php-devel/buildext %{modname} "php_auth_nds.c" \
    "-lncp" "-I%{_includedir}/ncp -DHAVE_DLFCN_H -DCOMPILE_DL_AUTH_NDS -DNCPFS_VERSION=\"%{version}\""

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc site README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-31mdv2012.0
+ Revision: 806422
- fix build
- sync with the latest ncpfs cooker source
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-29
+ Revision: 761199
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-28
+ Revision: 696392
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-27
+ Revision: 695349
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-26
+ Revision: 646611
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-25mdv2011.0
+ Revision: 629764
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-24mdv2011.0
+ Revision: 628066
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-23mdv2011.0
+ Revision: 600460
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-22mdv2011.0
+ Revision: 588742
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-21mdv2010.1
+ Revision: 514516
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-20mdv2010.1
+ Revision: 485337
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-19mdv2010.1
+ Revision: 468142
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-18mdv2010.0
+ Revision: 451251
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 2.2.6-17mdv2010.0
+ Revision: 397263
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-16mdv2010.0
+ Revision: 376971
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-15mdv2009.1
+ Revision: 346393
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-14mdv2009.1
+ Revision: 341706
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-13mdv2009.1
+ Revision: 321702
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-12mdv2009.1
+ Revision: 310247
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-11mdv2009.0
+ Revision: 238376
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-10mdv2009.0
+ Revision: 200186
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-9mdv2008.1
+ Revision: 162212
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-8mdv2008.1
+ Revision: 107605
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-7mdv2008.0
+ Revision: 77527
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-6mdv2008.0
+ Revision: 39482
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-5mdv2008.0
+ Revision: 33795
- rebuilt against new upstream version (5.2.3)
- rebuilt against new upstream version (5.2.2)


* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-3mdv2007.0
+ Revision: 78124
- fix deps

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-2mdv2007.1
+ Revision: 78055
-rebuilt for php-5.2.0
- Import php-auth_nds

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-1
- rebuilt for php-5.1.6

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.6-5
- rebuilt for php-4.4.4

* Sun Aug 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.6-4mdv2007.0
- rebuilt for php-4.4.3

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.6-3mdk
- rebuild

* Mon Jan 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.6-2mdk
- rebuilt against php-4.4.2

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.6-1mdk
- rebuilt for php-4.4.1
- fix versioning

* Tue Jul 12 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- rebuilt for php-4.4.0 final

* Wed Jul 06 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC2.1mdk
- rebuilt for php-4.4.0RC2

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_2.2.6-0.RC1.1mdk
- rebuilt for php-4.4.0RC1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_2.2.6-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_2.2.6-1mdk
- renamed to php4-*

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_2.2.6-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_2.2.6-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_2.2.6-1mdk
- 2.2.6
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_2.2.5-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_2.2.5-1mdk
- rebuild for php 4.3.10

* Fri Dec 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_2.2.5-1mdk
- sync with ncpfs-2.2.5

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_2.2.4-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_2.2.4-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.2.4-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.2.4-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.2.4-2mdk
- move scandir to /etc/php4.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.2.4-1mdk
- fix url
- fix invalid-build-requires
- built for php 4.3.6

