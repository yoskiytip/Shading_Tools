'''
This tool scans a texture directory and creates shading networks based on texture names
Designed for Maya / Redshift
Created by Roman Zhuk, 2018
'''


from maya import cmds

from shading_tools_v01.utils import shading_tools_utils; reload( shading_tools_utils )

def setup_RS_bump_node( material, texture ):
    bump = '%s_rsBump' % material
    cmds.shadingNode( 'RedshiftBumpMap', asUtility=True, n=bump )
    cmds.connectAttr( ('%s.outColor' % texture), ('%s.input' % bump) )
    return bump


def setup_RS_normal_node( material, texture ):
    normal = '%s_rsNormal' % material
    cmds.shadingNode( 'RedshiftNormalMap', asUtility=True, n=normal)
    texture_path = cmds.getAttr( '%s.fileTextureName' % texture )
    cmds.setAttr( ('%s.tex0' % normal), str(texture_path), type='string' )
    return normal


def channel_from_textureName( material, texture ):
    if   texture == 'Diffuse' : return ( '%s.diffuse_color' % material )
    elif texture == 'Translucency' : return ( '%s.transl_color' % material )
    elif texture == 'Translucency Mask': return ('%s.transl_weight' % material)
    elif texture == 'Reflection' : return ('%s.refl_color' % material)
    elif texture == 'Reflection Mask' : return ( '%s.refl_weight' % material )
    elif texture == 'Roughness' : return ( '%s.refl_roughness' % material )
    elif texture == 'Glossiness' : return ( '%s.refl_roughness' % material )
    elif texture == 'Anisotropy' : return ( '%s.refl_aniso' % material )
    elif texture == 'IOR' : return ( '%s.refl_ior' % material )
    elif texture == 'Refraction': return ('%s.refr_color' % material)
    elif texture == 'Refraction Mask'  : return ( '%s.refr_weight' % material )
    elif texture == 'SSS Mask' : return ( '%s.ms_amount' % material )
    elif texture == 'SSS layer 1' : return ( '%s.ms_color0' % material )
    elif texture == 'SSS layer 2' : return ( '%s.ms_color1' % material )
    elif texture == 'SSS layer 3' : return ( '%s.ms_color2' % material )
    elif texture == 'Opacity': return ('%s.opacity_color' % material)
    elif texture == 'Emission' : return ( '%s.emission_color' % material )
    elif texture == 'Emission Weight' : return ( '%s.emission_weight' % material )
    elif texture == 'Normal' : return ( '%s.bump_input' % material )
    elif texture == 'Bump' : return ( '%s.bump_input' % material )
    elif texture == 'Height' : return ( '%s.bump_input' % material )
    # In case of displacement
    # elif texture == 'Displacement':
    #     shadingGrp = cmds.listConnections( ('%s.outColor' % material), d=True )
    #     if shadingGrp[0] != None and shadingGrp[0] != '':
    #         return ('%s.rsDisplacementShader' % shadingGrp[0])
    #     else:
    #         shadingGrp = shading_tools_utils.create_shading_grp( material )
    #         return ('%s.rsDisplacementShader' % shadingGrp[0])
    else:
        cmds.warning('Unrecognized texture type: %s' % texture)
        return None


def material_from_textureSet( mat_name, textureSet_dict, folder_path ):
    # Create material
    cmds.shadingNode( 'RedshiftMaterial', asShader=True, n=mat_name )
    # Create UV node
    uv = '%s_uv' % mat_name
    shadingGrp = '%s_SG' % mat_name
    cmds.shadingNode( 'place2dTexture', asUtility=True, n=uv )
    # Loop through each texture set
    for tex_type in textureSet_dict:
        matConnection = channel_from_textureName( mat_name, tex_type )
        if matConnection == None:
            continue
        tex = '%s_%s' % (mat_name, tex_type)
        cmds.shadingNode( 'file', asTexture=True, n=tex )
        # Set texture path
        try:
            cmds.setAttr( ('%s.fileTextureName' % tex), ('%s/%s' % (folder_path, textureSet_dict[tex_type])), type='string' )
        except:
            cmds.warning('Unexceptable texure name! For %s' % tex)
        # Connect uv node to the texture
        cmds.connectAttr( ('%s.outUV' % uv), ('%s.uvCoord' % tex), force=True )
        # Choose colorspace
        if tex_type != 'Diffuse':
            cmds.setAttr( ('%s.colorSpace' % tex), 'Raw', type='string' )
        # Connect texture to material:
        # Diffuse
        # Translucency
        # Translucency_Mask
        if tex_type == 'Translucency Mask':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # Reflection
        # Reflection Mask
        elif tex_type == 'Reflection Mask':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # Roughness
        elif tex_type == 'Roughness':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # Glossiness
        elif tex_type == 'Glossiness':
            reverse = shading_tools_utils.setup_reverse_node( mat_name, tex, tex_type )
            cmds.connectAttr( ('%s.output.outputX' % reverse), matConnection )
        # Anisotropy
        elif tex_type == 'Anisotropy':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # IOR
        elif tex_type == 'IOR':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # Refraction
        # Refraction Mask
        elif tex_type == 'Refraction Mask':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # SSS Mask
        elif tex_type == 'SSS Mask':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # SSS layer 1
        # SSS layer 2
        # SSS layer 3
        # Opacity
        # Emission
        # Emission Weight
        elif tex_type == 'SSS Weight':
            cmds.connectAttr(('%s.outColor.outColorR' % tex), matConnection)
        # Bump
        elif tex_type == 'Bump':
            bump = setup_RS_bump_node(mat_name, tex)
            cmds.connectAttr(('%s.out' % bump), ('%s.bump_input' % mat_name))
        # Normal
        elif tex_type == 'Normal':
            normal = setup_RS_normal_node( mat_name, tex )
            cmds.delete( tex )
            cmds.connectAttr(('%s.outDisplacementVector' % normal), ('%s.bump_input' % mat_name))
        elif tex_type == 'Displacement':
            continue
        else:
            try:
                cmds.connectAttr( ('%s.outColor' % tex), matConnection )
            except:
                continue
    # Create material SG
    if not ( cmds.objExists( shadingGrp ) ):
        shading_tools_utils.create_shading_grp( mat_name )

#'''
# 'Diffuse'
# 'Translucency'
# 'Translucency_Mask'
# 'Reflection'
# 'Reflection Mask'
# 'Roughness'
# 'Glossiness'
# 'Anisotropy'
# 'IOR'
# 'Refraction'
# 'Refraction Mask'
# 'SSS Mask'
# 'SSS layer 1'
# 'SSS layer 2'
# 'SSS layer 3'
# 'Opacity'
# 'Emission'
# 'Emission Weight'
# 'Bump'
# 'Normal'
#'''

def create_RS_materials( folder_path, suffixes ):
    # 1. Get texture set dictionary from the textures folder
    texSets_dict = shading_tools_utils.textures_by_mats( folder_path, suffixes )
    number = 1
    for texSet in texSets_dict:
        if ( cmds.objExists( ('rs_%s' % texSet) ) ):
            continue
        material_from_textureSet( ('rs_%s' % texSet), texSets_dict[texSet], folder_path )
        print( '%s : %s' % (number, texSet) )
        number += 1
        cmds.clearCache( all=True )


def check_textureSets_number( folder_path, suffixes ):
    texSets_dict = shading_tools_utils.textures_by_mats(folder_path, suffixes)
    for texSet in texSets_dict:
        if ( cmds.objExists( ('rs_%s' % texSet) ) ):
            continue
        # print ( texSet )
    print ( 'total material number: %s' % str(len(texSets_dict)))




