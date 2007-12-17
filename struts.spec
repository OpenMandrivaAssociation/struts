# FIXME:
# W: struts class-path-in-manifest /usr/share/java/struts-1.2.9.jar

%define gcj_support     1
%define full_name       jakarta-%{name}
%define _localstatedir  %{_var}
%define tomcat3appsdir  %{_localstatedir}/lib/tomcat3/webapps
%define tomcat4appsdir  %{_localstatedir}/lib/tomcat4/webapps
%define tomcat5appsdir  %{_localstatedir}/lib/tomcat5/webapps
%define tomcat5ctxdir   %{_sysconfdir}/tomcat5/Catalina/localhost
%define section         free
%define webapps         blank documentation example examples tiles-documentation
%define webapplibs      commons-beanutils commons-digester commons-fileupload commons-validator oro struts

Name:           struts
Version:        1.2.9
Release:        %mkrel 5.4
Epoch:          0
Summary:        Web application framework
License:        Apache License
Group:          Development/Libraries/Java
Source0:        http://apache.org/dist/struts/source/struts-%{version}-src-MDVCLEAN.tar.bz2
Source2:        tomcat4-context-allowlinking.xml
Source3:        tomcat5-context-allowlinking.xml
Patch0:         %{name}-%{version}.build.patch
Patch1:         %{name}-%{version}.bz157205.patch
Url:            http://struts.apache.org/
Requires:       servletapi5
Requires:       jdbc-stdext
Requires:       jakarta-commons-beanutils >= 0:1.7.0
Requires:       jakarta-commons-digester >= 0:1.6
Requires:       jakarta-commons-fileupload >= 0:1.0
Requires:       jakarta-commons-logging >= 0:1.0.4
Requires:       jakarta-commons-validator >= 0:1.1.4
Requires:       jsp
Requires:       oro >= 0:2.0.7
BuildRequires:  java-rpmbuild >= 1.5
BuildRequires:  ant >= 1.6.1
BuildRequires:  antlr >= 2.7.2
BuildRequires:  ant-trax
BuildRequires:  ant-nodeps
BuildRequires:  jaxp_transform_impl
BuildRequires:  xalan-j2
BuildRequires:  sed
BuildRequires:  servletapi5
BuildRequires:  jdbc-stdext
BuildRequires:  jakarta-commons-beanutils >= 0:1.7.0
BuildRequires:  jakarta-commons-digester >= 0:1.6
BuildRequires:  jakarta-commons-fileupload >= 0:1.0
BuildRequires:  jakarta-commons-logging >= 0:1.0.4
BuildRequires:  jakarta-commons-validator >= 0:1.1.4
BuildRequires:  jsp
BuildRequires:  oro >= 0:2.0.7
Group:          Development/Java
# RHEL4 and FC4
#Obsoletes:     struts11 <= 0:1.1-1jpp_7fc
# libgcj aot-compiled native libraries
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 0:1.0.35
%else
BuildArch:      noarch
%endif

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
Foundation.

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

%if 0
%package webapps-tomcat3
Summary:        Sample %{name} webapps for tomcat3
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       tomcat3

%description webapps-tomcat3
Sample %{name} webapps for tomcat3.

%package webapps-tomcat4
Summary:        Sample %{name} webapps for tomcat4
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       tomcat4

%description webapps-tomcat4
Sample %{name} webapps for tomcat4.
%endif

%package webapps-tomcat5
Summary:        Sample %{name} webapps for tomcat5
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       tomcat5

%description webapps-tomcat5
Sample %{name} webapps for tomcat5.

%prep
%setup -n %{name}-%{version}-src -q
%patch0
%patch1 -p1

mkdir lib; pushd lib
  ln -s $(find-jar jspapi) .
popd

%build
# build struts
export CLASSPATH=
export OPT_JAR_LIST="ant/ant-nodeps ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} -Djdbc20ext.jar=$(find-jar jdbc-stdext) \
        -Dcommons-beanutils.jar=$(build-classpath commons-beanutils) \
        -Dcommons-digester.jar=$(build-classpath commons-digester) \
        -Dcommons-fileupload.jar=$(build-classpath commons-fileupload) \
        -Dcommons-logging.jar=$(build-classpath commons-logging) \
        -Dcommons-validator.jar=$(build-classpath commons-validator) \
        -Djakarta-oro.jar=$(build-classpath oro) \
        -Djsp.jar=$(build-classpath jspapi) \
        -Dservlet.jar=$(build-classpath servletapi5) \
        -Dantlr.jar=$(build-classpath antlr) \
        compile.library compile.webapps compile.javadoc

%install
%{__rm} -rf %{buildroot}
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 target/library/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/documentation/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf target/documentation/api
# data
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 target/library/*.tld $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 target/library/*.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}

%if 0
# tomcat 3 webapps
install -d -m 755 $RPM_BUILD_ROOT%{tomcat3appsdir}
for webapp in %{webapps}; do
    cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcat3appsdir}/%{name}-$webapp
    # tomcat3 doesn't support allowLinking, this might not work
       # XXX: move to %%post/preun
       for jar in %{webapplibs}; do
        (cd $RPM_BUILD_ROOT%{tomcat3appsdir}/%{name}-$webapp/WEB-INF/lib \
        && ln -sf ../../../../../..%{_javadir}/$jar.jar .)
       done
    (cd $RPM_BUILD_ROOT%{tomcat3appsdir}/%{name}-$webapp/WEB-INF \
    && for tld in ../../../../..%{_datadir}/%{name}/*.tld; do ln -sf $tld `basename $tld`; done)
done

# tomcat 4 webapps
install -d -m 755 $RPM_BUILD_ROOT%{tomcat4appsdir}
for webapp in %{webapps}; do
    cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcat4appsdir}/%{name}-$webapp
    cat %{SOURCE2} | sed -e "s/@@@APPNAME@@@/$webapp/g;" > $RPM_BUILD_ROOT%{tomcat4appsdir}/%{name}-$webapp.xml
       # XXX: move to %%post/preun
       for jar in %{webapplibs}; do
        (cd $RPM_BUILD_ROOT%{tomcat4appsdir}/%{name}-$webapp/WEB-INF/lib \
        && ln -sf ../../../../../../..%{_javadir}/$jar.jar .)
    done
    (cd $RPM_BUILD_ROOT%{tomcat4appsdir}/%{name}-$webapp/WEB-INF \
    && for tld in ../../../../../..%{_datadir}/%{name}/*.tld; do ln -sf $tld `basename $tld`; done)
done
%endif

# tomcat 5 webapps
install -d -m 755 $RPM_BUILD_ROOT%{tomcat5appsdir}
install -d -m 755 $RPM_BUILD_ROOT%{tomcat5ctxdir}
for webapp in %{webapps}; do
    cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp
    cat %{SOURCE3} | sed -e "s/@@@APPNAME@@@/$webapp/g;" > $RPM_BUILD_ROOT%{tomcat5ctxdir}/%{name}-$webapp.xml
        # XXX: move to %%post/preun
        for jar in %{webapplibs}; do
        (cd $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp/WEB-INF/lib \
        && ln -sf ../../../../../../..%{_javadir}/$jar.jar .)
    done
    (cd $RPM_BUILD_ROOT%{tomcat5appsdir}/%{name}-$webapp/WEB-INF \
    && for tld in ../../../../../..%{_datadir}/%{name}/*.tld; do ln -sf $tld `basename $tld`; done)
done

%{__perl} -pi -e 's|\r$||g' \
  README LICENSE.txt NOTICE.txt STATUS.txt INSTALL target/documentation/uml/Credits.html
find $RPM_BUILD_ROOT -name download.cgi | xargs %{__chmod} 755
find $RPM_BUILD_ROOT -name download.cgi | xargs %{__perl} -pi -e 's|\r$||g'

%if %{gcj_support}
%{_bindir}/aot-compile-rpm

%clean
%{__rm} -rf %{buildroot}

%post
%{update_gcjdb}

%postun
%{clean_gcjdb}

%if 0
%post webapps-tomcat3
%{update_gcjdb}

%postun webapps-tomcat3
%{clean_gcjdb}

%post webapps-tomcat4
%{update_gcjdb}

%postun webapps-tomcat4
%{clean_gcjdb}
%endif

%post webapps-tomcat5
%{update_gcjdb}

%postun webapps-tomcat5
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%doc INSTALL LICENSE.txt README NOTICE.txt STATUS.txt
%{_javadir}/*
%{_datadir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files manual
%defattr(-,root,root)
%doc target/documentation/*.html
%doc target/documentation/*.gif
%doc target/documentation/uml
%doc target/documentation/userGuide
%doc target/documentation/images

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}

%if 0
%files webapps-tomcat3
%defattr(-,tomcat3,tomcat3)
%dir %{tomcat3appsdir}/%{name}-blank
%{tomcat3appsdir}/%{name}-blank/*
%dir %{tomcat3appsdir}/%{name}-documentation
%{tomcat3appsdir}/%{name}-documentation/*
%dir %{tomcat3appsdir}/%{name}-example
%{tomcat3appsdir}/%{name}-example/*
%dir %{tomcat3appsdir}/%{name}-examples
%{tomcat3appsdir}/%{name}-examples/*
%dir %{tomcat3appsdir}/%{name}-tiles-documentation
%{tomcat3appsdir}/%{name}-tiles-documentation/*
%attr(-,root,root) %{_libdir}/gcj/%{name}/*classes.jar.*

%files webapps-tomcat4
%defattr(-,tomcat,tomcat)
%dir %{tomcat4appsdir}/%{name}-blank
%{tomcat4appsdir}/%{name}-blank/*
%dir %{tomcat4appsdir}/%{name}-documentation
%{tomcat4appsdir}/%{name}-documentation/*
%dir %{tomcat4appsdir}/%{name}-example
%{tomcat4appsdir}/%{name}-example/*
%dir %{tomcat4appsdir}/%{name}-examples
%{tomcat4appsdir}/%{name}-examples/*
%dir %{tomcat4appsdir}/%{name}-tiles-documentation
%{tomcat4appsdir}/%{name}-tiles-documentation/*
%{tomcat4appsdir}/%{name}-*.xml
%attr(-,root,root) %{_libdir}/gcj/%{name}/*classes.jar.*
%endif

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
%config(noreplace) %{tomcat5ctxdir}/%{name}-*.xml
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*classes.jar.*
%endif


