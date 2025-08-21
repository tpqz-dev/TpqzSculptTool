
import bpy
from  .utils import *
class bbp_remesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_remesh"
    bl_label = "bbp_remesh"
    #create property
    value: bpy.props.StringProperty(name = 'value', default = '1')
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("remesh "+self.value)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.fill_holes(sides=0)
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.context.object.data.remesh_mode = 'QUAD'
        #bpy.ops.object.quadriflow_remesh (target_faces=int(3000))
        #bpy.ops.object.quadriflow_remesh(use_mesh_symmetry=False, use_preserve_sharp=False, use_preserve_boundary=False, preserve_paint_mask=False, smooth_normals=False, mode='FACES', target_faces=int(self.value))
        #voxel remesh
        bpy.context.object.data.remesh_voxel_size = float(self.value)
        bpy.context.object.data.remesh_voxel_adaptivity = 0
        bpy.context.object.data.use_remesh_fix_poles = True
        bpy.context.object.data.use_remesh_preserve_attributes = True
        bpy.ops.object.voxel_remesh()
        #force_symmetry_x()
        return {'FINISHED'} 

class bbp_close_hole(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_close_hole"
    bl_label = "bbp_close_hole"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_close_hole---")
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.fill_holes(sides=0 )
        bpy.ops.object.editmode_toggle()
        bpy.ops.sculpt.sculptmode_toggle()
        #force_symmetry_x()
        return {'FINISHED'} 



class bbp_mask_subdivide(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_mask_subdivide"
    bl_label = "bbp_mask_subdivide"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_mask_subdivide---")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')  
        bpy.ops.object.mode_set(mode='SCULPT')
        print("select masked verices---")
        select_masked_verts(context)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        
        # bpy.ops.object.editmode_toggle()
        # bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.subdivide()
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'} 
 
class bbp_mask_unsubdivide(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_mask_unsubdivide"
    bl_label = "bbp_mask_unsubdivide"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_mask_subdivide---")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')  
        bpy.ops.object.mode_set(mode='SCULPT')
        print("select masked verices---")
        select_masked_verts(context)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.unsubdivide()
        bpy.ops.object.editmode_toggle()
        bpy.ops.sculpt.sculptmode_toggle()
        return {'FINISHED'} 

class bbp_spherize(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_spherize"
    bl_label = "bbp_spherize"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_spherize---")
        # 
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        bpy.ops.transform.shrink_fatten(value=0.087961, use_even_offset=False, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.tosphere(value=1, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.object.voxel_remesh()
        #force_symmetry_x()
        return {'FINISHED'}


class bbp_decimate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_decimate"
    bl_label = "bbp_decimate"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context)
        print("bbp_decimate---")
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = bpy.context.scene.ratio_float
        bpy.context.object.modifiers["Decimate"].use_symmetry = True
        bpy.context.object.modifiers["Decimate"].symmetry_axis = 'X'
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier="Decimate")
        #force_symmetry_x()
        return {'FINISHED'}


        
class bbp_sculpt_solidify(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_solidify"
    bl_label = "bbp_sculpt_solidify"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("bbp_sculpt_solidify ")
        active_obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        bool_mod = active_obj.modifiers.new(type="SOLIDIFY", name="TPQZ_BOOL")
        bool_mod.thickness = bpy.context.scene.solidify_float
        print("name = "+bool_mod.name)
        if bpy.context.scene.solidify_bool==True :
            print("apply solidify")
            #bool_mod.modifier_apply(modifier="TPQZ_BOOL")
            bpy.ops.object.modifier_apply(modifier="TPQZ_BOOL")
            #force_symmetry_x()

        else:
            print("no apply")
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

class bbp_sculpt_merge(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_merge"
    bl_label = "bbp_sculpt_merge"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("bbp_sculpt_merge")
        active_obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        bool_mod = active_obj.modifiers.new(type="WELD", name="TPQZ_WELD_BOOL")
        bool_mod.merge_threshold = bpy.context.scene.merge_float
        print("name = "+bool_mod.name)
        if bpy.context.scene.merge_bool==True :
            print("apply weld")
            bpy.ops.object.modifier_apply(modifier="TPQZ_WELD_BOOL")
            

        else:
            print("no apply")
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

class bbp_sculpt_inflate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_sculpt_inflate"
    bl_label = "bbp_sculpt_inflate"
    bl_options = {"REGISTER", "UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        print("bbp_sculpt_inflate")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        active_obj = bpy.context.active_object
        bpy.ops.transform.shrink_fatten(value=bpy.context.scene.inflate_float, use_even_offset=False, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False)

        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}



class bbp_mirror(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_mirror"
    bl_label = "bbp_mirror"
    bl_options = {"REGISTER", "UNDO"}
    #create property
    value: bpy.props.StringProperty(name = 'value', default = 'X')
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and  context.active_object.mode=="SCULPT"

    def execute(self, context):
        #main(context
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')    
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        if self.value =="X":
            bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
        elif self.value =="Y":
            bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((0, 1, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
        else :
            bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((0, 0, 1), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))

        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        bpy.ops.object.mode_set(mode='SCULPT')
        #force_symmetry_x()
        return {'FINISHED'}


class bbp_symetry(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_symetry"
    bl_label = "bbp_symetry"
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
            bpy.ops.mesh.symmetrize(direction='NEGATIVE_X')
        elif val=="Y":
            bpy.ops.mesh.symmetrize(direction='NEGATIVE_Y')
        else:
            bpy.ops.mesh.symmetrize(direction='NEGATIVE_Z')

        bpy.ops.object.mode_set(mode='SCULPT')
        #force_symmetry_x()
        return {'FINISHED'}
    

class bbp_rotate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_rotate"
    bl_label = "bbp_rotate"
    bl_options = {"REGISTER", "UNDO"}
    value: bpy.props.StringProperty(name='value', default='X')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == "SCULPT"

    def execute(self, context):
        val = self.value

        if val == "X":
            bpy.ops.transform.rotate(value=0.785398, orient_axis='X')  # 45 degrees in radians
        elif val == "Y":
            bpy.ops.transform.rotate(value=0.785398, orient_axis='Y')  # 45 degrees in radians
        elif val == "Z":
            bpy.ops.transform.rotate(value=0.785398, orient_axis='Z')  # 45 degrees in radians

        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

class bbp_quadriflow_remesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_quadriflow_remesh"
    bl_label = "Quadriflow Remesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object found")
            return {'CANCELLED'}

        print(f"Starting Quadriflow Remesh with faces")
        
        try:
      
            bpy.ops.object.quadriflow_remesh(
            use_mesh_symmetry= bpy.context.scene.mesh_symmetry,
            use_preserve_sharp=bpy.context.scene.preserve_sharp ,
            use_preserve_boundary=bpy.context.scene.preserve_boundary ,
            preserve_attributes=context.scene.preserve_attributes ,
            smooth_normals=bpy.context.scene.smooth_normals,
            target_faces=bpy.context.scene.target_faces,
            mode="FACES"
            )

        except RuntimeError as re:
            self.report({'ERROR'}, "Remeshing: {0}".format(re))
           
        else:
            self.report({'INFO'}, "Remeshing completed") 
            

        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}
    
class bbp_quadriflow_auto_remesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.bbp_quadriflow_auto_remesh"
    bl_label = "Quadriflow auto_remesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object found")
            return {'CANCELLED'}

        print(f"Starting Quadriflow Remesh with faces")
        
        try:
            #decimate
            print("bbp_decimate---")
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].ratio = 0.2
            bpy.context.object.modifiers["Decimate"].use_symmetry = True
            bpy.context.object.modifiers["Decimate"].symmetry_axis = 'X'
            bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier="Decimate")

        
            #quadriflow
            bpy.ops.object.quadriflow_remesh(
            use_mesh_symmetry= bpy.context.scene.mesh_symmetry,
            use_preserve_sharp=bpy.context.scene.preserve_sharp ,
            use_preserve_boundary=bpy.context.scene.preserve_boundary ,
            preserve_attributes=context.scene.preserve_attributes ,
            smooth_normals=bpy.context.scene.smooth_normals,
            target_faces=bpy.context.scene.target_faces,
            mode="FACES")

            #merge
            bpy.ops.object.mode_set(mode='OBJECT')
            bool_mod = obj.modifiers.new(type="WELD", name="TPQZ_WELD_BOOL")
            bool_mod.merge_threshold = 0.1 #bpy.context.scene.merge_float
            print("name = "+bool_mod.name)
            print("apply weld")
            bpy.ops.object.modifier_apply(modifier="TPQZ_WELD_BOOL")
            bpy.ops.sculpt.sculptmode_toggle()
    
        except RuntimeError as re:
            self.report({'ERROR'}, "Remeshing: {0}".format(re))
        else:
            self.report({'INFO'}, "Remeshing completed")  
        
        
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}
    