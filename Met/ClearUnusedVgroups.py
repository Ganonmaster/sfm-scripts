import bpy

#Removes all vertex groups that don't have a bone associated with them.
#Select armature, script will clean all its children.

armature = bpy.context.object

bones = armature.data.bones
boneNames = []
for b in bones:
    boneNames.append(b.name)
    
print(boneNames)

meshes = armature.children

for m in meshes:
    vGroups = m.vertex_groups
    for v in vGroups:
        if v.name not in boneNames:
            print("removed %s" %v.name)
            vGroups.remove(v)