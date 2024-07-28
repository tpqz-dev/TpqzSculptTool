import bpy
import bmesh

def pivot_to_unmasked():
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    bpy.context.object.use_mesh_mirror_x = False
    bpy.context.object.use_mesh_mirror_y = False
    bpy.context.object.use_mesh_mirror_z = False
    bpy.ops.sculpt.set_pivot_position(mode ='UNMASKED')

def force_symmetry_x():
    #bool_force_x = bpy.types.Scene.tpqz_force_symmetry 
    #print("bool_force_x = "  )
    #print( bool_force_x )
    #if bool_force_x == True :
    bpy.context.object.use_mesh_mirror_x = True
    bpy.context.object.use_mesh_mirror_y = False
    bpy.context.object.use_mesh_mirror_z = False
    bpy.ops.sculpt.set_pivot_position(mode='UNMASKED')

def pivot_to_center():
        bpy.context.object.use_mesh_mirror_x = False
        bpy.ops.sculpt.set_pivot_position(mode='UNMASKED')

def greaterDimension(dim):
    dx= dim[0]
    dy= dim[1]
    dz= dim[2]
    m1 = max(dx,dy)
    m2 = max(m1,dz)
    return m2/2


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
     bpy.ops.object.mode_set(mode='SCULPT')
     bm = bmesh.new() # New bmesh container
     bm.from_mesh(context.sculpt_object.data) # Fill container with our object        
     mask = bm.verts.layers.float.get('.sculpt_mask')# get mask points
    #print("number of elements "+ str(bm.verts.layers.paint_mask.verify()))
     bm.verts.ensure_lookup_table() # Just incase > Remove if unneccessary   
    # filtered_list = list(filter(lambda x: (x[mask] > 0), bm.verts))
     res = False if mask is None else True
     return res; 

  
        
def duplicate(context):
        currentObject = context.active_object
        #bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
     
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.sculpt.sculptmode_toggle()
        force_symmetry_x()
        #bpy.ops.mesh.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = currentObject
        currentObject.select_set(True)
        #bpy.ops.mesh.sculpt_vertex_color_add()

def set_move_brush():
    bpy.ops.wm.tool_set_by_id(name="builtin.move")

    def is_null(value):
        if value is None:
            return True
        else:
            return False