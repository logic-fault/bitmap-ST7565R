# Brock Anderson 2012
# Released to public domain 

# Designed for dogm-128 lcd screens
#    http://www.lcd-module.com/eng/pdf/grafik/dogm128e.pdf
#
# alternatively, should be generically compatible with any st7565R driven lcd
#    http://www.gpegint.com/files/library/files/supportpdf/ST7565R_V17_960601.pdf

import Image
import argparse
import sys

BLACK_THRESHOLD  = 128    # degree of blackness at which the pixel is considered on / black

# defaults that may be affected by arguments that are passed
DEFAULT_SCREEN_PAGES       =   8    # number of pages the screen is broken into vertically
DEFAULT_SCREEN_COLUMNS     = 128    # number of columns wide the screen is
DEFAULT_BITS_HIGH_PER_PAGE =   8    # number of rows high a page is

# parse command line arguments
parser = argparse.ArgumentParser(description = 'Top level command line parser for bitmap-ST7565R.py')
parser.add_argument('input_bmp', metavar='bitmap', type=argparse.FileType('rb'), nargs=1,
                    help = 'black and white input bitmap')
parser.add_argument('output_header', metavar='header', type=argparse.FileType('w'), default = 'graphics_arrays.h', nargs=1,
                     help = 'output header file (contains graphics array)')
parser.add_argument('--pages', type=int, nargs='?', default=DEFAULT_SCREEN_PAGES,
                     help = 'pages lcd screen is vertically divideded into')
parser.add_argument('--columns', type=int, nargs='?', default=DEFAULT_SCREEN_COLUMNS,
                     help = 'width of lcd screen in columns')

prog_args = parser.parse_args()
		
# load data needed for bitmap processing loop		
screen_pages       = prog_args.pages
screen_columns     = prog_args.columns
bits_high_per_page = DEFAULT_BITS_HIGH_PER_PAGE
bmp_in     = prog_args.input_bmp[0]
header_out = prog_args.output_header[0]

# load bitmap
im = Image.open(bmp_in);

#check dimensions
size = im.size
if size[0] < screen_columns:
   sys.exit("Error: image not wide enough.  width=" + str(size[0]) +
            "px.  Must be at least " + str(screen_columns) + "px")
elif size[0] > screen_columns:
   print "Warning: truncating image width from " + str(size[0]) + "px to " + str(screen_columns) + 'px .'
  
if size[1] < screen_pages * bits_high_per_page:
   sys.exit("Error: image not high enough.  height=" + str(size[0]) +
            "px.  Must be at least " + str(screen_pages * bits_high_per_page) + "px")
elif size[1] > screen_pages * bits_high_per_page:
   print "Warning: truncating image height from " + str(size[1]) +  "px to " + str(screen_pages * bits_high_per_page) + "px ."
   
#clip image to size
im = im.crop( [0, 0, screen_columns, screen_pages * bits_high_per_page])

# load the pixel data into an array object
pix=im.getdata()

header_def = str(header_out.name.split('.')[0]).upper() + "_H"
header_out.write("#ifndef " + header_def + "\n")
header_out.write("#define " +  header_def + "\n\n")
accessor_str = "unsigned const char * graphics_" + str(header_out.name.split('.')[0]) + " [] = {"

# process the bitmap
for page in range(screen_pages):
   variable_name = "graphics_" + str(header_out.name.split('.')[0]) + "_" + str(page)
   header_out.write("unsigned const char " +  variable_name  + "[] = { \n" )
   for column in range(screen_columns):
       out = 0;
       for bit in range(bits_high_per_page):
           pixel_num = screen_columns * ( bits_high_per_page * page + bit) + column
           pixel_val = pix[pixel_num]
           if pixel_val < BLACK_THRESHOLD:
               out = out + (1 << bit)
       header_out.write( "                                   " + str(out) + ",\n" )	   
   header_out.write( "                                  }; \n" )
   accessor_str += variable_name + ", "
accessor_str += " };"
header_out.write(accessor_str + "\n")
header_out.write("#endif /* " + header_def + " */ \n")
   
   



       

