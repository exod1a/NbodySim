# makefile

# compiler and flags
CXX = gcc
FLAGS = -Wall -std=c99 -O3 -shared

all: A1.so A2.so

A1.so: A1.c A1.h 
	${CXX} ${FLAGS} -Wl,-install_name,A1.so -o A1.so -fPIC A1.c

A2.so: A2.c A2.h
	${CXX} ${FLAGS} -WL,-install_name,A2.so -o A2.so -fPIC A2.c

# delete .so and .pyc files
clean:
	rm -f *.so *.pyc
