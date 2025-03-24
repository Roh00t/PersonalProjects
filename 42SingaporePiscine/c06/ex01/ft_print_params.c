#include <unistd.h>
int	main(int argc, char **argv)
{
	char	**arg_ptr;
	char	*name;

	arg_ptr = ++argv;
	while (*arg_ptr && argc)
	{
		name = *arg_ptr;
		while (*name)
		{
			write (1, name, 1);
			name++;
		}
		write (1, "\n", 1);
		arg_ptr++;
	}
	return (0);
}
