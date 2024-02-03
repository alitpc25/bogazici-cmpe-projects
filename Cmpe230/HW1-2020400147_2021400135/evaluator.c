#include "ast.c"
#include "lookup.c"
#include <stdlib.h>

// Long long int is used to store 64 bit integers.

long long int eval(ast root) {
    if(!root) return 0;
    // leaf node i.e, an integer or identifier
    if (!root->left && !root->right) {
        if(isdigit(root->data[0])) {
            // integer
            char* number = root->data;
            return strtoll(number, NULL, 10);
        } else {
            // identifier
            if(!root->data) {
                printf("Error!");
            } else {
                if(!search(root->data)) {
                    // if the identifier is not found in the hash table, return 0 as default.
                    return 0;
                } else {
                    return search(root->data)->data;
                }
            }
        }
    }

    // Evaluating the left and right subtrees recursively.
    
    long long int l_val = eval(root->left);

    long long int r_val = eval(root->right);

    if(strcmp(root->data, "+") == 0) {
        return l_val + r_val;
    } else if(strcmp(root->data, "-") == 0) {
        return l_val - r_val;
    } else if (strcmp(root->data, "*") == 0) {
        return l_val * r_val;
    } else if (strcmp(root->data, "&") == 0) {
        return l_val & r_val;
    } else if (strcmp(root->data, "|") == 0) {
        return l_val | r_val;
    } else if(strcmp(root->data, "xor") == 0) {
        return l_val ^ r_val;
    } else if(strcmp(root->data, "ls") == 0) {
        return l_val << r_val;
    } else if(strcmp(root->data, "rs") == 0) {
        return l_val >> r_val;
    } else if(strcmp(root->data, "rr") == 0) {
        return (l_val >> r_val) | (l_val << (64 - r_val));
    } else if(strcmp(root->data, "lr") == 0) {
        return (l_val << r_val) | (l_val >> (64 - r_val));
    } else if(strcmp(root->data, "not") == 0) {
        return ~l_val;
    }
}