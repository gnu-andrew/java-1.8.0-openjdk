#!/bin/bash

# Generates the 'source tarball' for JDK 8 projects.
#
# Usage: generate_source_tarball.sh <hg directory root> <version>
#
# Examples:
#  sh generate_source_tarball.sh ${HOME}/trees/jdk8u51-b16 jdk8u51-b16
#
# This script creates a single source tarball out of the repository
# based on the given tag and removes code not allowed in fedora. For
# consistency, the source tarball will always contain 'openjdk' as the top
# level folder.

set -e

TREE="$1"
VERSION="$2"

if [[ "${TREE}" = "" ]] ; then
    echo "No repository specified."
    exit -1
fi
if [[ "${VERSION}" = "" ]]; then
    echo "No version/tag specified."
    exit -1;
fi

mkdir jdk8u
pushd jdk8u

hg clone ${TREE} openjdk
pushd openjdk

repos="corba hotspot jdk jaxws jaxp langtools nashorn"

for subrepo in $repos
do
    hg clone ${TREE}/${subrepo}
done

echo "Removing EC source code we don't build"
rm -vrf jdk/src/share/native/sun/security/ec/impl

echo "Syncing EC list with NSS"
patch -Np1 < ../../pr2126.patch

popd

find openjdk -name '.hg' | xargs rm -rvf
tar cJf jdk8u-${VERSION}.tar.xz openjdk

popd

mv jdk8u/jdk8u-${VERSION}.tar.xz .
