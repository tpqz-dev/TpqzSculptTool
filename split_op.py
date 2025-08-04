import bpy
from  .utils import *
class bbp_copy_face_set(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_copy_face_set"
    bl_label = "bbp_copy_face_set"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_copy_face_set---")
        # -------------

        src_obj=context.active_object
        new_obj = src_obj.copy()
        new_obj.data = src_obj.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)
    
        src_obj.select_set(True)
        new_obj.select_set(False)
        bpy.context.view_layer.objects.active = src_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='SCULPT')
        
        src_obj.select_set(False)
        new_obj.select_set(True)
        bpy.context.view_layer.objects.active = new_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.object.mode_set(mode='SCULPT')

        src_obj.select_set(True)
        new_obj.select_set(False)
        bpy.context.view_layer.objects.active = src_obj

        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        bpy.context.object.use_mesh_mirror_x = False
        bpy.context.object.use_mesh_mirror_y = False
        bpy.context.object.use_mesh_mirror_z = False
        force_symmetry_x()
        return {'FINISHED'} 



class bbp_split_hiddenpg(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_split_hiddenpg"
    bl_label = "bbp_split_hidden_pg"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_split_hidden face set---")
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
        bpy.ops.paint.hide_show_all(action='SHOW')
        bpy.ops.sculpt.paint_mask_slice(fill_holes=False, new_object=True)
        bpy.ops.object.mode_set(mode='SCULPT')
  
        return {'FINISHED'}  
    
class bbp_split_group(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_split_group"
    bl_label = "bbp_split_group"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_split_group---")
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.sculpt.sculptmode_toggle()
        return {'FINISHED'}        
  
#bbp_split_face_set 
class bbp_split_face_set(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_split_face_set"
    bl_label = "bbp_split_face_set"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'cube')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        print("bbp_split_face_set")
        result = bpy.ops.mesh.face_set_extract('INVOKE_DEFAULT')
        print(result)
        self.report({'INFO'}, "a message")
        if result != {'RUNNING_MODAL'}: # <--- Important to check the result
            bpy.ops.object.mode_set(mode='SCULPT')
            force_symmetry_x()
          
        return {'FINISHED'}
    
