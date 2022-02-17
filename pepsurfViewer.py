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
from collections import defaultdict

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
            self.job_parms['cluster_paths'] = self.extract_pepsurf_clusters(self.input, self.job_parms['pepsurf_cluster_count'])
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

    def extract_pepsurf_clusters(self, input, num_clust):
        c = 1
        cluster_paths = {}
        print_state = False
        with open(self.input, mode='r') as f:
            print("Opened file...")
            for line in f:
                if "!" in line and "#name=select_cluster" in line:
                    cluster=[]
                    cluster_paths[c]=cluster
                    c+=1
                    print_state = True
                elif "!!---------" in line:
                    print_state = False
                elif "====== END OF PEPSURF PiPE BLOCK ======" in line:
                    break
                elif print_state:
                    line_add = line.replace("select", "").replace("ed or ", "").replace("!  ", "").rstrip().split(", ")
                    for item in line_add:
                        if "!" in item:
                            pass
                        else:
                            cluster.append(item)
        return cluster_paths

    def color_pdb_default(self):
        print("Setting Default Colors...")
        yasara.HideAll()
        yasara.ColorBG(self.background_color)
        yasara.ColorAll(self.color_carbon)
        return

    def display_pdb_chains(self, pepsurf_chains):
        self.color_pdb_default()
        for inx, chain in enumerate(pepsurf_chains):
            print(chain)
            yasara.ColorMol(chain + " and !HetGroup", self.color_chain[inx])
        return

    def display_pepsurf_clusters(self, pepsurf_chains, cluster_paths):
        s = self.select_chain_members(cluster_paths)
        self.color_clusters(pepsurf_chains, s)
        return

    def select_chain_members(self, cluster_paths):
        selection = {}
        for cluster in cluster_paths:
            cluster_select = defaultdict(list)
#            print(cluster_paths[cluster])
            for item in cluster_paths[cluster]:
                c = self.id_pdb_chain(item)
                a = self.id_aa_residue(item)
                p = self.id_aa_pos(item)
                cluster_select[c].append(a + " " + p)
            selection[cluster] = cluster_select
#        print(selection)
        return selection

    def id_pdb_chain(self, item):
        return item.split(':')[-1]

    def id_aa_residue(self, item):
        return item.split(':')[0][0:3]

    def id_aa_pos(self, item):
        return item.split(':')[0][3:]

    def color_clusters(self, chains, selection):
        print("Coloring...")
        for idx, item in enumerate(selection):
#            print(selection) # Gives all clusters
            print(item) #Gives Cluster Number
#            print(selection[item]) # Gives each cluster individually
            for j, k in selection[item].items():
                print(j) # Gives Mol Chain
                print(k) # Gives list of residues
                for i in k:
                    print(i)
                    yasara.SelectRes(i + " and Mol " + j, mode='add')
            yasara.ColorRes('selected', self.cluster_color[item-1])
            yasara.DuplicateRes('selected')
            yasara.ColorObj(item+1, self.cluster_color[item-1])
            yasara.NameObj(item+1,"Cluster " + str(item))
            yasara.UnselectAll()
        return

try:
    if yasara.request=="LoadPepSurfPDB":
        if yasara.storage.objects:
            print("Storage Exists...")
            # Clear storage for new PDB Loading...
            yasara.Clear()
            yasara.storage.objects = {}
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
            p.display_pepsurf_clusters(p.job_parms['pepsurf_chains'], p.job_parms['cluster_paths'])
        else:
            print("Error: Need to load a PepSurfPDB...")
except:
    yasara.plugin.end("Unknown request: {}".format(yasara.request))

# Stop the Plugin
yasara.plugin.end()
