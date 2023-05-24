#include <stdio.h>
#define MEM_SIZE 640  // �ڴ��ܴ�С����λΪ KB

typedef struct block_t {  // �ڴ��ṹ��
    int id;  // �ڴ���ʶ��
    int size;  // �ڴ���С����λΪ KB
} block_t;

int next_id = 1;  // ��һ���ڴ��ı�ʶ��
block_t mem[MEM_SIZE] = {0};  // �ڴ�ռ䣬��ʼ��Ϊ 0
int num_blocks = 0;  // �ѷ����ڴ����
// �ϲ����ڵĿ��п�
void merge_free_blocks() {
    int i, j;
    for (i = 0; i < MEM_SIZE; i++) {
        if (mem[i].id == 0) {  // �ҵ�һ�����п�
            for (j = i + 1; j < MEM_SIZE && mem[j].id == 0; j++)
                ;
            if (j < MEM_SIZE) {  // ��������зǿ��п飬���Ժϲ�
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
// ��ʾ�ڴ�������������к��ѷ�������
void show_mem() {
    int i;
    printf("���з�����\n");
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
    printf("�ѷ��������\n");
    for (i = 0; i < num_blocks; i++)
        printf("%d-%d : %d KB\n", mem[i].id, mem[i].id + mem[i].size - 1, mem[i].size * sizeof(block_t));
}

// �״���Ӧ�㷨�����ڴ�
void allocate(int id, int size) {
    int i;
    for (i = 0; i < MEM_SIZE; i++) {
        if (mem[i].id == 0 && mem[i].size >= size) {  // �ҵ���һ�����п�
            if (mem[i].size > size) {  // �ָ��ڴ��
                block_t new_block = {next_id++, size};
                int j;
                for (j = MEM_SIZE - 1; j > i; j--) {
                    mem[j] = mem[j - 1];
                }
                mem[i] = new_block;
                mem[i + size] = (block_t){0, mem[i].size - size};
            } else {  // ֱ��ʹ���������п�
                mem[i] = (block_t){next_id++, mem[i].size};
            }
            num_blocks++;
            printf("��ҵ %d ������ %d KB ���ڴ�\n", id, size);
            show_mem();
            merge_free_blocks();
            break;
        }
    }
    if (i == MEM_SIZE) {
        printf("��ҵ %d �����ڴ�ʧ�ܣ�û���㹻�Ŀ��пռ�\n", id);
    }
}

// �ҵ��ڴ�� id ��Ӧ��λ��
int find_index(int id) {
    int i;
    for (i = 0; i < num_blocks; i++)
        if (mem[i].id == id)
            return i;
    return -1;
}



// �ͷ��ڴ�
void deallocate(int id) {
    int i = find_index(id);
    if (i == -1) {
        printf("�ڴ�� %d ������\n", id);
    } else {
        mem[i].id = 0;
        num_blocks--;
        merge_free_blocks();
        printf("��ҵ %d �ͷ��� %d KB ���ڴ�\n", id, mem[i].size);
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