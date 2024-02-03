#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "token.h"

// Lexer function returns 0 if there is error, 1 if there is no error.
int lexer(char input[], Token* tokens) {
    int index = 0;
    int tokenIndex = 0;
    if(strlen(input) <= 1) {
        // If input is empty or just a newline character, return 0, not an error.
        return 0;
    }
    while(index<strlen(input)) {
        while(index<strlen(input) && isspace(input[index])) {
            // skip whitespace
            index++;
        }

        char currentChar = input[index];
 
        if(isalpha(currentChar)) {
            if(tokenIndex > 0 && tokens[tokenIndex-1].type == IDENTIFIER) {
                // If two identifier calls are next to each other without an operator, return error.
                printf("Error!\n");
                return 0;
            }
            char* temp = (char*) malloc(sizeof(char)*256);
            int tempIndex = 0;
            while(index<strlen(input) && (isalpha(input[index]))) {
                temp[tempIndex] = input[index];
                tempIndex++;
                index++;
            }
            temp[tempIndex] = '\0';
            Token token;
            token.value = temp;
            if(strcmp(token.value, "xor") == 0 || strcmp(token.value, "ls") == 0 || strcmp(token.value, "rs") == 0 || strcmp(token.value, "lr") == 0 || strcmp(token.value, "rr") == 0 || strcmp(token.value, "not") == 0) {
                token.type = FUNCTION;
            } else {
                // Identifier name cannot be a function name.
                token.type = IDENTIFIER;
            }
            tokens[tokenIndex] = token;
            index--;
        } else if(isdigit(currentChar)) {
            if(tokenIndex > 0 && tokens[tokenIndex-1].type == INT_LITERAL) {
                // If two integers are next to each other without an operator, return error.
                printf("Error!\n");
                return 0;
            }
            char* temp = (char*) malloc(sizeof(char)*256);
            int tempIndex = 0;
            while(index<strlen(input) && isdigit(input[index])) {
                temp[tempIndex] = input[index];
                tempIndex++;
                index++;
            }
            temp[tempIndex] = '\0';
            Token token;
            token.value = temp;
            token.type = INT_LITERAL;
            tokens[tokenIndex] = token;
            index--;
        } else if(currentChar == '+' || currentChar == '-' || currentChar == '*' || currentChar == '&' || currentChar == '|') {
            Token token;
            token.type = OPERATOR;
            char* temp = (char*) malloc(sizeof(char)*256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        }  else if(currentChar == '=') {
            Token token;
            token.type = ASSIGN;
            char* temp = (char*) malloc(sizeof(char)*256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        } else if(currentChar == '(') {
            Token token;
            token.type = LEFT_PARANTHESES;
            char* temp = (char*) malloc(sizeof(char)*256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        } else if(currentChar == ')') {
            Token token;
            token.type = RIGHT_PARANTHESES;
            char* temp = (char*) malloc(sizeof(char)*256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        } else if(currentChar == ',') {
            Token token;
            token.type = DELIMITER;
            char* temp = (char*) malloc(sizeof(char)*256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        } else if(currentChar == '%') {
            // If the input is a comment, skip the rest of the line.
            break;
        } else if (currentChar == '\0') {
            break;
        } else {
            printf("Error!\n");
            return 0;
        }
        index++;
        tokenIndex++;
    }
    // Add an END token to the end of the array to indicate the end of the input.
    Token token;
    token.type = END;
    token.value = "END";
    tokens[tokenIndex] = token;
    return 1;
}