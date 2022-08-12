// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    //sets an input pointer for the input file to read from
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    //set a pointer for the output file to write to.
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    //defines a var that defines our volume factor
    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    uint8_t* header = malloc(sizeof(uint8_t) * HEADER_SIZE);
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);
    free(header);

    // TODO: Read samples from input file and write updated data to output file
    int16_t *byte = malloc(sizeof(int16_t));
    while (fread(byte, sizeof(int16_t), 1, input))
    {
        int16_t newByte = *byte * factor;
        fwrite(&newByte, sizeof(int16_t), 1, output);
    }
    free(byte);


    // Close files
    fclose(input);
    fclose(output);
}
