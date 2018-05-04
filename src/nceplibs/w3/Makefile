
include $(CONFIG)
LIB_4 = libw3_i4r4.a
LIB_8 = libw3_i4r8.a

SRCS_f := $(wildcard *.f)
SRCS_c := $(wildcard *.c)
SRCS   := $(SRCS_f) $(SRCS_c)
OBJS_4 := $(SRCS_f:.f=.o_4) $(SRCS_c:.c=.o_4)
OBJS_8 := $(patsubst %.o_4,%.o_8,$(OBJS_4))

CFLAGS += -DLINUX

.PHONY: all install uninstall

all: $(LIB_4) $(LIB_8)

install: all
	$(INSTALL) -C -m 640 $(LIB_4) $(LIBDIR)
	$(INSTALL) -C -m 640 $(LIB_8) $(LIBDIR)
	cd $(LIBDIR) && ln -sf $(LIB_8) libw3.a

uninstall:
	$(RM) $(LIBDIR)/$(LIB_4)
	$(RM) $(LIBDIR)/$(LIB_8)
	$(RM) $(LIBDIR)/libw3.a

include $(MKRULES)
