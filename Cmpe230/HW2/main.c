#include "parser.c"

void strip_extension(char *fname);
void add_extension(char *s);
char *create_file(char *file_name);
int check_if_exists(char* identifier);
int check_if_allocated(char* identifier);

char** identifiers_list;
int identifiers_list_index = 0;
char** allocated_identifiers;
int allocated_identifiers_index = 0;

int main(int argc, char **argv)
{

    // Create a file with the same name as the input file but with .ll extension.
    FILE *freadpointer = fopen(argv[1], "r");
    FILE *fwritepointer = fopen(create_file(argv[1]), "w");

    // Write the first lines of the LLVM IR code.
    fprintf(fwritepointer, "; ModuleID = \'advcalc2ir\'\n");
    fprintf(fwritepointer, "declare i32 @printf(i8*, ...)\n");
    fprintf(fwritepointer, "@print.str = constant [4 x i8] c\"%%d\\0A\\00\"\n");
    fprintf(fwritepointer, "\n");
    fprintf(fwritepointer, "define i32 @main() {\n");

    char line[256 + 1] = "";

    // Read the file line by line and parse it.
    // Firstly, we need to read the file line by line, parse every line and store root nodes of the ASTs in an array.
    // Then, we will evaluate the ASTs one by one and print the equivalent LLVM IR code.

    ast* roots = (ast*)malloc(sizeof(ast) * 256);
    int rootsIndex = 0;

    // To keep identifiers names in array so that we can check whether an identifier is called before it is declared.
    identifiers_list = (char**)malloc(sizeof(char*) * 256);

    int line_number = 0;

    allocated_identifiers = (char**)malloc(sizeof(char) * 256);

    while (!feof(freadpointer))
    {
        while (fgets(line, sizeof(line), freadpointer))
        {

            line_number++;

            char temp[257];
            strcpy(temp, line);

            Token *tokens = (Token *)malloc(sizeof(Token) * 256);

            // If the line is empty, contains only whitespaces or comments, continue.
            if (lexer(temp, tokens, line_number) == 0 || tokens[0].type == END)
            {
                continue;
            }

            ast root = NULL; // AST for evaluation part9
            int tokenIndex = 0;
            // If line contains =, this is an assignment. Otherwise, it is just expression.
            if (strchr(line, '=') == NULL)
            {
                // EXPRESSION
                root = parser(tokens, &tokenIndex, 0, line_number);
                if (root == NULL)
                {
                    printf("Error on line %d!\n", line_number);
                }
                roots[rootsIndex++] = root;
            }
            else
            {
                // ASSIGNMENT
                root = parser(tokens, &tokenIndex, 1, line_number);
                if (root == NULL)
                {
                    printf("Error on line %d!\n", line_number);
                }
                if(check_if_allocated(root->left->data) == 0) {
                    fprintf(fwritepointer, "\t%%%s = alloca i32\n", root->left->data);
                    allocated_identifiers[allocated_identifiers_index++] = root->left->data;
                }
                roots[rootsIndex++] = root;
            }
        }
    }

    line_number = 0;

    fclose(freadpointer);
    
    int temp_registers_index = 0;

    // Evaluate the ASTs one by one and print the equivalent LLVM IR code.
    for(int i = 0; i < rootsIndex; i++)
    {
        line_number++;
        
        if(strcmp(roots[i]->data, "=") == 0) {
            char* result_of_eval_right = eval(roots[i]->right, fwritepointer, line_number, &temp_registers_index);
            identifiers_list[identifiers_list_index++] = roots[i]->left->data;
            if(isdigit(result_of_eval_right[0]) != 0) {
                fprintf(fwritepointer, "\tstore i32 %s, i32* %%%s\n", result_of_eval_right, roots[i]->left->data);
            } else {
                fprintf(fwritepointer, "\tstore i32 %%%s, i32* %%%s\n", result_of_eval_right, roots[i]->left->data);
            }
        } else {
            //ONLY CHANGE IS HERE
            //Before, this line was here. It is wrong since we didn't check whether returned value is an integer or register.
            //fprintf(fwritepointer, "\tcall i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @print.str, i32 0, i32 0), i32 %%%s)\n", eval(roots[i], fwritepointer, line_number, &temp_registers_index));
            //After, the correct code is:
            char* result_of_eval = eval(roots[i], fwritepointer, line_number, &temp_registers_index);
            if(isdigit(result_of_eval[0]) != 0) {
                fprintf(fwritepointer, "\tcall i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @print.str, i32 0, i32 0), i32 %s)\n", result_of_eval);
            } else {
                fprintf(fwritepointer, "\tcall i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @print.str, i32 0, i32 0), i32 %%%s)\n", result_of_eval);
            }
        }
    }

    fprintf(fwritepointer, "\tret i32 0\n");
    fprintf(fwritepointer, "}");
    fclose(fwritepointer);
}

// To strip the extension of the .adv file.
void strip_extension(char *fname)
{
    char *end = fname + strlen(fname);

    while (end > fname && *end != '.' && *end != '\\' && *end != '/')
    {
        --end;
    }
    if ((end > fname && *end == '.') &&
        (*(end - 1) != '\\' && *(end - 1) != '/'))
    {
        *end = '\0';
    }
}

// To add the .ll extension to the file.
void add_extension(char *s)
{
    char *s1 = ".ll";
    int i;
    int j = strlen(s);

    for (i = 0; s1[i] != '\0'; i++)
    {
        s[i + j] = s1[i];
    }

    s[i + j] = '\0';
}

// To create the output file name.
char *create_file(char *file_name)
{
    strip_extension(file_name);
    add_extension(file_name);
    return file_name;
}

// To check if the identifier is present in the identifiers_list.
int check_if_exists(char* identifier) {
    for(int i = 0; i < identifiers_list_index; i++) {
        if(strcmp(identifier, identifiers_list[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// To check if the identifier is already allocated.
int check_if_allocated(char* identifier) {
    for(int i = 0; i < allocated_identifiers_index; i++) {
        if(strcmp(identifier, allocated_identifiers[i]) == 0) {
            return 1;
        }
    }
    return 0;
}