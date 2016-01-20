import bpy

ob = bpy.context.object

if ob.type == 'ARMATURE':

    for bone in ob.pose.bones:
        print(bone)
        bone.custom_shape = None
