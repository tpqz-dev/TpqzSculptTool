import bpy
from  .utils import *
class bbp_join_meshes(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_join_meshes"
    bl_label = "bbp_join_meshes"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        """bpy.ops.sculpt.sculptmode_toggle()
        
        currentObject = context.active_object
        objs = []
        for obj in bpy.context.scene.objects: 
            print(obj.name, obj, obj.type)
            if obj.type == 'MESH': 
                objs.append(obj)
        print(objs)"""
        # TODO not working (why ???) 
        print("******************")
        print("sculpt mode toggle")
        bpy.ops.sculpt.sculptmode_toggle()
        print("join")
        bpy.ops.object.join()
        print("sculpt mode toggle")
        bpy.ops.sculpt.sculptmode_toggle()
        print("******************")
        force_symmetry_x()
        return {'FINISHED'}


#bbp_join_choosed_object
class bbp_join_choosed_object(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_join_choosed_object"
    bl_label = "bbp_join_choosed_object"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        print(bpy.context.scene.list_chosen_object);
        if bpy.context.scene.list_chosen_object is not None:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.list_chosen_object.select_set(True)
            bpy.ops.object.join()
            bpy.ops.object.mode_set(mode='SCULPT')
            bpy.context.scene.list_chosen_object=None
            force_symmetry_x()
        else :
            print("Nothing to join");

        return {'FINISHED'}     