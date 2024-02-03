#include "parser.c"

int main()
{
    char line[256 +1] = "";  
    printf("> ");

    while (fgets(line, sizeof(line), stdin)){
        // in case of Ctrl+D, EXIT
        if(line == NULL){
            break;
        }

        char temp[257];
        strcpy(temp, line);
        
        Token* tokens = (Token*) malloc(sizeof(Token)*256);
        
        // If the line is empty, contains only whitespaces or comments, continue.
        if(lexer(temp, tokens) == 0 || tokens[0].type == END){
            printf("> ");
            continue;
        }
        
        ast root = NULL; // AST for evaluation part.
        int tokenIndex = 0;

        // If line contains =, this is an assignment. Otherwise, it is just expression.
        if(strchr(line, '=') == NULL){
            //EXPRESSION
            root = parser(tokens, &tokenIndex, 0);
            if(root != NULL) {
                printf("%lld\n", eval(root));
            }
            //preorder(root);
        }else{
            //ASSIGNMENT
            root = parser(tokens, &tokenIndex, 1);
            if(root == NULL) {
                printf("Error!\n");
                printf("> ");
                continue;
            }
            //preorder(root);
            char* identifier = root->left->data;
            long long int result = eval(root->right);
            insert(identifier, result);
        }

        printf("> ");
    }
    return 0;
}