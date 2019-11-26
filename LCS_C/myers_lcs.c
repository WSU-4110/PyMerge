//
// Created by Malcolm Hall on 11/5/19.
//


/**********************************************************************************
*       HEADER FILES
**********************************************************************************/
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "myers_lcs.h"

/**********************************************************************************
*       DEFINES
**********************************************************************************/
#define NONE -1
#define EOL '\n'
#define TRUE 1U
#define FALSE 0U

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
    diffConfig->maxLineLength = 0U;
    diffConfig->leftLineCnt = getFileLineCnt(diffConfig->leftFp, &(diffConfig->maxLineLength));
    diffConfig->rightLineCnt = getFileLineCnt(diffConfig->rightFp, &(diffConfig->maxLineLength));
    diffConfig->totalSize = diffConfig->leftLineCnt + diffConfig->rightLineCnt;
    diffConfig->arraySize = (2U * diffConfig->totalSize + 1U);

    diffConfig->boundedArray = (long*)malloc(diffConfig->arraySize * sizeof(long));
    memset(diffConfig->boundedArray, 0U, diffConfig->arraySize * sizeof(long));

    diffConfig->kCandidates = (Snake_t**)malloc(diffConfig->arraySize * sizeof(Snake_t*));

//    for (unsigned long i = 0; i < diffConfig->maxLineCnt; i++)
//    {
//        initSnake(diffConfig->kCandidates[i]);
//    }

    diffConfig->maxLineCnt = Max(diffConfig->leftLineCnt, diffConfig->rightLineCnt);

    diffConfig->leftLines = (char**)malloc(diffConfig->maxLineCnt * sizeof(char*));
    diffConfig->rightLines = (char**)malloc(diffConfig->maxLineCnt * sizeof(char*));

    diffConfig->leftOutp = (long*)malloc(diffConfig->maxLineCnt * sizeof(long));
    memset(diffConfig->leftOutp, NONE, diffConfig->maxLineCnt * sizeof(long));
    diffConfig->rightOutp = (long*)malloc(diffConfig->maxLineCnt * sizeof(long));
    memset(diffConfig->rightOutp, NONE, diffConfig->maxLineCnt * sizeof(long));
}


/**********************************************************************************
 * @brief
 * @param line1
 * @param line2
 * @return
 */
Boolean_t lineEqual(char *line1, char *line2, long maxSize)
{
//    Boolean_t equal = TRUE;
//    uint32_t i = 0U;
//
//    if ((line1 == NULL) && (line2 == NULL))
//    {
//        equal = TRUE;
//    }
//    else if ((line1 != NULL) && (line2 != NULL)) {
//        while ((*line1 != EOL) && (*line2 != EOL) && equal && (i < maxSize))
//        {
//            printf("%c", *line1);
//            equal = (Boolean_t)(*(line1++) == *(line2++));
//            i++;
//        }
//    }
//    else
//    {
//        equal = FALSE;
//    }
//    return equal;

    if (strcmp(line1, line2) == 0)
    {
        return TRUE;
    }
    else
    {
        return FALSE;
    }
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

    while (getline(&diffConfig->leftLines[i], &len, diffConfig->leftFp) != NONE) {
        printf("%s", diffConfig->leftLines[i]);
        i++;
    }

    i = 0U;
    while (getline(&diffConfig->rightLines[i], &len, diffConfig->rightFp) != NONE) {
        printf("%s", diffConfig->rightLines[i]);
        i++;
    }
}


/**********************************************************************************
 * @brief
 * @param fp
 * @param maxLineLen
 * @return
 */
unsigned long getFileLineCnt(FILE *fp, unsigned long *maxLineLen)
{
    unsigned long lineCnt = 0U;
    char lineChar = '$';    /* Placeholder char */
    unsigned long charCnt = 0U;

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
 * @param array
 * @param size
 */
inline void reverseArray(long *array, unsigned long size)
{
    unsigned long i = Max(size - 1U, 0U);
    unsigned long j = 0U;
    long tmp = 0;

    while (i > j)
    {
        tmp = array[i];
        array[i] = array[j];
        array[j] = tmp;
        i--;
        j++;
    }
}


/**********************************************************************************
 * @brief
 * @param diffConfig
 */
void freeDiffConfig(DiffConfig_t *diffConfig)
{
    if (diffConfig->boundedArray != NULL)
    {
        free(diffConfig->boundedArray);
    }
    if (diffConfig->kCandidates != NULL)
    {
        free(diffConfig->kCandidates);
    }
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


void lcs(DiffConfig_t *diffConfig)
{
    int match_idx[2] = {-1};
    long k = NONE;
    unsigned long idx = 0;
    long x_idx = 0;
    long y_idx = 0;
    Snake_t *snake;
    long i = 0;

    for (long long d = 0; d < diffConfig->totalSize + 1; d++)
    {
        k = 0 - d;
        while (k < (d + 1))
        {
            if (k == -d
            || (k != d
            && diffConfig->boundedArray[diffConfig->totalSize + k - 1]
            < diffConfig->boundedArray[diffConfig->totalSize + k + 1]))
            {
                idx = diffConfig->totalSize + k + 1;
                x_idx = diffConfig->boundedArray[idx];
            }
            else
            {
                idx = diffConfig->totalSize + k - 1;
                x_idx = diffConfig->boundedArray[idx] + 1;
            }
            y_idx = x_idx - k;
            snake = diffConfig->kCandidates[idx];

            /*
             *
             while x_idx < len(left_set) and y_idx < len(right_set) and left_set[x_idx] == right_set[y_idx]:
                snake = ((x_idx, y_idx), snake)
                x_idx += 1
                y_idx += 1
            if x_idx >= len(left_set) and y_idx >= len(right_set):
                while snake:
                    outp[0].append(snake[0][0])
                    outp[1].append(snake[0][1])
                    snake = snake[1]
                outp[0].reverse()
                outp[1].reverse()
                return outp
            bounded_array[total_size + k] = x_idx
            k_candidates[total_size + k] = snake
            print(snake)
             */

            while ((x_idx < diffConfig->leftLineCnt)
            && (y_idx < diffConfig->rightLineCnt)
            && lineEqual(diffConfig->leftLines[x_idx], diffConfig->rightLines[y_idx], 0))
            {
                addSnakeHead(snake, x_idx, y_idx);
                x_idx++;
                y_idx++;
            }
//            if ((x_idx >= diffConfig->leftLineCnt) && (y_idx >= diffConfig->rightLineCnt))
//            {
//                while (snake->body != NULL)
//                {
//                    diffConfig->rightOutp[i++] = snake->head[0];
//                    diffConfig->leftOutp[i++] = snake->head[1];
//                    snake = snake->body;
//                }
//            }
            diffConfig->boundedArray[diffConfig->totalSize + k] = x_idx;
            diffConfig->kCandidates[diffConfig->totalSize + k] = snake;

            k += 2;
        }
    }
}


void initSnake(Snake_t *snake)
{
    snake->head = (unsigned long*)(malloc(2 * sizeof(unsigned long)));
    snake->head[0] = -2;
    snake->head[1] = -2;
    snake->body = NULL;
}

void addSnakeHead(Snake_t *snake, long x, long y)
{
    Snake_t *newHead = (Snake_t*)(malloc(sizeof(Snake_t)));
    newHead->head[0] = x;
    newHead->head[1] = y;
    newHead->body = snake->body;
    snake->body = newHead;
}

void removeSnakeHead(Snake_t *snake)
{
    Snake_t *oldHead = snake;
    snake = snake->body;
    free(oldHead);
}


static inline unsigned long Max(unsigned long a, unsigned long b)
{
    return (a > b ? a : b);
}


/**********************************************************************************
*       END OF FILE
**********************************************************************************/
