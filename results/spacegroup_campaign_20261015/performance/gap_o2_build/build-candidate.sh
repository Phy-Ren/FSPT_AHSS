#!/bin/bash
set -euo pipefail
export LC_ALL=C
export PATH=/home/user/xyren/miniforge3/envs/gap-centos6/bin:$PATH
cd /home/user/xyren/software/gap-4.13.1-o2-20261015
trap 'code=$?; printf "%s\n" "$code" > build.exit' EXIT
/home/user/xyren/software/gap-4.13.1/configure --disable-maintainer-mode CFLAGS='-O2 -Wno-error=incompatible-pointer-types' CXXFLAGS='-g -O2' > configure.stdout.log 2> configure.stderr.log
make -j8 > make.stdout.log 2> make.stderr.log
