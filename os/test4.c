#include<stdio.h>
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>
#define NUM 5
int main(){
	void print_msg(char *m);
	pid_t Child1;
	Child1=fork();
	if(Child1<0){
		printf("error\n");
		exit(0);
	}else if(Child1==0){
		print_msg(" Good ");
		exit(0);
	}
	pid_t Child2;
	Child2=fork();
	if(Child2<0){ 
		printf("error\n");
		exit(0);
	}else if(Child2==0){
		print_msg(" Morning ");
		exit(0);
	}
	print_msg(" 202008064710 ");
	printf("\n");
	return 0;
}
void print_msg(char *m){ 
	int i;
	for(i = 0; i<NUM; i++){
		printf("%s",m);
		fflush(stdout);
		sleep(1);
	}
}