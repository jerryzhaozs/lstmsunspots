#include <iostream>
using namespace std;
 
#define FREE 0
#define BUSY 1
#define MAX_length 640
 
typedef struct freeArea {
    int flag;
    int size;
    int ID;
    int address;
} Elemtype;
 
typedef struct Free_Node {
    Elemtype date;
    struct Free_Node *front;
    struct Free_Node *next;
} Free_Node, *FNodeList;

FNodeList block_first, block_last;

void init() {
    block_first = new Free_Node;
    block_last = new Free_Node;
    block_first->front = NULL;
    block_first->next = block_last;
    block_last->front = block_first;
    block_last->next = NULL;
    block_last->date.address = 0;
    block_last->date.flag = FREE;
    block_last->date.ID = FREE;
    block_last->date.size = MAX_length;
}

int alloc(int tag) {
    int ID, size1;
    cout << "��������ҵ�ţ�";
    cin >> ID;
    cout << "�����������ڴ��С��";
    cin >> size1;
    if (ID <= 0 || size1 <= 0) {
        cout << "ERROR,��������ȷ��ID�������С" << endl;
        return 0;
    }
    FNodeList temp = (FNodeList)malloc(sizeof(Free_Node));
    temp->date.ID = ID;
    temp->date.size = size1;
    temp->date.flag = BUSY;
    FNodeList p = block_first->next;
    while (p) {
        if (p->date.flag == FREE && p->date.size >= size1) {
            if (p->date.size == size1) {
                p->date.flag = BUSY;
                p->date.ID = ID;
                return 1;
            } else {
                temp->next = p;
                temp->front = p->front;
                temp->date.address = p->date.address;
                p->front->next = temp;
                p->front = temp;
                p->date.size -= size1;
                p->date.address += size1;
                return 1;
            }
        }
        p = p->next;
    }
    return 0;
}

int alloc2(int tag) {
	int ID, size1;
	cout << "��������ҵ�ţ�";
	cin >> ID;
	cout << "�����������ڴ��С��";
	cin >> size1;
	if (ID <= 0 || size1 <= 0) {
		cout << "ERROR,��������ȷ��ID�������С" << endl;
		return 0;
	}
	FNodeList temp = (FNodeList)malloc(sizeof(Free_Node));
	temp->date.ID = ID;
	temp->date.size = size1;
	temp->date.flag = BUSY;
	FNodeList p = block_first->next;
	FNodeList best_fit = NULL; // ��С�ʺϿ�ָ��
	while (p) {
		if (p->date.flag == FREE && p->date.size >= size1) {
			if (!best_fit || p->date.size < best_fit->date.size) { // ������С�ʺϿ�ָ��
				best_fit = p;
			}
		}
		p = p->next;
	}
	if (best_fit) {
		if (best_fit->date.size == size1) {
			best_fit->date.flag = BUSY;
			best_fit->date.ID = ID;
			return 1;
		} else {
			temp->date.address = best_fit->date.address;
			temp->next = best_fit;
			temp->front = best_fit->front;
			best_fit->front->next = temp;
			best_fit->front = temp;
			best_fit->date.size -= size1;
			best_fit->date.address += size1;
			return 1;
		}
	}
	return 0;
}

int free(int ID) {
    FNodeList p = block_first->next;
    while (p) {
        if (p->date.ID == ID) {
            p->date.flag = FREE;
            p->date.ID = FREE;
            if (p->front->date.flag == FREE && p->next->date.flag != FREE) {
                p->front->date.size += p->date.size;
                p->front->next = p->next;
                p->next->front = p->front;
            }
            if (p->front->date.flag != FREE && p->next->date.flag == FREE) {
                p->date.size += p->next->date.size;
                if (p->next->next) {
                    p->next->next->front = p;
                    p->next = p->next->next;
                } else {
                    p->next = p->next->next;
                }
            }
            if (p->front->date.flag == FREE && p->next->date.flag == FREE) {
                p->front->date.size += p->date.size + p->next->date.size;
                if (p->next->next) {
                    p->next->next->front = p->front;
                    p->front->next = p->next->next;
                } else {
                    p->front->next = p->next->next;
                }
            }
            break;
        }
        p = p->next;
    }
    cout << "���ճɹ���" << endl;
    return 1;
}

void show() {
    cout << "------------------" << endl;
    cout << "�ڴ�������" << endl;
    cout << "------------------" << endl;
    FNodeList p = block_first->next;
    while (p) {
        cout << "�����ţ�";
        if (p->date.ID == FREE) {
            cout << "FREE" << endl;
        } else {
            cout << p->date.ID<<endl;
        }
        cout << "��ʼ��ַ��" << p->date.address << endl;
        cout << "�ڴ��С��" << p->date.size << endl;
        cout << "����״̬��";
        if (p->date.flag == FREE) {
            cout << "����" << endl;
        } else {
            cout << "�ѷ���" << endl;
        }
        cout << "------------------" << endl;
        p = p->next;
    }
}

int main() {
	init();
	int choice;
	do {
		cout << "1.�״���Ӧ�㷨�����ڴ�" << endl;
		cout << "2.�����Ӧ�㷨�����ڴ�" << endl;
		cout << "3.�����ڴ�" << endl;
		cout << "4.�鿴�ڴ����" << endl;
		cout << "0.�˳�����" << endl;
		cout << "������ָ�";
		cin >> choice;
		switch (choice) {
			case 1:
			if (alloc(1)) {
				cout << "����ɹ���" << endl;
			} else {
				cout << "����ʧ�ܣ�" << endl;
			}
			break;
			case 2:
			if (alloc2(1)) {
				cout << "����ɹ���" << endl;
			} else {
				cout << "����ʧ�ܣ�" << endl;
			}
			// cout << "�ù���δʵ�֣�" << endl;
			break;
			case 3: {
				int ID;
				cout << "������Ҫ���յ���ҵ�ţ�";
				cin >> ID;
				if (free(ID)) {
					cout << "���ճɹ���" << endl;
				} else {
					cout << "����ʧ�ܣ�" << endl;
				}
				break;
			}
			case 4:
			show();
			break;
			case 0:
			cout << "�������˳���" << endl;
			break;
			default:
			cout << "��Чָ����������룡" << endl;
			break;
		}
	} while (choice);
	return 0;
}