import bpy
# renaming from valve to blender convention for mirroring.
vGroupList = []
myObject = bpy.context.object

boneDict = {
    'ValveBiped.Bip01_Pelvis' : 'Pelvis',
    'ValveBiped.Bip01_Spine1' : 'Spine1',
    'ValveBiped.Bip01_Spine2' : 'Spine2',
    'ValveBiped.Bip01_Hips' : 'Hips',
    'ValveBiped.Bip01_Neck' : 'Neck',
    'ValveBiped.Bip01_Head' : 'Head',
    
    'ValveBiped.Bip01_L_Clavicle' : 'Clavicle.L',
    'ValveBiped.Bip01_R_Clavicle' : 'Clavicle.R',
    'ValveBiped.Bip01_L_Upperarm' : 'UpperArm.L',
    'ValveBiped.Bip01_R_Upperarm' : 'UpperArm.R',
    'ValveBiped.Bip01_L_UpperArm' : 'UpperArm.L',
    'ValveBiped.Bip01_R_UpperArm' : 'UpperArm.R',
    'ValveBiped.Bip01_L_Forearm' : 'Forearm.L',
    'ValveBiped.Bip01_R_Forearm' : 'Forearm.R',
    'ValveBiped.Bip01_L_Hand' : 'Hand.L',
    'ValveBiped.Bip01_R_Hand' : 'Hand.R',
    
    'ValveBiped.Bip01_L_Finger0' : 'Finger0.L',
    'ValveBiped.Bip01_L_Finger01' : 'Finger01.L',
    'ValveBiped.Bip01_L_Finger02' : 'Finger02.L',
    'ValveBiped.Bip01_L_Finger1' : 'Finger1.L',
    'ValveBiped.Bip01_L_Finger11' : 'Finger11.L',
    'ValveBiped.Bip01_L_Finger12' : 'Finger12.L',
    'ValveBiped.Bip01_L_Finger2' : 'Finger2.L',
    'ValveBiped.Bip01_L_Finger21' : 'Finger21.L',
    'ValveBiped.Bip01_L_Finger22' : 'Finger22.L',
    'ValveBiped.Bip01_L_Finger3' : 'Finger3.L',
    'ValveBiped.Bip01_L_Finger31' : 'Finger31.L',
    'ValveBiped.Bip01_L_Finger32' : 'Finger32.L',
    'ValveBiped.Bip01_L_Finger4' : 'Finger4.L',
    'ValveBiped.Bip01_L_Finger41' : 'Finger41.L',
    'ValveBiped.Bip01_L_Finger42' : 'Finger42.L',
    
    'ValveBiped.Bip01_R_Finger0' : 'Finger0.R',
    'ValveBiped.Bip01_R_Finger01' : 'Finger01.R',
    'ValveBiped.Bip01_R_Finger02' : 'Finger02.R',
    'ValveBiped.Bip01_R_Finger1' : 'Finger1.R',
    'ValveBiped.Bip01_R_Finger11' : 'Finger11.R',
    'ValveBiped.Bip01_R_Finger12' : 'Finger12.R',
    'ValveBiped.Bip01_R_Finger2' : 'Finger2.R',
    'ValveBiped.Bip01_R_Finger21' : 'Finger21.R',
    'ValveBiped.Bip01_R_Finger22' : 'Finger22.R',
    'ValveBiped.Bip01_R_Finger3' : 'Finger3.R',
    'ValveBiped.Bip01_R_Finger31' : 'Finger31.R',
    'ValveBiped.Bip01_R_Finger32' : 'Finger32.R',
    'ValveBiped.Bip01_R_Finger4' : 'Finger4.R',
    'ValveBiped.Bip01_R_Finger41' : 'Finger41.R',
    'ValveBiped.Bip01_R_Finger42' : 'Finger42.R',
        
    'ValveBiped.Bip01_L_Thigh' : 'Thigh.L',
    'ValveBiped.Bip01_R_Thigh' : 'Thigh.R',
    'ValveBiped.Bip01_L_Calf' : 'Calf.L',
    'ValveBiped.Bip01_R_Calf' : 'Calf.R',
    'ValveBiped.Bip01_L_Foot' : 'Foot.L',
    'ValveBiped.Bip01_R_Foot' : 'Foot.R',
    'ValveBiped.Bip01_L_Toe0' : 'Toe.L',
    'ValveBiped.Bip01_R_Toe0' : 'Toe.R',
    }

for bone in myObject.data.bones:
    try: 
        bone.name = boneDict.get(bone.name)
    except TypeError:
        #print("Not found in Bones dict: %s" % bone.name)
        continue
            