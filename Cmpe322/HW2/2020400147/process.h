typedef enum {
    SILVER,
    GOLD,
    PLATINUM
} ProcessType;

typedef struct {
    int processNo;
    int priority;
    int arrivalTime;
    ProcessType type;
    int executedTime;
    int startTime;
    int endTime;
    int waitingTime;
    int turnaroundTime;
    int executedTimeQs;
    int lastExecutedAt;
    int lastExecutedLine;
    int instructionCount;
} Process;