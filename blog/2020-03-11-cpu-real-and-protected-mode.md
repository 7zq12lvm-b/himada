---
title: "关于保护模式和实模式"
authors: [mingqiang]
tags: ["旧站归档"]
---

这篇文章最初发表于 2020-03-11，现从旧站迁入。

<!-- truncate -->

刚才纠结，如果在实模式下dos拥有主机的完全控制权限，可以操作真正的寄存器和内存，那不就是会影响到其他程序的运行吗？然后再想到什么操作系统内存分页机制给了每一个进程一个独立的地址空间，就认为windows下debug是虚拟出的地址空间和寄存器，我们操作的并不是真正的元器件。然后.....就感觉这块好乱。查了些资料算是弄清楚了：

> Real mode, also called real address mode, is an operating mode of all x86-compatible CPUs. The mode gets its name from the fact that addresses in real mode always correspond to real locations in memory. Real mode is characterized by a 20-bit segmented memory address space (giving exactly 1 MiB of addressable memory) and unlimited direct software access to all addressable memory, I/O addresses and peripheral hardware. Real mode provides no support for memory protection, multitasking, or code privilege levels.\[1\]

也即是说实模式下程序拥有对全部内存空间的直接访问能力。80286以前的CPU只支持实模式运行。1982年Intel发布了80286 CPU引入了保护模式的概念，实现保护地址空间的功能需要操作系统的协作，为了兼容以前的操作系统，286以后的CPU也支持以实模式启动，也就是说今天的酷睿i7装上1985年的dos系统仍然可以完美运行，不需要模拟。BIOS引导程序就是工作在实模式下。

Windows/386，发布于1988年，开始初步支持保护模式运行。而后在Windows3.0中完全实现了保护模式，Windows3.0同时有三种模式： "real mode", "standard mode" and "386-enhanced mode"，Windows3.1取消了纯实模式的支持，但是这些系统以及以后的Win95都不被看做完全意义上的现代X86系统，因为它们只在实现特定功能才转换到保护模式，而Unix、Linux、OS/2、Windows NT 3.x以后的操作系统在启动后立即切换到保护模式并不再换回实模式，所以被认为是现代操作系统。

而为了兼容以前dos系统下以实模式运行的程序，引入了虚拟8086实模式的概念:

> The third mode of processor operation is actually an additional capability, an enhancement, of protected mode. Protected mode is normally used to run graphical multitasking operating systems such as the various flavors of Windows. **There is often a desire to be able to run DOS programs under Windows, but DOS programs need to be run in real mode, not protected mode.**

> Virtual real mode was created to solve this problem. In essence, it emulates real mode from within protected mode, allowing DOS programs to run. A protected mode operating system such as Windows can in fact create multiple virtual real mode machines, each of which appear to the software running them as if they are the only software running on the machine. Each virtual machine gets its own 1 MB address space, an image of the real hardware BIOS routines, everything.

> **Virtual real mode is what is used when you use a DOS box or run a DOS game in Windows 95. When you start a DOS application, Windows 95 creates a virtual DOS machine for it to run under. Virtual real mode was introduced starting with the 386 family of processors.\[2\]**

DOS，或者说MS-DOS系统，发布于1981年，最后支持到2000年。当它作为主操作系统(而不是虚拟机)运行时，是运行在CPU的实模式下，它是一个单任务操作系统，没有对多进程的内存保护，也就不支持多进程，所以没有内存分页这样的技术（分页，segmentation，是保护模式的操作系统才有的技术，由80386CPU引入），支持20位的地址总线，寻址空间1MB，其中只有0-640K是给程序运行用的，其他地址空间用于其他功能。DOS中的debug也就是运行在实模式下，可以访问全部地址空间，由于是单进程的操作系统，也就没有“访问到其他程序的地址空间导致该程序崩溃”的问题存在。而Windows XP中的debug是运行在“虚拟8086实模式”下的。

> VM86 mode uses a segmentation scheme identical to that of real mode (for compatibility reasons) which creates 20-bit linear addresses in the same manner as 20-bit physical addresses are created in real mode, **but are subject to protected mode's memory paging mechanism.\[3\]**

也就是说，虚拟8086实模式为dos程序虚拟了一个1MB的地址空间，之后仍然服从分页机制，分页对于该DOS程序是透明的，在其看来，这1MB的地址空间就是连续的。\[4.无关：惊讶地发现ms dos竟然被微软开源了，全是汇编看不懂但还是感觉很牛逼\]

1.[https://en.wikipedia.org/wiki/Real\_mode](https://en.wikipedia.org/wiki/Real_mode)

2.[https://www.cs.yale.edu/flint/feng/research/BIOS/procModes.htm](https://www.cs.yale.edu/flint/feng/research/BIOS/procModes.htm)

3.[https://en.wikipedia.org/wiki/Virtual\_8086\_mode](https://en.wikipedia.org/wiki/Virtual_8086_mode)

4.[https://github.com/microsoft/MS-DOS](https://github.com/microsoft/MS-DOS)

[https://www.quora.co/What-are-CPU-real-mode-and-protected-mode](https://www.quora.co/What-are-CPU-real-mode-and-protected-mode)
