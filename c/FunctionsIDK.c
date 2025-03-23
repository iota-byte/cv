#include <stdio.h>
#include <stdbool.h>
#include <stdarg.h>  

#define c_assert(e)   ((e) ? true : (tst_debugging("%s,%d : assertion '%s' failed \n", __FILE__, __LINE__, #e), false))

void tst_debugging(const char* format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}

#define ERROR -1

int main() {
    int p = -1; 

    if (!c_assert(p >= 0)) {
        return ERROR;
    }
    
    return 0;
}
