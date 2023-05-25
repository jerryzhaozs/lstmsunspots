#include <stdio.h>
#include <stdlib.h>

#define MEMORY_SIZE 640 // 内存大小为640KB
#define MIN_BLOCK_SIZE 4 // 最小块大小为4KB

// 内存块结构体
typedef struct block {
    int start_addr; // 起始地址
    int size; // 大小
    int is_free; // 是否空闲
    struct block* next; // 下一个块
} Block;

Block* head = NULL; // 内存块链表头指针

/**
 * 初始化内存块链表
 */
void init_memory() {
    head = (Block*)malloc(sizeof(Block));
    head->start_addr = 0;
    head->size = MEMORY_SIZE;
    head->is_free = 1;
    head->next = NULL;
}

/**
 * 显示内存块信息
 */
void show_memory() {
    printf("Memory status:\n");
    Block* p = head;
    while (p != NULL) {
        printf("[%dKB, %dKB) %s\n", p->start_addr, p->start_addr + p->size, p->is_free ? "Free" : "Allocated");
        p = p->next;
    }
    printf("\n");
}

/**
 * 分配内存块
 * @param size 要分配的大小
 * @return 分配的内存块起始地址，如果分配失败则返回-1
 */
int allocate_memory(int size) {
    // 计算需要分配的块大小
    int block_size = ((size - 1) / MIN_BLOCK_SIZE + 1) * MIN_BLOCK_SIZE;
    // 遍历内存块链表，找到第一个空闲的块并且大小大于等于要分配的块
    Block* p = head;
    while (p != NULL && (!p->is_free || p->size < block_size)) {
        p = p->next;
    }
    if (p == NULL) { // 没有找到可用块
        return -1;
    }
    if (p->size > block_size) { // 如果找到的块比需要的块大，则拆分成两个块
        Block* new_block = (Block*)malloc(sizeof(Block));
        new_block->start_addr = p->start_addr + block_size;
        new_block->size = p->size - block_size;
        new_block->is_free = 1;
        new_block->next = p->next;
        p->next = new_block;
        p->size = block_size;
    }
    p->is_free = 0; // 标记为已分配
    return p->start_addr;
}

/**
 * 回收内存块
 * @param start_addr 要回收的内存块起始地址
 */
// void free_memory(int start_addr) {
    // /*遍历内存块链表，找到要回收的块*/
    // Block* p = head;
    // while (p != NULL && p->start_addr != start_addr) {
        // p = p->next;
    // }
    // if (p == NULL) { // 没有找到要回收的块
        // return;
    // }
    // p->is_free = 1; // 标记为空闲
    // /*尝试和相邻的空闲块合并*/
    // while (p->next != NULL && p->next->is_free) {
		// printf("United foreward!");
        // Block* next_block = p->next;
        // p->size += next_block->size;
        // p->next = next_block->next;
        // free(next_block);
    // }
    // while (p != head && p->is_free && p->next != NULL && p->next->is_free) {
		// printf("United backward!");
        // Block* prev_block = head;
        // while (prev_block->next != p) {
            // prev_block = prev_block->next;
        // }
        // Block* next_block = p->next;
        // prev_block->size += p->size + next_block->size;
        // prev_block->next = next_block->next;
        // free(p);
        // free(next_block);
        // p = prev_block;
    // }
// }
void free_memory(int start_addr) {
// 遍历内存块链表，找到要回收的块
Block* p = head;
while (p != NULL && p->start_addr != start_addr) {
p = p->next;
}
if (p == NULL) { // 没有找到要回收的块
return;
}
p->is_free = 1; // 标记为空闲

// 尝试和相邻的空闲块合并
Block* prev_block = NULL;
Block* next_block = NULL; 
while (p->next != NULL && p->next->is_free) {
    printf("United forward!\n");
    next_block = p->next;
    p->size += next_block->size;
    p->next = next_block->next;
    free(next_block);
}
prev_block = p;
p = p->next;
while (p != NULL && p->is_free) {
    printf("United backward!\n");
    prev_block->size += p->size;
    prev_block->next = p->next;
    free(p);
    p = prev_block->next;
}
if (prev_block->next != NULL && prev_block->next->is_free) {
    prev_block->size += prev_block->next->size;
    Block* temp = prev_block->next;
    prev_block->next = temp->next;
    free(temp);
}
}
int main() {
    init_memory();
    show_memory();

    int addr1= allocate_memory(130);
	if (addr1 == -1) {
	printf("Allocate memory failed\n");
	} else {
	printf("Allocate 130KB memory at %dKB\n", addr1);
	}
	show_memory();

	int addr2 = allocate_memory(60);
	if (addr2 == -1) {
		printf("Allocate memory failed\n");
	} else {
		printf("Allocate 60KB memory at %dKB\n", addr2);
	}
	show_memory();

	int addr3 = allocate_memory(100);
	if (addr3 == -1) {
		printf("Allocate memory failed\n");
	} else {
		printf("Allocate 100KB memory at %dKB\n", addr3);
	}
	show_memory();

	free_memory(addr2);
	printf("Free memory at %dKB\n", addr2);
	show_memory();

	free_memory(addr3);
	printf("Free memory at %dKB\n", addr3);
	show_memory();
	
	free_memory(addr1);
	printf("Free memory at %dKB\n", addr1);
	show_memory();

	return 0;
}