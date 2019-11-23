/**********************************************************************************
File: xml_writer.c
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
#include "xml_writer.h"


/**********************************************************************************
*       DEFINES
**********************************************************************************/


/**********************************************************************************
*       FUNCTION IMPLEMENTATIONS
**********************************************************************************/

/**********************************************************************************
 * @brief
 * @param fd
 * @param left
 * @param right
 * @param idx
 */
inline void writeMatchTag(FILE *fd, long long left, long long right, long long idx)
{
    fprintf(fd, "\t\t<match left=\"%lld\" right=\"%lld\" index=\"%lld\"/>\n", left, right, idx);
}


/**********************************************************************************
 * @brief
 * @param rightFile
 * @param leftFile
 * @param rightSet
 * @param leftSet
 * @param size
 */
void writeLCSOutpFile(
        char *rightFile,
        char*leftFile,
        char *outp_file,
        long *rightSet,
        long *leftSet,
        long size
        )
{
    FILE *fd = fopen(outp_file, "w+");

    fprintf(fd, "<lcs_output>\n");
    fprintf(fd, "\t<meta>\n");
    fprintf(fd, "\t\t<left_file>%s</left_file>\n", leftFile);
    fprintf(fd, "\t\t<right_file>%s</right_file>\n", rightFile);
    fprintf(fd, "\t\t<line_length>%lld</line_length>\n", size);
    fprintf(fd, "\t</meta>\n");
    fprintf(fd, "\t<matches>\n");
    for (long long i = 0; i < size; i++)
    {
        writeMatchTag(fd, leftSet[i], rightSet[i], i);
    }
    fprintf(fd, "\t</matches>\n");
    fprintf(fd, "</lcs_output>\n");
    fclose(fd);
}



/**********************************************************************************
*       END OF FILE
**********************************************************************************/

