#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define forr(i, a, b) for(int i = (a); i < (b); i++)

void genNums(int n, const char *nombreArchivo, int max) {
    FILE *archivo = fopen(nombreArchivo, "w");
    forr(i, 0, n) fprintf(archivo, "%d\n", (rand()%max)+1);
    fclose(archivo);
}

int main() {
    srand(time(NULL));
    int n = 1000000;
    genNums(n, "ccuatro.txt", 4);
    genNums(n, "cocho.txt", 8);
    return 0;
}