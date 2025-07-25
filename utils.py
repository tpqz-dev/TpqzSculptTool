import bpy
import bmesh

def pivot_to_unmasked():
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    bpy.context.object.use_mesh_mirror_x = False
    bpy.context.object.use_mesh_mirror_y = False
    bpy.context.object.use_mesh_mirror_z = False
    bpy.ops.sculpt.set_pivot_position(mode ='UNMASKED')

def force_symmetry_x():
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
    print("function call ---")

    # Store original active object
    original_obj = bpy.context.object

    # Ensure we're in SCULPT mode
    if bpy.context.object.mode != 'SCULPT':
        bpy.ops.object.mode_set(mode='SCULPT')

    # Run mask extract
    bpy.ops.sculpt.paint_mask_extract()

    # The new extracted object becomes the active object
    extracted_obj = bpy.context.object
    print(f"Extracted object: {extracted_obj.name}")

    # Find the solidify modifier on extracted object
    solidify_mod = None
    for mod in extracted_obj.modifiers:
        if mod.type == 'SOLIDIFY':
            solidify_mod = mod
            break

    if solidify_mod:
        solidify_mod.thickness = 0.05
        solidify_mod.offset = 1.0

        # Apply modifier
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(modifier=solidify_mod.name)
    else:
        print("No solidify modifier found!")

    # Enter EDIT mode to shrink/fatten
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.transform.shrink_fatten(
        value=0.0769038,
        use_even_offset=False,
        mirror=True,
        use_proportional_edit=False
    )

    # Back to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Apply voxel remesh
    extracted_obj.data.remesh_voxel_size = 0.0265
    bpy.ops.object.voxel_remesh()

    # Back to sculpt mode and select Draw brush
    bpy.ops.object.mode_set(mode='SCULPT')
    bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")

    # Optionally re-select original object 
    # bpy.context.view_layer.objects.active = original_obj

    print("Sculpt extract complete!")




    
def isMasked(context):
     bpy.ops.object.mode_set(mode='SCULPT')
     bm = bmesh.new() # New bmesh container
     bm.from_mesh(context.sculpt_object.data) # Fill container with our object        
     mask = bm.verts.layers.float.get('.sculpt_mask')# get mask points
    #print("number of elements "+ str(bm.verts.layers.paint_mask.verify()))
     bm.verts.ensure_lookup_table() # Just incase > Remove if unneccessary   
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
        bpy.context.view_layer.objects.active = currentObject
        currentObject.select_set(True)

def set_move_brush():
    bpy.ops.wm.tool_set_by_id(name="builtin.move")

    def is_null(value):
        if value is None:
            return True
        else:
            return False
        
def select_masked_verts(context):
    obj = context.object

    if obj is None or obj.type != 'MESH':
        print("Pas d'objet mesh sélectionné.")
        return

    if context.mode != 'SCULPT':
        bpy.ops.object.mode_set(mode='SCULPT')

    me = obj.data

    # read masked SCULPT
    bm = bmesh.new()
    bm.from_mesh(me)
    mask_layer = bm.verts.layers.float.get('.sculpt_mask')

    if not mask_layer:
        print("no mask.")
        bm.free()
        return

    masked_verts_indices = []
    bm.verts.ensure_lookup_table()
    for i, v in enumerate(bm.verts):
        if v[mask_layer] > 0.0:
            masked_verts_indices.append(i)

    bm.free()

    # EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()
   

    # select all
    for v in bm.verts:
        v.select = False

    # select vertices masked
    for i in masked_verts_indices:
        bm.verts[i].select = True

    bmesh.update_edit_mesh(me)
    print(f"{len(masked_verts_indices)} sommets masqués sélectionnés.")