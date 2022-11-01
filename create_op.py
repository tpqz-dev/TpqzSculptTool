import bpy
import bmesh
from  .utils import *


def bbpSculptExtract(context):
     print("function call---")
     # verify dyn topo
     # verify mask created
     #bpy.ops.mesh.masktovgroup()
     bpy.ops.mesh.paint_mask_extract()
     #bpy.ops.object.apply_all_modifiers()
     bpy.context.object.modifiers["geometry_extract_solidify"].thickness = 0.05
     bpy.context.object.modifiers["geometry_extract_solidify"].offset = 1
     bpy.ops.object.modifier_apply(modifier="geometry_extract_solidify")
     bpy.ops.object.editmode_toggle()
     bpy.ops.mesh.select_all(action='TOGGLE')
     bpy.ops.transform.shrink_fatten(value=0.0769038, use_even_offset=False, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
     bpy.ops.sculpt.sculptmode_toggle()
     bpy.context.object.data.remesh_voxel_size = 0.0265
     bpy.ops.object.voxel_remesh()
     bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")
     #bpy.ops.mesh.sculpt_vertex_color_add()

    
def isMasked(context):
     bmeshContainer = bmesh.new() # New bmesh container
     bmeshContainer.from_mesh(context.sculpt_object.data) # Fill container with our object        
     mask = bmeshContainer.verts.layers.paint_mask.verify() # Set the active mask layer as custom layer
     print("number of elements "+ str(bmeshContainer.verts.layers.paint_mask.verify()))
     bmeshContainer.verts.ensure_lookup_table() # Just incase > Remove if unneccessary   
     filtered_list = list(filter(lambda x: (x[mask] > 0), bmeshContainer.verts))      
     print("number of elements "+str(len(filtered_list)))   
     return len(filtered_list)>0; 

def pivot_to_unmasked():
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    bpy.context.object.use_mesh_mirror_x = False
    bpy.context.object.use_mesh_mirror_y = False
    bpy.context.object.use_mesh_mirror_z = False
    bpy.ops.sculpt.set_pivot_position(mode ='UNMASKED')

def duplicate(context):
        currentObject = context.active_object
        #bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.sculpt.sculptmode_toggle()
        pivot_to_unmasked()
        #bpy.ops.mesh.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = currentObject
        currentObject.select_set(True)
        #bpy.ops.mesh.sculpt_vertex_color_add()

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
        bpy.ops.mesh.paint_mask_slice(new_object=True)
        bpy.ops.object.mode_set(mode='SCULPT')
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
        #main(context)
        print("bbp_duplicate---")
        duplicate(context)

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
            bpy.ops.mesh.paint_mask_extract()
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            duplicate(context)

        bpy.ops.object.mode_set(mode='OBJECT')
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
        print("new dimensions "+str(context.active_object.dimensions) )
        bpy.ops.object.mode_set(mode='OBJECT')
     
        print("new dimensions x "+str(dx) )
        print("new dimensions y "+str(dy) )
        print("new dimensions z "+str(dz) )
        bpy.context.object.location = [lx,ly,lz]
        bpy.context.view_layer.update() 
        print("altered dimensions "+str( bpy.context.object.dimensions) )
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode='SCULPT')
        #bpy.ops.object.delete_all_modifiers()
        pivot_to_unmasked()
     
        return {'FINISHED'}    


     

