#include <unistd.h>
void	ft_print_alphabet(void)
{
	char	ascii;

	ascii = 97;
	while (ascii < 123)
	{
		write(1, &ascii, 1);
		ascii++;
	}
}