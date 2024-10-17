%{?_javapackages_macros:%_javapackages_macros}
%global master_version 4
Name:          struts
Version:       1.3.10
Release:       12.3
Summary:       Web application framework
Group:         Development/Java
License:       ASL 2.0
URL:           https://struts.apache.org/
# wget http://www.apache.org/dist/struts/source/struts-1.3.10-src.zip
# remove non free resources
# unzip -qq struts-1.3.10-src.zip
# rm -r struts-1.3.10/src/core/src/main/resources/org/apache/struts/resources/web-app_2_3.dtd
# tar czf struts-1.3.10-clean-src.tar.gz struts-1.3.10
Source0:       %{name}-%{version}-clean-src.tar.gz
# wget -O struts-master-4-pom.xml http://svn.apache.org/repos/asf/struts/maven/tags/STRUTS_MASTER_4/pom.xml
Source1:       %{name}-master-%{master_version}-pom.xml
# add struts-master relativePath
Patch0:        %{name}-%{version}-parent-pom.patch
# add 
#  org.jboss.spec.javax.el jboss-el-api_2.2_spec
#  org.apache.maven.plugins maven-resources-plugin configuration
# change 
#  myfaces myfaces-jsf-api 1.0.9 with org.jboss.spec.javax.faces jboss-jsf-api_2.1_spec
#  jakarta-taglibs-standard with jboss-jstl-1.2-api
#  javax.servlet servlet-api with org.jboss.spec.javax.servlet jboss-servlet-api_3.0_spec
#  javax.servlet jsp-api with org.jboss.spec.javax.servlet.jsp jboss-jsp-api_2.2_spec
# fix
#  bsf gId
#  maven-compiler-plugin build source/target
#  build for junit servlet-3.0-api
Patch1:        %{name}-%{version}-jboss.patch
# Thanks to Arun Babu Neelicattu aneelica@redhat.com
# and Brandon.Vincent@asu.edu
Patch2: struts-1.3.10-CVE-2014-0114.patch

BuildRequires: java-devel

BuildRequires: mvn(antlr:antlr)
BuildRequires: mvn(commons-beanutils:commons-beanutils)
BuildRequires: mvn(commons-chain:commons-chain)
BuildRequires: mvn(commons-digester:commons-digester)
BuildRequires: mvn(commons-fileupload:commons-fileupload)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(commons-validator:commons-validator)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.bsf:bsf)
BuildRequires: mvn(org.jboss.spec.javax.el:jboss-el-api_2.2_spec)
BuildRequires: mvn(org.jboss.spec.javax.faces:jboss-jsf-api_2.1_spec)
BuildRequires: mvn(org.jboss.spec.javax.servlet.jsp:jboss-jsp-api_2.2_spec)
BuildRequires: mvn(org.jboss.spec.javax.servlet.jstl:jboss-jstl-api_1.2_spec)
BuildRequires: mvn(org.jboss.spec.javax.servlet:jboss-servlet-api_3.0_spec)
BuildRequires: mvn(oro:oro)

BuildRequires: maven-local
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch
Obsoletes:     %{name}-manual < %{version}
Obsoletes:     %{name}-webapps-tomcat5 < %{version}

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

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find -name "*.jar" -delete
find -name "*.class" -delete
%patch0 -p0
%patch1 -p1
%patch2 -p0

sed -i 's/\r//' LICENSE.txt NOTICE.txt

# fix non ASCII chars
for s in src/tiles/src/main/java/org/apache/struts/tiles/ComponentDefinition.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

%pom_remove_parent src
#cp -p %{SOURCE1} pom.xml

cd src
%mvn_file :%{name}-core %{name}/core
%mvn_file :%{name}-el %{name}/el
%mvn_file :%{name}-extras %{name}/extras
%mvn_file :%{name}-faces %{name}/faces
%mvn_file :%{name}-mailreader-dao %{name}/mailreader-dao
%mvn_file :%{name}-scripting %{name}/scripting
%mvn_file :%{name}-taglib %{name}/taglib
%mvn_file :%{name}-tiles %{name}/tiles

%build

cd src
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install

(
cd src
%mvn_install
)

#install -pm 644 pom.xml %%{buildroot}%%{_mavenpomdir}/JPP.%%{name}-master.pom
#%%add_maven_depmap JPP.%%{name}-master.pom

%files -f src/.mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt NOTICE.txt

%files javadoc -f src/.mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 gil cattaneo <puntogil@libero.it> 1.3.10-8
- switch to XMvn
- minor changes to adapt to current guideline

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.3.10-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 gil cattaneo <puntogil@libero.it> 1.3.10-4
- replace tomcat 7.x apis with jboss apis

* Fri Jun 29 2012 gil cattaneo <puntogil@libero.it> 1.3.10-3
- replace jakarta-taglibs-standard with jboss-jstl-1.2-api

* Sat Jun 23 2012 gil cattaneo <puntogil@libero.it> 1.3.10-2
- removed non-free resources

* Sat May 26 2012 gil cattaneo <puntogil@libero.it> 1.3.10-1
- initial rpm
