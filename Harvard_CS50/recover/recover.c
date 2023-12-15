#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>



typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check for correct usage
    if (argc != 2)
    {
        printf("input should be two\n");
        return 1;
    }

    // Open the file for reading
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 4;
    }



    // repeat until end of card
        // read 512 bytes into a buffer
        // If start of new jpg
    BYTE block[512];
    int jpeg_count = 0;
    FILE * jpeg_file = NULL;

    while (1)
    {
        size_t byteread = fread(block, 1, 512, file);
        // after reading break the loop
        if (byteread == 0)
        {
            break;
        }

        // check the jpeg file signature
        if (block[0] == 0xFF && block[1] == 0xD8 &&
            block[2] == 0xFF && (block[3] & 0xF0) == 0xE0)
        {
             // Close the previous JPEG file if it was open
            if (jpeg_file)
            {
                fclose(jpeg_file);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", jpeg_count);
            jpeg_count ++;
            jpeg_file = fopen(filename, "w");
        }

        // write the file into new file
        if (jpeg_file)
        {
            fwrite(block, 1, byteread, jpeg_file);
        }
    }

    //Close the last file
    if (jpeg_file)
    {
        fclose(jpeg_file);
    }
    // close the file
    fclose(file);
}