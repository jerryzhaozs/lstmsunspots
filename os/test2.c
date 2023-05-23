#include <unistd.h>
#include "pthread.h"
#include "stdio.h"
#include "stdlib.h"
#include "semaphore.h"
#define NUM 5
int ID[NUM]={0,1,2,3,4};
sem_t sem_chopsticks[NUM];
sem_t sem_eaters;
int eaters_num=0;
//初始化信号量
void sem_signal_init(){
	sem_init(&sem_eaters,0,NUM-1);// 吃饭人数上限设置为4人
    for (int i=0;i<NUM;i++)
        sem_init(&sem_chopsticks[i],0,1);
}
//哲学家线程
void philosopher(void * ptid){
    int pthread_id = *(int *)ptid%NUM;
    printf("哲学家%d 正在思考\n",pthread_id);
	//sem_wait(&sem_eaters);//等待吃饭人数上限
	
    // printf("哲学家%d 正在等待左筷子:%d\n",pthread_id,pthread_id);
    // sem_wait(&sem_chopsticks[pthread_id]);
    // printf("哲学家%d 正在使用左筷子:%d\n",pthread_id,pthread_id);
	// sleep(1);//在此处暂停一秒使阻塞更容易发生
    // printf("哲学家%d 正在等待右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
    // sem_wait(&sem_chopsticks[(pthread_id+1)%NUM]);
    // printf("哲学家%d 正在使用右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
	if(pthread_id&1){
		printf("哲学家%d 正在等待左筷子:%d\n",pthread_id,pthread_id);
		sem_wait(&sem_chopsticks[pthread_id]);
		printf("哲学家%d 正在使用左筷子:%d\n",pthread_id,pthread_id);
		sleep(1);//在此处暂停一秒使阻塞更容易发生
		printf("哲学家%d 正在等待右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
		sem_wait(&sem_chopsticks[(pthread_id+1)%NUM]);
		printf("哲学家%d 正在使用右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
	}else{
		printf("哲学家%d 正在等待右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
		sem_wait(&sem_chopsticks[(pthread_id+1)%NUM]);
		printf("哲学家%d 正在使用右筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
		sleep(1);//在此处暂停一秒使阻塞更容易发生
		printf("哲学家%d 正在等待左筷子:%d\n",pthread_id,pthread_id);
		sem_wait(&sem_chopsticks[pthread_id]);
		printf("哲学家%d 正在使用左筷子:%d\n",pthread_id,pthread_id);
	}
	
    printf("哲学家%d 正在吃饭，至此共有%d位哲学家完成用餐\n",pthread_id,eaters_num);
    printf("哲学家%d 释放左筷子:%d\n",pthread_id,(pthread_id+1)%NUM);
    sem_post(&sem_chopsticks[(pthread_id+1)%NUM]);
    printf("哲学家%d 释放右筷子:%d\n",pthread_id,pthread_id);
    sem_post(&sem_chopsticks[pthread_id]);
    eaters_num++;//吃过饭的人数量+1
	sem_post(&sem_eaters);//正在吃饭的人数-1
    printf("哲学家%d 已完成用餐，至此共有%d位哲学家完成用餐\n",pthread_id,eaters_num);
}
int main(){
    for (int t=0;t<10;t++){
        printf("********************** 第 %d 次尝试 ******************************\n",t+1);
        pthread_t philosopher_threads[NUM];
        sem_signal_init();//信号量初始化
        for(int i=0;i<NUM;i++)//创建哲学家线程
            pthread_create(&philosopher_threads[i],NULL,(void *)&philosopher,&ID[i]);
        for(int i=0;i<NUM;i++)//线程资源
            pthread_join(philosopher_threads[i], NULL);
        for(int i=0;i<NUM;++i)//释放信号量
            sem_destroy(&sem_chopsticks[i]);
		sem_destroy(&sem_eaters);
        eaters_num = 0;//完成用餐人数归零
    }
    return 0;
}