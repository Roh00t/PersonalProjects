#include <stdio.h>

void my_printf(const char *format,...);

int main(){
	my_printf("Hello, %s!\n", "World");
	my_printf("Number: %d, Character: %c\n", 42, 'A');
	my_printf("This is %% literal percent\n");
	my_printf("This is a float: %f\n", 2322.2312123);
	my_printf("Another hex example: %x\n", 3735928559); // 0xdeadbeef
	return 0;
}

