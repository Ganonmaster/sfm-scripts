import bpy
#This script will apply the shapekey in slot #1 as the Basis. Probably.

#What the script expects: Have the mesh selected, and your desired new base shape in slot 1. (don't delete your old basis, leave it to me <3)
#Read thingName from the info bar after sliding any shapekey:
#bpy.data.shape_keys[">THIS HERE<"].key_blocks["Smile"].value=0.69

thingName = "Key.000"

#Way it works:
    #Move newBase to top, set it to 1.
    #now do this for each shapekey:
        #set it to 1
        #make new from mix
        #delete old one
        #rename new one to old one's name
    #delete your old Basis
    #you should be good.



shapeKeys = bpy.data.shape_keys[thingName].key_blocks
length = len(shapeKeys)

for key in shapeKeys: #wiping values
    key.value = 0

shapeKeys[1].value = 1
bpy.ops.object.shape_key_add(from_mix=True) #duplicating goal shape (is this even necessary? I don't care, won't fix what's working >D)
#note: the new shapekey gets automatically selected.
bpy.ops.object.shape_key_move(type='TOP')

for i in range(0, length-2): #for each shapekey, but we will be altering the array we would be iterating through, so this feels safer than foreach.
	bpy.context.object.active_shape_key_index = 3 #we are using the number 3 rather than i because, again, we are altering the order as we are iterating.
	shapeName = shapeKeys[3].name
	shapeKeys[3].value = 1
	bpy.ops.object.shape_key_add(from_mix=True) #selects new shapekey automatically
	bpy.context.object.active_shape_key_index = 3
	bpy.ops.object.shape_key_remove(all=False)
	bpy.data.shape_keys[thingName].key_blocks[length].name = shapeName #renaming new flex


#now I remove the old basis
bpy.context.object.active_shape_key_index = 0
bpy.ops.object.shape_key_remove(all=False)


bpy.context.object.active_shape_key_index = 1
bpy.ops.object.shape_key_remove(all=False)
shapeKeys[0].name="Basis"                   #like nothing ever happened.