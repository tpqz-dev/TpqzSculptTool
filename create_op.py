import bpy
import bmesh
from  .utils import *


class bbp_sculpt(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt"
    bl_label = "bbp_sculpt"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("extractAndSculpt---")
        if isMasked(context):
            bbpSculptExtract(context)
            force_symmetry_x()
        return {'FINISHED'}  
    
class bbp_editselect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_editselect"
    bl_label = "bbp_editselect"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("extractAndSculpt---")
        if isMasked(context):
            select_masked_verts(context)
        return {'FINISHED'}  
    
class bbp_xtract(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_xtract"
    bl_label = "bbp_xtract"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("extract---")
        if isMasked(context):
            bpy.ops.sculpt.paint_mask_extract(add_solidify=False)
            bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}  

class bbp_mask_new_object(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_mask_new_object"
    bl_label = "bbp_mask_new_object"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("bbp_mask_new_object ")
        bpy.ops.ed.undo_push(message="new object step")
        bpy.ops.sculpt.paint_mask_slice(new_object=True)
        bpy.ops.object.mode_set(mode='SCULPT')
        force_symmetry_x()
        set_move_brush()
        return {'FINISHED'}


class bbp_duplicate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_duplicate"
    bl_label = "bbp_duplicate"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        print("bbp_duplicate---")
        duplicate(context)
        force_symmetry_x()
        set_move_brush()
        return {'FINISHED'} 

class bbp_insert_object(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_insert_object"
    bl_label = "bbp_insert_object"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name = 'value', default = 'cube')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        print("insert object")
        if isMasked(context):
            print("- create with mask")
            bpy.ops.sculpt.paint_mask_extract()
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            print("- create no mask")
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            plane = bpy.context.active_object
            bpy.ops.object.select_all(action='DESELECT') 
            plane.select_set(True)
            bpy.context.view_layer.objects.active = plane  
            plane.name = "tmp_3dObject"

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        original_dimensions =  bpy.context.object.dimensions
        original_location =  bpy.context.object.location
        print("original_dimensions "+str(original_dimensions))
        dx= original_dimensions[0]
        dy= original_dimensions[1]
        dz= original_dimensions[2]
        lx = original_location[0]
        ly = original_location[1]
        lz = original_location[2]
        gdim = greaterDimension(original_dimensions)
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.delete(type='VERT')
        cursor_location = bpy.context.scene.cursor.location
        val = self.value
        if val == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=cursor_location, scale=(gdim,gdim,gdim))
        elif val=="sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=cursor_location, scale=(gdim, gdim,gdim))
        elif val=="torus":
            bpy.ops.mesh.primitive_torus_add(align='WORLD',  location=cursor_location, rotation=(0, 0, 0), major_radius=1*gdim, minor_radius=gdim*0.25, abso_major_rad=gdim*1.25, abso_minor_rad=gdim*0.75)
        elif val=="cone":
            bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=cursor_location, scale=(gdim, gdim, gdim))
        elif val=="plane":
            bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD',  location=cursor_location, scale=(gdim, gdim, gdim))
        else:
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=cursor_location , scale=(gdim, gdim, gdim))
        #print("new dimensions "+str(context.active_object.dimensions) )
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.object.location = [lx,ly,lz]
        bpy.context.view_layer.update() 
        print("altered dimensions "+str( bpy.context.object.dimensions) )
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode='SCULPT')
        #force_symmetry_x()
        pivot_to_center()
        set_move_brush()
        return {'FINISHED'}    


     

