#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("A Simple Kernel Module Example");

static int __init simple_module_init(void) {
    printk(KERN_INFO "Simple Module Loaded\n");
    return 0;
}

static void __exit simple_module_exit(void) {
    printk(KERN_INFO "Simple Module Unloaded\n");
}

module_init(simple_module_init);
module_exit(simple_module_exit);

