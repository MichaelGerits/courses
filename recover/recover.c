#include <stdio.h>
#include <stdlib.h>
#include<stdint.h>

int main(int argc, char *argv[])
{
    //checks for the correct amount of arguments.
    if (argc != 2)
    {
        printf("Usage: ./recover <forensic image>\n");
        return 1;
    }
    //checks if it can open the file.
    FILE *raw_card = fopen(argv[1], "r");
    if (raw_card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    // initializes some variables and pointers
    typedef uint8_t BYTE;
    int file_count = 0;
    char *file_name = malloc(sizeof(char) * 8);
    FILE *jpg = NULL;
    //allocates memory for our scan block (a jpeg is a mltitude of 512 bytes)
    BYTE *block = malloc(sizeof(BYTE) * 512);
    //goes through each of bytes block in our forensic image
    while (fread(block, sizeof(BYTE) * 512, 1, raw_card) == 1)
    {
        //checks if the block is a start of a new jpg                checks the first bits of the fourth byte
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            //closes previous jpg
            if (file_count > 0)
            {
                fclose(jpg);
            }
            file_count++;
            //opens new jpg with appropriate name.
            sprintf(file_name, "%03i.jpg", file_count - 1);
            jpg = fopen(file_name, "w");
            //writes the block of data to the new jpg
            fwrite(block, sizeof(BYTE) * 512, 1, jpg);

        }
        // if the current jpeg is longer than one block => checks if there even is a file and then adds that block of data
        else if (file_count > 0)
        {
            fwrite(block, sizeof(BYTE) * 512, 1, jpg);
        }
    }
    //closes the final jpg and free's any allocated data left.
    fclose(jpg);
    free(block);
    free(file_name);
}