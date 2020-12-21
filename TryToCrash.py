# coding:utf-8
"""
import sys
scripts_path = 'y:/scripts/unreal'
if not scripts_path in sys.path:
    sys.path.insert(0, scripts_path)
from TryToCrash import *
"""

import maya.cmds as cmds
import maya.mel as mel
import re
import os
import logging
import time


mel.eval('source "C:/Program Files/Autodesk/Maya2016/scripts/others/hyperShadePanel.mel";')
mel.eval('source "C:/ProgramData/Redshift/Plugins/Maya/Common/scripts/redshiftInstallCallbacks.mel";')
mel.eval('source "C:/ProgramData/Redshift/Plugins/Maya/Common/scripts/override/2016/MLdeleteUnused.mel";')

global texture_node_dict, warn_count


def init_global_var():
    global texture_node_dict, warn_count
    texture_node_dict = {
        'file': 'fileTextureName',
        'RedshiftNormalMap': 'tex0',
    }
    warn_count = 0


def make_dock_control_only(dock_control_name):
    if cmds.dockControl(dock_control_name, ex=1, q=1):
        cmds.deleteUI(dock_control_name)


def make_window_only(win_name):
    if cmds.window(win_name, ex=1, q=1):
        cmds.deleteUI(win_name)


def is_udim(file_is):
    searchObj = re.search(u'\.[0-9]{4}\.', file_is)
    if searchObj:
        return True
    else:
        return False


def create_file_texture():
    file_node = mel.eval('string $file_node = `hyperShadePanelCreate "2dTexture" file`;')
    return file_node


def delete_unused_material():
    mel.eval('MLdeleteUnused;')


def create_rs_ao():
    return cmds.shadingNode("RedshiftAmbientOcclusion", asTexture=1, )


def create_remap_hsv():
    return cmds.shadingNode('remapHsv', asUtility=1)


def create_contrast():
    return cmds.shadingNode('contrast', asUtility=1)


def create_layered_texture():
    lay_node = mel.eval('renderCreateNode "-asTexture" "" layeredTexture "" 0 0 0 0 0 "";')
    return lay_node


def create_material():
    rs_m_node = mel.eval(
        'string $rs_m_node = `rsCreateShadingNode "rendernode/redshift/shader/surface" "-asShader" "" RedshiftMaterial`;')

    # set default attribute for material
    cmds.setAttr('%s.refl_brdf' % rs_m_node, 1)
    cmds.setAttr('%s.refl_fresnel_mode' % rs_m_node, 2)
    cmds.setAttr('%s.refl_reflectivity' % rs_m_node, .234, .234, .234, type='double3')

    return rs_m_node


def create_normal_node():
    rs_nor_node = mel.eval(
        'string $rs_nor_node = `rsCreateShadingNode "rendernode/redshift/shader/utility" "-asUtility" "" RedshiftNormalMap`;')
    return rs_nor_node


def main():
    import time
    print(time.asctime( time.localtime(time.time()) ))

if __name__ == '__main__':
    main()
