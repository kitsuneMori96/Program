#include<bits/stdc++.h>
using namespace std;

#define MAX_SIZE 100
typedef int ElemType;

typedef struct {
    ElemType data[MAX_SIZE];
    int length;
} Sqlist;

typedef struct LNode {
    ElemType data;
    struct LNode *next=nullptr;
} LNode , *LinkList;



void InitList(Sqlist &L) {
    L.length = 0;
}

void PrintList(const Sqlist &L) {
    for (int i = 0; i < L.length; i++) {
        cout << L.data[i] << " ";
    }
    cout << endl;
}

void addElem(Sqlist &L, int pos, ElemType elem) {
    if (pos < 0 || pos > L.length) {
        cout << "Invalid position!" << endl;
        return;
    }

    if (L.length == MAX_SIZE) {
        cout << "List is full!" << endl;
        return;
    }

    for (int i = L.length - 1; i >= pos; i--) {
        L.data[i + 1] = L.data[i];
    }

    L.data[pos] = elem;
    L.length++;
}

void deleteElem(Sqlist &L, int pos) {
    if (pos < 0 || pos >= L.length) {
        cout << "Invalid position!" << endl;
        return;
    }

    for (int i = pos; i < L.length - 1; i++) {
        L.data[i] = L.data[i + 1];
    }

    L.length--;
}


