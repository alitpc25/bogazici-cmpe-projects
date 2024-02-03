#include "ast.c"
#include <stdlib.h>

int check_if_exists(char* identifier);

char* eval(ast root, FILE *fwritepointer, int line_number, int* temp_registers_index) {
    if(!root) return 0;
    // leaf node i.e, an integer or identifier
    if (!root->left && !root->right) {
        if(isdigit(root->data[0])) {
            // integer
            return root->data;
        } else {
            // identifier
            if(!root->data) {
                printf("Error on line %d!\n", line_number);
            } else {
                if(!check_if_exists(root->data)) {
                    // if the identifier is not found in the identifiers_list, print error.
                    printf("Error on line %d!\n", line_number);
                } else {
                    // Convert temp_registers_index to string and add x to the front of it.
                    char* temp = malloc(10);
                    sprintf(temp, "x%d", *(temp_registers_index));
                    fprintf(fwritepointer, "\t%%x%d = load i32, i32* %%%s\n", *(temp_registers_index), root->data);
                    *(temp_registers_index) = *(temp_registers_index) + 1;
                    return temp;
                }
            }
        }
    }

    // Evaluating the left and right subtrees recursively.
    
    char* l_val = eval(root->left,fwritepointer, line_number, temp_registers_index);

    char* r_val = eval(root->right,fwritepointer, line_number, temp_registers_index);

    char* str = malloc(10);
    sprintf(str, "x%d", *(temp_registers_index));

    // Printing the LLVM IR code for the expression according to the type of the l_val and r_val (register or integer).

    if(strcmp(root->data, "+") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = add i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = add i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = add i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = add i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if(strcmp(root->data, "-") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sub i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sub i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sub i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sub i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if (strcmp(root->data, "*") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = mul i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = mul i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = mul i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = mul i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if (strcmp(root->data, "/") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sdiv i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sdiv i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sdiv i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = sdiv i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if (strcmp(root->data, "%") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = srem i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = srem i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = srem i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = srem i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if (strcmp(root->data, "&") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = and i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = and i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = and i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = and i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if (strcmp(root->data, "|") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = or i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = or i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = or i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = or i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if(strcmp(root->data, "xor") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if(strcmp(root->data, "ls") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if(strcmp(root->data, "rs") == 0) {
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val);
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val);
        }
    } else if(strcmp(root->data, "rr") == 0) {
        // These two must be checked.
        // Implementing right rotate with LLVM IR.
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %s\n", *(temp_registers_index), l_val, r_val); // n >> d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n << (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n >> d) | (n << (32 - d))
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val); // n >> d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %%%s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n << (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n >> d) | (n << (32 - d))
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val); // n >> d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n << (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n >> d) | (n << (32 - d))
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val); // n >> d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %%%s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n << (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n >> d) | (n << (32 - d))
        }
    } else if(strcmp(root->data, "lr") == 0) {
        // These two must be checked.
        // Implementing left rotate with LLVM IR.
        if(isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %s\n", *(temp_registers_index), l_val, r_val); // n << d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n >> (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n << d) | (n >> (32 - d))
        } else if(isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %s, %%%s\n", *(temp_registers_index), l_val, r_val); // n << d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %%%s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n >> (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n << d) | (n >> (32 - d))
        } else if(!isdigit(l_val[0]) && isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %s\n", *(temp_registers_index), l_val, r_val); // n << d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n >> (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n << d) | (n >> (32 - d))
        } else if(!isdigit(l_val[0]) && !isdigit(r_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = shl i32 %%%s, %%%s\n", *(temp_registers_index), l_val, r_val); // n << d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = sub i32 32, %%%s\n", *(temp_registers_index), r_val); // 32 - d
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = ashr i32 %%%s, %%x%d\n", *(temp_registers_index), l_val, *(temp_registers_index) - 1); // n >> (32 - d)
            *(temp_registers_index) = *(temp_registers_index) + 1;
            fprintf(fwritepointer, "\t%%x%d = or i32 %%x%d, %%x%d\n", *(temp_registers_index), *(temp_registers_index) - 3, *(temp_registers_index) - 1); // (n << d) | (n >> (32 - d))
        }
    } else if(strcmp(root->data, "not") == 0) {
        if(isdigit(l_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %s, -1\n", *(temp_registers_index), l_val);
        } else if(!isdigit(l_val[0])) {
            fprintf(fwritepointer, "\t%%x%d = xor i32 %%%s, -1\n", *(temp_registers_index), l_val);
        }
    }
    *(temp_registers_index) = *(temp_registers_index) + 1;
    return str;
}