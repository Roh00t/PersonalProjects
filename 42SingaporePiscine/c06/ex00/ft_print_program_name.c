#include <unistd.h>
int	main(int argc, char **argv)
{
	char	*name;

	name = argv[0];
	while (*name && argc)
	{
		write (1, name, 1);
		name++;
	}
	write (1, "\n", 1);
	return (0);
}
