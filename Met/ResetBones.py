import bpy

for b in bpy.context.object.data.edit_bones:
    b.tail = b.head
    b.tail.z+=.01
    b.roll = 0