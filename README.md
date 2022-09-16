# Determining Dependencies in Make rules automatically and intelligently

When using general makefile rules, often all headers need to be added as a dependency to the rule, and thus a single header file change will trigger a full rebuild - even if the header is only used in a few files. The usual way around this is to have CMAKE generate the makefile or to handwrite a rule for every file specifically, but both those solutions are painful. 
```Make
%.o: %.c $(ALL_HEADERS)
	@echo "dependencies:" $^ 
	$(CC) -c -o $@ $<
```

However, GNU makefiles have a feature that allow passing variables like `$@` and `%.c` into a shell script which can then determine the dependencies. This is called second expansion and allows make to compute dependencies for each files automatically.

```Make
.SECONDEXPANSION:
%.o: %.c $$(shell ./dependency.py %.c)
	@echo "dependencies:" $^ 
	$(CC) -c -o $@ $<
```

`dependency.py` is just a simple script that uses regex to recursively search for includes using quotes (`"`) in each `%.c` file.

Makefile output

```
dependencies: main.c main.h extra.h base.h other.h
gcc -c -o main.o main.c
dependencies: other.c other.h
gcc -c -o other.o other.c
gcc main.o other.o -o main
```
Notice that the dependencies are only those used by the specific C source file.

## Notes

Secondary expansion is a GNU make specific feature. While the example is for C files, this can easily be extending for C++ or anything else where the dependencies can be computed from the source file.
