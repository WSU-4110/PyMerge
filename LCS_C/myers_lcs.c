/**********************************************************************************
File: myers_lcs.c
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

/**********************************************************************************
*       HEADER FILES
**********************************************************************************/
#include <stdlib.h>
#include <string.h>
#include <sys/proc_info.h>
#include "myers_lcs.h"

/**********************************************************************************
*       DEFINES
**********************************************************************************/
#define NONE -1
#define EOL '\n'

#ifndef TRUE
    #define TRUE 1U
#endif

#ifndef FALSE
    #define FALSE 0U
#endif

/**********************************************************************************
*       FUNCTION IMPLEMENTATIONS
**********************************************************************************/

/**********************************************************************************
 * @brief Loads a DiffConfig struct with file info and memory allocations.
 * @param diffConfig
 * @param leftFile
 * @param rightFile
 */
void loadDiffConfig(DiffConfig_t *diffConfig, const char *leftFile, const char *rightFile)
{
    diffConfig->leftFp = fopen(leftFile, "r");
    diffConfig->rightFp = fopen(rightFile, "r");
    diffConfig->maxLineLen = 0U;
    diffConfig->leftLineCnt = getFileLineCnt(diffConfig->leftFp, &(diffConfig->maxLineLen));
    diffConfig->rightLineCnt = getFileLineCnt(diffConfig->rightFp, &(diffConfig->maxLineLen));
    diffConfig->totalSize = diffConfig->leftLineCnt + diffConfig->rightLineCnt;
    diffConfig->arySize = (2U * diffConfig->totalSize + 1U);

    diffConfig->maxLineCnt = Max(diffConfig->leftLineCnt, diffConfig->rightLineCnt);

    diffConfig->leftLines = (char**)malloc(diffConfig->maxLineCnt * sizeof(char*));
    diffConfig->rightLines = (char**)malloc(diffConfig->maxLineCnt * sizeof(char*));

    diffConfig->leftOutp = (long long*)malloc(diffConfig->maxLineCnt * sizeof(long long));
    memset(diffConfig->leftOutp, NONE, diffConfig->maxLineCnt * sizeof(long long));
    diffConfig->rightOutp = (long long*)malloc(diffConfig->maxLineCnt * sizeof(long long));
    memset(diffConfig->rightOutp, NONE, diffConfig->maxLineCnt * sizeof(long long));
}


/**********************************************************************************
 * @brief
 * @param line1
 * @param line2
 * @return
 */
static inline Boolean_t lineEqual(char *line1, char *line2)
{
    return (strcmp(line1, line2) == 0) ? TRUE : FALSE;
}


/**********************************************************************************
 * @brief
 * @param diffConfig
 */
void loadFileLines(DiffConfig_t *diffConfig)
{
    /* Instead of allocating the entire line array at once, allocate an array of maximum
     * line length and read the chars into that, recording the size of the line when \n
     * is reached. Allocate an array of this size and store at the index in the
     * rightLines or leftLines array.
     *
     * This will significantly reduce memory usage.
     *
     */
    unsigned long i = 0U;
    size_t len = 0U;

    fseek(diffConfig->leftFp, 0, SEEK_SET);
    fseek(diffConfig->rightFp, 0, SEEK_SET);

    while (getline(&diffConfig->leftLines[i++], &len, diffConfig->leftFp) != NONE) {}
    //diffConfig->leftLines[diffConfig->maxLineCnt] = "$$ENDTOKEN$$";
    //printf("%d, %s\n", i, diffConfig->leftLines[i]);
    i = 0U;
    while (getline(&diffConfig->rightLines[i++], &len, diffConfig->rightFp) != NONE) {}
    //diffConfig->rightLines[diffConfig->maxLineCnt] = "$$ENDTOKEN$$";
    //
    //printf("%d, %s\n", i, diffConfig->rightLines[i]);


}


/**********************************************************************************
 * @brief
 * @param fp
 * @param maxLineLen
 * @return
 */
long long getFileLineCnt(FILE *fp, long long *maxLineLen)
{
    long long lineCnt = 0U;
    char lineChar = '$';    /* Placeholder char */
    long long charCnt = 0U;

    while (lineChar != EOF) {
        lineChar = (char)fgetc(fp);
        charCnt++;
        if (lineChar == EOL)
        {
            lineCnt++;
            *maxLineLen = Max(charCnt , *maxLineLen);
            charCnt = 0;
        }
    }

    lineCnt += (lineCnt == 0U ? 0U : 1U);
    return lineCnt;
}


/**********************************************************************************
 * @brief
 * @param diffConfig
 */
void freeDiffConfig(DiffConfig_t *diffConfig)
{
    if (diffConfig->leftOutp != NULL)
    {
        free(diffConfig->leftOutp);
    }
    if (diffConfig->rightOutp != NULL)
    {
        free(diffConfig->rightOutp);
    }
    if (diffConfig->leftFp != NULL)
    {
        fclose(diffConfig->leftFp);
    }
    if (diffConfig->rightFp != NULL)
    {
        fclose(diffConfig->rightFp);
    }
}


/**********************************************************************************
 * @brief
 * @param diffConfig
 */
void lcs(DiffConfig_t *diffConfig)
{
    unsigned long idx = 0;
    long x_idx = 0;
    long y_idx = 0;
    struct Snake_t *snake = (struct Snake_t*)malloc(sizeof(struct Snake_t));
    struct Snake_t *kLines[diffConfig->arySize];
    long boundedAry[diffConfig->arySize];
    long long totalSizeK = 0;
    memset(boundedAry, 0, diffConfig->arySize * sizeof(long));

    initSnake(snake);
    for (unsigned long r = 0; r < diffConfig->arySize; r++)
    {
        kLines[r] = (struct Snake_t*)malloc(sizeof(struct Snake_t));
        initSnake(kLines[r]);
    }

    for (long long d = 0; d < diffConfig->totalSize + 1; d++)
    {
        for (long long k = -d; k < (d + 1); k += 2)
        {
            totalSizeK = diffConfig->totalSize + k;

            if (k == -d
            || (k != d
            && boundedAry[totalSizeK - 1]
            < boundedAry[totalSizeK + 1]))
            {
                idx = totalSizeK + 1;
                x_idx = boundedAry[idx];
            }
            else
            {
                idx = totalSizeK - 1;
                x_idx = boundedAry[idx] + 1;
            }
            y_idx = x_idx - k;
            //snake = copySnake(kLines[idx]);
            snake = kLines[idx];

            while ((x_idx < diffConfig->leftLineCnt)
            && (y_idx < diffConfig->rightLineCnt)
            && lineEqual(diffConfig->leftLines[x_idx], diffConfig->rightLines[y_idx]))
            {
                //printSnake(snake);
                snake->tail = addSnakeHead(snake, x_idx, y_idx);
                x_idx++;
                y_idx++;
            }
            if ((x_idx >= diffConfig->leftLineCnt) && (y_idx >= diffConfig->rightLineCnt))
            {
                snake = snake->tail;
                while (snake != NULL)
                {
                    long long outp_idx = Max(snake->head[0], snake->head[1]);
                    diffConfig->rightOutp[outp_idx] = snake->head[0];
                    diffConfig->leftOutp[outp_idx] = snake->head[1];
                    snake = snake->tail;
                }
                return;
            }
            boundedAry[totalSizeK] = x_idx;
            kLines[totalSizeK] = copySnake(snake);
        }
    }
    if (snake != NULL)
    {
        free(snake);
    }
    free(kLines);
    free(boundedAry);
}


/**********************************************************************************
 * @brief
 * @param snake
 */
static inline void initSnake(struct Snake_t *snake)
{
    /* Check for NULL ptr and allocate memory if necessary  */
    if (snake == NULL) {
        snake = (struct Snake_t*)(malloc(sizeof(struct Snake_t)));
    }

    /* Set the values for the head indices to -1 to indicate no match   */
    snake->head[0U] = -1;
    snake->head[1U] = -1;
    snake->tail = NULL;
}


/**********************************************************************************
 * @brief
 * @param snake
 * @return
 */
struct Snake_t *copySnake(struct Snake_t *snake)
{
    struct Snake_t *current = snake;
    struct Snake_t *newSnake = NULL;
    struct Snake_t *tail = NULL;

    while (current != NULL)
    {
        if (newSnake == NULL)
        {
            newSnake = (struct Snake_t*)malloc(sizeof(struct Snake_t));
            newSnake->head[0] = current->head[0];
            newSnake->head[1] = current->head[1];
            newSnake->tail = NULL;
            tail = newSnake;
        }
        else
        {
            tail->tail = (struct Snake_t*)malloc(sizeof(struct Snake_t));
            tail = tail->tail;
            tail->head[0] = current->head[0];
            tail->head[1] = current->head[1];
            tail->tail = NULL;
        }
        current = current->tail;
    }
    return newSnake;
}


/**********************************************************************************
 * @brief
 * @param snake
 * @param x
 * @param y
 * @return
 */
static inline struct Snake_t *addSnakeHead(struct Snake_t *snake, long x, long y)
{
    struct Snake_t *newHead = (struct Snake_t*)(malloc(sizeof(struct Snake_t)));
    initSnake(newHead);
    newHead->head[0U] = x;
    newHead->head[1U] = y;
    newHead->tail = snake->tail;
    return newHead;
}


/**********************************************************************************
 * @brief
 * @param a
 * @param b
 * @return
 */
static inline long long Max(long long a, long long b)
{
    return (a > b ? a : b);
}


/**********************************************************************************
 * @brief
 * @param snake
 */
void printSnake(struct Snake_t *snake) {
    struct Snake_t *current = snake;
    while (current != NULL)
    {
        printf("(%lld, %lld)->", current->head[0], current->head[1]);
        current = current->tail;
    }
    printf("\n");
}


/**********************************************************************************
*       END OF FILE
**********************************************************************************/
