SHELL=/bin/sh
include ${BUILD_DIR}/configure.external
LIB     = $(LIBDIR)/libnemsio.a

OBJ  = nemsio_openclose.o nemsio_read.o nemsio_write.o nemsio_module.o nemsio_module_mpi.o

$(LIB): $(OBJ)
	$(AR) -ruv $(ARFLAGS_NEMSIO) $@ $(OBJ)
	$(CP) *.mod $(INCMOD)

  MAKE_DEPEND = Makefile.dependency
include $(MAKE_DEPEND)

.SUFFIXES: .f90 .o

.f90.o:
	$(DM_F90) $(FFLAGS_NEMSIO) -c $*.f90

nemsio_read.o: nemsio_openclose.o
nemsio_write.o: nemsio_openclose.o
nemio_module.o: nemsio_openclose.o nemsio_read.o nemsio_write.o
nemsio_module_mpi.o: nemsio_openclose.o nemsio_read.o nemsio_write.o

clean:
	rm -f *.o *.mod $(INCMOD)/nemsio_*.mod $(LIB)
	
