# Name of the library to be created
NAME = libft.a

# Compiler and compiling flags
CC = cc
CFLAGS = -Wall -Wextra -Werror


# Command to remove files
RM = rm -f


# Explicitly list source files and directories
SOURCES = ./srcs/ft_putchar.c ./srcs/ft_swap.c ./srcs/ft_putstr.c ./srcs/ft_strlen.c ./srcs/ft_strcmp.c
OBJECTS = ${SOURCES:.c=.o}
HEADERS = ./includes


# Archiver and its flags for creating static library
LIBC = ar rcs
LIBR = ranlib


# Compile .c to .o, and specify header dependencies
.c.o:
	@echo "Compiling $<"
	${CC} ${CFLAGS} -I ${HEADERS} -c $< -o ${<:.c=.o}


# Rule to create the static library
${NAME}: ${OBJECTS}
			@echo "Creating library $(NAME)"
			${LIBC} ${NAME} ${OBJECTS}
			${LIBR} ${NAME}


# Default rule
all: ${NAME}


# Rule to clean object files
clean:
		@echo "Cleaning up object files"
		${RM} ${OBJECTS}


# Rule to fully clean the project
fclean: clean
		@echo "Removing library $(NAME)"
		${RM} ${NAME}


# Rule to re-make everything
re: fclean all
