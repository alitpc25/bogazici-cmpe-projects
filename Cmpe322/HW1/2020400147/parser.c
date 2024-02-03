// <root> -> alias <alias_name> "=" "<command>" | alias <alias_name> "=" "<command>" "&" | <command>
// <command> -> <command_name> <lists> "&" | <command_name> <lists> | <command_name> "&" | <command_name>
// <lists> -> <arguments> | <redirect> | <arguments> <redirect>
// <redirect> -> ">" <filename> | ">>" <filename> | ">>>" <filename>
// <arguments> -> <argument> | <argument> <arguments>
// <argument> -> "-"<identifier> | <identifier>
// <filename> -> <identifier>
// <command_name> -> <identifier> | <alias_name>
// <alias_name> -> <identifier>
// <identifier> -> <letter> | <identifier> <letter> | <identifier> <digit>

#include "lexer.c"
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <fcntl.h>
#include <dirent.h>
#include <stdbool.h>

int originalStdout;

int len(Token *tokens) {
    int i = 0;
    while(tokens[i].type != END) {
        i++;
    }
    return i;
}

int numberOfCurrentProcesses() {
    DIR *procDir = opendir("/proc");
    if (procDir == NULL) {
        perror("Error opening /proc directory");
        exit(EXIT_FAILURE);
    }

    int runningProcesses = 0;
    struct dirent *entry;

    while ((entry = readdir(procDir)) != NULL) {
        if (entry->d_type == DT_DIR && strspn(entry->d_name, "0123456789") == strlen(entry->d_name)) {
            runningProcesses++;
        }
    }

    closedir(procDir);
    return runningProcesses;
}

char* getLastExecutedCommand() {
    FILE *fp;
    fp = fopen(".myshellhistory", "r");
    if(fp == NULL) {
        return NULL;
    }
    char* line = NULL;
    size_t len = 0;
    ssize_t read;
    char* lastLine = malloc(sizeof(char) * 256);
    char* secondLastLine = malloc(sizeof(char) * 256);
    while((read = getline(&line, &len, fp)) != -1) {
        strcpy(secondLastLine, lastLine);
        strcpy(lastLine, line);
    }
    fclose(fp);
    return secondLastLine;
}

// Aliases will be stored in a config file called .myshellaliases and will be loaded when the shell starts.

void storeAlias(char* aliasName, char* command) {
    FILE *fp;
    fp = fopen(".myshellaliases", "a");
    fprintf(fp, "%s=%s\n", aliasName, command);
    fclose(fp);
}

int addAliasHelper(Token *tokens, int *tokenIndex) {
    if(tokens[*tokenIndex].type != ALIAS) {
        printf("Invalid argument\n");
        return 0;
    }

    (*tokenIndex)++;

    if(tokens[*tokenIndex].type != IDENTIFIER) {
        printf("Invalid argument\n");
        return 0;
    }

    char* aliasName = tokens[*tokenIndex].value;

    (*tokenIndex)++;

    if(strcmp(tokens[*tokenIndex].value, "=") != 0) {
        printf("Invalid argument\n");
        return 0;
    }

    (*tokenIndex)++;

    if(tokens[*tokenIndex].type != STRING_LITERAL) {
        printf("Invalid argument\n");
        return 0;
    }

    char* command = tokens[*tokenIndex].value;

    (*tokenIndex)++;

    if(tokens[*tokenIndex].type != END) {
        printf("Invalid argument\n");
        return 0;
    }

    storeAlias(aliasName, command);

    return 1;
}

int addAlias(Token *tokens, int *tokenIndex) {
    if(tokens[len(tokens) - 1].type == AMPERSAND) {
        // run in background
        pid_t pid = fork(); // pid returns 0 if child process, pid of child process if parent
        if(pid == 0) {
            // child process
            // remove the ampersand from the arguments since it is not needed
            tokens[len(tokens) - 1].type = END;
            addAliasHelper(tokens, tokenIndex);
            kill(getpid(), SIGKILL);
        } else {
            // parent process
            return 1;
        }
    } else {
        // run in foreground
        return addAliasHelper(tokens, tokenIndex);
    }
}

void execCommand(char* args[]) {
    // First check if the command is a built-in command
    // If yes, exec it
    // If not, search the path for the command
    // If it is executable, exec it
    // If not executable, print error msg
    if(strcmp(args[0], "bello") == 0) {
        char hostname[256];
        gethostname(hostname,256);
        char* currentDir = getenv("PWD");
        char *tty_name = ttyname(STDIN_FILENO);
        char* home = getenv("HOME");

        char* lastExecutedCommand = getLastExecutedCommand();

        printf("Username: %s\n", getenv("USER"));
        printf("Hostname: %s\n", hostname);
        printf("Last Executed Command: %s", lastExecutedCommand);
        printf("TTY: %s\n", tty_name);
        printf("Current Shell Name: %s\n", getenv("SHELL"));      
        printf("Home Location: %s\n", home);
        time_t current_time;
        struct tm *time_info;

        time(&current_time);
        time_info = localtime(&current_time);
        printf("Current Time and Date: %s", asctime(time_info));
        printf("Current number of proccesses being executed: %d\n", numberOfCurrentProcesses()); 
        dup2(originalStdout, STDOUT_FILENO);
    } else if(strcmp(args[0], "echo") == 0) {
        // echo the arguments
        for(int i = 1; args[i] != NULL; i++) {
            printf("%s", args[i]);
        }
        printf("\n");
        dup2(originalStdout, STDOUT_FILENO);
    } else if(strcmp(args[0], "exit") == 0) {
        // exit the shell
        exit(0);
    } else {
        execvp(args[0], args); // execute the command with the arguments 

        // if we reach this point, the command is not executable        
        printf("Command not found\n");
        exit(0);
    }
}

void writeReverseToFile(const char *inputFileName, const char *outputFileName) {
    // Open the input file for reading
    FILE *inputFile = fopen(inputFileName, "r");
    if (inputFile == NULL) {
        perror("6Error opening input file");
        return;
    }

    // Open a file for writing
    FILE *outputFile = fopen(outputFileName, "a");
    if (outputFile == NULL) {
        perror("7Error opening file");
        fclose(inputFile);
        return;
    }

    // Read the input file and reverse its content
    char buffer[1024];
    size_t bytesRead;

    while ((bytesRead = fread(buffer, 1, sizeof(buffer), inputFile)) > 0) {
        // Reverse the content and write it to the output file
        for (size_t i = bytesRead; i > 0; i--) {
            fputc(buffer[i - 1], outputFile);
        }
    }

    // Close the files
    fclose(inputFile);
    fclose(outputFile);
}

char* tempFilename = ".myShellTempReverseFile";

void redirectOutput(char* filename, TokenType type, char* args[], int *argsIndex) {
    int fd;
    if(type == GREATER_THAN) {
        // > will overwrite the file
        fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        originalStdout = dup(STDOUT_FILENO);
        dup2(fd, STDOUT_FILENO); 
        close(fd);
    } else if(type == DOUBLE_GREATER_THAN) {
        // >> will append to the file
        fd = open(filename, O_WRONLY | O_CREAT | O_APPEND, 0644);
        originalStdout = dup(STDOUT_FILENO);
        dup2(fd, STDOUT_FILENO); 
        close(fd);
    } else if(type == TRIPLE_GREATER_THAN) {
        // >>> will append same as >>, but in reverse order
        
        pid_t pid = fork(); // pid returns 0 if child process, pid of child process if parent
        if(pid == 0) {
            // child process
            fd = open(tempFilename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
            originalStdout = dup(STDOUT_FILENO);
            dup2(fd, STDOUT_FILENO);
            close(fd);
            args[*argsIndex] = NULL;
            execCommand(args);
            kill(getpid(), SIGKILL); // if the command is built-in, it will not exit the child process, so we will kill it
        } else {
            // parent process
            wait(NULL);
            if(strcmp(args[0], "bello") != 0 && strcmp(args[0], "echo") != 0 && strcmp(args[0], "exit") != 0) {
                dup2(originalStdout, STDOUT_FILENO);
            }
            writeReverseToFile(tempFilename, filename);
            if(strcmp(args[0], "bello") != 0 && strcmp(args[0], "echo") != 0 && strcmp(args[0], "exit") != 0) {
                kill(getpid(), SIGKILL);
            }
        }
    }
}

int evalArgumentList(Token *tokens, int *tokenIndex, char* args[], int *argsIndex) {
    while(tokens[*tokenIndex].type == IDENTIFIER || tokens[*tokenIndex].type == STRING_LITERAL) {
        if(tokens[*tokenIndex].type == IDENTIFIER || tokens[*tokenIndex].type == STRING_LITERAL) {
            char* arg = (char *)malloc(sizeof(char) * 256);
            strncpy(arg, tokens[*tokenIndex].value, strlen(tokens[*tokenIndex].value));
            arg[strlen(tokens[*tokenIndex].value)] = '\0';
            args[*argsIndex] = arg;
            (*argsIndex)++;
        } else {
            printf("Invalid argument\n");
            return 0;
        }
        (*tokenIndex)++;
    }
    return 1;
}

int evalRedirect(Token *tokens, int *tokenIndex, char* args[], int *argsIndex, TokenType type) {
    (*tokenIndex)++;
    if(tokens[*tokenIndex].type != IDENTIFIER && tokens[*tokenIndex].type != STRING_LITERAL) {
        printf("Invalid argument\n");
        return 0;
    }
    char* filename = tokens[*tokenIndex].value;
    (*tokenIndex)++;
    if(tokens[*tokenIndex].type != END) {
        printf("Invalid argument\n");
        return 0;
    }

    if(filename != NULL) {
        redirectOutput(filename, type, args, argsIndex);
    }
    return 1;
}

void evalCommand(Token *tokens, int *tokenIndex) {

    char* commandName = tokens[*tokenIndex].value;

    (*tokenIndex)++;

    int argsIndex = 0;
    char* args[256];

    args[argsIndex] = commandName;
    argsIndex++;

    bool isReverseRedirect = false;
    int evalResult = 1;

    while(tokens[*tokenIndex].type != END) {

        // If last token is an ampersand, run the command in the background else run it in the foreground.
        if(tokens[*tokenIndex].type == IDENTIFIER || tokens[*tokenIndex].type == STRING_LITERAL) {
            evalResult = evalArgumentList(tokens, tokenIndex, args, &argsIndex);
        } else if(tokens[*tokenIndex].type == GREATER_THAN || tokens[*tokenIndex].type == DOUBLE_GREATER_THAN || tokens[*tokenIndex].type == TRIPLE_GREATER_THAN) {
            // it should execute the command and redirect the output accordingly
            if(tokens[*tokenIndex].type == TRIPLE_GREATER_THAN) {
                isReverseRedirect = true;
            }
           evalResult = evalRedirect(tokens, tokenIndex, args, &argsIndex, tokens[*tokenIndex].type);
        } else {
            printf("Invalid argument\n");
            return;
        }

        if(evalResult == 0) {
            return;
        }
    }

    if(isReverseRedirect) {
        remove(tempFilename);
        return;
    }
    
    args[argsIndex] = NULL;
    execCommand(args);
}

void executeCommandInBackground(Token *tokens, int *tokenIndex) {
    pid_t pid = fork(); // pid returns 0 if child process, pid of child process if parent
    if(pid == 0) {
        // child process
        // remove the ampersand from the arguments since it is not needed
        tokens[len(tokens) - 1].type = END;
        evalCommand(tokens, tokenIndex);
    } else {
        // parent process
        return;
    }
}

void executeCommandInForeground(Token *tokens, int *tokenIndex) {
    pid_t pid = fork(); // pid returns 0 if child process, pid of child process if parent
    if(pid == 0) {
        // child process
        evalCommand(tokens, tokenIndex);
    } else {
        // parent process
        waitpid(pid, NULL, 0);
        return;
    }
}

void execBuiltInCommand(Token *tokens, int *tokenIndex) {
    if(tokens[len(tokens) - 1].type == AMPERSAND) {
        tokens[len(tokens) - 1].type = END;
    }
    evalCommand(tokens, tokenIndex);
}

// Commands will be executed with the execv() function.
void startCommand(Token *tokens, int *tokenIndex) {
    // built-in commands will be executed in the shell process. there are three: bello, echo and exit.
    if(strcmp(tokens[*tokenIndex].value, "bello") == 0 || strcmp(tokens[*tokenIndex].value, "echo") == 0 || strcmp(tokens[*tokenIndex].value, "exit") == 0) {
        execBuiltInCommand(tokens, tokenIndex);
    } else {
        if(tokens[len(tokens) - 1].type == AMPERSAND) {
            // run in background
            executeCommandInBackground(tokens, tokenIndex);
        } else {
            // run in foreground
            executeCommandInForeground(tokens, tokenIndex);
        }
    }
}