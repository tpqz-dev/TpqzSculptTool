
import bpy

class bbp_boolean(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_boolean"
    bl_label = "bbp_boolean"
    bl_options = {'REGISTER', "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'UNION')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and bpy.context.scene.mychosenObject != context.active_object

    def execute(self, context):
        #main(context)
        chosenObj = bpy.context.scene.mychosenObject
        
        print("--- bbp_boolean "+chosenObj.name)
        #main(context)
        chosenObj = bpy.context.scene.mychosenObject
        active_obj = bpy.context.active_object
        print("chosenObj "+chosenObj.name)
        print("active_obj "+active_obj.name)
    
        # modifiers 
        bool_mod = active_obj.modifiers.new(type="BOOLEAN", name="tpqz_boolean")
        bpy.context.object.modifiers["tpqz_boolean"].object = chosenObj
        bpy.ops.object.modifier_set_active(modifier="tpqz_boolean")
        bpy.context.object.modifiers["tpqz_boolean"].operation = self.value
        bpy.ops.object.modifier_apply(modifier="tpqz_boolean")
        bpy.ops.object.mode_set(mode='OBJECT')
        # delete
        bpy.ops.object.select_all(action='DESELECT')
        chosenObj.select_set(True)
        bpy.ops.object.delete(use_global=False, confirm=False)
        bpy.ops.object.mode_set(mode='SCULPT')    
        #remove from ui 
        bpy.context.scene.mychosenObject=None
        return {'FINISHED'}  