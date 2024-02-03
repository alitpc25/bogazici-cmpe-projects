#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "process.h"
#include <stdbool.h>

Process *processes = NULL;

int *instructionLength = NULL;

char ***processInstructions = NULL;

int contextSwitchTime = 10;
int silverProcessTimeQuantum = 80;
int goldProcessTimeQuantum = 120;
int platinumProcessTimeQuantum = 120;

int *willExecProcesses = NULL;

int readDefinition(char *fileName) {
    FILE *fp = fopen(fileName, "r");
    if (fp == NULL) {
        printf("Error: cannot open file %s\n", fileName);
        exit(1);
    }
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    while ((read = getline(&line, &len, fp)) != -1) {
        char *token = strtok(line, " ");
        int processNo = atoi(token + 1); // skip the first character 'P'
        processes[processNo - 1].processNo = processNo;
        willExecProcesses[processNo - 1] = 1; // will execute this process
        token = strtok(NULL, " ");
        processes[processNo - 1].priority = atoi(token);
        token = strtok(NULL, " ");
        processes[processNo - 1].startTime = atoi(token);
        processes[processNo - 1].arrivalTime = atoi(token);
        token = strtok(NULL, " ");
        if(token[strlen(token) - 1] == '\n') {
            token[strlen(token) - 1] = '\0';
        }
        if (strcmp(token, "GOLD") == 0) {
            processes[processNo - 1].type = GOLD;
        }
        else if (strcmp(token, "SILVER") == 0) {
            processes[processNo - 1].type = SILVER;
        }
        else if (strcmp(token, "PLATINUM") == 0) {
            processes[processNo - 1].type = PLATINUM;
        }
        processes[processNo - 1].executedTime = 0;
        processes[processNo - 1].executedTimeQs = 0;
        processes[processNo - 1].lastExecutedAt = -1;
        processes[processNo - 1].lastExecutedLine = 0;
    }
    fclose(fp);
}

int readInstructionLengths() {
    FILE *fp = fopen("instructions.txt", "r");
    if (fp == NULL) {
        printf("Error: cannot open file %s\n", "instruction_lengths.txt");
        exit(1);
    }
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    int i = 0;
    while ((read = getline(&line, &len, fp)) != -1) {
        char *token = strtok(line, " ");
        token = strtok(NULL, " ");
        instructionLength[i] = atoi(token);
        i++;
    }
    fclose(fp);
}

int readProcessInstructions() {
    for (int i = 1; i < 11; i++) {
        // read files from P0.TXT to P10.TXT
        char fileName[10];
        sprintf(fileName, "P%d.txt", i);
        FILE *fp = fopen(fileName, "r");
        if (fp == NULL) {
            printf("Error: cannot open file %s\n", fileName);
            exit(1);
        }
        char *line = NULL;
        size_t len = 0;
        ssize_t read;
        int j = 0;
        processInstructions[i - 1] = (char **)malloc(256 * sizeof(char *)); // assume each process has at most 256 instructions
        while ((read = getline(&line, &len, fp)) != -1) {
            // each line consists of a single instruction string
            processInstructions[i - 1][j] = (char *)malloc(10 * sizeof(char));
            strcpy(processInstructions[i - 1][j], line);
            if (processInstructions[i - 1][j][strlen(processInstructions[i - 1][j]) - 1] == '\n') {
                processInstructions[i - 1][j][strlen(processInstructions[i - 1][j]) - 1] = '\0';
            }
            j++;
        }
        processes[i-1].instructionCount = j-1;
        processInstructions[i - 1][j] = NULL;
        fclose(fp);
    }
}

int main(int argc, char *argv[]) {
    // INITIALIZATIONS
    // processes[i-1] = Pi
    processes = (Process *)malloc(10 * sizeof(Process));
    willExecProcesses = (int *)malloc(10 * sizeof(int));

    readDefinition("definition.txt");

    instructionLength = (int *)malloc(21 * sizeof(int));
    readInstructionLengths();

    processInstructions = (char ***)malloc(10 * sizeof(char **));

    readProcessInstructions();
    for (int i = 0; i < 10; i++) {
        int j = 0;
        while (processInstructions[i][j] != NULL) {
            j++;
        }
    }

    // MAIN ALGORITHM
    // platinum processes are executed immediately, no preemption
    // priority order: type > priority > arrival time > process number (reverse order) for example, P1 > P2
    // If a silver process gets three quantums of execution, at the end of the third, it becomes a gold process.
    // If a gold process gets five quantums of execution (when it is gold), at the end of the fifth, it becomes a platinum process.
    // Other than the time quantum, silver and gold processes have no differences in importance of execution.
    // You cannot context switch during an instruction, you can context switch at the end of an instruction since instructions are atomic.
    // floating point: 1 digit after the decimal point

    int currentTime = 0;
    int processToExec = -1;

    while (1) {
        // check if there are any processes left
        int allProcessesFinished = 1;
        for (int i = 0; i < 10; i++) {
            if (willExecProcesses[i] == 1) {
                allProcessesFinished = 0;
                break;
            }
        }
        if (allProcessesFinished) {
            break;
        }

        int *readyQueue = (int *)malloc(10 * sizeof(int));

        for (int i = 0; i < 10; i++) {
            if (willExecProcesses[i] == 1 && processes[i].arrivalTime <= currentTime) {
                readyQueue[i] = 1;
                if (processes[i].type == SILVER && processes[i].executedTimeQs == 3) {
                    processes[i].type = GOLD;
                    processes[i].executedTimeQs = 0;
                } else if (processes[i].type == GOLD && processes[i].executedTimeQs == 5) {
                    processes[i].type = PLATINUM;
                    processes[i].executedTimeQs = 0;
                }
            }
        }

        // if there are no processes to execute, skip time idle
        int noProcessesToExec = 1;
        for (int i = 0; i < 10; i++) {
            if (readyQueue[i] == 1) {
                noProcessesToExec = 0;
                break;
            }
        }
        if (noProcessesToExec) {
            currentTime++;
            continue;
        }

        // find the process to execute
        for (int i = 0; i < 10; i++) {
            if (readyQueue[i] == 1) {
                if (processToExec == -1) {
                    processToExec = i;
                } else {
                    if (processToExec == i) {
                        continue;
                    }
                    if (processes[i].type == PLATINUM) {
                        if (processes[processToExec].type != PLATINUM) {
                            processToExec = i;
                        } else {
                            if (processes[i].priority > processes[processToExec].priority) {
                                processToExec = i;
                            } else if (processes[i].priority == processes[processToExec].priority) {
                                if (processes[i].arrivalTime < processes[processToExec].arrivalTime) {
                                    processToExec = i;
                                } else if (processes[i].arrivalTime == processes[processToExec].arrivalTime) {
                                    char processNoStr[3];
                                    sprintf(processNoStr, "%d", processes[i].processNo);
                                    char processToExecNoStr[3];
                                    sprintf(processToExecNoStr, "%d", processes[processToExec].processNo);
                                    if (strcmp(processNoStr, processToExecNoStr) < 0) {
                                        processToExec = i;
                                    }
                                }
                            }
                        }
                    } else {
                        if(processes[processToExec].type == PLATINUM) {
                            continue;
                        }
                        if (processes[i].priority > processes[processToExec].priority) {
                            processToExec = i;
                        } else if (processes[i].priority == processes[processToExec].priority) {
                            if (processes[i].arrivalTime == processes[processToExec].arrivalTime) {
                                char processNoStr[3];
                                sprintf(processNoStr, "%d", processes[i].processNo);
                                char processToExecNoStr[3];
                                sprintf(processToExecNoStr, "%d", processes[processToExec].processNo);
                                if (strcmp(processNoStr, processToExecNoStr) < 0) {
                                    processToExec = i;
                                }
                            } else if (processes[i].arrivalTime < processes[processToExec].arrivalTime) {
                                processToExec = i;
                            }
                        }
                    }
                }
            }
        }
        bool contextSwitched = false;
        // context switch. if same process, no context switch
        if (processToExec != -1 && processes[processToExec].lastExecutedAt == currentTime) {
            // no context switch
        } else {
            contextSwitched = true;
            currentTime += contextSwitchTime;
        }

        int execTime = 0;
        //printf("%d\tP%d\t%s\t%d\n", currentTime, processToExec+1, instrToExec, processes[processToExec].type);

        // execute the process
        processes[processToExec].executedTimeQs++;
        if (processes[processToExec].type == PLATINUM) {
            while (1) {
                char *instrToExec = processInstructions[processToExec][processes[processToExec].lastExecutedLine];
                int instrToExecNo = atoi(instrToExec + 5); // skip the first 5 characters 'INSTR'
                if (strstr(instrToExec, "exit") != NULL) {
                    instrToExecNo = 21;
                }
                int instrToExecTime = instructionLength[instrToExecNo - 1];

                if (instrToExecTime > 0) {
                    //printf("%d\tP%d\t%s\t%d\n", currentTime, processToExec+1, instrToExec, processes[processToExec].type);
                    execTime += instrToExecTime;

                    processes[processToExec].lastExecutedLine++;
                    processes[processToExec].executedTimeQs++;
                    processes[processToExec].executedTime += instrToExecTime;
                    currentTime += instrToExecTime;
                    processes[processToExec].arrivalTime = currentTime;
                    processes[processToExec].lastExecutedAt = currentTime;

                    if (processes[processToExec].lastExecutedLine > processes[processToExec].instructionCount) {
                        willExecProcesses[processToExec] = 2; // finished
                        processes[processToExec].endTime = currentTime;
                        processes[processToExec].turnaroundTime = processes[processToExec].endTime - processes[processToExec].startTime;
                        processes[processToExec].waitingTime = processes[processToExec].turnaroundTime - processes[processToExec].executedTime;
                        processToExec = -1; // SET TO RESTART 
                        break;
                    }
                }
            }
        } else {
            int shouldPreempt = 0;
            while (1) {
                char *instrToExec = processInstructions[processToExec][processes[processToExec].lastExecutedLine];
                int instrToExecNo = atoi(instrToExec + 5); // skip the first 5 characters 'INSTR'
                if (strstr(instrToExec, "exit") != NULL) {
                    instrToExecNo = 21;
                }
                int instrToExecTime = instructionLength[instrToExecNo - 1];
            
                int timeQuantum = goldProcessTimeQuantum;
                if(processes[processToExec].type == SILVER) {
                    timeQuantum = silverProcessTimeQuantum;
                }
                if (execTime < timeQuantum && instrToExecTime > 0) {
                    //printf("%d\tP%d\t%s\t%d\n", currentTime, processToExec+1, instrToExec, processes[processToExec].type);
                    execTime += instrToExecTime;
                    processes[processToExec].lastExecutedLine++;
                    processes[processToExec].executedTime += instrToExecTime;
                    currentTime += instrToExecTime;
                    processes[processToExec].arrivalTime = currentTime;
                    processes[processToExec].lastExecutedAt = currentTime;

                    if (processes[processToExec].lastExecutedLine > processes[processToExec].instructionCount) {
                        willExecProcesses[processToExec] = 2; // finished
                        processes[processToExec].endTime = currentTime;
                        processes[processToExec].turnaroundTime = processes[processToExec].endTime - processes[processToExec].startTime;
                        processes[processToExec].waitingTime = processes[processToExec].turnaroundTime - processes[processToExec].executedTime;
                        processToExec = -1; // SET TO START FROM 0   
                        break;
                    }
                } else {
                    break;
                }
                // Check for preemption
                for (int i = 0; i < 10; i++) {
                    if (willExecProcesses[i] == 1 && processes[i].startTime <= currentTime && ((!contextSwitched && processes[i].startTime >= currentTime-instrToExecTime) || (contextSwitched && processes[i].startTime >= currentTime-instrToExecTime-contextSwitchTime)) && (processes[i].priority > processes[processToExec].priority || processes[i].type == PLATINUM)) {
                        shouldPreempt = 1;
                        break;
                    }
                }
                if (shouldPreempt) {
                    break;
                } else {
                    contextSwitched = false;
                }
            }
        }
    }

/*
    // print results
    for(int i = 0; i<10; i++) {
        if(willExecProcesses[i] != 0) {
            printf("WAIT:%d\n", processes[i].waitingTime);
            printf("TURNA:%d\n", processes[i].turnaroundTime);
            printf("EXEC:%d\n", processes[i].executedTime);
            printf("EXECQ:%d\n", processes[i].executedTimeQs);
            printf("LAEXECAT:%d\n", processes[i].lastExecutedAt);
            printf("LAEXLINE:%d\n", processes[i].lastExecutedLine);
            printf("ARRIVE:%d\n", processes[i].arrivalTime);
            printf("END:%d\n", processes[i].endTime);
            printf("PID:%d\n", processes[i].processNo);
            printf("-----PROCESS%d-----\n", i);
        }
    }
*/

    // calc avg waiting time
    // count finished processes
    int finishedProcesses = 0;
    for (int i = 0; i < 10; i++) {
        if (willExecProcesses[i] == 2) {
            finishedProcesses++;
        }
    }

    float avgWaitingTime = 0;
    for (int i = 0; i < 10; i++) {
        avgWaitingTime += processes[i].waitingTime;
    }
    avgWaitingTime /= finishedProcesses;

    // calc avg turnaround time
    float avgTurnaroundTime = 0;
    for (int i = 0; i < 10; i++) {
        avgTurnaroundTime += processes[i].turnaroundTime;
    }
    avgTurnaroundTime /= finishedProcesses;

    if(avgWaitingTime == (int) avgWaitingTime) {
        printf("%d\n", (int) avgWaitingTime);
    } else {
        printf("%.1f\n", avgWaitingTime);
    }
    if(avgTurnaroundTime == (int) avgTurnaroundTime) {
        printf("%d\n", (int) avgTurnaroundTime);
    } else {
        printf("%.1f\n", avgTurnaroundTime);
    }
    return 0;
}