include ${BUILD_DIR}/configure.external
LIB = $(LIBDIR)/libbacio.a
INC = clib.h

OBJS = baciof.o bafrio.o chk_endianc.o
COBJS = byteswap.o bacio.o

$(LIB): $(OBJS) $(COBJS)
	$(AR) -ruv $(ARFLAGS_BACIO) $(LIB) $@ $^
	$(CP) *.mod $(INCMOD)

$(COBJS): %.o: $(INC)

  MAKE_DEPEND = Makefile.dependency
include $(MAKE_DEPEND)

%.o: %.f
	$(SFC) -c $(FFLAGS_BACIO) $*.f

%.o: %.c
	$(SCC) -c $(CFLAGS2) $*.c

clean:
	$(RM) baciof.o bafrio.o $(LIB) bacio.o byteswap.o chk_endianc.o *.mod $(INCMOD)/bacio_module.mod

