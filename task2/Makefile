main: main.o
	gcc -o main main.o

main.o: main.c
	gcc -g -O0 -c -Wall -Wextra main.c
clean:
	rm task4 *.o
indent:
	indent -kr -nut main.c
