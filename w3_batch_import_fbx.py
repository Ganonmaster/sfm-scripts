import os
import bpy

rootdir = 'E:/w3_export/characters/models/main_npc/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        
        if filepath.endswith(".fbx"):
            bpy.ops.import_scene.fbx( filepath = filepath )
