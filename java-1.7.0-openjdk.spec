# If gcjbootstrap is 1 OpenJDK is bootstrapped against
# java-1.5.0-gcj-devel.  If gcjbootstrap is 0 OpenJDK is built against
# java-1.6.0-openjdk-devel.
%global gcjbootstrap 0

# If debug is 1, OpenJDK is built with all debug info present.
%global debug 0

# If runtests is 0 test suites will not be run.
%global runtests 0

%global openjdkver 147
%global openjdkbuildver b%{openjdkver}
%global openjdkdate 27_jun_2011

%global snapshot_date 20110803
%global icedtea_jdk7_snapshot 3defd24c2671
%global corba_snapshot 616c760dc288
%global hotspot_snapshot 1dd9b3d73b22
%global jaxp_snapshot c40983d6ae70
%global jaxws_snapshot 83db5e316798
%global jdk_snapshot e46d527097f1
%global langtools_snapshot fb7fb3071b64

%global accessmajorver 1.23
%global accessminorver 0
%global accessver %{accessmajorver}.%{accessminorver}
%global accessurl http://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/

%global jaxpurl     http://dlc.sun.com.edgesuite.net/jaxp/1.4.5/jaxp145_01.zip
%global jafurl      https://java.net/downloads/jax-ws/JDK7/jdk7-jaf-2010_08_19.zip
%global jaxwsurl    http://dlc.sun.com.edgesuite.net/glassfish/components/jax-ws/openjdk/jdk7/jdk7-jaxws2_2_4-b03-2011_05_27.zip

%global openjdkurlbase http://www.java.net/download/openjdk/jdk7/promoted/
%global openjdkurl %{openjdkurlbase}%{openjdkbuildver}/
%global openjdkzip  openjdk-7-fcs-src-%{openjdkbuildver}-%{openjdkdate}.zip

%global mauvedate 2008-10-22

%global multilib_arches ppc64 sparc64 x86_64

%global jit_arches %{ix86} x86_64 sparcv9 sparc64

%ifarch x86_64
%global archbuild amd64
%global archinstall amd64
%endif
%ifarch ppc
%global archbuild ppc
%global archinstall ppc
%endif
%ifarch ppc64
%global archbuild ppc64
%global archinstall ppc64
%endif
%ifarch i386
%global archbuild i586
%global archinstall i386
%endif
%ifarch i686
%global archbuild i586
%global archinstall i386
%endif
%ifarch ia64
%global archbuild ia64
%global archinstall ia64
%endif
%ifarch s390
%global archbuild s390x
%global archinstall s390x
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archbuild sparc
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archbuild sparcv9
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archbuild %{_arch}
%global archinstall %{_arch}
%endif

%if %{debug}
%global debugbuild debug_build
%else
%global debugbuild %{nil}
%endif

%global buildoutputdir openjdk/build/linux-%{archbuild}

%global with_pulseaudio 1

%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap %{nil}
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%ifarch %{multilib_arches}
%global syslibdir       %{_prefix}/lib64
%global _libdir         %{_prefix}/lib
%global archname        %{name}.%{_arch}
%else
%global syslibdir       %{_libdir}
%global archname        %{name}
%endif

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global priority        17000
%global javaver         1.7.0
%global buildver        0

# Standard JPackage directories and symbolic links.
# Make 64-bit JDKs just another alternative on 64-bit architectures.
%ifarch %{multilib_arches}
%global sdklnk          java-%{javaver}-%{origin}.%{_arch}
%global jrelnk          jre-%{javaver}-%{origin}.%{_arch}
%global sdkdir          %{name}-%{version}.%{_arch}
%else
%global sdklnk          java-%{javaver}-%{origin}
%global jrelnk          jre-%{javaver}-%{origin}
%global sdkdir          %{name}-%{version}
%endif
%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%global jrebindir       %{_jvmdir}/%{jrelnk}/bin
%ifarch %{multilib_arches}
%global jvmjardir       %{_jvmjardir}/%{name}-%{version}.%{_arch}
%else
%global jvmjardir       %{_jvmjardir}/%{name}-%{version}
%endif

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetdir /usr/share/systemtap/tapset/%{_build_cpu}
%endif

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{buildver}
Release: 0.1.%{snapshot_date}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/ openjdk -r %{icedtea_jdk7_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/corba/ openjdk/corba -r %{corba_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/hotspot/ openjdk/hotspot -r %{hotspot_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/jaxp/ openjdk/jaxp -r %{jaxp_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/jaxws/ openjdk/jaxws -r %{jaxws_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/jdk/ openjdk/jdk -r %{jdk_snapshot}
# hg clone http://icedtea.classpath.org/hg/icedtea7-forest/langtools/ openjdk/langtools -r %{langtools_snapshot}
# find openjdk -name ".hg" -exec rm -rf '{}' \;
# find openjdk -name ".hgtags" -exec rm -rf '{}' \;
# tar czf icedtea-jdk7-%{snapshot_date}.tar.gz openjdk
Source0:  icedtea-jdk7-%{snapshot_date}.tar.gz

# Gnome access bridge
Source1:  %{accessurl}%{accessmajorver}/java-access-bridge-%{accessver}.tar.bz2

# README file
Source2:  README.src

# Mauve test suite
# FIXME: Is this applicable for 7?
Source3:  mauve-%{mauvedate}.tar.gz
Source4:  mauve_tests

# jaxp drop
Source5:  %{jaxpurl}

# jaf drop
Source6:  %{jafurl}

# jaxws drop
Source7:  %{jaxwsurl}

# javac wrapper (used during bootstrap to strip what ecj doesn't support)
Source8: javac-wrapper

# Auto-generated files (used only in bootstrap)
# To reproduce: 
# build OpenJDK7 tarball above with any JDK
# mv generated.build generated
# tar czf generated-files.tar.gz generated
Source9: generated-files.tar.gz

# Class rewrite to rewrite rhino heirarchy
Source10: class-rewriter.tar.gz

# Systemtap tapsets. Zipped up to keep it small.
Source11: systemtap-tapset.tar.gz

# .desktop files. Zipped up to keep it small.
Source12: desktop-files.tar.gz

# nss configuration file
Source13: nss.cfg

# FIXME: Taken from IcedTea snapshot 877ad5f00f69, but needs to be moved out
# hg clone -r 877ad5f00f69 http://icedtea.classpath.org/hg/icedtea7
Source14: pulseaudio.tar.gz

# Removed libraries that we link instead
Source15: remove-intree-libraries.sh

# RPM/distribution specific patches

# Allow TCK to pass with access bridge wired in
Patch1:   java-1.7.0-openjdk-java-access-bridge-tck.patch

# Adjust idlj compilation switches to match what system idlj supports
Patch2:   java-1.7.0-openjdk-java-access-bridge-idlj.patch

# Disable access to access-bridge packages by untrusted apps
Patch3:   java-1.7.0-openjdk-java-access-bridge-security.patch

# Ignore AWTError when assistive technologies are loaded 
Patch4:   java-1.7.0-openjdk-accessible-toolkit.patch

# Build docs even in debug
Patch5:   java-1.7.0-openjdk-debugdocs.patch
Patch6:   %{name}-debuginfo.patch

#
# OpenJDK specific patches
#

# Use system JPEG and zlib libraries.
Patch100: libraries.patch

# Add com.sun.image.codec.jpeg support
Patch101: jpegclasses.patch

# Produces the "expected" behavior for full screen applications or other
# situations where developers wish to present elements that would cover things
# like panels
Patch102: override-redirect-metacity.patch

# GCC 4.3 miscompilation failure fix:
# http://icedtea.classpath.org/hg/icedtea/rev/f06de06e1ed4
Patch103: hotspot-gcc-pr36917.patch

# Add support for using an alternate jar tool in JDK building. 
Patch104: alt-jar.patch

# FIXME: Uses size_t and idx_t types [May be obsolete]
Patch105: use-idx_t.patch

# Cleans up crypto API to allow unlimited strength usage
Patch106: clean-crypto.patch

# FIXME: Hardens code, unknown origin [May be obsolete]
Patch107: jvmtiEnv.patch

# Add rhino jars to bootclasspath
Patch108: update-bootclasspath.patch

# Updates list of files to be compiled
Patch109: javafiles.patch

# Add rhino support
Patch110: rhino.patch

# We build from OpenJDK6 .. this causes some warnings. Make warnings non-fatal
Patch111: make-warnings-nonfatal.patch

#
# Bootstrap patches (code with this is never shipped)
#

# Explicitly set javac, so that the bootstrap version is used
Patch200: bootstrap-ant-javac.patch

# Adjusted generated sources path to use prebuilt ones
Patch201: bootstrap-corba-defs.patch

# Do not use idlj to generate sources, as we use prebuilt ones
Patch202: bootstrap-corba-idlj.patch

# Disable decending into sources dir for generation
Patch203: bootstrap-corba-no-gen.patch

# Explicitly compile ORB.java
Patch204: bootstrap-corba-orb.patch

# Don't build demos in bootstrap
Patch205: bootstrap-demos.patch

# Change hex constants to be numbers instead of 0x... so that ecj can compile them right
Patch206: bootstrap-ecj-fphexconstants.patch

# Adjust opt flags to remove what ecj doesn't support
Patch207: bootstrap-ecj-opts.patch

# use pre-generated font config files
Patch208: bootstrap-fontconfig.patch

# Don't write auto-generation message in bootstrap
Patch209: bootstrap-generated-comments.patch

# Adjust bootclasspath to match what ecj has
Patch210: bootstrap-xbootclasspath.patch

# Wire in icedtea rt.jar (FIXME: name needs update, kept same for now to match icedtea name)
Patch211: bootstrap-icedteart.patch

# Wire in custom compiles rt classes
Patch212: bootstrap-jar.patch

# Compile inner opengl class explicitly
Patch213: bootstrap-javah.patch

# Disable ct.sym creation for bootstrap
Patch214: bootstrap-symbols.patch

# Disable icon generation for bootstrap
Patch215: bootstrap-tobin.patch

# Don't run test_gamma
Patch216: bootstrap-test_gamma.patch

# Disable requirement of module_lib path which bootstrap java_home doesn't have
Patch217: bootstrap-tools.jar.patch

# Allow -J opts to jar only if jar knows of them
Patch218: bootstrap-jopt.patch

# Explicitly add jaxp classes to classpath
Patch219: bootstrap-jaxp-dependency.patch

# Don't fork when generating stubs
Patch220: bootstrap-genstubs-nofork.patch

# Remove dependency on ProcessBuilder which is package private to Oracle implementation
Patch221: bootstrap-break-processbuilder-dependency.patch

# Allow to build with 1.5
Patch222: bootstrap-revert-6973616.patch

# Avoid trying to load system zone info provider and failing
Patch223: bootstrap-revert-6941137.patch

# Replace usage of string switch with if/elseif/else
Patch224: bootstrap-ecj-stringswitch.patch

# Allow langtools to use older jdk
Patch225: bootstrap-langtools-force-old-jdk.patch

# Access JDK sources and classes from langtools build
Patch226: bootstrap-corba-dependencies.patch

# Access langtools classes for Javadoc
Patch227: bootstrap-jaxws-langtools-dependency.patch

# Access JDK sources for com.sun.net.httpserver
Patch228: bootstrap-jaxws-jdk-dependency.patch

# Access JDK and generated sources to build servicability agent
Patch229: bootstrap-hotspot-jdk-dependency.patch

# Remove use of multi-catch and replace with regular multi-level catch
Patch230: bootstrap-ecj-multicatch.patch

# Remove use of try-with-resources and replace with manual close
Patch231: bootstrap-ecj-trywithresources.patch

# Disable auto-boxing and manally cast
Patch232: bootstrap-ecj-autoboxing.patch

# Use custom xslt processor
Patch233: bootstrap-xsltproc.patch

# Use constants from interface rather than impl
Patch234: bootstrap-pr40188.patch

# Remove use of diamond operator and replace with manual
Patch235: bootstrap-ecj-diamond.patch

# Adjust javah switches to only use what bootstrap version supports
Patch236: bootstrap-javah-xbootclasspath.patch

#
# Optional component packages
#

# Make the ALSA based mixer the default when building with the pulseaudio based
# mixer
Patch300: pulse-soundproperties.patch

# SystemTap support
# Workaround for RH613824
Patch301: systemtap-alloc-size-workaround.patch
Patch302: systemtap-gcc-4.5.patch
Patch303: systemtap.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: wget
BuildRequires: xalan-j2
BuildRequires: xerces-j2
BuildRequires: xorg-x11-proto-devel
BuildRequires: mercurial
BuildRequires: ant
BuildRequires: ant-nodeps
BuildRequires: libXinerama-devel
BuildRequires: rhino
BuildRequires: redhat-lsb
%if %{gcjbootstrap}
BuildRequires: java-1.5.0-gcj-devel
%else
BuildRequires: java-1.6.0-openjdk-devel
%endif
# Mauve build requirements.
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: xorg-x11-fonts-Type1
BuildRequires: xorg-x11-fonts-misc
BuildRequires: freetype-devel >= 2.3.0
BuildRequires: fontconfig
BuildRequires: ecj
# Java Access Bridge for GNOME build requirements.
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: libbonobo-devel
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
# PulseAudio build requirements.
%if %{with_pulseaudio}
BuildRequires: pulseaudio-libs-devel >= 0.9.11
BuildRequires: pulseaudio >= 0.9.11
%endif
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif

ExclusiveArch: x86_64 i686

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
BuildRequires: prelink
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif
# visualvm build requirements.
BuildRequires: jakarta-commons-logging

Requires: rhino
Requires: libjpeg = 6b
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 3.0
Provides: java-sasl = %{epoch}:%{version}
Provides: java-fonts = %{epoch}:%{version}

%description
The OpenJDK runtime environment.

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage javadoc provides.
Provides: java-javadoc = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

%prep
%setup -q -c -n %{name}
%setup -q -n %{name} -T -D -a 3
%setup -q -n %{name} -T -D -a 1
cp %{SOURCE2} .
cp %{SOURCE4} .

# OpenJDK patches
%patch100
%patch101
%patch102
%patch103
%patch104
%patch105
%patch106
%patch107
%patch108
%patch109
%patch110
%patch111

# pulseaudio support
%if %{with_pulseaudio}
%patch300
%endif

# Add systemtap patches if enabled
%if %{with_systemtap}
%patch301
%patch302
%patch303
%endif

# Remove libraries that are linked
sh %{SOURCE15}

# Copy jaxp, jaf and jaxws drops
mkdir drops/
cp %{SOURCE5} drops/
cp %{SOURCE6} drops/
cp %{SOURCE7} drops/

# Extract the generated files
tar xzf %{SOURCE9}

# Extract the rewriter (to rewrite rhino classes)
tar xzf %{SOURCE10}

# Extract systemtap tapsets
%if %{with_systemtap}

tar xzf %{SOURCE11}

for file in tapset/*.in; do

    OUTPUT_FILE=`echo $file | sed -e s:\.in$::g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/amd64/server/libjvm.so:g $file > $OUTPUT_FILE
    sed -i -e '/@ABS_CLIENT_LIBJVM_SO@/d' $OUTPUT_FILE
    sed -i -e s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir}:g $OUTPUT_FILE
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE

done

%endif

# Pulseaudio
%if %{with_pulseaudio}
tar xzf %{SOURCE14}
%endif

# Extract desktop files
tar xzf %{SOURCE12}

# If bootstrapping, apply additional patches
%if %{gcjbootstrap}

cp -a openjdk openjdk-boot

# Add bootstrap patches
%patch200
%patch201
%patch202
%patch203
%patch204
%patch205
%patch206
%patch207
%patch208
%patch209
%patch210
%patch211
%patch212
%patch213
%patch214
%patch215
%patch216
%patch217
%patch218
%patch219
%patch220
%patch221
%patch222
%patch223
%patch224
%patch225
%patch226
%patch227
%patch228
%patch229
%patch230
%patch231
%patch232
%patch233
%patch234
%patch235
%patch236

%endif

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

# Build IcedTea and OpenJDK.
%ifarch sparc64 alpha
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

patch -l -p0 < %{PATCH3}
patch -l -p0 < %{PATCH4}

%if %{debug}
patch -l -p0 < %{PATCH5}
patch -l -p0 < %{PATCH6}
%endif

# Build the re-written rhino jar
mkdir -p rhino/{old,new}

# Compile the rewriter
(cd rewriter 
 javac com/redhat/rewriter/ClassRewriter.java
)

# Extract rhino.jar contents and rewrite
(cd rhino/old 
 jar xf /usr/share/java/rhino.jar
)

java -cp rewriter com.redhat.rewriter.ClassRewriter \
    $PWD/rhino/old \
    $PWD/rhino/new \
    org.mozilla \
    sun.org.mozilla

(cd rhino/old
 for file in `find -type f -not -name '*.class'` ; do
     new_file=../new/`echo $file | sed -e 's#org#sun/org#'`
     mkdir -pv `dirname $new_file`
     cp -v $file $new_file
     sed -ie 's#org\.mozilla#sun.org.mozilla#g' $new_file
 done
)

(cd rhino/new
   jar cfm ../rhino.jar META-INF/MANIFEST.MF sun
)

%if %{gcjbootstrap}

mkdir -p bootstrap/boot

# Copy over JAVA_HOME from /usr/lib/jvm/java-gcj/
cp -aL %{_jvmdir}/java-gcj/* bootstrap/boot/ || : # broken symlinks can be non-fatal but may cause this to fail

# Replace javac with a wrapper that does some magic
cp -af %{SOURCE8} bootstrap/boot/bin/javac
chmod u+x bootstrap/boot/bin/javac # SOURCE8 may not be +x
sed -i -e s:@RT_JAR@:$PWD/bootstrap/boot/jre/lib/rt.jar:g bootstrap/boot/bin/javac

# Link the native2ascii binary
ln -sf /usr/bin/gnative2ascii bootstrap/boot/bin/native2ascii

# We don't need a disassebler, fake it
echo "#!/bin/sh
exit 0" > bootstrap/boot/bin/javap
chmod u+rx bootstrap/boot/bin/javap # We need to run this during build

# Modules directory
mkdir -p bootstrap/boot/lib/modules

# jdk1.6.0 link
rm -f bootstrap/jdk1.6.0
ln -sf boot bootstrap/jdk1.6.0

# Update rt.jar with newer classes
# Extra classes to compile for reasons like
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=42003
echo "openjdk-boot/jdk/src/share/classes/java/util/regex/Matcher.java 
openjdk-boot/jdk/src/share/classes/javax/management/remote/JMXServiceURL.java 
openjdk-boot/jdk/src/share/classes/javax/management/modelmbean/ModelMBeanInfo.java 
openjdk-boot/jdk/src/share/classes/javax/swing/plaf/basic/BasicDirectoryModel.java
openjdk-boot/langtools/src/share/classes/javax/tools/JavaFileManager.java" > rt-source-files

mkdir -p rt
bootstrap/jdk1.6.0/bin/javac -g -encoding utf-8    -source 6 -target 6 -d rt \
  -classpath %{_jvmdir}/java-gcj/jre/lib/rt.jar \
  -sourcepath 'generated:openjdk-boot/jdk/src/share/classes:openjdk-boot/jdk/src/solaris/classes:openjdk-boot/langtools/src/share/classes:openjdk-boot/corba/src/share/classes' \
  -bootclasspath "\'\'" @rt-source-files

pushd rt
zip -qur ../bootstrap/jdk1.6.0/jre/lib/rt.jar *
popd

# clean up
rm -f rt-source-files
rm -rf rt

# Build it
pushd openjdk-boot
cp -a ../generated generated.build
chmod u+rwx generated.build

make \
  ALT_DROPS_DIR=$PWD/../drops \
  ALT_JDK_IMPORT_PATH="$PWD/../bootstrap/jdk1.6.0" \
  ANT="/usr/bin/ant" \
  ALT_BOOTDIR="$PWD/../bootstrap/jdk1.6.0" \
  ICEDTEA_RT="$PWD/../bootstrap/jdk1.6.0/jre/lib/rt.jar" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  NO_DOCS="true" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  DISABLE_NIMBUS="true" \
  XSLT="/usr/bin/xsltproc" \
  FT2_CFLAGS="-I/usr/include/freetype2 " \
  FT2_LIBS="-lfreetype "

export JDK_TO_BUILD_WITH=$PWD/build/linux-%{archbuild}/j2sdk-image

popd

%else

export JDK_TO_BUILD_WITH=/usr/lib/jvm/java-openjdk

%endif

pushd openjdk >& /dev/null

make \
  ALT_DROPS_DIR=$PWD/../drops \
  ALT_BOOTDIR="$JDK_TO_BUILD_WITH" \
  ANT="/usr/bin/ant" \
  DISTRO_NAME="Fedora" \
  DISTRO_PACKAGE_VERSION="fedora-%{release}-%{_arch}" \
  JDK_UPDATE_VERSION="%{openjdkbuildver}" \
  MILESTONE="fcs" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  STATIC_CXX="false" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  FT2_CFLAGS="-I/usr/include/freetype2 " \
  FT2_LIBS="-lfreetype " \
  %{debugbuild}

popd >& /dev/null

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Build pulseaudio and install it to JDK build location
%if %{with_pulseaudio}
pushd pulseaudio
make JAVA_HOME=$JAVA_HOME -f Makefile.pulseaudio
cp -pPRf build/native/libpulse-java.so $JAVA_HOME/jre/lib/%{archinstall}/
cp -pPRf build/pulse-java.jar $JAVA_HOME/jre/lib/ext/
popd
%endif

# Build Java Access Bridge for GNOME.
pushd java-access-bridge-%{accessver}
  patch -l -p1 < %{PATCH1}
  patch -l -p1 < %{PATCH2}
  OLD_PATH=$PATH
  export PATH=$JAVA_HOME/bin:$OLD_PATH
  ./configure
  make
  export PATH=$OLD_PATH
  cp -a bridge/accessibility.properties $JAVA_HOME/jre/lib
  cp -a gnome-java-bridge.jar $JAVA_HOME/jre/lib/ext
popd

%if %{runtests}
# Run jtreg test suite.
{
  echo ====================JTREG TESTING========================
  export DISPLAY=:20
  Xvfb :20 -screen 0 1x1x24 -ac&
  echo $! > Xvfb.pid
  make jtregcheck -k
  kill -9 `cat Xvfb.pid`
  unset DISPLAY
  rm -f Xvfb.pid
  echo ====================JTREG TESTING END====================
} || :

# Run Mauve test suite.
{
  pushd mauve-%{mauvedate}
    ./configure
    make
    echo ====================MAUVE TESTING========================
    export DISPLAY=:20
    Xvfb :20 -screen 0 1x1x24 -ac&
    echo $! > Xvfb.pid
    $JAVA_HOME/bin/java Harness -vm $JAVA_HOME/bin/java \
      -file %{SOURCE4} -timeout 30000 2>&1 | tee mauve_output
    kill -9 `cat Xvfb.pid`
    unset DISPLAY
    rm -f Xvfb.pid
    echo ====================MAUVE TESTING END====================
  popd
} || :
%endif

%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

pushd %{buildoutputdir}/j2sdk-image

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset
  cp -a $RPM_BUILD_DIR/%{name}/tapset/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset/
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{archname}/jce/vanilla

  # Install versionless symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{name}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

popd


# Install nss.cfg
install -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole policytool ; do
    desktop-file-install --vendor=%{name} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}.files
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post
ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{name}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{name}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{name}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{name}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{name}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{name}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{name}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{name}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi

update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%post devel
ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{name}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{name}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{name}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{name}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{name}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{name}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{name}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{name}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{name}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{name}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{name}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{name}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{name}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{name}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{name}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{name}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{name}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{name}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{name}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{name}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{name}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{name}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{name}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{name}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{name}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{name}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{name}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

exit 0

%postun devel
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

exit 0

%post javadoc
alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{name}/api \
  %{priority}

exit 0

%postun javadoc
if [ $1 -eq 0 ]
then
  alternatives --remove javadocdir %{_javadocdir}/%{name}/api
fi

exit 0


%files -f %{name}.files
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/jre/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE
%doc %{buildoutputdir}/j2sdk-image/jre/THIRD_PARTY_README

%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
%{_jvmdir}/%{jredir}/lib/security/nss.cfg

%files devel
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/LICENSE
%doc %{buildoutputdir}/j2sdk-image/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/apt-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jrunscript-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/schemagen-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/wsgen-%{name}.1*
%{_mandir}/man1/wsimport-%{name}.1*
%{_mandir}/man1/xjc-%{name}.1*
%ifarch %{jit_arches}
%{tapsetdir}/*.stp
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip
%if %{runtests}
# FIXME: put these in a separate testresults subpackage.
%doc mauve_tests
%doc mauve-%{mauvedate}/mauve_output
%doc test/jtreg-summary.log
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE

%changelog
* Fri Aug 05 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110803
- Used forest on classpath.org rather than the one on openjdk.net
- Added in-tree-removal script to remove libraries that we manually link
- Updated snapshots
- Added DISTRO_NAME and FreeType header/lib locations
- Removed application of patch100 (now in forest)
- Removed application of patch113 (now in forest)

* Wed Aug 03 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110729
- Initial build from java-1.6.0-openjdk RPM
