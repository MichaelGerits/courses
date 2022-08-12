#include "helpers.h"
#include <math.h>


// Convert image to grayscale (works)
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        for (int collumn = 0; collumn < width; collumn++)
        {
            int blue_val = image[row][collumn].rgbtBlue;
            int green_val = image[row][collumn].rgbtGreen;
            int red_val = image[row][collumn].rgbtRed;
            int average_val = round((blue_val + green_val + red_val)/3.00);

            if (average_val > 255)
            {
                average_val = 255;
            }

            image[row][collumn].rgbtBlue = average_val;
            image[row][collumn].rgbtGreen = average_val;
            image[row][collumn].rgbtRed = average_val;
        }
    }
    return;
}
void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}
// Reflect image horizontally (works)
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        for (int collumn = 0; collumn < width / 2; collumn++)
        {
            swap(&image[row][collumn], &image[row][width - collumn - 1]);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image_copy[height][width];
    for (int row = 0; row < height; row++)
    {
        for (int collumn = 0; collumn < width; collumn++)
        {
            image_copy[row][collumn] = image[row][collumn];
        }
    }
    //go through each row
    for (int row = 0; row < height; row++)
    {
        //go through each collumn
        for (int collumn = 0; collumn < width; collumn++)
        {
            float sum_blue;
            float sum_green;
            float sum_red;
            int n_count;
            sum_blue = sum_green = sum_red = n_count = 0;

            // For each pixel, loop vertical and horizontal
            for (int box_row = -1; box_row < 2; box_row++)
            {
                for (int box_collumn = -1; box_collumn < 2; box_collumn++)
                {
                    // Check if pixel is outside rows
                    if (row + box_row < 0 || row + box_row >= height)
                    {
                        continue;
                    }
                    // Check if pixel is outside columns
                    if (collumn + box_collumn < 0 || collumn + box_collumn >= width)
                    {
                        continue;
                    }
                    // Otherwise add to sums
                    sum_red += image_copy[row + box_row][collumn + box_collumn].rgbtRed;
                    sum_blue += image_copy[row + box_row][collumn + box_collumn].rgbtBlue;
                    sum_green += image_copy[row + box_row][collumn + box_collumn].rgbtGreen;
                    n_count++;
                }

            }
            // Get average and blur image
            image[row][collumn].rgbtRed = round(sum_red / n_count);
            image[row][collumn].rgbtGreen = round(sum_green / n_count);
            image[row][collumn].rgbtBlue = round(sum_blue / n_count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //set up Gx matrix
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

    //set up Gy matrix
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    //set up copy of image
    RGBTRIPLE image_copy[height][width];
    for (int row = 0; row < height; row++)
    {
        for (int collumn = 0; collumn < width; collumn++)
        {
            image_copy[row][collumn] = image[row][collumn];
        }
    }

    //go through each row
    for (int row = 0; row < height; row++)
    {
        //go through each collumn
        for (int collumn = 0; collumn < width; collumn++)
        {

            //set up channel values and pixels counter
            float gx_blue = 0;
            float gx_green = 0;
            float gx_red = 0;
            float gy_blue = 0;
            float gy_green = 0;
            float gy_red = 0;
            // For each pixel, loop vertical and horizontal
            for (int box_row = -1; box_row < 2; box_row++)
            {
                for (int box_collumn = -1; box_collumn < 2; box_collumn++)
                {
                    // Check if pixel is outside rows
                    if (row + box_row < 0 || row + box_row >= height)
                    {
                        continue;
                    }
                    // Check if pixel is outside columns
                    if (collumn + box_collumn < 0 || collumn + box_collumn >= width)
                    {
                        continue;
                    }

                    gx_red += image_copy[row + box_row][collumn + box_collumn].rgbtRed * Gx[1 + box_row][1 + box_collumn];
                    gx_green += image_copy[row + box_row][collumn + box_collumn].rgbtGreen * Gx[1 + box_row][1 + box_collumn];
                    gx_blue += image_copy[row + box_row][collumn + box_collumn].rgbtBlue * Gx[1 + box_row][1 + box_collumn];

                    gy_red += image_copy[row + box_row][collumn + box_collumn].rgbtRed * Gy[1 + box_row][1 + box_collumn];
                    gy_green += image_copy[row + box_row][collumn + box_collumn].rgbtGreen * Gy[1 + box_row][1 + box_collumn];
                    gy_blue += image_copy[row + box_row][collumn + box_collumn].rgbtBlue * Gy[1 + box_row][1 + box_collumn];
                }

            }
            // ccalculates the new values
            int red_val = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            if (red_val > 255)
            {
                red_val = 255;
            }

            int green_val = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            if (green_val > 255)
            {
                green_val = 255;
            }

            int blue_val = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            if (blue_val > 255)
            {
                blue_val = 255;
            }

            image[row][collumn].rgbtRed = red_val;
            image[row][collumn].rgbtGreen = green_val;
            image[row][collumn].rgbtBlue = blue_val;
        }
    }
    return;
}
