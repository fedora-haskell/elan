#!/bin/sh

VERSION="$(/usr/lib64/lean4/bin/lean --version | sed -e 's/Lean (version \(.*\), .*/\1/')"

for i in $(find ~/.elan/toolchains/ -maxdepth 1 -type l ); do
    if [ "$(readlink $i)" = "/usr/lib64/lean4" ]; then
        elan toolchain uninstall $(basename $i)
    fi
done

elan toolchain link $VERSION /usr/lib64/lean4
elan default $VERSION
