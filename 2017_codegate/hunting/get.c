#include <stdlib.h>
#include <stdio.h>
int main(){
  srand(time(0));
  for(int i =0; i<1000; i++){
    int r = rand();
    printf("%d\n",r); 
  }
}
