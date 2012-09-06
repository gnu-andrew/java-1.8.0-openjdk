#!/bin/bash

VERSION=$1
REV=$2
JDK8_URL=http://hg.openjdk.java.net/jdk8/jdk8

if test "x${VERSION}" = "x"; then
    echo "No version specified.":
    exit -1;
fi

wget -O root.tar.gz ${JDK8_URL}/archive/${VERSION}.tar.gz
tar xzf root.tar.gz
rm -f root.tar.gz
mv jdk8-${VERSION} jdk8
rm -f jdk8/.hg*
pushd jdk8

for repos in corba jaxp jaxws langtools hotspot jdk
do
    wget -O $repos.tar.gz ${JDK8_URL}/${repos}/archive/${VERSION}.tar.gz
    tar xzf $repos.tar.gz
    rm -f $repos.tar.gz
    mv $repos-${VERSION} $repos
    rm -f $repos/.hg*
done

popd
tar czf jdk8-${VERSION}.tar.gz jdk8
