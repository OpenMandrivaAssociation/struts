# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define full_name	jakarta-%{name}
%define tomcat5appsdir  %{_localstatedir}/lib/tomcat5/webapps
%define tomcat5ctxdir   %{_sysconfdir}/tomcat5/Catalina/localhost
%define webapps		blank documentation example examples tiles-documentation
%define webapplibs commons-beanutils commons-digester commons-fileupload commons-validator oro struts

Name:		struts
Version:	1.2.9
Release:	12
Epoch:		0
Summary:	Web application framework
License:	ASL 2.0
Group:          Development/Java
Source0:	%{name}-%{version}-src-RHCLEAN.tar.gz
Source2:	tomcat4-context-allowlinking.xml
Source3:	tomcat5-context-allowlinking.xml
#Patch0:		%{name}-%{version}.build.patch
Patch0:		struts-1.2.9-strutsel-build_xml.patch
Patch1:		struts-1.2.9-FacesRequestProcessor.patch
Patch2:		struts-1.2.9-HttpServletRequestWrapper.patch
Patch3:		struts-1.2.9-FacesTilesRequestProcessor.patch
Patch4:		struts-1.2.9-strutsfaces-example1-build_xml.patch
Patch5:		struts-1.2.9-strutsfaces-example2-build_xml.patch
Patch6:		struts-1.2.9-strutsfaces-systest1-build_xml.patch
Patch7:		struts-1.2.9.bz157205.patch
Patch8:		struts-1.2.9-CVE-2008-2025.patch
URL:		http://struts.apache.org/
Requires:	servlet25
Requires:	jakarta-commons-beanutils
Requires:	jakarta-commons-digester
Requires:	jakarta-commons-fileupload
Requires:	jakarta-commons-validator
Requires:	jakarta-oro
BuildRequires:	jpackage-utils >= 1.6
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:	ant >= 1.6
BuildRequires:	antlr
BuildRequires:	jaxp_transform_impl
BuildRequires:	sed
BuildRequires:	servlet25
BuildRequires:  jsp21
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-fileupload
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-commons-validator
BuildRequires:  jakarta-oro

Group:		Development/Java
BuildArch:	noarch

%description
Welcome to the Struts Framework! The goal of this project is to provide
an open source framework useful in building web applications with Java
Servlet and JavaServer Pages (JSP) technology. Struts encourages
application architectures based on the Model-View-Controller (MVC)
design paradigm, colloquially known as Model 2 in discussions on various
servlet and JSP related mailing lists.
Struts includes the following primary areas of functionality:
A controller servlet that dispatches requests to appropriate Action
classes provided by the application developer.
JSP custom tag libraries, and associated support in the controller
servlet, that assists developers in creating interactive form-based
applications.
Utility classes to support XML parsing, automatic population of
JavaBeans properties based on the Java reflection APIs, and
internationalization of prompts and messages.
Struts is part of the Jakarta Project, sponsored by the Apache Software
Foundation. The official Struts home page is at
http://jakarta.apache.org/struts.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package webapps-tomcat5
Summary:        Sample %{name} webapps for tomcat5
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       jakarta-commons-beanutils
Requires:       jakarta-commons-digester
Requires:       jakarta-commons-fileupload
Requires:       jakarta-commons-validator
Requires:       jakarta-oro
Requires:       tomcat5
Requires(post): %{name} = %{version}-%{release}
Requires(post): jakarta-commons-beanutils
Requires(post): jakarta-commons-digester
Requires(post): jakarta-commons-fileupload
Requires(post): jakarta-commons-validator
Requires(post): jakarta-oro
Requires(post): tomcat5
Requires(pre):  tomcat5
# for /bin/ln and /bin/rm
Requires(post): coreutils
Requires(preun): coreutils

%description webapps-tomcat5
Sample %{name} webapps for tomcat5.

%prep
%setup -n %{name}-%{version}-src -q
%patch0 -p0 -b .sav
%patch1 -p0 -b .sav
%patch2 -p0 -b .sav
%patch3 -p0 -b .sav
%patch4 -p0 -b .sav
%patch5 -p0 -b .sav
%patch6 -p0 -b .sav
%patch7 -p0 -b .sav
%patch8 -p1 -b .sav
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build

# build struts
export CLASSPATH=$(build-classpath servlet)
export ANT_OPTS="-Xmx256m"
STRUTS_BUILD_HOME=$(pwd)
ant -Dlibdir=/usr/share/java \
	-Dcommons-beanutils.jar=$(build-classpath commons-beanutils) \
	-Dcommons-digester.jar=$(build-classpath commons-digester) \
	-Dcommons-fileupload.jar=$(build-classpath commons-fileupload) \
	-Dcommons-logging.jar=$(build-classpath commons-logging) \
	-Dcommons-validator.jar=$(build-classpath commons-validator) \
	-Djakarta-oro.jar=$(build-classpath oro) \
        -Djdbc20ext.jar=$(find-jar jdbc-stdext) \
	-Djsp.jar=$(build-classpath jsp) \
	-Dservlet.jar=$(build-classpath servlet) \
	-Dantlr.jar=$(build-classpath antlr) \
	 dist
#	 compile.library compile.webapps compile.javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/lib/%{name}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/documentation/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/documentation/api

# data
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/*.tld $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/*.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/vali*.xml $RPM_BUILD_ROOT%{_datadir}/%{name}

# core docs
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs
cp -p {INSTALL,LICENSE.txt,NOTICE.txt,README,STATUS.txt} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p target/documentation/*.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs
cp -p target/documentation/*.gif $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs
cp -pr target/documentation/uml $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs
cp -pr target/documentation/userGuide $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs
cp -pr target/documentation/images $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/docs

# tomcat 5 webapps
install -d -m 755 $RPM_BUILD_ROOT%{tomcat5appsdir}
install -d -m 755 $RPM_BUILD_ROOT%{tomcat5ctxdir}
for webapp in %{webapps}; do
    cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp
    cat %{SOURCE3} | sed -e "s/@@@APPNAME@@@/$webapp/g;" > $RPM_BUILD_ROOT%{tomcat5ctxdir}/%{name}-$webapp.xml
	# XXX: move to %%post/preun
	rm -f $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp/WEB-INF/lib/*
    (cd $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp/WEB-INF \
    && for tld in ../../../../../..%{_datadir}/%{name}/*.tld; do ln -sf $tld `basename $tld`; done)
done

%post webapps-tomcat5
for webapp in %{webapps}; do
build-jar-repository -s -p %{tomcat5appsdir}/%{name}-$webapp/WEB-INF/lib commons-beanutils commons-digester commons-fileupload commons-validator oro
ln -s %{_javadir}/struts.jar %{tomcat5appsdir}/%{name}-$webapp/WEB-INF/lib
done

%preun webapps-tomcat5
for webapp in %{webapps}; do
rm -f %{tomcat5appsdir}/%{name}-$webapp/WEB-INF/lib/*
done

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/INSTALL
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/*.txt
%{_javadir}/%{name}.jar
%{_datadir}/%{name}

%files manual
%defattr(-,root,root)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/docs

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}

%files webapps-tomcat5
%defattr(-,tomcat,tomcat)
%dir %{tomcat5appsdir}/%{name}-blank
%{tomcat5appsdir}/%{name}-blank/*
%dir %{tomcat5appsdir}/%{name}-documentation
%{tomcat5appsdir}/%{name}-documentation/*
%dir %{tomcat5appsdir}/%{name}-example
%{tomcat5appsdir}/%{name}-example/*
%dir %{tomcat5appsdir}/%{name}-examples
%{tomcat5appsdir}/%{name}-examples/*
%dir %{tomcat5appsdir}/%{name}-tiles-documentation
%{tomcat5appsdir}/%{name}-tiles-documentation/*
%{tomcat5ctxdir}/%{name}-blank.xml
%{tomcat5ctxdir}/%{name}-documentation.xml
%{tomcat5ctxdir}/%{name}-example.xml
%{tomcat5ctxdir}/%{name}-examples.xml
%{tomcat5ctxdir}/%{name}-tiles-documentation.xml

