#include <stdio.h>
#define MEM_SIZE 640  // 内存总大小，单位为 KB

typedef struct block_t {  // 内存块结构体
    int id;  // 内存块标识符
    int size;  // 内存块大小，单位为 KB
} block_t;

int next_id = 1;  // 下一个内存块的标识符
block_t mem[MEM_SIZE] = {0};  // 内存空间，初始化为 0
int num_blocks = 0;  // 已分配内存块数
// 合并相邻的空闲块
void merge_free_blocks() {
    int i, j;
    for (i = 0; i < MEM_SIZE; i++) {
        if (mem[i].id == 0) {  // 找到一个空闲块
            for (j = i + 1; j < MEM_SIZE && mem[j].id == 0; j++)
                ;
            if (j < MEM_SIZE) {  // 如果后面有非空闲块，则尝试合并
                mem[i].size += mem[j].size;
                while (j < MEM_SIZE) {
                    mem[j - 1] = mem[j];
                    j++;
                }
                mem[MEM_SIZE - 1] = (block_t){0, 0};
            }
        }
    }
}
// 显示内存情况，包括空闲和已分配的情况
void show_mem() {
    int i;
    printf("空闲分区：\n");
    for (i = 0; i < MEM_SIZE && mem[i].id == 0; i++)
        ;
    while (i < MEM_SIZE) {
        int start = i;
        while (i < MEM_SIZE && mem[i].id == 0)
            i++;
        if (start < i)
            printf("%d-%d : %d KB\n", start, i - 1, (i - start) * sizeof(block_t));
        while (i < MEM_SIZE && mem[i].id != 0)
            i++;
    }
    printf("已分配分区：\n");
    for (i = 0; i < num_blocks; i++)
        printf("%d-%d : %d KB\n", mem[i].id, mem[i].id + mem[i].size - 1, mem[i].size * sizeof(block_t));
}

// 首次适应算法分配内存
void allocate(int id, int size) {
    int i;
    for (i = 0; i < MEM_SIZE; i++) {
        if (mem[i].id == 0 && mem[i].size >= size) {  // 找到第一个空闲块
            if (mem[i].size > size) {  // 分割内存块
                block_t new_block = {next_id++, size};
                int j;
                for (j = MEM_SIZE - 1; j > i; j--) {
                    mem[j] = mem[j - 1];
                }
                mem[i] = new_block;
                mem[i + size] = (block_t){0, mem[i].size - size};
            } else {  // 直接使用整个空闲块
                mem[i] = (block_t){next_id++, mem[i].size};
            }
            num_blocks++;
            printf("作业 %d 分配了 %d KB 的内存\n", id, size);
            show_mem();
            merge_free_blocks();
            break;
        }
    }
    if (i == MEM_SIZE) {
        printf("作业 %d 分配内存失败，没有足够的空闲空间\n", id);
    }
}

// 找到内存块 id 对应的位置
int find_index(int id) {
    int i;
    for (i = 0; i < num_blocks; i++)
        if (mem[i].id == id)
            return i;
    return -1;
}



// 释放内存
void deallocate(int id) {
    int i = find_index(id);
    if (i == -1) {
        printf("内存块 %d 不存在\n", id);
    } else {
        mem[i].id = 0;
        num_blocks--;
        merge_free_blocks();
        printf("作业 %d 释放了 %d KB 的内存\n", id, mem[i].size);
        show_mem();
    }
}

int main() {
    show_mem();
    allocate(1, 130);
    allocate(2, 60);
    allocate(3, 100);
    deallocate(2);
    deallocate(3);
    deallocate(1);
    return 0;
}