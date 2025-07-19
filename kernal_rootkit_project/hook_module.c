#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/syscalls.h>
#include <asm/paravirt.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("System Call Hooking Module");

unsigned long **sys_call_table;

asmlinkage long (*original_sys_open)(const char __user *, int, umode_t);

asmlinkage long hooked_sys_open(const char __user *filename, int flags, umode_t mode) {
    printk(KERN_INFO "Intercepted open: %s\n", filename);
    return original_sys_open(filename, flags, mode);
}

static int __init hook_module_init(void) {
    sys_call_table = (unsigned long **)kallsyms_lookup_name("sys_call_table");

    write_cr0(read_cr0() & (~0x10000)); // Disable write protection
    original_sys_open = (void *)sys_call_table[__NR_open];
    sys_call_table[__NR_open] = (unsigned long *)hooked_sys_open;
    write_cr0(read_cr0() | 0x10000);  // Enable write protection

    printk(KERN_INFO "Hook Module Loaded\n");
    return 0;
}

static void __exit hook_module_exit(void) {
    write_cr0(read_cr0() & (~0x10000)); // Disable write protection
    sys_call_table[__NR_open] = (unsigned long *)original_sys_open;
    write_cr0(read_cr0() | 0x10000);  // Enable write protection

    printk(KERN_INFO "Hook Module Unloaded\n");
}

module_init(hook_module_init);
module_exit(hook_module_exit);

