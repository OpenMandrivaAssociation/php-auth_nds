%define realname Auth NDS
%define modname auth_nds
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A21_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	2.2.6
Release:	%mkrel 19
Group:		Development/PHP
License:	GPL
URL:		ftp://platan.vc.cvut.cz/pub/linux/ncpfs/
Source0:	php-%{modname}-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ncpfs-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a dynamic shared object (DSO) that adds Auth NDS support to PHP.

%prep

%setup -q -n php-%{modname}-%{version}

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
