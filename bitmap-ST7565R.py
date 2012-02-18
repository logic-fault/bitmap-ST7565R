# Brock Anderson 2012
# Released to public domain 

import Image
import argparse

# load bitmap
im = Image.open("C:\src\micro\lcd_img\main_test.bmp");

# load the pixel data into an array object
pix=im.getdata()

SCREEN_PAGES       =   8    # number of pages the screen is broken into vertically
SCREEN_COLUMNS     = 128    # number of columns wide the screen is
BITS_HIGH_PER_PAGE =   8    # number of rows high a page is
BLACK_THRESHOLD    = 128    # degree of blackness at which the pixel is considered on / black


# convert the pixel array to a c array that can be directly placed in a header file with appropriate loaded const data
for page in range(0, SCREEN_PAGES):
   print "unsigned const char graphics" + str(page) + "[] = { "
   for column in range(SCREEN_COLUMNS):
       out = 0;
       for bit in range(BITS_HIGH_PER_PAGE):
           pixel_num = SCREEN_COLUMNS * ( BITS_HIGH_PER_PAGE * page + bit) + column
           pixel_val = pix[pixel_num]
           if pixel_val < BLACK_THRESHOLD:
               out = out + (1 << bit)
       # printf("%x , \n", out)
       print "                              " + str(out) + ","

   print "                            }; "


       

