import bpy

for b in bpy.context.object.data.edit_bones:
    if len(b.children)>0:
        child = b.children[0]
        b.tail = child.head
        #child.use_connect = True #Not what I needed