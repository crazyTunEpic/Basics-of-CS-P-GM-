all: primes

primes: primes.o
	gcc -o primes  primes.o

primes.o: primes.c
	gcc -g -O0 -c -Wall -Wextra primes.c
clean:
	rm *.o primes
indent:
	indent -kr -nut primes.c


