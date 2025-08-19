bl_info = {
    "name": "tpqz_sculpt",
    "author": "tpqz",
    "version": (0, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Tools>TPQZsculpt",
    "description": "Sculpting toolset",
    "warning": "",
    "doc_url": "",
    "category": "sculpt",
}

import bpy
import rna_keymap_ui

from  .utils import *
from  .gui import *
from  .create_op import *
from  .delete_op import *
from  .face_set_op import *
from  .focal_op import *
from  .join_op import *
from  .mesh_op import *
from  .pivot_op import *
from  .split_op import *
from  .boolean import *
#from .preferences import *

addon_keymaps = []

classes = (
    bbpSculptViewPanelObject,
    bbp_sculpt,
    bbp_xtract,
    bbp_delete,
    bbp_spherize,
    bbp_delete_hiddenpg,
    bbp_delete_masked,
    bbp_close_hole,
    bbp_mask_subdivide,
    bbp_duplicate,
    bbp_join_meshes,
    bbp_split_group,
    bbp_split_hiddenpg,
    bbp_remesh,
    bbp_delete_mesh,
    bbp_focal_view,
    bbp_join_choosed_object,
    bbp_sculpt_fade,
    bbp_sculpt_restore_x,
    bbp_mask_new_object,
    bbp_sculpt_unmasked_center,
    bbp_sculpt_solidify,
    bbp_delete_by_symetry,
    bbp_mirror,
    bbp_decimate,
    bbp_insert_object,
    bbp_split_face_set,
    bbp_copy_face_set,
    bbp_mask_hidden_face_set,
    bbp_split_by_symetry,
    bbp_symetry,
    bbp_boolean,
    custom_menu_tpqz_sculpt,
    call_menu_tpqz,
    bbp_editselect,
    bbp_empty_object,
    bbp_rotate,
    bbp_xtract_select_border,
    bbp_xpand_mask,
    bbp_restore_sculpt,
    bbp_quadriflow_remesh,
    bbp_sculpt_merge
    )

def scene_list_mesh_object_poll(self, object):
    return object.type == 'MESH'

kc = bpy.context.window_manager.keyconfigs.addon
if kc is not None:
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("object.call_menu_tpqz", 'X', 'PRESS', shift=False, ctrl=False,alt=True)
    addon_keymaps.append((km, kmi))

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # custom types
    bpy.types.Scene.solidify_float = bpy.props.FloatProperty(name="solidify_float", default=0.1)
    bpy.types.Scene.solidify_bool = bpy.props.BoolProperty(name="solidify_bool", default=True)
    
    bpy.types.Scene.merge_float = bpy.props.FloatProperty(name="merge_float", default=0.001)
    bpy.types.Scene.merge_bool = bpy.props.BoolProperty(name="merge_bool", default=True)
    
    bpy.types.Scene.tpqz_force_symmetry = bpy.props.BoolProperty(name="tpqz_force_symmetry", default=True)
    bpy.types.Scene.ratio_float = bpy.props.FloatProperty(name="ratio_float", default=0.2, min=0.01, max=1.0)
   


    bpy.types.Scene.mesh_symmetry = bpy.props.BoolProperty(
        name="mesh_symmetry",
        description="Use Mesh Symmetry",
        default=True,
   )
    bpy.types.Scene.preserve_boundary = bpy.props.BoolProperty(
        name="preserve_boundary",
        description="Preserve Sharp Edges",
        default=True,
    )
    bpy.types.Scene.preserve_sharp = bpy.props.BoolProperty(
        name="preserve_sharp",
        description="Preserve Sharp Edges",
        default=True,
    )
    bpy.types.Scene.preserve_attributes = bpy.props.BoolProperty(
        name="preserve_attributes",
        description="Preserve Paint Mask",
        default=True,   
    )   

    bpy.types.Scene.smooth_normals = bpy.props.BoolProperty(
        name="smooth_normals",
        description="Smooth Normals",
        default=True,
    )   
    bpy.types.Scene.target_faces = bpy.props.IntProperty(
        name="target_faces",
        description="Target Faces",
        default=100,
        min=100,
        max=10000000,
    )


    bpy.types.Scene.obj = bpy.props.StringProperty()
    bpy.types.Scene.list_chosen_object = bpy.props.PointerProperty(
    type=bpy.types.Object,
    poll=  scene_list_mesh_object_poll
    )
    bpy.types.INFO_HT_header.append(draw_item)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.list_chosen_object
    del bpy.types.Scene.solidify_float
    del bpy.types.Scene.solidify_bool
    del bpy.types.Scene.tpqz_force_symmetry 
    bpy.types.INFO_HT_header.remove(draw_item)
