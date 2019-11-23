/**********************************************************************************
File: xml_writer.h
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

#ifndef MYERSLCS_XML_WRITER_H
#define MYERSLCS_XML_WRITER_H

/**********************************************************************************
*       HEADER FILES
**********************************************************************************/
#include<stdio.h>
#include<fcntl.h>
#include<errno.h>

/**********************************************************************************
*       DATA STRUCTURES/VARIABLE DECLARATIONS
**********************************************************************************/



/**********************************************************************************
*       FUNCTION DECLARATIONS/PROTOTYPES
**********************************************************************************/
void writeMatchTag(FILE *fd, long long left, long long right, long long idx);

void writeLCSOutpFile(
        char *rightFile,
        char*leftFile,
        char *outp_file,
        long *rightSet,
        long *leftSet,
        long size
);


#endif //MYERSLCS_XML_WRITER_H
/**********************************************************************************
*       END OF FILE
**********************************************************************************/
