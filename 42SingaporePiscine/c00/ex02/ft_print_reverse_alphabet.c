#include <unistd.h>
void	ft_print_reverse_alphabet(void)
{
	char	ascii;

	ascii = 122;
	while (ascii > 96)
	{
		write(1, &ascii, 1);
		ascii--;
	}
}