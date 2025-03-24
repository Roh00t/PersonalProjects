#include <unistd.h>
int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

int	base_validation(char *str)
{
	int	i;
	int	j;

	i = 0;
	if (str[i] == '\0' || ft_strlen(str) == 1)
		return (0);
	while (str[i] != '\0')
	{
		if (str[i] <= 32 || str[i] == 127 || str[i] == 43 || str[i] == 45)
			return (0);
		j = i + 1;
		while (str[j] != '\0')
		{
			if (str[i] == str[j])
				return (0);
			j++;
		}
		i++;
	}
	return (i);
}

int	base_index(char str, char *base)
{
	int	i;

	i = 0;
	while (base[i] != '\0')
	{
		if (str == base[i])
			return (i);
		i++;
	}
	return (-1);
}

int	skip_space(char *str, int *ptr)
{
	int	count;
	int	i;

	i = 0;
	while ((str[i] >= 9 && str[i] <= 13) || str[i] == 32)
		i++;
	count = 1;
	while (str[i] && (str[i] == 43 || str[i] == 45))
	{
		if (str[i] == 45)
			count *= -1;
		i++;
	}
	*ptr = i;
	return (count);
}

int	ft_atoi_base(char *str, char *base)
{
	int	i;
	int	j;
	int	negative;
	int	nb2;

	j = 0;
	i = 0;
	if (base_validation(base))
	{
		negative = skip_space(str, &i);
		nb2 = base_index(str[i], base);
		while (nb2 != -1)
		{
			j = (j * base_validation(base)) + nb2;
			i++;
			nb2 = base_index(str[i], base);
		}
		return (j *= negative);
	}
	return (0);
}
