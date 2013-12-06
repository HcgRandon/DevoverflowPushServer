#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "include/cJSON/cJSON.c"

/* Resource Definitions */
char *name = "DvPush";

unsigned int norm = 0;
unsigned int warn = 1;
unsigned int crit = 2;

/* Function Definitions */
void _log(int, char *, char *);

void _log(int type, char *threadname, char *message) {
 if (type == norm) printf("[%s/INFO]: %s", threadname, message);
 else if (type == warn) printf("[%s/WARN]: %s", threadname, message);
 else if (type == crit) printf("[%s/CRIT]: %s", threadname, message);
 else printf("[%s]: %s", threadname, message);
}


