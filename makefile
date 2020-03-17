# makefile

# compiler and flags
CXX = gcc
FLAGS = -Wall -std=c99 -O3

# make executable
nbodysim: nbodysim.o energy.o
	${CXX} ${FLAGS} -o nbodysim nbodysim.o energy.o

# make object files
nbodysim.o: nbodysim.c
	${CXX} ${FLAGS} nbodysim.c -c -o nbodysim.o

energy.o: energy.c energy.h
	${CXX} ${FLAGS} energy.c -c -o energy.o

# delete object files and executable
clean:
	rm -f *.o nbodysim
