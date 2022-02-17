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
      FileSelectionWindow: Select PDB
        MultipleSelections: No
        Filename: pdb/*.pdb
      Request: LoadPepSurfPDB
MainMenu: View
  PullDownMenu after Atom apperance: _P_epSurf
    SubMenu: _V_iew PepSurf Clusters
      Request: ViewPepSurfPDB
"""

import yasara
import re

from container import *

if (yasara.storage==None):
    yasara.storage=container()
    yasara.storage.objects = {}
    print("Creating Storage...")
else:
    print("Storage Container Exists...")

class pepsurf():

    background_color = 'white'
    color_carbon = 'C8C8C8'
    color_sulfur = 'FFC832'
    color_phosphorus = 'FFA500'
    base_color = 'gray'
    color_chain = ['808080','B0B0B0','E0E0E0']
    cluster_color = ['FF6060','8080FF','FF40FF']

    def __init__(self, input=None, parms=None):

        self.input = input
        self.job_parms = {}

        if yasara.storage.objects:
            print("Object Exists...")
            self.input = None
            self.job_parms.update(parms)
        else:
            print("Creating new PepSurfPDB Object...")
            yasara.Clear()
            yasara.LoadPDB(self.input)
#           yasara.ZoomAll()
            self.extract_pepsurf_data(self.input)
            yasara.NameObj(1, self.job_parms['pepsurf_pdb_id'].upper())

    def extract_pepsurf_data(self, input):
        with open(self.input, mode='r') as f:
            for line in f:
                if "!" in line:
                    if "pepsurf_version" in line:
                        self.job_parms['pepsurf_version'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_run_number" in line:
                        self.job_parms['pepsurf_run_number'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_run_date" in line:
                        self.job_parms['pepsurf_run_date'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_pdb_id" in line:
                        self.job_parms['pepsurf_pdb_id'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_chains" in line and ";" in line:
                        self.job_parms['pepsurf_chains'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_identical_chains" in line:
                        self.job_parms['pepsurf_identical_chains'] = re.findall('"([^"]*)"', line)[0]
                    if "pepsurf_cluster_count" in line:
                        self.job_parms['pepsurf_cluster_count'] = line[-2:-1]

    def extract_pepsurf_clusters(self):
        pass

    def color_pdf_default(self):
        print("Setting Default Colors...")
        yasara.HideAll()
        yasara.ColorBG(self.background_color)
        yasara.ColorAll(self.color_carbon)
        return

    def display_pdb_chains(self, pepsurf_chains):
        self.color_pdf_default()
        for inx, chain in enumerate(pepsurf_chains):
            print(chain)
            yasara.ColorMol(chain + " and !HetGroup", self.color_chain[inx])
        return

try:
    if yasara.request=="LoadPepSurfPDB":
        if yasara.storage.objects:
            print("Storage Exists...")
            # Clear storage for new PDB Loading...
            yasara.Clear()
            yasara.storage.objects = {}
        else:
            print("Load Storage...")
            p = pepsurf(yasara.selection[0].filename[0])
#            yasara.storage.objects.append(p)
            yasara.storage.objects.update(p.job_parms)
            print(p.job_parms)
            print("Loading Complete...")

    if yasara.request=="ViewPepSurfPDB":
        print("ViewPepSurfPDB...")
        if yasara.storage.objects:
            print("Loading PepSurfPDB Parameters...")
#            p = pepsurf(yasara.storage.objects[0])
            p = pepsurf(parms = yasara.storage.objects)
            print(p.job_parms)
            p.display_pdb_chains(p.job_parms["pepsurf_chains"])
        else:
            print("Error: Need to load a PepSurfPDB...")
except:
    yasara.plugin.end("Unknown request: {}".format(yasara.request))

# Stop the Plugin
yasara.plugin.end()
