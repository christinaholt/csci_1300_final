#!/bin/bash -x


build_libs() {
  echo 'Building NCEP libraries'

  export CC=gcc FC=gfortran CXX=g++

  # Create a build directory under nceplibs and run cmake
  pushd src/nceplibs
  mkdir build
  pushd build
  cmake ..
  make
  popd
  popd
}

make_f2py() {
  echo 'Run f2py for nemsio_wrapper'

  # Run make to build the Fortran/Python shared object
  pushd src/nemsio_wrapper
  make
  popd
}

rm_conda_env() {
  conda info -e | grep -Eq pynemsio || return 0
  source deactivate
  conda env remove -n pynemsio -y
}

build_conda_env() {
  conda env create -n pynemsio -f pynemsio.yaml &&
  source activate pynemsio ||
  rm_conda_env
}

clean_all() {
  rm -rf src/nceplibs/build
  pushd src/nemsio_wrapper ; make clean ; popd
  rm_conda_env
}

build_all() {
  build_conda_env &&
  build_libs      &&
  make_f2py       ||
  echo "Build Failed! Consider running clean_all before trying again."
}
