CC = gcc
CFLAGS = -Wall -Wextra

all: primes goldbach

primes: primes.o calculate_primes.o
	$(CC) $(CFLAGS) -o primes primes.o calculate_primes.o

goldbach: goldbach.o calculate_primes.o
	$(CC) $(CFLAGS) -o goldbach goldbach.o calculate_primes.o

%.o: %.c calculate_primes.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.o primes goldbach
