# makefile

# compiler and flags
CXX = gcc
FLAGS = -Wall -std=c99 -O3 -shared

A1.so: A1.c A1.h
	${CXX} ${FLAGS} -Wl,-install_name,A1.so -o A1.so -fPIC A1.c

# make executable
#nbodysim: nbodysim.o energy.o
#	${CXX} ${FLAGS} -o nbodysim nbodysim.o energy.o

# make object files
#nbodysim.o: nbodysim.c
#	${CXX} ${FLAGS} nbodysim.c -c -o nbodysim.o

#energy.o: energy.c energy.h
#	${CXX} ${FLAGS} energy.c -c -o energy.o

# delete .so files
clean:
	rm -f *.so
