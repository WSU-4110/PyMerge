//
// Created by Malcolm Hall on 11/5/19.
//

#ifndef MYERSLCS_MYERS_LCS_H
#define MYERSLCS_MYERS_LCS_H

/**********************************************************************************
*       HEADER FILES
**********************************************************************************/
#include <stdio.h>
#include <stdint.h>

/**********************************************************************************
*       DATA STRUCTURES/VARIABLE DECLARATIONS
**********************************************************************************/

typedef struct {
    unsigned long *head;
    void *body;
} Snake_t;


typedef struct {
    FILE *leftFp;
    FILE *rightFp;
    unsigned long leftLineCnt;
    unsigned long rightLineCnt;
    unsigned long maxLineLength; // Remove
    unsigned long maxLineCnt;
    unsigned long totalSize;
    unsigned long arraySize;
    unsigned long outpSize;
    Snake_t **kCandidates;
    long *boundedArray;
    long *leftOutp;
    long *rightOutp;
    char **leftLines;
    char **rightLines;
//    unsigned int *binLeftLines;
//    unsigned int *binRightLines;
} DiffConfig_t;


typedef unsigned int Boolean_t;

/**********************************************************************************
*       FUNCTION DECLARATIONS/PROTOTYPES
**********************************************************************************/
void loadDiffConfig(DiffConfig_t *diffConfig, const char *leftFile, const char* rightFile);
Boolean_t lineEqual(char *line1, char *line2, long maxSize);
void loadFileLines(DiffConfig_t *diffConfig);
unsigned long getFileLineCnt(FILE *fp, unsigned long *maxLineLen);
inline void reverseArray(long *array, unsigned long size);
void freeDiffConfig(DiffConfig_t *diffConfig);
void lcs(DiffConfig_t *diffConfig);

void initSnake(Snake_t *snake);
void addSnakeHead(Snake_t *snake, long x, long y);
void removeSnakeHead(Snake_t *snake);

static inline unsigned long Max(unsigned long a, unsigned long b);


/**********************************************************************************
*       END OF FILE
**********************************************************************************/
#endif //MYERSLCS_MYERS_LCS_H