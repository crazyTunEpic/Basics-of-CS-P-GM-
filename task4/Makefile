CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: primes

primes: primes.o goldbach.o
	$(CC) $(CFLAGS) -o primes primes.o goldbach.o

goldbach.o: goldbach.c
	$(CC) $(CFLAGS) -c goldbach.c

primes.o: primes.c
	$(CC) $(CFLAGS) -c primes.c

clean:
	rm -f *.o primes
