#include "lexer.c"
#include "evaluator.c"

Token getCurrentToken(Token* tokens, int* tokenIndex) {
    return tokens[*tokenIndex];
}

int getLength(Token* tokens) {
    int i = 0;
    while(tokens[i].type != END) {
        i++;
    }
    return i;
}

ast parse_expr1(Token* tokens, int* tokenIndex, int line_number);

// expr7 -> identifier | constant
ast parse_expr7(Token* tokens, int* tokenIndex, int line_number) {
    if(getCurrentToken(tokens, tokenIndex).type == IDENTIFIER) {
        char* identifier = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        return insertNode(identifier);
    } else if(getCurrentToken(tokens, tokenIndex).type == INT_LITERAL) {
        char* number = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        return insertNode(number);
    } else {
        printf("Error on line %d!\n", line_number);
    }
}

// expr6 -> expr7 | "(" expr1 ")"
ast parse_expr6(Token* tokens, int* tokenIndex, int line_number) {
    if(getCurrentToken(tokens, tokenIndex).type == LEFT_PARANTHESES) {
        *tokenIndex = *tokenIndex+1;
        ast expr1 = parse_expr1(tokens, tokenIndex, line_number);
        if(expr1 == NULL) return NULL;
        if(getCurrentToken(tokens, tokenIndex).type == RIGHT_PARANTHESES) {
            *tokenIndex = *tokenIndex+1;
        } else {
            printf("Error on line %d!\n", line_number);
        }
        return expr1;
    } else {
        return parse_expr7(tokens, tokenIndex, line_number);
    }
}

// expr5 -> expr6 | not(expr1) | xor(expr1, expr1) | ls(expr1, expr1) | rs(expr1, expr1) | lr(expr1, expr1) | rr(expr1, expr1)
ast parse_expr5(Token* tokens, int* tokenIndex, int line_number) {

    if(getCurrentToken(tokens, tokenIndex).type == FUNCTION) {
        if(strcmp(getCurrentToken(tokens, tokenIndex).value, "not") == 0) {
            char* operator = getCurrentToken(tokens, tokenIndex).value;
            *tokenIndex = *tokenIndex+1;
            if(getCurrentToken(tokens, tokenIndex).type == LEFT_PARANTHESES) {
                *tokenIndex = *tokenIndex+1;
                ast expr6 = parse_expr1(tokens, tokenIndex, line_number);
                if(expr6 == NULL) return NULL;
                if(getCurrentToken(tokens, tokenIndex).type == RIGHT_PARANTHESES) {
                    *tokenIndex = *tokenIndex+1;
                } else {
                    printf("Error on line %d!\n", line_number);
                }
                ast temp = insertNode(operator);
                temp->left = expr6;
                temp->right = NULL;
                expr6 = temp;
                return expr6;
            } else {
                printf("Error on line %d!\n", line_number);
            }
        } else if(strcmp(getCurrentToken(tokens, tokenIndex).value, "xor") == 0
            || strcmp(getCurrentToken(tokens, tokenIndex).value, "ls") == 0
            || strcmp(getCurrentToken(tokens, tokenIndex).value, "rs") == 0
            || strcmp(getCurrentToken(tokens, tokenIndex).value, "lr") == 0
            || strcmp(getCurrentToken(tokens, tokenIndex).value, "rr") == 0 ) {
            char* operator = getCurrentToken(tokens, tokenIndex).value;
            *tokenIndex = *tokenIndex+1;
            if(getCurrentToken(tokens, tokenIndex).type == LEFT_PARANTHESES) {
                *tokenIndex = *tokenIndex+1;
                ast expr6 = parse_expr1(tokens, tokenIndex, line_number);
                if(expr6 == NULL) return NULL;
                if(getCurrentToken(tokens, tokenIndex).type == DELIMITER) {
                    *tokenIndex = *tokenIndex+1;
                } else {
                    printf("Error on line %d!\n", line_number);
                }
                ast expr7 = parse_expr1(tokens, tokenIndex, line_number);
                if(expr7 == NULL) return NULL;
                if(getCurrentToken(tokens, tokenIndex).type == RIGHT_PARANTHESES) {
                    *tokenIndex = *tokenIndex+1;
                } else {
                    printf("Error on line %d!\n", line_number);
                }
                ast temp = insertNode(operator);
                temp->left = expr6;
                temp->right = expr7;
                expr6 = temp;
                return expr6;
            } else {
                printf("Error on line %d!\n", line_number);
            }
        }
    } else {
        return parse_expr6(tokens, tokenIndex, line_number);
    }
}

// expr4 -> expr5 | expr4 "*" expr5 | expr4 "/" expr5 | expr4 "%" expr5
ast parse_expr4(Token* tokens, int* tokenIndex, int line_number) {
    ast expr5 = parse_expr5(tokens, tokenIndex, line_number);
    if(expr5 == NULL) return NULL;
    while(strcmp(getCurrentToken(tokens, tokenIndex).value, "*") == 0 || strcmp(getCurrentToken(tokens, tokenIndex).value, "/") == 0 || strcmp(getCurrentToken(tokens, tokenIndex).value, "%") == 0) {
        char* operator = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        ast expr4 = parse_expr5(tokens, tokenIndex, line_number);
        if(expr4 == NULL) return NULL;
        ast temp = insertNode(operator);
        temp->left = expr5;
        temp->right = expr4;
        expr5 = temp;
    }
    return expr5;
}

// expr3 -> expr4 | expr3 "+" expr4 | expr3 "-" expr4
ast parse_expr3(Token* tokens, int* tokenIndex, int line_number) {
    ast expr4 = parse_expr4(tokens, tokenIndex, line_number);
    if(expr4 == NULL) return NULL;
    while(strcmp(getCurrentToken(tokens, tokenIndex).value, "+") == 0 || strcmp(getCurrentToken(tokens, tokenIndex).value, "-") == 0) {
        char* operator = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        ast expr3 = parse_expr4(tokens, tokenIndex, line_number);
        if(expr3 == NULL) return NULL;
        ast temp = insertNode(operator);
        temp->left = expr4;
        temp->right = expr3;
        expr4 = temp;
    }
    return expr4;
}

// expr2 -> expr3 | expr2 "&" expr3
ast parse_expr2(Token* tokens, int* tokenIndex, int line_number) {
    ast expr3 = parse_expr3(tokens, tokenIndex, line_number);
    if(expr3 == NULL) return NULL;
    while(strcmp(getCurrentToken(tokens, tokenIndex).value, "&") == 0) {
        char* operator = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        ast expr2 = parse_expr3(tokens, tokenIndex, line_number);
        if(expr2 == NULL) return NULL;
        ast temp = insertNode(operator);
        temp->left = expr3;
        temp->right = expr2;
        expr3 = temp;
    }
    return expr3;
}

// expr1 -> expr2 | expr1 "|" expr2
ast parse_expr1(Token* tokens, int* tokenIndex, int line_number) {
    ast expr2 = parse_expr2(tokens, tokenIndex, line_number);
    if(expr2 == NULL) return NULL;
    while(strcmp(getCurrentToken(tokens, tokenIndex).value, "|") == 0) {
        char* operator = getCurrentToken(tokens, tokenIndex).value;
        *tokenIndex = *tokenIndex+1;
        ast expr1 = parse_expr2(tokens, tokenIndex, line_number);
        if(expr1 == NULL) return NULL;
        ast temp = insertNode(operator);
        temp->left = expr2;
        temp->right = expr1;
        expr2 = temp;
    }
    return expr2;
}

// root -> identifier "=" expr1 | expr1
ast parse_root(Token* tokens, int* tokenIndex, int operation, int line_number) {
    Token currentToken = getCurrentToken(tokens, tokenIndex);
    ast root = NULL;
    if(operation == 1) {
        // operation = 1 for assignment.
        char* identifier = currentToken.value;
        *tokenIndex = *tokenIndex+1;
        currentToken = getCurrentToken(tokens, tokenIndex);
        if(strcmp(currentToken.value, "=") != 0){
            return NULL;
        }
        root = insertNode(currentToken.value);
        root->left = insertNode(identifier);
        *tokenIndex = *tokenIndex+1;
        ast expr1 = parse_expr1(tokens, tokenIndex, line_number);
        if(expr1 == NULL) return NULL;
        root->right = expr1;
    } else {
        // operation = 0 for expression.
        ast expr1 = parse_expr1(tokens, tokenIndex, line_number);
        if(expr1 == NULL) return NULL;
        root = expr1;
    }
    return root;
}

ast parser(Token* tokens, int* tokenIndex, int operation, int line_number) {
    ast result = parse_root(tokens, tokenIndex, operation, line_number);
    if(*tokenIndex < getLength(tokens) && result != NULL) {
        // If there are still tokens left and the result is not NULL, then there is an error. For example 2+3().
        printf("Error on line %d!\n", line_number);
    }
    return result;
}