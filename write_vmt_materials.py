import bpy

#print(list(bpy.data.materials))

# absolute path to the vmt write directory
export_path = "F:/SteamLibrary/SteamApps/common/sourcefilmmaker/content/usermod/modelsrc/mats/"

# source engine relative path to textures
path_relative = "models/path_to_your_textures/"

for material in bpy.data.materials:
    print(material.active_texture.name)
    texture_name = material.active_texture.name
    
    part = texture_name.rpartition('.')
    texture_name = part[0]
            
    file = open(export_path+material.name+".vmt", 'a')
    file.write("\"VertexLitGeneric\"\n{\n $basetexture \"" + path_relative + texture_name + "\"\n \n}")
    file.close()
