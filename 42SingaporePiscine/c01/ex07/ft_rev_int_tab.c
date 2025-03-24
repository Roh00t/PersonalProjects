#include <unistd.h>
void	ft_swap(int *a, int *b)
{
	int	middleman;

	middleman = *a;
	*a = *b;
	*b = middleman;
}

void	ft_rev_int_tab(int *tab, int size)
{
	int	last_index;
	int	start_index;

	start_index = 0;
	last_index = size - 1;
	while (start_index < size / 2)
	{
		ft_swap(&tab[start_index], &tab[last_index - start_index]);
		start_index++;
	}
}
