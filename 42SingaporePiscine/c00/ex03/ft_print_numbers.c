#include <unistd.h>
void	ft_print_numbers(void)
{
	char	ascii;

	ascii = 48;
	while (ascii < 58)
	{
		write(1, &ascii, 1);
		ascii++;
	}
}