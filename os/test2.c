#include <stdio.h>
#define NUM 5
int main(void){
	void print_msg(char *m);
	print_msg("Good ");
	print_msg("Morning  ");
	print_msg("007\n");  //将007替换为本人学号
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