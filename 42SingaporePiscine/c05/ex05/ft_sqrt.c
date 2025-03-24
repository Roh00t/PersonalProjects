#include <unistd.h>
int	ft_sqrt(int nb)
{
	int	counter;
	int	number;

	number = nb;
	if (number <= 0)
		return (0);
	if (number == 1)
		return (1);
	counter = 2;
	if (number >= 2)
	{
		while (counter * counter <= number)
		{
			if (counter * counter == number)
				return (counter);
			counter++;
		}
	}
	return (0);
}
