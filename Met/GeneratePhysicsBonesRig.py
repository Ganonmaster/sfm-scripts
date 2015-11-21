import bpy

def extrude(x, y, z):
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":0, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

#what the script expects: You are in pose mode, with one or more bones selected. If you are doing hair, you need to do one string at a time.
#when finished: rename first vertex group to the parent bone of your bones.

#Way it works:
#	make a mesh that has a vertex at each bone (to later apply cloth physics on)
#	make a vertexgroup for each vert
#	make a vertexgroup that contains the whole mesh
#	extrude edges - having faces is necessary for collision detection.
#	enable cloth simulation, set pin.

#	unparent selected bones
#	sort them based on height(I'm not sure why I did this instead of sorting by hierarchy)
#	make copy location and stretch to constraints using the previously created mesh and its vertex groups
#	and then it should work! Alt+A to find out!

myArmature = bpy.context.object

bones = sorted(bpy.context.selected_pose_bones, key=lambda a:a.head.z, reverse=True)

bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=bones[0].head, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
#plane gets auto selected
meshName = "_Phys_%s" % bones[0].name
bpy.context.object.name = meshName

physMesh = bpy.context.object
physVerts = physMesh.data.vertices

#TODO: Instead of deselecting all, then reselecting one, find out how to deselect one.. >.>
bpy.ops.object.editmode_toggle() #ON
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.editmode_toggle() #OFF

#gotta select verts while in object mode(weird...)
for i in range(1,4):
    physVerts[i].select=True

bpy.ops.object.editmode_toggle() #ON
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.editmode_toggle() #OFF

physVerts[0].select=True
physVerts[0].co = (0, 0, 0)

bpy.ops.object.editmode_toggle() #ON
#extruding vert that we selected

for i in range(0, len(bones)):
    extrude(
    bones[i].tail.x - bones[i].head.x, 
    bones[i].tail.y - bones[i].head.y, 
    bones[i].tail.z - bones[i].head.z)

bpy.ops.object.editmode_toggle() #OFF

for i in range(0, len(physVerts)):
    bpy.ops.object.vertex_group_add() #adding a vGroup
    physMesh.vertex_groups[i].add([i], 1.0, 'ADD')    #adding vert to vGroup #(vertexIndex, Weight, 'garbage')
    if(i>0):
        physMesh.vertex_groups[i].name = bones[i-1].name #naming vGroup
    else:
        physMesh.vertex_groups[i].name = "Pin"
        
#extruding everything to have faces, which is necessary for collision.
bpy.ops.object.editmode_toggle()    #ON
bpy.ops.mesh.select_all(action='SELECT')
extrude(0, 0, 0)
bpy.ops.object.editmode_toggle()    #OFF

#making a vertexgroup that has all verts, which should be manually renamed to the parent bone of the string of bones.
bpy.ops.object.vertex_group_add()
lastG = physMesh.vertex_groups[len(physMesh.vertex_groups)-1]
lastG.name = "ALL"
for v in physVerts:
    lastG.add([v.index], 1.0, 'ADD')

bpy.ops.object.modifier_add(type='ARMATURE')
physMesh.modifiers["Armature"].object = myArmature
bpy.ops.object.modifier_add(type='CLOTH')
physMesh.modifiers["Cloth"].settings.use_pin_cloth=True
physMesh.modifiers["Cloth"].settings.vertex_group_mass = physMesh.vertex_groups[0].name
bpy.ops.object.modifier_add(type='COLLISION')

#parenting mesh to armature
physMesh.parent = myArmature

#We are done with everything we have to do on the mesh



#getting the constraints and unparenting done on the bones
bpy.context.scene.objects.active = myArmature

for i in range(0, len(bones)):
    CL = bones[i].constraints.new(type='COPY_LOCATION')
    CL.target = physMesh
    CL.subtarget = physMesh.vertex_groups[i].name
    
    ST = bones[i].constraints.new(type='STRETCH_TO')
    ST.target = physMesh
    ST.subtarget = physMesh.vertex_groups[i+1].name

#probably wanna do parent clearing at the end, because it deselects shit pretty weirdly.
bpy.ops.object.editmode_toggle() #ON
bpy.ops.armature.parent_clear(type='CLEAR')
