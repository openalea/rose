
# This file has been generated at Tue Mar 13 11:08:54 2012

from openalea.core import *


__name__ = 'Rose'

__editable__ = True
__description__ = 'Stuff to display rosebush'
__license__ = ''
__url__ = ''
__alias__ = []
__version__ = ''
__authors__ = ''
__institutes__ = ''
__icon__ = ''


__all__ = ['mesh_roseLeaflet_mesh_roseLeaflet', 'rose_geometry_ReconstructWithTurtle', 'rose_geometry_computeLeaflet4pts', 'rose_CropGeneration_2011', 'rose_MTG_union', 'rose_geometry_BezierPatchFlower', 'PlantFrame_Rose_PlantFrame_Rose', 'rose_HttpDir2DictOfFiles', 'rose_Files2MTGs', 'rose_GetMTG', 'rose_geometry_RawBud', 'rose_geometry_VertexVisitor', 'rose_geometry_PointArray', 'rose_LocalDir2DictOfFiles', 'PlantPositionning_PlantPositionning', 'rose_geometry_PolygonLeaflet', 'rose_geometry_RawFruit', 'SceneRotation_SceneRotation', 'rose_geometry_PetalMatrix', 'revolutiontestinonefile_revolutiontestinonefile', 'rose_geometry_BuiltBud', 'rose_GridFile2Dict', 'rose_geometry_RawFlower', 'rose_geometry_NoOrgan', 'Leaflet_Orientation_4points_Leaflet_Orientation_4points', 'rose_geometry_RevolutionBud', 'rose_geometry_RevolutionFig', '_91662352', 'rose_geometry_ControlPointsMatrix', 'rose_GetOrigin', 'CropGeneration_CropGeneration', 'rose_geometry_BudArray', 'leaflet_orientation_leaflet_orientation', 'tempPickleFile_tempPickleFile', 'rose_colors_ColorFuncs', 'rose_geometry_FineBudArray', 'rose_geometry_TaperedFlower']



mesh_roseLeaflet_mesh_roseLeaflet = Factory(name='mesh_roseLeaflet',
                authors=' (wralea authors)',
                description='build a triangleset from a profile',
                category='data processing',
                nodemodule='mesh_roseLeaflet',
                nodeclass='mesh_roseLeaflet',
                inputs=[{'interface': ISequence, 'name': 'x', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'y', 'value': None, 'desc': 'sequence of positions along the x axis'}],
                outputs=[{'interface': None, 'name': 'triangleSet', 'desc': 'width values againts x positions'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_ReconstructWithTurtle = Factory(name='ReconstructWithTurtle',
                authors=' (wralea authors)',
                description='builds a scene using the plantgl Turtle',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='ReconstructWithTurtle',
                inputs=[{'interface': IData, 'name': 'g', 'value': None, 'desc': 'a "Sagah2011" MTG'}, {'interface': IFunction, 'name': 'Visitor', 'value': None, 'desc': 'A function that builds the scene while walking throught the nodes of the MTG'}, {'interface': IFloat, 'name': 'powerParam', 'value': None, 'desc': 'the power parameter of the pipe model'}],
                outputs=[{'interface': IData, 'name': 'TheScene', 'desc': 'A 3D scene'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_computeLeaflet4pts = Factory(name='ComputeLeaflet4pts',
                authors=' (rose authors)',
                description='compute leaflet geometry from 4 points',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='computeLeaflet4pts',
                inputs=[{'interface': ISequence, 'name': 'x', 'value': [0.25, 0.5, 0.075, 1.0], 'desc': ''}, {'interface': ISequence, 'name': 'y', 'value': [0.81, 0.92, 0.95, 1.0], 'desc': 'sequence of positions along the y axis'}],
                outputs=[{'interface': IFunction, 'name': 'computeLeaflet4pts', 'desc': 'function that computes a leaflet from 4 digitization points'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_CropGeneration_2011 = Factory(name='CropGeneration_2011',
                authors=' (wralea authors)',
                description='creates a population of plants by associating plants numbers to positions in a grid',
                category='data processing',
                nodemodule='rose',
                nodeclass='CropGeneration_2011',
                inputs=[{'interface': IDict, 'name': 'plantlist', 'value': {}, 'desc': 'the dispatching of plants on the table'}, {'interface': IDict, 'name': 'existingmtglist', 'value': {}, 'desc': 'the dict of existing mtg:filename'}, {'interface': ISequence, 'name': 'excludelist', 'value': [], 'desc': 'list of plants not touse for filling'}, {'interface': IInt, 'name': 'n_x', 'value': 0, 'desc': 'nr of x points'}, {'interface': IInt, 'name': 'n_y', 'value': 0, 'desc': 'nr of y points'}, {'interface': IInt, 'name': 's_x', 'value': 0, 'desc': 'value for y stride'}, {'interface': IInt, 'name': 's_y', 'value': 0, 'desc': 'value  for Y stride'}, {'interface': ISequence, 'name': 'origin', 'value': [0, 0, 800], 'desc': 'the 3D coordinates of the 0,0 position'}, {'interface': IBool, 'name': 'DoFill', 'value': True, 'desc': 'If we fill missing data with existing data'}, {'interface': IBool, 'name': 'DoRotate', 'value': True, 'desc': 'wether we rotate the planst used for filling'}],
                outputs=[{'interface': IDict, 'name': 'dictofpositions', 'desc': 'dict of filenames associated with a list of coordinates and rotations'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_MTG_union = Factory(name='MTG_union',
                authors=' (rose authors)',
                description='garthers differents MTG objects in a single one.',
                category='data processing',
                nodemodule='rose',
                nodeclass='MTG_union',
                inputs=[{'interface': ISequence, 'name': 'mtgsin', 'value': {}, 'desc': 'a list of MTG objects to be glued together in a signle MTG object'}],
                outputs=[{'interface': IDict, 'name': 'mtgout', 'desc': 'An MTG object that holds the MTGs of the input list in a single one'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_BezierPatchFlower = Factory(name='BezierPatchFlower',
                authors=' (rose authors)',
                description='computes a flower.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='BezierPatchFlower',
                inputs=[{'interface': ISequence, 'name': 'controlPointMatrix', 'value': None, 'desc': 'control points matrix of Vector4'}, {'interface': IInt, 'name': 'uStride', 'value': 8, 'desc': '"U" stride'}, {'interface': IInt, 'name': 'vStride', 'value': 8, 'desc': '"V" stride'}],
                outputs=[{'interface': IFunction, 'name': 'BezierPatchFlower', 'desc': 'computes a red flower from 2 points and a diameter.'}],
                widgetmodule=None,
                widgetclass=None,
               )




PlantFrame_Rose_PlantFrame_Rose = Factory(name='PlantFrame_Rose',
                authors=' (wralea authors)',
                description='',
                category='scene design',
                nodemodule='PlantFrame_Rose',
                nodeclass='PlantFrame_Rose',
                inputs=[{'interface': None, 'name': 'mtg_file', 'value': None, 'desc': ''}, {'interface': None, 'name': 'drf_p', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}, {'interface': None, 'name': 'mtg_file', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_HttpDir2DictOfFiles = Factory(name='HttpDir2DictOfFiles',
                authors=' (rose authors) ',
                description='gets the files whose name matches "filter" on an URL and returns a dict which associates the names with a temp file on the local host.',
                category='Unclassified',
                nodemodule='rose',
                nodeclass='HttpDir2DictOfFiles',
                inputs=[{'interface': IStr, 'name': 'url', 'value': None, 'desc': 'An URL from which we download the files.'}, {'interface': IStr, 'name': 'filtre', 'value': None, 'desc': 'a string to filter filenames'}],
                outputs=[{'interface': IDict, 'name': 'dictoffiles', 'desc': 'a dict which associates PlantNum.mtg:realPathOfFile'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_Files2MTGs = Factory(name='Files2MTGs',
                authors=' (rose authors)',
                description='Makes MTG objects from MTG files',
                category='data processing',
                nodemodule='rose',
                nodeclass='Files2MTGs',
                inputs=[{'interface': IDict, 'name': 'cropdict', 'value': {}, 'desc': 'A dict which associates MTG filenames with lists of [positions, rotation] pairs.'}],
                outputs=[{'interface': ISequence, 'name': 'listOfMTGs', 'desc': 'A list of MTG objects, i.e MTG files shifted and rotated according to the input dict.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_GetMTG = Factory(name='GetMTG',
                authors=' (wralea authors)',
                description='generates a complete path to a file.    the argument is in the form of "NUM[-N]", which means that    we want to create an MTG object fom the NUM.mtg file.    To achieve that, the filename is splitted against the"-" (dash) separator    and the string ".mtg" is concatenated to it.',
                category='data processing',
                nodemodule='rose',
                nodeclass='GetMTG',
                inputs=[{'interface': IStr, 'name': 'dirname', 'value': '', 'desc': 'the name of the directory to read the file from'}, {'interface': IStr, 'name': 'IDplant', 'value': None, 'desc': 'The plantID to compute the filename from'}],
                outputs=[{'interface': IData, 'name': 'mtg', 'value': None, 'desc': 'the MTG structure built when reading the file'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_RawBud = Factory(name='RawBud',
                authors=' (rose authors)',
                description='builds a raw bud with a sphere and a cone',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='RawBud',
                inputs=[],
                outputs=[{'interface': IFunction, 'name': 'compute_bud', 'desc': 'function to draw a bud'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_VertexVisitor = Factory(name='VertexVisitor',
                authors=' (wralea authors)',
                description='function to visit MTG nodes',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='VertexVisitor',
                inputs=[{'interface': IFunction, 'name': 'leaf_factory', 'value': None, 'desc': 'function to compute leaflet geometry'}, {'interface': IFunction, 'name': 'compute_bud', 'value': None, 'desc': 'function to compute bud geometry'}, {'interface': IFunction, 'name': 'compute_sepal', 'value': None, 'desc': 'function to compute sepal geometry'}, {'interface': IFunction, 'name': 'flower_factory', 'value': None, 'desc': 'function to compute flower geometry'}],
                outputs=[{'interface': IFunction, 'name': 'VertexVisitor', 'desc': 'function to visit the MTG nodes'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_PointArray = Factory(name='PointArray',
                authors=' (rose authors)',
                description='returns a points array.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='PointArray',
                inputs=[],
                outputs=[{'interface': ISequence, 'name': 'pts_array', 'desc': 'A Vector2 array.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_LocalDir2DictOfFiles = Factory(name='LocalDir2DictOfFiles',
                authors=' (rose authors)',
                description='',
                category='data processing',
                nodemodule='rose',
                nodeclass='LocalDir2DictOfFiles',
                inputs=[{'interface': ISequence, 'name': 'listoffiles', 'value': None, 'desc': 'The list of files to make the dist from'}],
                outputs=[{'interface': IDict, 'name': 'dictoffiles', 'desc': 'a dict which associates PlantNum.mtg:realPathOfFile'}],
                widgetmodule=None,
                widgetclass=None,
               )




PlantPositionning_PlantPositionning = Factory(name='PlantPositionning',
                authors=' (wralea authors)',
                description='',
                category='data processing',
                nodemodule='PlantPositionning',
                nodeclass='PlantPositionning',
                inputs=[{'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'IDplant', 'value': None, 'desc': ''}, {'interface': IDict, 'name': 'plant_pos', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_PolygonLeaflet = Factory(name='PolygonLeaflet',
                authors=' (rose authors)',
                description='computes a quick leaflet.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='PolygonLeaflet',
                inputs=[],
                outputs=[{'interface': IFunction, 'name': 'PolygonLeaflet', 'desc': 'compute a 2 facets leaflets from 4 points.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_RawFruit = Factory(name='RawFruit',
                authors=' (rose authors)',
                description='computes a quick flower.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='RawFruit',
                inputs=[{'interface': IFunction, 'name': 'colorFunc', 'value': None, 'desc': 'a function to set the Turtle color'}],
                outputs=[{'interface': IFunction, 'name': 'RawFruit', 'desc': 'computes a red fruit from 2 points.'}],
                widgetmodule=None,
                widgetclass=None,
               )




SceneRotation_SceneRotation = Factory(name='SceneRotation',
                authors=' (wralea authors)',
                description='',
                category='scene design',
                nodemodule='SceneRotation',
                nodeclass='SceneRotation',
                inputs=[{'interface': None, 'name': 'scene', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_PetalMatrix = Factory(name='PetalMatrix',
                authors=' (wralea authors)',
                description='a control matrix points to control a bezier patch',
                category='data i/o',
                nodemodule='rose_geometry',
                nodeclass='PetalMatrix',
                inputs=[],
                outputs=[{'interface': IData, 'name': 'cmp', 'desc': 'a control points matrix to set up a bezier patch'}],
                widgetmodule=None,
                widgetclass=None,
               )




revolutiontestinonefile_revolutiontestinonefile = Factory(name='revolutiontestinonefile',
                authors=' (wralea authors)',
                description='test the load of uninode files',
                category='category test',
                nodemodule='revolutiontestinonefile',
                nodeclass='revolutiontestinonefile',
                inputs=[],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_BuiltBud = Factory(name='BuiltBud',
                authors=' (rose authors)',
                description='a function builds a bud with 2 spheres and a paraboloid.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='BuiltBud',
                inputs=[{'interface': IInt, 'name': 'stride', 'value': 10, 'desc': 'the number of splices of the graphic primitives.'}],
                outputs=[{'interface': IFunction, 'name': 'compute_bud', 'desc': 'function to draw a bud'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_GridFile2Dict = Factory(name='GridFile2Dict',
                authors=' (rose authors) ',
                description='Makes a dictionnary of pairs {plant num : plant position} in a 2D grid of int coordinates',
                category='data processing',
                nodemodule='rose',
                nodeclass='GridFile2Dict',
                inputs=[{'interface': IFileStr, 'name': 'GridFileName', 'value': '', 'desc': 'A file which contains a grid of plant numbers vs. positions in a 2D grid'}],
                outputs=[{'interface': IDict, 'name': 'dictOfPlantNums', 'desc': 'A dict which associates plant numbers with a position in a 2D grid.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_RawFlower = Factory(name='RawFlower',
                authors=' (rose authors)',
                description='computes a quick flower.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='RawFlower',
                inputs=[{'interface': IFunction, 'name': 'colorFunc', 'value': None, 'desc': 'a function to set the Turtle color'}],
                outputs=[{'interface': IFunction, 'name': 'RawFlower', 'desc': 'computes a conic red flower from 2 points and a diameter.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_NoOrgan = Factory(name='NoOrgan',
                authors=' (rose authors)',
                description='computes no leaflet in order to be able to look at the trunk.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='NoOrgan',
                inputs=[],
                outputs=[{'interface': IFunction, 'name': 'PolygonLeaflet', 'desc': 'Makes nothing.'}],
                widgetmodule=None,
                widgetclass=None,
               )




Leaflet_Orientation_4points_Leaflet_Orientation_4points = Factory(name='Leaflet Orientation 4points',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='Leaflet_Orientation_4points',
                nodeclass='Leaflet_Orientation_4points',
                inputs=[{'interface': IData, 'name': 'mtg', 'value': None, 'desc': ''}, {'interface': None, 'name': 'mesh', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_RevolutionBud = Factory(name='RevolutionBud',
                authors=' (rose authors)',
                description='draws up a bud from a revolution volume.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='RevolutionBud',
                inputs=[{'interface': IData, 'name': 'revFig', 'value': None, 'desc': 'a revolution volume'}, {'interface': IInt, 'name': 'stride', 'value': 8, 'desc': 'the rotation stride of the revolution figure'}],
                outputs=[{'interface': IFunction, 'name': 'rev_bud', 'desc': 'A function that draws a bud from a 3D revolution volume.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_RevolutionFig = Factory(name='RevolutionFig',
                authors=' (rose authors)',
                description='returns a 3D revolution volume.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='RevolutionFig',
                inputs=[{'interface': ISequence, 'name': 'pointArray', 'value': None, 'desc': 'a 2D points array'}, {'interface': IInt, 'name': 'stride', 'value': 8, 'desc': 'the 3D volume number of revolution slices.'}],
                outputs=[{'interface': IData, 'name': 'rev_fig', 'desc': 'A 3D revolution volume.'}],
                widgetmodule=None,
                widgetclass=None,
               )



_91662352 = DataFactory(name='rose.drf',
                    description='dressing file for rose stem',
                    editors=None,
                    includes=None,
                    )



rose_geometry_ControlPointsMatrix = Factory(name='ControlPointsMatrix',
                authors=' (wralea authors)',
                description='a control matrix points to control a bezier patch',
                category='data i/o',
                nodemodule='rose_geometry',
                nodeclass='ControlPointsMatrix',
                inputs=[],
                outputs=[{'interface': IData, 'name': 'cmp', 'desc': 'a control points matrix to set up a bezier patch'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_GetOrigin = Factory(name='GetOrigin',
                authors=' (rose authors) ',
                description='Makes a dictionnary of pairs {plant num : plant position} in a 2D grid of int coordinates',
                category='data processing',
                nodemodule='rose',
                nodeclass='GetOrigin',
                inputs=[{'interface': IFileStr, 'name': 'OriginFilename', 'value': '', 'desc': 'A file which contains a header line (i.e "x","y","z" and a data line with a 3D origine coordinate.'}],
                outputs=[{'interface': ISequence, 'name': 'origin', 'desc': 'A vector of 3D coordinates.'}],
                widgetmodule=None,
                widgetclass=None,
               )




CropGeneration_CropGeneration = Factory(name='CropGeneration',
                authors=' (wralea authors)',
                description='',
                category='data processing',
                nodemodule='CropGeneration',
                nodeclass='CropGeneration',
                inputs=[{'interface': IFileStr, 'name': 'txtfile', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'Plt_Not_Use', 'value': [], 'desc': ''}, {'interface': IBool, 'name': 'filling', 'value': True, 'desc': ''}, {'interface': IFloat, 'name': 'crop_width', 'value': 90.0, 'desc': ''}, {'interface': IFloat, 'name': 'crop_length', 'value': 200.0, 'desc': ''}, {'interface': IFloat, 'name': 'spacing', 'value': 15.0, 'desc': ''}],
                outputs=[{'interface': IDict, 'name': 'dico_complete', 'desc': ''}, {'interface': ISequence, 'name': 'IDplants', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_BudArray = Factory(name='budArray',
                authors=' (rose authors)',
                description='returns a points array.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='BudArray',
                inputs=[],
                outputs=[{'interface': ISequence, 'name': 'bud_array', 'desc': 'A Vector2 array.'}],
                widgetmodule=None,
                widgetclass=None,
               )




leaflet_orientation_leaflet_orientation = Factory(name='leaflet_orientation',
                authors=' (wralea authors)',
                description='',
                category='scene design',
                nodemodule='leaflet_orientation',
                nodeclass='leaflet_orientation',
                inputs=[{'interface': None, 'name': 'mtg', 'value': None, 'desc': ''}, {'interface': IFileStr, 'name': 'geom_file', 'value': None, 'desc': ''}, {'interface': None, 'name': 'mesh', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tempPickleFile_tempPickleFile = Factory(name='tempFile',
                authors=' (wralea authors)',
                description='returns a path to a file inside a temp dir according to the os ',
                category='data i/o',
                nodemodule='tempPickleFile',
                nodeclass='tempPickleFile',
                inputs=[{'interface': IStr, 'name': 'filename', 'value': None, 'desc': 'a name for a pickle file'}],
                outputs=[{'interface': IData, 'name': 'pickleFile', 'desc': 'returns a name for a pickle file'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_colors_ColorFuncs = Factory(name='colorFunc',
                authors=' (rose authors)',
                description='returns a list of colorFuncs.',
                category='data processing',
                nodemodule='rose_colors',
                nodeclass='ColorFuncs',
                inputs=[],
                outputs=[{'interface': ISequence, 'name': 'colorFuncs', 'desc': 'A list of functions to color the turtle.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_FineBudArray = Factory(name='fineBudArray',
                authors=' (rose authors)',
                description='returns a points array.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='FineBudArray',
                inputs=[],
                outputs=[{'interface': ISequence, 'name': 'bud_array', 'desc': 'A Vector2 array.'}],
                widgetmodule=None,
                widgetclass=None,
               )




rose_geometry_TaperedFlower = Factory(name='TaperedFlower',
                authors=' (rose authors)',
                description='computes a flower.',
                category='data processing',
                nodemodule='rose_geometry',
                nodeclass='TaperedFlower',
                inputs=[{'interface': ISequence, 'name': 'controlPointMatrix', 'value': None, 'desc': 'control points matrix of Vector4'}, {'interface': IInt, 'name': 'uStride', 'value': 8, 'desc': '"U" stride'}, {'interface': IInt, 'name': 'vStride', 'value': 8, 'desc': '"V" stride'}],
                outputs=[{'interface': IFunction, 'name': 'TaperedFlower', 'desc': 'computes a flower from 2 points and a diameter.'}],
                widgetmodule=None,
                widgetclass=None,
               )




