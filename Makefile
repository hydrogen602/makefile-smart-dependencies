CC := gcc

.PHONY: nop


all: main.o

.SECONDEXPANSION:
%.o: %.c $$(shell ./dependency.py %.c)
	@echo $@ $^

nop:
	@echo "hi"