#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            float greyness = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed)/3.0;
            int round_greyness = round(greyness);
            image[i][j].rgbtBlue = round_greyness;
            image[i][j].rgbtGreen = round_greyness;
            image[i][j].rgbtRed = round_greyness;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            float Blue= (float) image[i][j].rgbtBlue;
            float Green = (float) image[i][j].rgbtGreen;
            float Red = (float) image[i][j].rgbtRed;
            int sepiaRed = round(0.393 * Red + 0.769 * Green + 0.189 * Blue);
            int sepiaGreen = round(0.349 * Red + 0.686 * Green + 0.168 * Blue);
            int sepiaBlue = round(0.272 * Red + 0.534 * Green + 0.131 * Blue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;



        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE (*copy)[width] = malloc(height * sizeof(RGBTRIPLE[width]));
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][width - 1 - j];
        }
        for ( int k = 0; k < width; k++)
        {
            image[i][k] = copy[i][k];
        }
    }

    free(copy);
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE (*copy)[width] = malloc(height * sizeof(RGBTRIPLE[width]));
    for (int i = 0; i < height ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int k = 1; k < height-1 ; k++)
    {
        for (int l = 1; l < width-1 ; l++)
        {
            image[k][l].rgbtBlue = (float)((copy[k - 1][l - 1].rgbtBlue + copy[k - 1][l].rgbtBlue + copy[k - 1][l + 1].rgbtBlue +
                                   copy[k][l - 1].rgbtBlue + copy[k][l].rgbtBlue + copy[k][l + 1].rgbtBlue +
                                   copy[k + 1][l - 1].rgbtBlue + copy[k + 1][l].rgbtBlue + copy[k + 1][l + 1].rgbtBlue ) )/ 9.0;
            image[k][l].rgbtBlue = round(image[k][l].rgbtBlue);
            image[k][l].rgbtGreen = (float)((copy[k - 1][l - 1].rgbyetGreen + copy[k - 1][l].rgbtGreen + copy[k - 1][l + 1].rgbtGreen +
                                   copy[k][l - 1].rgbtGreen + copy[k][l].rgbtGreen + copy[k][l + 1].rgbtGreen +
                                   copy[k + 1][l - 1].rgbtGreen + copy[k + 1][l].rgbtGreen + copy[k + 1][l + 1].rgbtGreen )) / 9.0;
            image[k][l].rgbtGreen = round(image[k][l].rgbtGreen);
            image[k][l].rgbtRed = (float)((copy[k - 1][l - 1].rgbtRed + copy[k - 1][l].rgbtRed + copy[k - 1][l + 1].rgbtRed +
                                   copy[k][l - 1].rgbtRed + copy[k][l].rgbtRed + copy[k][l + 1].rgbtRed +
                                   copy[k + 1][l - 1].rgbtRed + copy[k + 1][l].rgbtRed + copy[k + 1][l + 1].rgbtRed )) / 9.0;
            image[k][l].rgbtRed = round(image[k][l].rgbtRed);
        }
    }

    image[0][0].rgbtBlue = ((copy[0][0].rgbtBlue + copy[0][1].rgbtBlue + copy[1][0].rgbtBlue +
                            copy[1][1].rgbtBlue)/4);
    image[0][0].rgbtGreen = ((copy[0][0].rgbtGreen + copy[0][1].rgbtGreen + copy[1][0].rgbtGreen +
                            copy[1][1].rgbtGreen)/4);
    image[0][0].rgbtRed = ((copy[0][0].rgbtRed + copy[0][1].rgbtRed + copy[1][0].rgbtRed +
                            copy[1][1].rgbtRed)/4);


    free(copy);
    return;
}
