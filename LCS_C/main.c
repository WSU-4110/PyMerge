#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h> // For exit() function
#include "myers_lcs.h"
#include "xml_writer.h"

#define LEFT_FILE_ARGV_IDX  1U
#define RIGHT_FILE_ARGV_IDX 2U
#define OUTP_FILE_ARGV_IDX 3U


int main(int argc, char *argv[])
{
    DiffConfig_t *diff = malloc(sizeof(DiffConfig_t));
    loadDiffConfig(diff, argv[LEFT_FILE_ARGV_IDX], argv[RIGHT_FILE_ARGV_IDX]);

    loadFileLines(diff);
    lcs(diff);

    writeLCSOutpFile(
                        argv[LEFT_FILE_ARGV_IDX],
                        argv[RIGHT_FILE_ARGV_IDX],
                        argv[OUTP_FILE_ARGV_IDX],
                        diff->leftOutp,
                        diff->rightOutp,
                        diff->maxLineCnt
                    );
    freeDiffConfig(diff);
    return 0;
}