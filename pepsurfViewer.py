# YASARA PLUGIN
# TOPIC:
# TITLE:        PepSurfViewer
# REQUIRES:     Viewer
# AUTHOR:       James W. Gillespie
# LICENSE:
# DESCRIPTION:
#
#===============================================================================
"""
MainMenu: File
  PullDownMenu: Load
    SubMenu after Electrostatic potential map: P_e_pSurf PDB file
      Request: LoadPepSurfPDB
MainMenu: View
  PullDownMenu after Atom apperance: _P_epSurf
    SubMenu: _V_iew PepSurf Clusters
      Request: ViewPepSurfPDB
"""

import yasara

try:
    if yasara.request=="ViewPepSurfPDB":
        yasara.ShowMessage("Hello from PepSurfViewer!")
    if yasara.request=="LoadPepSurfPDB":
        yasara.ShowMessage("Load PepSurf PDB File...")
except:
    yasara.plugin.end("Unknown request: {}".format(yasara.request))

# Stop the Plugin
yasara.plugin.end()
