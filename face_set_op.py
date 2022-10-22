import bpy

# bbp_mask_hidden_face_set,
class bbp_mask_hidden_face_set(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_mask_hidden_face_set"
    bl_label = "bbp_mask_hidden_face_set"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'cube')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        print("test")
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
        bpy.ops.sculpt.face_set_change_visibility(mode='SHOW_ALL')
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        
        return {'FINISHED'} 