#include <stdarg.h>
#include <stdio.h>

void my_printf(const char *format, ...){
	va_list args; // Used to declare a variable argument list. Declare a variable to hold the argument.
	va_start(args, format); // Initialize the variable argument list.

	for(const char *p = format; *p != '\0'; p++){
		if (*p == '%'){ 	// Check if the current characters is %
			p++;		// Move to the next character to check the format specifier.
			switch(*p){
				case 'd':{	// Handles integers
						 int num = va_arg(args, int);
						 printf("%d",num);
						 break;
					 }
				case 'c':{	// Handles Chars
						 char c = (char)va_arg(args,int); // char is promoted to int in variadic functions
						 putchar(c);
						 break;
					 }
				case 's':{	// Handles Strings
						 char *str = va_arg(args, char *);
						 printf("%s", str);
						 break;
					 }
				case 'f':{
						 // Handles Float.
						 double num = va_arg(args, double);
						 printf("%f", num); // use printf for implement manual conversion.
						 break;
					 }
				case 'x':{
						 // Handles Hexadecimal.
						 unsigned int num = va_arg(args, unsigned int);
						 char buffer[20]; //Buffer allocated to hold twenty bytes of hexadecimal string.
						 int index = 0;
						 if(num ==0){
							 buffer[index] = '0';// Handles the case where the number is 0.
						 }else{
							 while(num > 0){
								 // Convert number to decimal.
								 int digit = num % 16;
								 buffer[index++] = (digit < 10) ? (digit + '0') : (digit - 10 + 'a');
								 num /=16;
							 }
						 }
						 buffer[index] = '\0';
						 //Print buffer in reverse order (since digits were addded backwards)
						 for (int i = index - 1; i >= 0; i--){
							 putchar(buffer[i]);
						 }
						 break;
					 }

				default:{	// Handles unknown specifiers
						putchar('%');
						putchar(*p);
						break;
					}
			}
		}
			else{
				putchar(*p); // Print regular character as it is.
			}
		}
		va_end(args); 	// Clean up the variable argument list.
}
