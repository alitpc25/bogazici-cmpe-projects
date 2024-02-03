typedef enum {
    IDENTIFIER,
    INT_LITERAL,
    ASSIGN,
    OPERATOR,
    FUNCTION,
    LEFT_PARANTHESES,
    RIGHT_PARANTHESES,
    DELIMITER,
    COMMENT,
    END
} TokenType;

// Grouping tokens
typedef struct {
    TokenType type;
    char* value;
} Token;