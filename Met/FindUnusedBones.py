import bpy

vGroupList = []
myObject = bpy.context.object

for mesh in myObject.children:              #for each mesh
    for vGroup in mesh.vertex_groups:       #for each vertexgroup
        vGroupList.append(vGroup.name)
        
for bone in myObject.data.bones:            #for each bone
    if(bone.name not in vGroupList):
        bone.name = "UNUSED_"+bone.name