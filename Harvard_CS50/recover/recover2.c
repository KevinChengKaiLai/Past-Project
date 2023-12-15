#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s forensic_image\n", argv[0]);
        return 1;
    }

    // Open the forensic image file for reading
    FILE *file = fopen(argv[1], "rb");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open forensic image for reading.\n");
        return 1;
    }

    BYTE buffer[512];
    int jpeg_count = 0;
    FILE *jpeg_file = NULL;

    while (1)
    {
        size_t bytesRead = fread(buffer, 1, 512, file);

        if (bytesRead == 0)
            break;

        // Check for the JPEG signature
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0)
        {
            // If we've already found a JPEG, close it
            if (jpeg_file)
                fclose(jpeg_file);

            // Create a new JPEG file
            char filename[8];
            sprintf(filename, "%03d.jpg", jpeg_count);
            jpeg_count++;
            jpeg_file = fopen(filename, "wb");

            if (jpeg_file == NULL)
            {
                fprintf(stderr, "Could not create JPEG file.\n");
                return 1;
            }
        }

        // Write to the current JPEG file
        if (jpeg_file)
            fwrite(buffer, 1, bytesRead, jpeg_file);
    }

    // Close the last JPEG file
    if (jpeg_file)
        fclose(jpeg_file);

    // Close the input file
    fclose(file);

    return 0;
}
