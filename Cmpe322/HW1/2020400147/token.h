typedef enum {
    IDENTIFIER,
    STRING_LITERAL,
    GREATER_THAN,
    DOUBLE_GREATER_THAN,
    TRIPLE_GREATER_THAN,
    AMPERSAND,
    ALIAS,
    END
} TokenType;

// Grouping tokens
typedef struct {
    TokenType type;
    char* value;
} Token;