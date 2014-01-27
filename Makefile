all:
	clang -dynamiclib -o _reesa.so -lgmp reesa.c
