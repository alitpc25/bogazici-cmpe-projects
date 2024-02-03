#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "token.h"
#include <stdbool.h>

int findFromEnd(char *input, char c)
{
    int index = strlen(input) - 1;
    while (index >= 0 && input[index] != c)
    {
        index--;
    }
    return index;
}

// Lexer function returns 0 if there is error, 1 if there is no error.
int lexer(char input[], Token *tokens)
{
    int index = 0;
    int tokenIndex = 0;
    if (strlen(input) <= 1)
    {
        // If input is empty or just a newline character, return 0, not an error.
        return 0;
    }

    bool isInputAlias = false;

    while (index < strlen(input))
    {
        while (index < strlen(input) && isspace(input[index]))
        {
            // skip whitespace
            index++;
        }

        if (input[index] == '>')
        {
            if (index + 2 < strlen(input) && input[index + 1] == '>' && input[index + 2] == '>')
            {
                Token token;
                token.type = TRIPLE_GREATER_THAN;
                char *temp = (char *)malloc(sizeof(char) * 256);
                temp[0] = input[index];
                temp[1] = input[index + 1];
                temp[2] = input[index + 2];
                temp[3] = '\0';
                token.value = temp;
                tokens[tokenIndex] = token;
                index += 2;
            } else if (index + 1 < strlen(input) && input[index + 1] == '>')
            {
                Token token;
                token.type = DOUBLE_GREATER_THAN;
                char *temp = (char *)malloc(sizeof(char) * 256);
                temp[0] = input[index];
                temp[1] = input[index + 1];
                temp[2] = '\0';
                token.value = temp;
                tokens[tokenIndex] = token;
                index++;
            }
            else
            {
                Token token;
                token.type = GREATER_THAN;
                char *temp = (char *)malloc(sizeof(char) * 256);
                temp[0] = input[index];
                temp[1] = '\0';
                token.value = temp;
                tokens[tokenIndex] = token;
            }
        }
        else if (input[index] == '&')
        {
            Token token;
            token.type = AMPERSAND;
            char *temp = (char *)malloc(sizeof(char) * 256);
            temp[0] = input[index];
            temp[1] = '\0';
            token.value = temp;
            tokens[tokenIndex] = token;
        }
        else if (input[index] == '"' && isInputAlias)
        {
            char *temp = (char *)malloc(sizeof(char) * 256);
            int tempIndex = 0;
            index++;

            int lastQuoteIndex = findFromEnd(input, '"');

            while (index < strlen(input) && (input[index] != '"' || index != lastQuoteIndex ))
            {
                temp[tempIndex] = input[index];
                tempIndex++;
                index++;
            }
            temp[tempIndex] = '\0';
            Token token;
            token.type = STRING_LITERAL;
            token.value = temp;
            tokens[tokenIndex] = token;
        }
        else if (input[index] == '\0')
        {
            break;
        }
        else if (input[index] != ' ')
        {
            char *temp = (char *)malloc(sizeof(char) * 256);
            int tempIndex = 0;
            while (index < strlen(input) && input[index] != ' ')
            {
                temp[tempIndex] = input[index];
                tempIndex++;
                index++;
            }
            temp[tempIndex] = '\0';
            Token token;
            token.value = temp;
            if (strcmp(token.value, "alias") == 0)
            {
                token.type = ALIAS;
                isInputAlias = true;
            }
            else
            {
                token.type = IDENTIFIER;
            }
            tokens[tokenIndex] = token;
            index--;
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