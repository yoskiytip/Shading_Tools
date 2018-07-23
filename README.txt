# Maya Redshift texture processor
# Created by Roman Zhuk, 2018

EWorks with maya 2017 and later

Instruction:
1. Create a folder 'shading_tools_v01' in your .../documents/maya/scripts directory
2. Download all files to the 'shading_tools_v01' folder
3. In Maya, run from Script Editor (python mode) the following:

# For WINDOWS:
import sys
paths = sys.path
tool_path = 'C:/Users/.../Documents/maya/scripts/shading_tools_v01' # REPLACE ... WITH YOUR USER NAME
if tool_path not in paths:
    sys.path.append( tool_path )

import shading_tools_GUI
reload(shading_tools_GUI)

shading_tools_GUI.create()

# For Mac or Linux just replace the path with a corresponding format

4. Run


Using the tool:
1. Choose a folder with your textures
2. Fill up the fields with respective prefixes for your texture channels
3. Use 'Check Tex Sets' button to list all texture sets that were found
4. Use 'Process All' button to create shading networks from your textures


Warning:
This tool was made for my personal use. Some bugs may be found.
