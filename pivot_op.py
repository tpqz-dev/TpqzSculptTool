import bpy
from  .utils import *
class bbp_sculpt_restore_x(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_restore_x"
    bl_label = "bbp_sculpt_restore_x"
 
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("restorex ")
        bpy.context.object.use_mesh_mirror_x = True
        bpy.ops.sculpt.set_pivot_position(mode='UNMASKED')
        return {'FINISHED'}

class bbp_sculpt_unmasked_center(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_unmasked_center"
    bl_label = "bbp_sculpt_unmasked_center"
 
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("restorex ")
        bpy.context.object.use_mesh_mirror_x = False
        bpy.ops.sculpt.set_pivot_position(mode='UNMASKED')
        return {'FINISHED'}

def pivot_to_unmasked():
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        bpy.context.object.use_mesh_mirror_x = False
        bpy.context.object.use_mesh_mirror_y = False
        bpy.context.object.use_mesh_mirror_z = False
        bpy.ops.sculpt.set_pivot_position(mode ='UNMASKED')