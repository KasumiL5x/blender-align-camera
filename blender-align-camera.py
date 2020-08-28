bl_info = {
	"name": "Align Camera",
	"author": "Daniel Green (KasumiL5x)",
	"version": (1, 0),
	"blender": (2, 83, 5),
	"location": "",
	"description": "Aligns the viewport camera to the selected polygons.",
	"category": "Development"
}

import bpy

class DEV_OT_align_camera(bpy.types.Operator):
	bl_idname = 'dev.align_camera'
	bl_label = 'Align Camera'

	# @classmethod
	# def poll(self, context):
	# 	# RegionView3D is accessible & 1+ faces are selected.
	# 	return len(self.__get_selected_faces())
	# #end

	def execute(self, context):
		selected_faces = self.__get_selected_faces()
		return {'FINISHED'}
	#end

	def __get_selected_faces(self):
		# Active object (if multiple are selected, first; if none selected, last active).
		obj = bpy.context.object

		# Safety check for no mesh.
		# if None == obj or obj.type != 'MESH':
		# 	return []

		# Store old mode and switch to edit mode (faces only valid in edit mode).
		# old_mode = obj.mode
		# bpy.ops.object.mode_set(mode='EDIT')

		# Extract selected faces (must toggle for the list to update, not sure if it's a bug?).
		bpy.ops.object.editmode_toggle()
		selected_faces = list(filter(lambda x: x.select, bpy.context.object.data.polygons))
		bpy.ops.object.editmode_toggle()

		# Restore old edit mode.
		# bpy.ops.object.mode_set(mode=old_mode)

		return selected_faces
	#end
#end

class DEV_PT_align_camera(bpy.types.Panel):
	bl_label = "Align Camera"
	bl_idname = "DEV_PT_align_camera"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Viewport Align"
	bl_context = "mesh_edit" # https://blender.stackexchange.com/a/73154

	def draw(self, context):
		layout = self.layout

		layout.label(text='Align Camera')
		layout.operator(DEV_OT_align_camera.bl_idname)
	#end
#end

def register():
	bpy.utils.register_class(DEV_PT_align_camera)
	bpy.utils.register_class(DEV_OT_align_camera)
#end

def unregister():
	bpy.utils.unregister_class(DEV_PT_align_camera)
	bpy.utils.unregister_class(DEV_OT_align_camera)
#end

if __name__ == '__main__':
	register()