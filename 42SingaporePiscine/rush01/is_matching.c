#include "rush01.h"

int	is_matching(char boundary[4][4], char u_bound[4][4])
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	while (i < SIZE)
	{
		j = 0;
		while (j < SIZE)
		{
			if (boundary[i][j] != u_bound[i][j])
				return (0);
			j++;
		}
		i++;
	}
	return (1);
}
