# Inefficient little script that compares bones between several armatures, deletes duplicates and joins the result

import bpy
from pprint import pprint

selected_objects = [ o for o in bpy.context.scene.objects if o.select]
active_object = bpy.context.object

duplicate_bone_set = set()

for object in selected_objects:
    if object != active_object:
        selected_edit_bones = object.data.bones
        
        for bone in selected_edit_bones:
            for active_bone in active_object.data.bones:
                if bone.name == active_bone.name:
                    print('Found duplicate bone:', bone.name)
                    duplicate_bone_set.add(bone.name)

for object in selected_objects:
    if object != active_object:
        bpy.context.scene.objects.active = object
        bpy.ops.object.mode_set(mode='EDIT')
        selected_edit_bones = object.data.edit_bones
        
        for bone in selected_edit_bones:
            if bone.name in duplicate_bone_set:
                print('deleting bone', bone.name)
                selected_edit_bones.remove(bone)
        bpy.ops.object.mode_set(mode='OBJECT')


bpy.context.scene.objects.active = active_object
bpy.ops.object.join()
