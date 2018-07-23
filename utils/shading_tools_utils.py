'''
This tool scans a texture directory and creates shading networks based on texture names
Designed for Maya / Redshift
Created by Roman Zhuk, 2018
'''


import os
from maya import cmds

# Add new dictionary to and existing dictionary
def add_to_dict( dict_of_dicts, dict, item, content ):
    if dict in dict_of_dicts:
        dict_of_dicts[dict][item] = content
    else:
        dict_of_dicts[dict] = { item : content }

# DEF to parse all the textures in folder to split them into material groups
def textures_by_mats( folder_path, suffixes ):
    # 1. Catch all texture files into a list
    all_textures = os.listdir( folder_path )
    # 2. Create a materials dictionary that will hold textures dictionaries
    mats_dict = {}
    for texture in all_textures:
        tex_name = texture.split('.')
        for suffix in suffixes:
            if suffixes[suffix] in tex_name[0]:
                newMat = tex_name[0].replace( ('_%s' % suffixes[suffix]), '' )
                add_to_dict( mats_dict, newMat, suffix, texture )

    # for item in mats_dict:
    #     print( item, mats_dict[item] )

    return mats_dict


def create_shading_grp( material ):
    shadingGrp = '%s_SG' % material
    if (cmds.objExists( shadingGrp )) :
        return shadingGrp
    cmds.sets( renderable=True, noSurfaceShader=True, empty=True, n=shadingGrp )
    cmds.connectAttr(('%s.outColor' % material), ('%s.surfaceShader' % shadingGrp), force=True)
    return shadingGrp


def setup_reverse_node( material, texture, texture_type ):
    reverse = '%s_%s_reverse' % (material, texture_type)
    cmds.shadingNode('reverse', asUtility=True, n=reverse)
    cmds.connectAttr(('%s.outColor' % texture), ('%s.input' % reverse), force=True)
    return reverse


'''
suffixes = [ 'Diffuse',
             'Glossiness',
             'ior',
             'Normal',
             'Reflection',
             'Displacement',
             'mask',
             'bump',
             'Height',
             'Translucency',
             'Refraction',
             'Mask_Translucency']
'''