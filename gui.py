import bpy
 #draw panel       
class call_menu_tpqz(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.call_menu_tpqz"
    bl_label = "call_menu_tpqz"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #main(context)
        print("custom menu")
        bpy.ops.wm.call_menu(name=custom_menu_tpqz_sculpt.bl_idname)
        return {'FINISHED'} 
class bbpSculptViewPanelObject(bpy.types.Panel):
    """Creates the Create Object Panel"""
    bl_label = "TPQZ sculpt"
    bl_idname = "UI_PT_TpqzSculpt"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TPQZ"
        
    def draw(self, context):
        
        # usefull variables
        scene = context.scene 
        obj = context.object
        brush = context.tool_settings.sculpt.brush

        #-------------------------------------------------------------------------------------
        # pivot
        #-------------------------------------------------------------------------------------  
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        row = col.row()
        row.label(text="pivot:", icon="PIVOT_INDIVIDUAL")
        row = col.row()
        
        row.operator("object.bbp_sculpt_restore_x", text="sym",icon="ORIENTATION_GIMBAL")
        row.operator("sculpt.set_pivot_position", text="unmask",icon="ORIENTATION_LOCAL").mode='UNMASKED'
        row.operator("object.bbp_sculpt_unmasked_center", text="center",icon="ORIENTATION_VIEW")
        row.operator("sculpt.set_pivot_position", text="origin",icon="ORIENTATION_GLOBAL").mode='ORIGIN'

        #-------------------------------------------------------------------------------------
        # create
        #-------------------------------------------------------------------------------------
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        row = col.row()
        row.label(text="create:", icon="LAYERGROUP_COLOR_01")
        row = col.row()
        row.operator("object.bbp_sculpt", text="Xtract & Solidify",icon="OUTLINER_OB_VOLUME")
        row.operator("object.bbp_xtract", text="Xtract",icon="OUTLINER_OB_VOLUME")
        # row = col.row()
        # row.operator("object.bbp_copy_face_set", text="Xtract faceset",icon="MESH_CUBE")
        row = col.row()
        row.operator("object.bbp_editselect", text="masked edit",icon="OUTLINER_OB_VOLUME")
        row.operator("object.bbp_xtract_select_border", text="border edit",icon="OUTLINER_OB_VOLUME")
        row = col.row()
        row.operator("object.bbp_empty_object", text="empty edit",icon="OUTLINER_OB_VOLUME")  
        row = col.row()
        row.operator("object.bbp_duplicate", text="mesh duplicate",icon="OUTLINER_OB_VOLUME")
        
        #"object:"
        row.separator(factor=2)
        row = col.row()
        row.operator("object.bbp_insert_object", text="cube",icon="MESH_CUBE").value="cube"
        row.operator("object.bbp_insert_object", text="sphere",icon="MESH_UVSPHERE").value="sphere"
        row.operator("object.bbp_insert_object", text="cylinder",icon="MESH_CYLINDER").value="cylinder"
        row = col.row()
        row.operator("object.bbp_insert_object", text="torus",icon="MESH_TORUS").value="torus"
        row.operator("object.bbp_insert_object", text="cone",icon="MESH_CONE").value="cone"
        row.operator("object.bbp_insert_object", text="plane",icon="MESH_PLANE").value="plane"

        #-------------------------------------------------------------------------------------
        # face set/Mask
        #-------------------------------------------------------------------------------------
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        col.separator()
        row = col.row()
        row.label(text="face set :", icon="LAYERGROUP_COLOR_02")
        row = col.row()
        row.operator("sculpt.face_sets_create", text="visible", icon="FACE_MAPS").mode = 'VISIBLE'
        row.operator("sculpt.face_sets_init", text="loose", icon="FACE_MAPS").mode = "LOOSE_PARTS"
        row = col.row()
        row.operator("sculpt.face_sets_create", text="masked", icon="FACE_MAPS").mode = "MASKED"
        row.operator("object.bbp_mask_hidden_face_set", text="mask hidden", icon="FACE_MAPS") 
        row = col.row()
        row.operator("object.bbp_xpand_mask", text="expand mask", icon="FACE_MAPS")
      
        #-------------------------------------------------------------------------------------
        # split
        #-------------------------------------------------------------------------------------        
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        row = col.row()
        row.label(text="split:", icon="LAYERGROUP_COLOR_03")
        row = col.row()
        row.operator("object.bbp_mask_new_object", text="mask",icon="ADD")
        row.operator("object.bbp_split_hiddenpg", text="hidden",icon="MOD_PHYSICS")
        row.operator("object.bbp_split_group", text="loose",icon="OUTLINER_OB_POINTCLOUD")

        #-------------------------------------------------------------------------------------
        # Remesh
        #------------------------------------------------------------------------------------- 
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        col.separator()
        row = col.row()
        row.label(text="remesh:", icon="LAYERGROUP_COLOR_04")
        row = col.row()
        row.operator("object.bbp_remesh", text="1").value = "1"
        row.operator("object.bbp_remesh", text=".2").value = "0.2"
        row.operator("object.bbp_remesh", text=".07").value = "0.07"
        row.operator("object.bbp_remesh", text=".05").value = "0.05"
        row.operator("object.bbp_remesh", text=".03").value = "0.03"
        row.operator("object.bbp_remesh", text=".01").value = "0.01"

        #-------------------------------------------------------------------------------------
        # mesh ops
        #------------------------------------------------------------------------------------- 
        row = col.row()
        row.label(text="mesh ops:", icon="LAYERGROUP_COLOR_05")
        row = col.row()
        row.operator("object.bbp_close_hole", text="close holes")
        row.operator("object.bbp_mask_subdivide", text="mask subdivide")
        row = col.row()
        row.operator("object.bbp_spherize", text="sb-sphere")    
        row = layout.row(align=True)
        col = row.column()
        col.prop(scene, 'ratio_float', text="val")
        col = row.column()
        col.operator("object.bbp_decimate", text="decimate")
        row = layout.row(align=True)  # Align=True keeps spacing tight
        # First column: Float property
        col1 = row.column()
        col1.prop(scene, 'solidify_float', text="val")

        # Second column: Operator button
        col2 = row.column()
        col2.operator("object.bbp_sculpt_solidify", text="Solidify")

        # Third column: Boolean toggle
        col3 = row.column()
        col3.prop(scene, "solidify_bool", text="Apply")

        #-------------------------------------------------------------------------------------
        # delete
        #------------------------------------------------------------------------------------- 
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        row = col.row()
        row = col.row()
        row.label(text="delete:", icon="CANCEL")
        row = col.row()
        row.operator("object.bbp_delete_mesh", text="mesh",icon="CANCEL")
        row.operator("object.bbp_delete_hiddenpg", text="hidden face set",icon="CANCEL")
        row = col.row()
        row.operator("object.bbp_delete_masked", text="masked",icon="CANCEL")
        row.operator("sculpt.paint_mask_slice", text="masked&close",icon="CANCEL").new_object=False
        row = col.row()
        row.operator("object.bbp_delete_by_symetry", text="byX",icon="CANCEL").value = "X"
        row.operator("object.bbp_delete_by_symetry", text="byY",icon="CANCEL").value = "Y"
        row.operator("object.bbp_delete_by_symetry", text="byZ",icon="CANCEL").value = "Z"
        row = col.row()
        
        #-------------------------------------------------------------------------------------
        # join
        #------------------------------------------------------------------------------------- 
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        row = col.row()
        row.label(text="join:", icon="MOD_BOOLEAN")
        row = col.row()
        row.operator("object.bbp_join_meshes", text="join from outliner",icon="LINKED")
        row = layout.row()
        col = row.column()
        col.prop(scene, "list_chosen_object",text="Target",icon="LINKED")
        col = row.column()
        row.operator("object.bbp_join_choosed_object", text="join",icon="LINKED")
      
        #-------------------------------------------------------------------------------------
        # boolean
        #-------------------------------------------------------------------------------------  

        # New row
        row = layout.row()
        # Bool diff button
        col = row.column()
        col.operator('object.bbp_boolean', text='Difference', icon='MOD_BOOLEAN').value="DIFFERENCE"
        
        # Bool union button
        col = row.column()
        col.operator('object.bbp_boolean', text='Union', icon='MOD_BOOLEAN').value="UNION"

        # Bool union button
        col = row.column()
        col.operator('object.bbp_boolean', text='Intersect', icon='MOD_BOOLEAN').value="INTERSECT"
        #-------------------------------------------------------------------------------------
        # symmetry
        #------------------------------------------------------------------------------------- 

        layout = self.layout
        box = layout.box()
        col = box.column(align = True)

        row = col.row()
        row.label(text="Flip/Sim/Slice/Rotate:", icon="MOD_MIRROR")

        # Flip 
        row = col.row()
        row.operator('object.bbp_mirror', text='FlipX', icon='MOD_MIRROR').value = "X"
        row.operator('object.bbp_mirror', text='FlipY', icon='MOD_MIRROR').value = "Y"
        row.operator('object.bbp_mirror', text='FlipZ', icon='MOD_MIRROR').value = "Z"

        # Symmetrize negative
        row = col.row()
        row.operator('object.bbp_symetry', text="SymX", icon='MOD_MESHDEFORM').value = "X"
        row.operator('object.bbp_symetry', text="SymY", icon='MOD_MESHDEFORM').value = "Y"
        row.operator('object.bbp_symetry', text="SymZ", icon='MOD_MESHDEFORM').value = "Z"

        # Slice
        row = col.row()
        row.operator('object.bbp_split_by_symetry', text='SliceX', icon='MOD_MIRROR').value = "X"
        row.operator('object.bbp_split_by_symetry', text='SliceY', icon='MOD_MIRROR').value = "Y"
        row.operator('object.bbp_split_by_symetry', text='SliceZ', icon='MOD_MIRROR').value = "Z"

        row = col.row()
        row.operator('object.bbp_rotate', text='RotateX', icon='MOD_MIRROR').value = "X"
        row.operator('object.bbp_rotate', text='RotateY', icon='MOD_MIRROR').value = "Y"
        row.operator('object.bbp_rotate', text='RotateZ', icon='MOD_MIRROR').value = "Z"


class custom_menu_tpqz_sculpt(bpy.types.Menu):
    bl_label = "TPQZ Custom Menu"
    bl_idname = "OBJECT_MT_custom_menu_tpqz"


    def draw(self, context):
        brush = context.tool_settings.sculpt.brush
        layout = self.layout
        scene = context.scene

        layout.prop(brush, 'use_frontface', text="front")  
        layout.prop(brush, 'use_automasking_face_sets', text="faces set")  
        layout.prop(brush, 'use_automasking_topology', text="topo") 

        layout.operator("object.bbp_focal_view", text="focal 35",icon="RESTRICT_RENDER_ON").value = "35"
        layout.operator("object.bbp_focal_view", text="focal 50",icon="RESTRICT_RENDER_ON").value = "50"
        layout.operator("object.bbp_focal_view", text="focal 80",icon="RESTRICT_RENDER_ON").value = "80"
        layout.operator("object.bbp_focal_view", text="focal 90",icon="RESTRICT_RENDER_ON").value = "90" 
        
        layout.operator("object.bbp_sculpt_fade", text="Fade",icon="GHOST_ENABLED").value = "fade"
        layout.operator("object.bbp_sculpt_fade", text="Unfade",icon="OUTLINER_OB_LIGHT").value = "unfade"
       

def draw_item(self, context):
    layout = self.layout
    layout.menu(CustomMenuTpqz.bl_idname)
