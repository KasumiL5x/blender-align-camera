import bpy
import mathutils

def __get_average_normal(obj, faces):
    # https://blenderartists.org/t/vector-from-local-to-global-space/542177
    mat = obj.matrix_world.inverted().transposed().to_3x3()
    average = mathutils.Vector()
    for f in faces:
        ws_normal = mat @ f.normal # Convert normal to worldspace.
        ws_normal.normalize()
        average += ws_normal
    average.normalize()
    return average

def __get_average_position(obj, faces):
    average = mathutils.Vector()
    for f in faces:
        average += obj.matrix_world @ f.center
    return average / len(faces)

def __get_camera_position(mat):
    inv = mat.inverted()
    return mathutils.Vector((inv[0][3], inv[1][3], inv[2][3]))

def __set_camera_attrs(position, target):
    raise NotImplementedError()
    
def lookat(pos, target):
    camdir = (pos - target).normalized()
    worldUp = mathutils.Vector((0, 0, 1))
    right = worldUp.cross(camdir)
    up = camdir.cross(right)
    
    m1 = mathutils.Matrix()
    m2 = mathutils.Matrix()
    
    # other
    m1[0] = mathutils.Vector((right.x, right.y, right.z, 0))
    m1[1] = mathutils.Vector((up.x, up.y, up.z, 0))
    m1[2] = mathutils.Vector((camdir.x, camdir.y, camdir.z, 0))
    
    # pos
    m2[0][3] = -pos.x
    m2[1][3] = -pos.y
    m2[2][3] = -pos.z
    
    lookat = m1 @ m2
    return lookat
        
def look_at_selected_faces():
    # Need to switch to object mode or the poly select count isn't right.
    bpy.ops.object.mode_set()
    
    # TODO: Clean this up as it may be None, not a mesh, etc.
    # Get selected faces of the active object.
    selected_faces = []
    for ply in bpy.context.selected_objects[0].data.polygons:
        if ply.select:
            selected_faces.append(ply)
    
    if not len(selected_faces):
        print('No faces selected.')
        return
    
    # Compute average normal.
    average_normal = __get_average_normal(bpy.context.selected_objects[0], selected_faces)
    # Compute average position.
    average_position = __get_average_position(bpy.context.selected_objects[0], selected_faces)
    
    v3d = next(filter(lambda x: x.type == 'VIEW_3D', bpy.context.screen.areas), None)
    r3d = v3d.spaces[0].region_3d
    
    # Debug display as an arrow.
#    bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=average_position)
#    bpy.context.object.rotation_mode = 'QUATERNION'
#    bpy.context.object.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(average_normal)

    #
    #
    #
    # TODO: Get the viewport region_3d and then pull the position from it.
    #       Then fill in the rest with the matrix setting etc.
    #       I think I can ignore the matrices and set params then tell it to update the matrices internally?

    # TODO: Have some condition that defines this, maybe even a UI element in a Panel?
    camera_position = __get_camera_position(r3d.view_matrix)
    
    # distance from camera's current position to average position
    initial_distance = (average_position - camera_position).length
    # new position from average along normal by the initial camera's distance
    new_position = (average_position + average_normal * initial_distance)
    
    lmat = lookat(new_position, average_position)
    r3d.view_matrix = lmat
    r3d.view_location = average_position
    
    # Set camera.
#    __set_camera_attrs(new_position, average_position)
    # https://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/CommandsPython/viewPlace.html
#    cmds.viewPlace(str(active_camera), an=True, eye=new_position, la=average_position, up=[0.0, 1.0, 0.0])
    
    # Back to edit mode (todo: go back to original mode)
    #bpy.ops.object.mode_set(mode='EDIT')
    
look_at_selected_faces()