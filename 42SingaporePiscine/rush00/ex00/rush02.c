void	ft_putchar(char c);
void	draw_line(int length, char first_character,
	char second_character, char third_character)
{
	int	column_index;

	column_index = 0;
	while (column_index < length)
	{
		if (column_index == 0)
			ft_putchar(first_character);
		else if (column_index == length - 1)
			ft_putchar(third_character);
		else
			ft_putchar(second_character);
		column_index++;
	}
	ft_putchar('\n');
}
void	rush(int y, int x)
{
	int	row_index;

	row_index = 0;
	if (y <= 0 || x <= 0)
		return ;
	while (row_index < x)
	{
		if (row_index == 0)
			draw_line(y, 'A', 'B', 'A');
		else if (row_index == x - 1)
			draw_line(y, 'C', 'B', 'C');
		else
			draw_line(y, 'B', ' ', 'B');
		row_index++;
	}
}
