#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define SIZE 256

// Hash table implementation for storing variables and their values.

struct Item {
   long long int data;   
   char* key;
};

struct Item* hashArray[SIZE]; 
struct Item* item;

int hashCode(char* key) {
    unsigned hashCode = 0;
    while (*key) hashCode+= *(key++);
    return hashCode % SIZE;
}

struct Item *search(char* key) {
   //get the hash 
   int hashIndex = hashCode(key);  
   //move in array until an empty 
   while(hashArray[hashIndex] != NULL) {
	
    if(strcmp(hashArray[hashIndex]->key, key) == 0) {
        return hashArray[hashIndex]; 
    }
			
      //go to next cell
      ++hashIndex;
		
      //wrap around the table
      hashIndex %= SIZE;
   }        
	
   return NULL;        
}

void insert(char* key,long long int data) {

   struct Item *item = (struct Item*) malloc(sizeof(struct Item));
   item->data = data;  
   item->key = key;

   //get the hash 
   int hashIndex = hashCode(key);

   //move in array until an empty cell
   while(hashArray[hashIndex] != NULL) {
        if(strcmp(hashArray[hashIndex]->key, key) == 0) {
            hashArray[hashIndex]->data = data;
            return;
        }

        //go to next cell
        ++hashIndex;

        //wrap around the table
        hashIndex %= SIZE;
   }
	
   hashArray[hashIndex] = item;
}