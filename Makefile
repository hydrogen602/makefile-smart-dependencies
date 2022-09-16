CC := gcc
EXE := main
OBJS := main.o other.o

all: $(OBJS)
	$(CC) $^ -o $(EXE)

.SECONDEXPANSION:
%.o: %.c $$(shell ./dependency.py %.c)
	@echo "dependencies:" $^ 
	$(CC) -c -o $@ $<

clean:
	rm -f *.o $(EXE)