#include<stdio.h>
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>
int main(){
	pid_t Child1;
	Child1=fork();
	if(Child1<0){
		printf("error\n");
		exit(0);
	}else if(Child1==0){
		printf("Child1 process!\n");
		printf("PID=%d PPID=%d\n",getpid(),getppid()); 
		exit(0);
	}else{
		pid_t Child2;
		Child2=fork();
		if(Child2<0){ 
			printf("error\n");
			exit(0);
		}else if(Child2==0){
			printf("Child2 process!\n");
			printf("PID=%d PPID=%d\n",getpid(),getppid()); 
			exit(0);
		}else{
			wait(0);
			printf("Parent process!\n");
			printf("PID=%d PPID=%d\n",getpid(),getppid()); 
			exit(0);
		}
	}
	return 0;
}