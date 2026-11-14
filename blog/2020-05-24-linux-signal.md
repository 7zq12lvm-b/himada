---
title: "一个Linux上关于Signal的小问题"
authors: [mingqiang]
tags: ["旧站归档"]
---

这篇文章最初发表于 2020-05-24，现从旧站迁入。

<!-- truncate -->

最近的Linux课程中遇到了一个小问题，昨天询问了老师，老师暂未回复，不过我查找资料后似乎找到了答案。

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-1024x580.png)

代码如下：

```text
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>
#include<signal.h>
int main()
{
        pid_t pid=fork();
        if(pid>0){

                printf("Im parent\n");
                printf("dying....\n") ;
                sleep(5);
                printf("parent died\n");

        }else{
                while(1){
                  printf("Im child\n");
                  sleep(1);
                }
        }
        return 0;
}
```

首先解释第一个问题，看kill -2和Ctrl+C 的区别：

> **Ctrl-C** on the other hand sends the signal to **more than one process**: all sub processes of the foreground process are also notified (except background processes). That is the important difference between these two approaches.

> https://ajhaupt.blogspot.com/2011/01/whats-difference-between-ctrl-c-and.html

Ctrl+C会给当前进程组内所有进程发送SIGINT信号，实际编程测试也是如此。

测试代码：

```text
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>
#include<signal.h>
void catch(int sig)
{
        printf("%d sig received\n",sig);
}
int main()
{
        pid_t pid=fork();
        if(pid>0){
                printf("Im parent\n");
                printf("dying....\n") ;
                signal(SIGINT,catch);
                while(1);
                printf("parent died\n");

        }else{
                signal(SIGINT,catch);
                while(1);
        }
        return 0;
}
```

可以看到，按下一次Ctrl+C后，控制台打印了两条received信息，也就是说父子进程都收到了SIGINT信号。 而kill -2 进程ID 只会杀死对应的进程。

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-1.png)

然后是第二个问题，为什么在前五秒父子进程均存活时，Ctrl+C可以同时杀死父子进程，而父进程结束后，Ctrl+C却无法杀死子进程了呢？

这是因为父进程退出后，子进程被init领养，变成了后台进程，也就是前台tty不再属于子进程。这可以从ps aux 中STAT一列中得知。

```text
使用ps命令查看进程的当前状态，其中STAT列的含义如下：

    D 不可中断的休眠。通常是IO。
    R 运行。正在运行或者在运行队列中等待。
    S 休眠。在等待某个事件，信号。
    T 停止。进程接收到信息SIGSTOP，SIGSTP，SIGTIN，SIGTOU信号。
    W paging，在2.6之后不用。
    X 死掉的进程，不应该出现。
    Z 僵死进程。

通常还会跟随如下字母表示更详细的状态。

    < 高优先级
    N 低优先级
    L 有pages在内存中locked。用于实时或者自定义IO。
    s 进程领导者，其有子进程。
    l 多线程
    + 位于前台进程组。
```

在前5秒，父进程未结束时，此时ps aux 状态：

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-4.png)

可以看到./a.out状态均为S+，也就是属于休眠中的前台进程，此时在原控制台按Ctrl+C父子进程正常结束。

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-2.png)

当父进程结束后，可以看到控制台重新出现了一次主机名，这是bash抢占了子进程的表现：

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-5.png)

此时./a.out的STAT为S，变成了后台休眠，当然Ctrl+C就无法将信号直接送达，此时相当于对bash按Ctrl+C，无任何效果。

![](/img/wordpress-archive/2020/05/%E5%9B%BE%E7%89%87-6.png)
