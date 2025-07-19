#include <unistd.h>
void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	*ft_print_memory(void *addr, unsigned int size)
{
	unsigned int	i;
	unsigned char	*counter;
	char			*hex;

	counter = (unsigned char *)addr;
	hex = "0123456789abcdef";
	i = 0;
	while (i < size)
	{
		ft_putchar(hex[counter[i] / 16]);
		ft_putchar(hex[counter[i] % 16]);
		if ((i + 1) % 2 == 0)
			ft_putchar(' ');
		i++;
	}
	return (addr);
}