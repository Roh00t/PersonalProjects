#include <unistd.h>
void	ft_swap(int *a, int *b)
{
	int	middleman;

	middleman = *a;
	*a = *b;
	*b = middleman;
}

void	ft_sort_int_tab(int *tab, int size)
{
	int	start_index;
	int	last_index;
	int	counter;

	counter = size;
	last_index = size - 1;
	while (counter > 0)
	{
		start_index = 0;
		while (start_index < last_index)
		{
			if (tab[start_index] > tab[start_index + 1])
			{
				ft_swap(&tab[start_index], &tab[start_index + 1]);
			}
			start_index++;
		}
		counter--;
	}	
}
