#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dxfgrabber, argparse, string, sys

parser = argparse.ArgumentParser(description='Openscad dxf parser options.')
parser.add_argument('--width', type=float, nargs=1, required=True, help='Track width')
parser.add_argument('inputfile', default='None', help='Input file')
parser.add_argument('outputfile', default='None', help='Input file')
args = parser.parse_args()

if args.inputfile == 'None' or args.outputfile == 'None':
    parser.print_help()
    sys.exit(-1)

# Text for the file header, the parameter is the name of the module, ex "LOGO".
header = """(module %(name)s
"""

# Text for the file footer, the only parameter is the name of the module
footer = """)
"""

# draw a line
# (from http://www.compuphase.com/electronics/LibraryFileFormats.pdf)
def make_line(x0, y0, x1, y1):
    return """  (fp_line
    (start %(0)s %(1)s)
    (end %(2)s %(3)s)
    (layer Edge.Cuts)
    (width %(4)0.2f)
  )
""" % {"0":x0, "1":y0, "2":x1, "3":y1, "4":args.width[0]}

def conv_dxf_to_module(module_name, entities):
    module = header % {"name": module_name}
    for entity in entities:
        if entity.dxftype == "LINE":
            module += make_line(entity.start[0], entity.start[1], entity.end[0], entity.end[1])
    module += footer % {"name": module_name}
    return module


dxf = dxfgrabber.readfile(args.inputfile)
header_var_count = len(dxf.header) 
layer_count = len(dxf.layers) 
entity_count = len(dxf.entities) 
outfile=open(args.outputfile, 'w')
outfile.write(conv_dxf_to_module("DP5050", dxf.entities))
outfile.close()
