#include <unistd.h>
#include "rush01.h"
void	print_solution(char solution[4][4])
{
	char			c;
	unsigned int	i;
	unsigned int	j;

	i = 0;
	while (i < SIZE)
	{
		j = 0;
		while (j < SIZE)
		{
			c = solution[i][j] + '0';
			write(1, &c, 1);
			j++;
		}
		write(1, "\n", 1);
		i++;
	}
}