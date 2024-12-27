# Name of the module
obj-m := rootkit_module.o

# Kernel build directory
KDIR := /lib/modules/$(shell uname -r)/build

# Current directory
PWD := $(shell pwd)

# Default target: build the module
all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

# Clean target: remove generated files
clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
