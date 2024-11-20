CC = gcc
CFLAGS = -g -Wall -fPIC

OBJS = rational.o rat_math.o rat_io.o

.PHONY: all clean

all: librational.a

librational.a: $(OBJS)
	ar -rcs librational.a $(OBJS)

clean:
	rm -f $(OBJS) librational.a
