all:
	clang -shared -Wl,-soname,_reesa.so -lgmp -fPIC -o _reesa.so -x c reesa.c
