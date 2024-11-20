CC = gcc
CFLAGS = -g -Wall -I./rational
RATIONAL_DIR = rational
LIBRARY = librational.a

all: calc

# Сборка исполняемого файла calc
calc: calc.o $(RATIONAL_DIR)/$(LIBRARY)
	$(CC) -o calc calc.o -L$(RATIONAL_DIR) -l rational

# Сборка объектного файла для calc
calc.o: calc.c
	$(CC) $(CFLAGS) -c calc.c

# Сборка библиотеки librational
$(RATIONAL_DIR)/$(LIBRARY):
	make -C $(RATIONAL_DIR)

clean:
	rm -f *.o calc
	make -C $(RATIONAL_DIR) clean
