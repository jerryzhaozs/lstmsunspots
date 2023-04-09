#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>
int main(){
	pid_t Child1;
	Child1=fork();
	if(Child1<0){
		printf("Child1 error\n");
		exit(0);
	}else if(Child1==0){
		printf("Child1 process ");
		printf("PID:%d PPID:%d\n",getpid(),getppid());
		exit(0);
	}else{
		pid_t Child2;
		Child2=fork();
		if(Child2<0){
			printf("Child2 error\n");
			exit(0);
		}else if(Child2==0){
			printf("Child2 process ");
			printf("PID:%d PPID:%d\n",getpid(),getppid());
			exit(0);
		}else{
			printf("Parent process ");
			printf("PID:%d PPID:%d\n",getpid(),getppid());
			exit(0);
		}
	}
	return 0;
}
