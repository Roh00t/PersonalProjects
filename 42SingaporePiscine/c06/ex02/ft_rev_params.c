#include <unistd.h>
int	main(int argc, char **argv)
{
	int	i;
	int	args;

	args = argc - 1;
	while (args > 0 && argc)
	{
		i = 0;
		while (argv[args][i])
		{
			write(1, &argv[args][i], 1);
			i++;
		}
		write(1, "\n", 1);
		args--;
	}
	return (0);
}
