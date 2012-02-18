# Brock Anderson 2012
# Released to public domain 

import Image
import argparse

BLACK_THRESHOLD  = 128    # degree of blackness at which the pixel is considered on / black

# defaults that may be affected by arguments that are passed
DEFAULT_SCREEN_PAGES       =   8    # number of pages the screen is broken into vertically
DEFAULT_SCREEN_COLUMNS     = 128    # number of columns wide the screen is
DEFAULT_BITS_HIGH_PER_PAGE =   8    # number of rows high a page is

# parse command line arguments
parser = argparse.ArgumentParser(description = 'Top level command line parser for bitmap-ST7565R.py')
parser.add_argument('input_bmp', metavar='bitmap', nargs=1
                    help = 'black and white bitmap file to convert to C style array for lcd')
parser.add_argument('output_header', metavar='header', type=argparse.FileType('w'), default = 'graphics_arrays.h', nargs=1
                     help = 'Header file in which to save lcd data array')
parser.add_argument('--pages', type=int, nargs='?', default=DEFAULT_SCREEN_PAGES
                     help = 'Number of pages the lcd screen is vertically divided into')
parser.add_argument('--columns' type=int, nargs='?', default=DEFAULT_SCREEN_COLUMNS
                     help = 'Number of columns')

prog_args = parser.parse_args()

# test output
print prog_args
		
# load data needed for bitmap processing loop		
screen_pages       = prog_args['pages']
screen_columns     = prog_args['columns']
bits_high_per_page = DEFAULT_BITS_HIGH_PER_PAGE

# load bitmap
im = Image.open(input_bmp);

# load the pixel data into an array object
pix=im.getdata()


# convert the pixel array to a c array that can be directly placed in a header file with appropriate loaded const data
for page in range(screen_pages):
   print "unsigned const char graphics" + str(page) + "[] = { "
   for column in range(screen_columns):
       out = 0;
       for bit in range(bits_high_per_page):
           pixel_num = screen_columns * ( bits_high_per_page * page + bit) + column
           pixel_val = pix[pixel_num]
           if pixel_val < BLACK_THRESHOLD:
               out = out + (1 << bit)
       # printf("%x , \n", out)
       print "                              " + str(out) + ","

   print "                            }; "


       

