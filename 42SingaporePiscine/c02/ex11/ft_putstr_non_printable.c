#include <unistd.h>
void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_putstr_non_printable(char *str)
{
	char	*counter;
	char	*hex;

	hex = "0123456789abcdef";
	counter = (char *)str;
	while (*counter != '\0')
	{
		if (*counter >= ' ' && *counter <= '~')
			write(1, counter, 1);
		else
		{
			ft_putchar('\\');
			ft_putchar(hex[*counter / 16]);
			ft_putchar(hex[*counter % 16]);
		}
		counter++;
	}
}
