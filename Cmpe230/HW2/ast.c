#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Abstract Syntax tree to convert infix expressions.

typedef struct node {
    char* data;
    struct node *left, *right;
} * ast;

// Function to add new node to the tree
ast insertNode(char* str) {
    ast n = (ast)malloc(sizeof(struct node));
    n->data = (char*)malloc(strlen(str) + 1);
    strcpy(n->data, str);
    n->left = n->right = NULL;
    return n;
}

// Function to print the preorder traversal of the tree
void preorder(ast root)
{
    if (root)
    {
        printf("%s\n", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}