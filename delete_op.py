import bpy
from  .utils import *
class bbp_delete_masked(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_delete_masked"
    bl_label = "bbp_delete_masked"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_delete_masked---")
        bpy.ops.mesh.paint_mask_slice(fill_holes=False, new_object=False)
        return {'FINISHED'}  
    
class bbp_delete_mesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_delete_mesh"
    bl_label = "bbp_delete_mesh"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        currentObject = context.active_object
        print("object to delete delete "+currentObject.name)
        objs = []
        for obj in bpy.context.scene.objects: 
            print(obj.name, obj, obj.type)
            if obj.type == 'MESH'and obj!= currentObject and obj.hide_get()!=True : 
                objs.append(obj) 
                
        print(objs)
        scene = bpy.context.scene
        
        if len(objs)>=1 :
            # no object : return to object mmode
            print("returning to object mode all")
            lastObj = objs[-1]
           
            #bpy.ops.sculpt.sculptmode_toggle()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            print("delete "+currentObject.name+" new object = " + str(lastObj ))
            
            currentObject.select_set(True) 
            bpy.ops.object.delete()
            lastObj.select_set(True) 
            bpy.context.view_layer.objects.active = lastObj
            bpy.ops.object.mode_set(mode='SCULPT')
       
        else :
            print ("nothing to delete : one object remaining")
            bpy.ops.object.mode_set(mode='SCULPT')

   
        return {'FINISHED'} 

# define the filter method
def filter_on_custom_prop(self, object):
    return "MyCustomPropName" in object

# define the property by using the bpy.props.PointerProperty and its poll function
bpy.types.Object.my_object = bpy.props.PointerProperty(
    type=bpy.types.Object,
    poll=filter_on_custom_prop
)


class bbp_delete_by_symetry(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_delete_by_symetry"
    bl_label = "bbp_delete_by_symetry"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'X')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        val = self.value
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')    
        if val == "X":
            bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_outer=True, xstart=651, xend=657, ystart=596, yend=65, flip=False)
        elif val=="Y":
             bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_outer=True, xstart=651, xend=657, ystart=596, yend=65, flip=False)
        else:
             bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_outer=True, xstart=651, xend=657, ystart=596, yend=65, flip=False)

        bpy.ops.object.mode_set(mode='SCULPT')
        force_symmetry_x()
        return {'FINISHED'}


class bbp_delete(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_delete"
    bl_label = "bbp_delete"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_delete---")
        force_symmetry_x()
        return {'FINISHED'}  
    
class bbp_delete_hiddenpg(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_delete_hiddenpg"
    bl_label = "bbp_delete_hidden_pg"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_delete_hidden_pg---")
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.sculpt.sculptmode_toggle()
        force_symmetry_x()
        return {'FINISHED'}   


class bbp_split_by_symetry(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_split_by_symetry"
    bl_label = "bbp_split_by_symetry"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'X')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        val = self.value
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')    
        if val == "X":
            bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_outer=False, xstart=651, xend=657, ystart=596, yend=65, flip=False)
        elif val=="Y":
             bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_outer=False, xstart=651, xend=657, ystart=596, yend=65, flip=False)
        else:
             bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_outer=False, xstart=651, xend=657, ystart=596, yend=65, flip=False)

        bpy.ops.object.mode_set(mode='SCULPT')
        force_symmetry_x()
        return {'FINISHED'}