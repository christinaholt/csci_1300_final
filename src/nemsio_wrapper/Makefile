
W3_DIR      = ../nceplibs/build/w3/
BACIO_DIR   = ../nceplibs/build/bacio/
NEMSIO_DIR  = ../nceplibs/build/nemsio/


.PHONY: all build

all: build

build:
	f2py -c nemsio_wrapper.f90  -m nemsio_wrapper --verbose -I${NEMSIO_DIR} -L${W3_DIR} -L${BACIO_DIR} -L${NEMSIO_DIR} -lbacio -lw3 -lnemsio

clean:
	rm -rf nemsio_wrapper.so


