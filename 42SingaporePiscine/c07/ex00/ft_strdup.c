#include <stdlib.h>

char	*ft_strdup(char *src)
{
	int		src_len;
	int		i;
	char	*dest;

	src_len = 0;
	while (src[src_len] != '\0')
		src_len++;
	dest = (char *)malloc(sizeof(char) * (src_len + 1));
	if (dest == NULL)
		return (NULL);
	i = 0;
	while (src[i] != '\0')
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
