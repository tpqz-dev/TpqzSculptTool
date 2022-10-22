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

addon_keymaps = []

classes = (
    bbpSculptViewPanelObject,
    bbp_sculpt,
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
    bbp_insert_object,
    bbp_split_face_set,
    bbp_copy_face_set,
    bbp_mask_hidden_face_set,
    bbp_split_by_symetry,
    bbp_boolean,
    custom_menu_tpqz_sculpt,
    call_menu_tpqz
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
    #bpy.utils.register_module(__name__)
    bpy.types.Scene.solidify_float = bpy.props.FloatProperty(name="solidify_float", default=0.1)
    bpy.types.Scene.solidify_bool = bpy.props.BoolProperty(name="solidify_bool", default=True)
    bpy.types.Scene.obj = bpy.props.StringProperty()
    bpy.types.Scene.list_chosen_object = bpy.props.PointerProperty(
    type=bpy.types.Object,
    poll=  scene_list_mesh_object_poll
    )
    bpy.types.INFO_HT_header.append(draw_item)

def unregister():
    #bpy.utils.unregister_module(__name__)
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.list_chosen_object
    del bpy.types.Scene.solidify_float
    del bpy.types.Scene.solidify_bool
    bpy.types.INFO_HT_header.remove(draw_item)