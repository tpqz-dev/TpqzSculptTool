import bpy

class bbp_focal_view(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_focal_view"
    bl_label = "bbp_focal_view"
    bl_options = {"REGISTER", "UNDO"}
    #create property
    value: bpy.props.StringProperty(name = 'value', default = '50')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #print(self.value)
        val = int(self.value)
      
        self.report({'INFO'},"focal set to "+str(self.value))
        bpy.context.space_data.lens = int(self.value)
        return {'FINISHED'} 

class bbp_sculpt_fade(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_fade"
    bl_label = "bbp_sculpt_fade"
    #create property
    value: bpy.props.StringProperty(name = 'value', default = '1')
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("FADE "+self.value)
        if self.value == "fade":
            bpy.context.space_data.overlay.fade_inactive_alpha = 0.579167
            bpy.context.space_data.overlay.show_fade_inactive = True
        else :
            bpy.context.space_data.overlay.show_fade_inactive = False
        return {'FINISHED'}


