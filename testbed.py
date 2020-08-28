import bpy
import mathutils

def cam_pos(mat):
    inv = mat.inverted()
    return mathutils.Vector((inv[0][3], inv[1][3], inv[2][3]))

def set_cam_pos(mat, x, y, z):
    inv = mat.inverted()
    inv[0][3] = x
    inv[1][3] = y
    inv[2][3] = z
    return inv.inverted()

def set_cam_tgt(mat, campos, tgtpos):
    dir = (tgtpos-campos).normalized()
    
    inv = mat.inverted()
    inv[0][2] = dir.x
    inv[1][2] = dir.y
    inv[2][2] = dir.z
    return inv.inverted()

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


v3d = next(filter(lambda x: x.type == 'VIEW_3D', bpy.context.screen.areas), None)
r3d = v3d.spaces[0].region_3d

#print(r3d.view_matrix.inverted())
pos = cam_pos(r3d.view_matrix)
#print(pos)

lookat_mat = lookat(pos, mathutils.Vector((0, 0, 0)))

#new_mat = set_cam_pos(r3d.view_matrix, pos[0], pos[1], pos[2])
#new_mat = set_cam_tgt(new_mat, pos, mathutils.Vector((0, 0, 0)))
r3d.view_matrix = lookat_mat
r3d.view_location = (0,0, 0)
#r3d.update()