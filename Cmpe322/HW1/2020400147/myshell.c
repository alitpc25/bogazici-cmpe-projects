#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include "parser.c"

char* getCommandFromAlias(char* aliasName) {
    aliasName = strtok(aliasName, "\n");
    FILE *fp;
    fp = fopen(".myshellaliases", "r");
    if(fp == NULL) {
        return NULL;
    }
    char* line = NULL;
    size_t len = 0;
    ssize_t read;
    while((read = getline(&line, &len, fp)) != -1) {
        char* alias = strtok(line, "=");
        if(strcmp(alias, aliasName) == 0) {
            char* command = strtok(NULL, "=");
            command[strlen(command) - 1] = '\0';
            return command;
        }
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    char* username = getenv("USER");
    char hostname[256];
    gethostname(hostname,256);
    char* home = getenv("HOME");
    char* currentDir = getenv("PWD");
    if(strstr(currentDir, home) != NULL) {
        char* temp = malloc(sizeof(char) * 100);
        strcpy(temp, "~");
        strcat(temp, strstr(currentDir, home) + strlen(home));
        strcpy(currentDir, temp);
    }
    while(1) {
        printf("%s@%s> %s --- ", username, hostname, currentDir);
        char *line = NULL;
        size_t len = 0;
        ssize_t read;

        read = getline(&line, &len, stdin);

        if (read == -1) {
            printf("Invalid argument\n");
            exit(1);
        }
        
        if (strcmp(line, "exit\n") == 0) {
            exit(0);
        }

        if (line[0] == '\n')
        {
            continue;
        }

        char tempLine[256];
        strcpy(tempLine, line);

        char* lineTokens[256];
        char *lineToken = strtok(line, " ");
        int tokenCount = 0;

        // Tokenize the line and store tokens in the array
        while (lineToken != NULL && tokenCount < 256) {
            lineTokens[tokenCount] = lineToken;
            lineToken = strtok(NULL, " ");
            tokenCount++;
        }

        char temp[256];

        char* aliasString = "alias ";

        // check if first element is stored as alias
        if(strstr(line, aliasString) == NULL) {
            char* command = getCommandFromAlias(lineTokens[0]);
            if(command != NULL) {
                strcpy(temp, command);
            } else {
                strcpy(temp, line);
            }
        } else {
            strcpy(temp, line);
        }
        for(int i = 1; i < tokenCount; i++) {
            strcat(temp, " ");
            strcat(temp, lineTokens[i]);
        }

        // remove newline char from input if exists
        if (temp[strlen(temp) - 1] == '\n') {
            temp[strlen(temp) - 1] = '\0';
        }

        Token *tokens = (Token *)malloc(sizeof(Token) * 256);

        // If the line is empty, contains only whitespaces or comments, continue.
        if (lexer(temp, tokens) == 0 || tokens[0].type == END)
        {
            continue;
        }
        
        FILE *fp;
        fp = fopen(".myshellhistory", "a");
        fprintf(fp, "%s\n", temp);
        fclose(fp);

        int tokenIndex = 0;

        if(strstr(temp, aliasString) != NULL) {
            addAlias(tokens, &tokenIndex);
        } else {
            startCommand(tokens, &tokenIndex);
        }

        free(tokens);

        // To periodically check if any background processes have finished
        waitpid(-1,NULL,WNOHANG);
    }
}