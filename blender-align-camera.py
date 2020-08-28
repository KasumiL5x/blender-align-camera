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
import mathutils

class DEV_OT_align_camera(bpy.types.Operator):
	bl_idname = 'dev.align_camera'
	bl_label = 'Align Camera'

	@classmethod
	def poll(self, context):
		return (bpy.context.object is not None) and ('MESH' == bpy.context.object.type)
	#end

	def execute(self, context):
		obj = bpy.context.object
		selected_faces = self.__get_selected_faces(obj)
		r3d = self.__get_region3d()

		if not len(selected_faces):
			print('No faces selected.')
			return {'FINISHED'}

		# Average (world space) normal.
		average_normal = self.__get_average_normal(obj, selected_faces)
		# Average (world space) position.
		average_position = self.__get_average_position(obj, selected_faces)
		# Extract the camera's current position from its view matrix (world space).
		camera_position = self.__extract_camera_position(r3d.view_matrix)
		# Distance from the camera's current position to the average position.
		initial_distance = (average_position - camera_position).length
		# New camera position from average position along average normal by the camera's initial distance.
		new_cam_position = (average_position + average_normal * initial_distance)

		print(average_normal)
		print(average_position)
		print(camera_position)
		print(initial_distance)
		print(new_cam_position)

		return {'FINISHED'}
	#end

	def __get_region3d(self):
		# Get the 3D view area.
		v3c = next(filter(lambda x: 'VIEW_3D' == x.type, bpy.context.screen.areas), None)
		if None == v3c:
			return None

		# Same for the SpaceView3D. Seems to always be one but just in case.
		sv3d = next(filter(lambda x: 'VIEW_3D' == x.type, v3c.spaces), None)
		if None == sv3d:
			return None

		return sv3d.region_3d
	#end

	def __get_selected_faces(self, obj):
		# Extract selected faces (must toggle for the list to update, not sure if it's a bug?).
		bpy.ops.object.editmode_toggle()
		selected_faces = list(filter(lambda x: x.select, obj.data.polygons))
		bpy.ops.object.editmode_toggle()
		return selected_faces
	#end

	def __get_average_normal(self, obj, faces):
		# https://blenderartists.org/t/vector-from-local-to-global-space/542177
		mat = obj.matrix_world.inverted().transposed().to_3x3()
		average = mathutils.Vector()
		for f in faces:
			ws_normal = mat @ f.normal # Convert normal to worldspace.
			ws_normal.normalize()
			average += ws_normal
		average.normalize()
		return average
	#end

	def __get_average_position(self, obj, faces):
		average = mathutils.Vector()
		for f in faces:
			average += obj.matrix_world @ f.center
		return average / len(faces)
	#end

	def __extract_camera_position(self, mat):
		# FYI Blender uses "OpenGL oriented" matrices.
		inv = mat.inverted()
		return mathutils.Vector((inv[0][3], inv[1][3], inv[2][3]))
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