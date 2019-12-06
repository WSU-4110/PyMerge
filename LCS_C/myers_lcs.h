/**********************************************************************************
File: myers_lcs.h
Author: Malcolm Hall
Description:


Copyright (C) 2019  Malcolm Hall

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
**********************************************************************************/

#ifndef MYERSLCS_MYERS_LCS_H
#define MYERSLCS_MYERS_LCS_H

/**********************************************************************************
*       HEADER FILES
**********************************************************************************/
#include <stdio.h>



/**********************************************************************************
*       DATA STRUCTURES/VARIABLE DECLARATIONS
**********************************************************************************/

typedef unsigned int Boolean_t;

struct Snake_t {
    long long head[2U];
    struct Snake_t *tail;
};


typedef struct {
    FILE *leftFp;
    FILE *rightFp;
    long long leftLineCnt;
    long long rightLineCnt;
    long long maxLineLen; // Remove
    long long maxLineCnt;
    long long totalSize;
    long long arySize;
    long long *leftOutp;
    long long *rightOutp;
    char **leftLines;
    char **rightLines;
} DiffConfig_t;


/**********************************************************************************
*       FUNCTION DECLARATIONS/PROTOTYPES
**********************************************************************************/
void loadDiffConfig(DiffConfig_t *diffConfig, const char *leftFile, const char* rightFile);
static inline Boolean_t lineEqual(char *line1, char *line2);
void loadFileLines(DiffConfig_t *diffConfig);
long long getFileLineCnt(FILE *fp, long long *maxLineLen);
void freeDiffConfig(DiffConfig_t *diffConfig);
void lcs(DiffConfig_t *diffConfig);

static inline void initSnake(struct Snake_t *snake);
struct Snake_t *copySnake(struct Snake_t *snake);
static inline struct Snake_t *addSnakeHead(struct Snake_t *snake, long x, long y);
void printSnake(struct Snake_t *snake);
static inline long long Max(long long a, long long b);
void reverseArray(long *ary, int size);



#endif //MYERSLCS_MYERS_LCS_H
/**********************************************************************************
*       END OF FILE
**********************************************************************************/
