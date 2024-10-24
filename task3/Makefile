lychrel: lychrel.o
	gcc -o lychrel  lychrel.o

lychrel.o: lychrel.c
	gcc -g -O0 -c -Wall -Wextra -std=c99  lychrel.c

clean:
	rm lychrel lychrel.o

indent:
	indent -kr -nut lychrel.c

