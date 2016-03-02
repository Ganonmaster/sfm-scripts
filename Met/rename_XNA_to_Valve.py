import bpy
#XNA Cleanup + renaming to ValveBiped convention

#look through every mesh's vertexgroups, and add their names to a list.
#Then, look through every bone in the armature of the meshes, and if their name isnt contained in the list, rename them to DELETEME_x (cause idk how to delete via script, lel ._.
#I should probably remake this with regex. maybe later.


#need the armature to be selected, which is the parent of each mesh.
vGroupList = []
myObject = bpy.context.object

for mesh in myObject.children:              #for each mesh
    for vGroup in mesh.vertex_groups:       #for each vertexgroup
        vGroupList.append(vGroup.name)
        
for bone in myObject.data.bones:            #for each bone
    if(bone.name not in vGroupList):
        bone.name = "DELETEME"

jpDict = {'root pelvis' : 'ValveBiped.Bip01_Pelvis',
    'pelvis' : 'ValveBiped.Bip01_Hips',
    'spine lower' : 'ValveBiped.Bip01_Spine1',
    'spine middle' : 'ValveBiped.Bip01_Spine2',
    'spine midle' : 'ValveBiped.Bip01_Spine2',
    'spine upper' : 'ValveBiped.Bip01_Spine2',
    'head neck lower' : 'ValveBiped.Bip01_Neck',
    'head neck upper' : 'ValveBiped.Bip01_Head',
   
    'arm left shoulder 1' : 'ValveBiped.Bip01_L_Clavicle',
    'arm right shoulder 1' : 'ValveBiped.Bip01_R_Clavicle',
    'arm left shoulder 2' : 'ValveBiped.Bip01_L_UpperArm',
    'arm right shoulder 2' : 'ValveBiped.Bip01_R_UpperArm',
    'arm left elbow' : 'ValveBiped.Bip01_L_Forearm',
    'arm right elbow' : 'ValveBiped.Bip01_R_Forearm',
    'arm left wrist' : 'ValveBiped.Bip01_L_Hand',
    'arm right wrist' : 'ValveBiped.Bip01_R_Hand',
	
    'arm left shoulder' : 'ValveBiped.Bip01_L_Clavicle',
    'arm right shoulder' : 'ValveBiped.Bip01_R_Clavicle',
    'arm left arm' : 'ValveBiped.Bip01_L_UpperArm',
    'arm right arm' : 'ValveBiped.Bip01_R_UpperArm',
    'arm left elbow' : 'ValveBiped.Bip01_L_Forearm',
    'arm right elbow' : 'ValveBiped.Bip01_R_Forearm',
    'arm left wrist' : 'ValveBiped.Bip01_L_Hand',
    'arm right wrist' : 'ValveBiped.Bip01_R_Hand',
    'arm left handwrist' : 'ValveBiped.Bip01_L_Hand',
    'arm right handwrist' : 'ValveBiped.Bip01_R_Hand',
	
    'arm left finger 1a' : 'ValveBiped.Bip01_L_Finger0',
    'arm left finger 1b' : 'ValveBiped.Bip01_L_Finger01',
    'arm left finger 1c' : 'ValveBiped.Bip01_L_Finger02',
    'arm left finger 2a' : 'ValveBiped.Bip01_L_Finger1',
    'arm left finger 2b' : 'ValveBiped.Bip01_L_Finger11',
    'arm left finger 2c' : 'ValveBiped.Bip01_L_Finger12',
    'arm left finger 3a' : 'ValveBiped.Bip01_L_Finger2',
    'arm left finger 3b' : 'ValveBiped.Bip01_L_Finger21',
    'arm left finger 3c' : 'ValveBiped.Bip01_L_Finger22',
    'arm left finger 4a' : 'ValveBiped.Bip01_L_Finger3',
    'arm left finger 4b' : 'ValveBiped.Bip01_L_Finger31',
    'arm left finger 4c' : 'ValveBiped.Bip01_L_Finger32',
    'arm left finger 5a' : 'ValveBiped.Bip01_L_Finger4',
    'arm left finger 5b' : 'ValveBiped.Bip01_L_Finger41',
    'arm left finger 5c' : 'ValveBiped.Bip01_L_Finger42',
    'arm right finger 1a' : 'ValveBiped.Bip01_R_Finger0',
    'arm right finger 1b' : 'ValveBiped.Bip01_R_Finger01',
    'arm right finger 1c' : 'ValveBiped.Bip01_R_Finger02',
    'arm right finger 2a' : 'ValveBiped.Bip01_R_Finger1',
    'arm right finger 2b' : 'ValveBiped.Bip01_R_Finger11',
    'arm right finger 2c' : 'ValveBiped.Bip01_R_Finger12',
    'arm right finger 3a' : 'ValveBiped.Bip01_R_Finger2',
    'arm right finger 3b' : 'ValveBiped.Bip01_R_Finger21',
    'arm right finger 3c' : 'ValveBiped.Bip01_R_Finger22',
    'arm right finger 4a' : 'ValveBiped.Bip01_R_Finger3',
    'arm right finger 4b' : 'ValveBiped.Bip01_R_Finger31',
    'arm right finger 4c' : 'ValveBiped.Bip01_R_Finger32',
    'arm right finger 5a' : 'ValveBiped.Bip01_R_Finger4',
    'arm right finger 5b' : 'ValveBiped.Bip01_R_Finger41',
    'arm right finger 5c' : 'ValveBiped.Bip01_R_Finger42',
    
    'Hand Left Thumb 1' : 'ValveBiped.Bip01_L_Finger0',
    'Hand Left Thumb 2' : 'ValveBiped.Bip01_L_Finger01',
    'Hand Left Thumb 3' : 'ValveBiped.Bip01_L_Finger02',
    'Hand Left Index 1' : 'ValveBiped.Bip01_L_Finger1',
    'Hand Left Index 2' : 'ValveBiped.Bip01_L_Finger11',
    'Hand Left Index 3' : 'ValveBiped.Bip01_L_Finger12',
    'Hand Left Middle 1' : 'ValveBiped.Bip01_L_Finger2',
    'Hand Left Middle 2' : 'ValveBiped.Bip01_L_Finger21',
    'Hand Left Middle 3' : 'ValveBiped.Bip01_L_Finger22',
    'Hand Left Ring 1' : 'ValveBiped.Bip01_L_Finger3',
    'Hand Left Ring 2' : 'ValveBiped.Bip01_L_Finger31',
    'Hand Left Ring 3' : 'ValveBiped.Bip01_L_Finger32',
    'Hand Left Pinky 1' : 'ValveBiped.Bip01_L_Finger4',
    'Hand Left Pinky 2' : 'ValveBiped.Bip01_L_Finger41',
    'Hand Left Pinky 3' : 'ValveBiped.Bip01_L_Finger42',
    'Hand Right Thumb 1' : 'ValveBiped.Bip01_R_Finger0',
    'Hand Right Thumb 2' : 'ValveBiped.Bip01_R_Finger01',
    'Hand Right Thumb 3' : 'ValveBiped.Bip01_R_Finger02',
    'Hand Right Index 1' : 'ValveBiped.Bip01_R_Finger1',
    'Hand Right Index 2' : 'ValveBiped.Bip01_R_Finger11',
    'Hand Right Index 3' : 'ValveBiped.Bip01_R_Finger12',
    'Hand Right Middle 1' : 'ValveBiped.Bip01_R_Finger2',
    'Hand Right Middle 2' : 'ValveBiped.Bip01_R_Finger21',
    'Hand Right Middle 3' : 'ValveBiped.Bip01_R_Finger22',
    'Hand Right Ring 1' : 'ValveBiped.Bip01_R_Finger3',
    'Hand Right Ring 2' : 'ValveBiped.Bip01_R_Finger31',
    'Hand Right Ring 3' : 'ValveBiped.Bip01_R_Finger32',
    'Hand Right Pinky 1' : 'ValveBiped.Bip01_R_Finger4',
    'Hand Right Pinky 2' : 'ValveBiped.Bip01_R_Finger41',
    'Hand Right Pinky 3' : 'ValveBiped.Bip01_R_Finger42',
    
    
    
    'hand left thump' : 'ValveBiped.Bip01_L_Finger0',
    'hand left thump1' : 'ValveBiped.Bip01_L_Finger0',
    'hand left thump2' : 'ValveBiped.Bip01_L_Finger01',
    'hand left thump3' : 'ValveBiped.Bip01_L_Finger02',
    'hand left finger1a' : 'ValveBiped.Bip01_L_Finger1',
    'hand left finger1b' : 'ValveBiped.Bip01_L_Finger11',
    'hand left finger1c' : 'ValveBiped.Bip01_L_Finger12',
    'hand left finger2a' : 'ValveBiped.Bip01_L_Finger2',
    'hand left finger2b' : 'ValveBiped.Bip01_L_Finger21',
    'hand left finger2c' : 'ValveBiped.Bip01_L_Finger22',
    'hand left finger3a' : 'ValveBiped.Bip01_L_Finger3',
    'hand left finger3b' : 'ValveBiped.Bip01_L_Finger31',
    'hand left finger3c' : 'ValveBiped.Bip01_L_Finger32',
    'hand left finger4a' : 'ValveBiped.Bip01_L_Finger4',
    'hand left finger4b' : 'ValveBiped.Bip01_L_Finger41',
    'hand left finger4c' : 'ValveBiped.Bip01_L_Finger42',
    'hand right thump' : 'ValveBiped.Bip01_R_Finger0',
    'hand right thump1' : 'ValveBiped.Bip01_R_Finger0',
    'hand right thump2' : 'ValveBiped.Bip01_R_Finger01',
    'hand right thump3' : 'ValveBiped.Bip01_R_Finger02',
    'hand right finger1a' : 'ValveBiped.Bip01_R_Finger1',
    'hand right finger1b' : 'ValveBiped.Bip01_R_Finger11',
    'hand right finger1c' : 'ValveBiped.Bip01_R_Finger12',
    'hand right finger2a' : 'ValveBiped.Bip01_R_Finger2',
    'hand right finger2b' : 'ValveBiped.Bip01_R_Finger21',
    'hand right finger2c' : 'ValveBiped.Bip01_R_Finger22',
    'hand right finger3a' : 'ValveBiped.Bip01_R_Finger3',
    'hand right finger3b' : 'ValveBiped.Bip01_R_Finger31',
    'hand right finger3c' : 'ValveBiped.Bip01_R_Finger32',
    'hand right finger4a' : 'ValveBiped.Bip01_R_Finger4',
    'hand right finger4b' : 'ValveBiped.Bip01_R_Finger41',
    'hand right finger4c' : 'ValveBiped.Bip01_R_Finger42',
    
    
    
    'arm left finger thumb 1' : 'ValveBiped.Bip01_L_Finger0',
    'arm left finger thumb 2' : 'ValveBiped.Bip01_L_Finger01',
    'arm left finger thumb 3' : 'ValveBiped.Bip01_L_Finger02',
    'arm left finger index 1' : 'ValveBiped.Bip01_L_Finger1',
    'arm left finger index 2' : 'ValveBiped.Bip01_L_Finger11',
    'arm left finger index 3' : 'ValveBiped.Bip01_L_Finger12',
    'arm left finger middle 1' : 'ValveBiped.Bip01_L_Finger2',
    'arm left finger middle 2' : 'ValveBiped.Bip01_L_Finger21',
    'arm left finger middle 3' : 'ValveBiped.Bip01_L_Finger22',
    'arm left finger ring 1' : 'ValveBiped.Bip01_L_Finger3',
    'arm left finger ring 2' : 'ValveBiped.Bip01_L_Finger31',
    'arm left finger ring 3' : 'ValveBiped.Bip01_L_Finger32',
    'arm left finger pinky 1' : 'ValveBiped.Bip01_L_Finger4',
    'arm left finger pinky 2' : 'ValveBiped.Bip01_L_Finger41',
    'arm left finger pinky 3' : 'ValveBiped.Bip01_L_Finger42',
    'arm right finger thumb 1' : 'ValveBiped.Bip01_R_Finger0',
    'arm right finger thumb 2' : 'ValveBiped.Bip01_R_Finger01',
    'arm right finger thumb 3' : 'ValveBiped.Bip01_R_Finger02',
    'arm right finger index 1' : 'ValveBiped.Bip01_R_Finger1',
    'arm right finger index 2' : 'ValveBiped.Bip01_R_Finger11',
    'arm right finger index 3' : 'ValveBiped.Bip01_R_Finger12',
    'arm right finger middle 1' : 'ValveBiped.Bip01_R_Finger2',
    'arm right finger middle 2' : 'ValveBiped.Bip01_R_Finger21',
    'arm right finger middle 3' : 'ValveBiped.Bip01_R_Finger22',
    'arm right finger ring 1' : 'ValveBiped.Bip01_R_Finger3',
    'arm right finger ring 2' : 'ValveBiped.Bip01_R_Finger31',
    'arm right finger ring 3' : 'ValveBiped.Bip01_R_Finger32',
    'arm right finger pinky 1' : 'ValveBiped.Bip01_R_Finger4',
    'arm right finger pinky 2' : 'ValveBiped.Bip01_R_Finger41',
    'arm right finger pinky 3' : 'ValveBiped.Bip01_R_Finger42',
	
    'Bip01_L_Finger0' : 'ValveBiped.Bip01_L_Finger0',
    'Bip01_L_Finger01' : 'ValveBiped.Bip01_L_Finger01',
    'Bip01_L_Finger02' : 'ValveBiped.Bip01_L_Finger02',
    'Bip01_L_Finger1' : 'ValveBiped.Bip01_L_Finger1',
    'Bip01_L_Finger11' : 'ValveBiped.Bip01_L_Finger11',
    'Bip01_L_Finger12' : 'ValveBiped.Bip01_L_Finger12',
    'Bip01_L_Finger2' : 'ValveBiped.Bip01_L_Finger2',
    'Bip01_L_Finger21' : 'ValveBiped.Bip01_L_Finger21',
    'Bip01_L_Finger22' : 'ValveBiped.Bip01_L_Finger22',
    'Bip01_L_Finger3' : 'ValveBiped.Bip01_L_Finger3',
    'Bip01_L_Finger31' : 'ValveBiped.Bip01_L_Finger31',
    'Bip01_L_Finger32' : 'ValveBiped.Bip01_L_Finger32',
    'Bip01_L_Finger4' : 'ValveBiped.Bip01_L_Finger4',
    'Bip01_L_Finger41' : 'ValveBiped.Bip01_L_Finger41',
    'Bip01_L_Finger42' : 'ValveBiped.Bip01_L_Finger42',
    'Bip01_R_Finger0' : 'ValveBiped.Bip01_R_Finger0',
    'Bip01_R_Finger01' : 'ValveBiped.Bip01_R_Finger01',
    'Bip01_R_Finger02' : 'ValveBiped.Bip01_R_Finger02',
    'Bip01_R_Finger1' : 'ValveBiped.Bip01_R_Finger1',
    'Bip01_R_Finger11' : 'ValveBiped.Bip01_R_Finger11',
    'Bip01_R_Finger12' : 'ValveBiped.Bip01_R_Finger12',
    'Bip01_R_Finger2' : 'ValveBiped.Bip01_R_Finger2',
    'Bip01_R_Finger21' : 'ValveBiped.Bip01_R_Finger21',
    'Bip01_R_Finger22' : 'ValveBiped.Bip01_R_Finger22',
    'Bip01_R_Finger3' : 'ValveBiped.Bip01_R_Finger3',
    'Bip01_R_Finger31' : 'ValveBiped.Bip01_R_Finger31',
    'Bip01_R_Finger32' : 'ValveBiped.Bip01_R_Finger32',
    'Bip01_R_Finger4' : 'ValveBiped.Bip01_R_Finger4',
    'Bip01_R_Finger41' : 'ValveBiped.Bip01_R_Finger41',
    'Bip01_R_Finger42' : 'ValveBiped.Bip01_R_Finger42',
    
    'leg left thigh' : 'ValveBiped.Bip01_L_Thigh',
    'leg right thigh' : 'ValveBiped.Bip01_R_Thigh',
    'leg left knee' : 'ValveBiped.Bip01_L_Calf',
    'leg right knee' : 'ValveBiped.Bip01_R_Calf',
    'leg left ankle' : 'ValveBiped.Bip01_L_Foot',
    'leg right ankle' : 'ValveBiped.Bip01_R_Foot',
    'leg left toes' : 'ValveBiped.Bip01_L_Toe0',
    'leg right toes' : 'ValveBiped.Bip01_R_Toe0',
    
    'leg left thigh adj.' : 'Twist_Thigh.L',
    'leg right thigh adj.' : 'Twist_Thigh.R',
    'leg left twist thigh 1' : 'Twist_Thigh.L',
    'leg right twist thigh 1' : 'Twist_Thigh.R',
    'leg left twist thigh 2' : 'Twist_Thigh_2.L',
    'leg right twist thigh 2' : 'Twist_Thigh_2.R',
    'leg left twist upper 1' : 'Twist_Thigh.L',
    'leg right twist upper 1' : 'Twist_Thigh.R',
    'leg left twist upper 2' : 'Twist_Thigh_2.L',
    'leg right twist upper 2' : 'Twist_Thigh_2.R',
    'leg left thigh twist a' : 'Twist_Thigh.L',
    'leg right thigh twist a' : 'Twist_Thigh.R',
    'leg left thigh twist b' : 'Twist_Thigh_2.L',
    'leg right thigh twist b' : 'Twist_Thigh_2.R',
    'leg left thigh ctr' : 'Twist_Thigh.L',
    'leg right thigh ctr' : 'Twist_Thigh.R',
    'leg left thigh ctr2' : 'Twist_Thigh_2.L',
    'leg right thigh ctr2' : 'Twist_Thigh_2.R',
    'leg left thigh ctrl 1' : 'Twist_Thigh.L',
    'leg right thigh ctrl 1' : 'Twist_Thigh.R',
    'leg left thigh ctrl 2' : 'Twist_Thigh_2.L',
    'leg right thigh ctrl 2' : 'Twist_Thigh_2.R',
    'leg left knee adj.' : 'Adjust_Knee.L',
    'leg right knee adj.' : 'Adjust_Knee.R',    
    'leg left knee ctrl' : 'Adjust_Knee.L',
    'leg right knee ctrl' : 'Adjust_Knee.R',    
    'leg left knee adjuster' : 'Adjust_Knee.L',
    'leg right knee adjuster' : 'Adjust_Knee.R',
    'leg left knee ctr' : 'Adjust_Knee.L',
    'leg right knee ctr' : 'Adjust_Knee.R',
    'leg left adjuster knee' : 'Adjust_Knee.L',
    'leg right adjuster knee' : 'Adjust_Knee.R',
	
    'leg left butt' : 'Butt.L',
    'leg right butt' : 'Butt.R',
    'leg left butt ctr' : 'Butt.L',
    'leg right butt ctr' : 'Butt.R',
    'leg left adjuster bottom' : 'Butt.L',
    'leg right adjuster bottom' : 'Butt.R',
	
    'arm left shoulder adj.' : 'Twist_Shoulder.L',
    'arm right shoulder adj.' : 'Twist_Shoulder.R',
    'arm left shoulder ctrl 1' : 'Twist_Shoulder.L',
    'arm right shoulder ctrl 1' : 'Twist_Shoulder.R',
    'arm left shoulder ctrl 2' : 'Twist_Shoulder_2.L',
    'arm right shoulder ctrl 2' : 'Twist_Shoulder_2.R',
    'arm left twist upper 1' : 'Twist_Shoulder.L',
    'arm right twist upper 1' : 'Twist_Shoulder.R',
    'arm left twist upper 2' : 'Twist_Shoulder_2.L',
    'arm right twist upper 2' : 'Twist_Shoulder_2.R',
    'arm left arm twist a' : 'Twist_Shoulder.L',
    'arm right arm twist a' : 'Twist_Shoulder.R',
    'arm left arm twist b' : 'Twist_Shoulder_2.L',
    'arm right arm twist b' : 'Twist_Shoulder_2.R',
    'arm left upper 1' : 'Twist_Shoulder_2.L',
    'arm right upper 1' : 'Twist_Shoulder_2.R',
    'arm left shoulder 2 ctr' : 'Twist_Shoulder.L',
    'arm right shoulder 2 ctr' : 'Twist_Shoulder.R',
    'arm left shoulder 2 ctr2' : 'Twist_Shoulder_2.L',
    'arm right shoulder 2 ctr2' : 'Twist_Shoulder_2.R',
	
    'arm left elbow adj.' : 'Adjust_Elbow.L',
    'arm right elbow adj.' : 'Adjust_Elbow.R',
    'arm left adjuster elbow' : 'Adjust_Elbow.L',
    'arm right adjuster elbow' : 'Adjust_Elbow.R',
    'arm left elbow adjuster' : 'Adjust_Elbow.L',
    'arm right elbow adjuster' : 'Adjust_Elbow.R',
    'arm left elbow ctrl' : 'Adjust_Elbow.L',
    'arm right elbow ctrl' : 'Adjust_Elbow.R',
    'arm left wrist ctrl 1' : 'Twist_Elbow.L',
    'arm right wrist ctrl 1' : 'Twist_Elbow.R',
    'arm left wrist ctrl 2' : 'Twist_Elbow_2.L',
    'arm right wrist ctrl 2' : 'Twist_Elbow_2.R',
    'arm left twist lower 1' : 'Twist_Elbow.L',
    'arm right twist lower 1' : 'Twist_Elbow.R',
    'arm left twist lower 2' : 'Twist_Elbow_2.L',
    'arm right twist lower 2' : 'Twist_Elbow_2.R',
    'arm left elbow ctr' : 'Adjust_Elbow.L',
    'arm right elbow ctr' : 'Adjust_Elbow.R',
    'arm left elbow ctr2' : 'Twist_Elbow.L',
    'arm right elbow ctr2' : 'Twist_Elbow.R',
    'arm left wrist ctr' : 'Twist_Elbow_2.L',
    'arm right wrist ctr' : 'Twist_Elbow_2.R',
    'arm left lower 1' : 'Twist_Elbow.L',
    'arm right lower 1' : 'Twist_Elbow.R',
    'arm left wrist a' : 'Twist_Elbow.L',
    'arm right wrist a' : 'Twist_Elbow.R',
    'arm left lower 2' : 'Twist_Elbow_2.L',
    'arm right lower 2' : 'Twist_Elbow_2.R',
    'arm left wrist b' : 'Twist_Elbow_2.L',
    'arm right wrist b' : 'Twist_Elbow_2.R',
	
    'arm left finger metacarpal' : 'Metacarpal.L',
    'arm right finger metacarpal' : 'Metacarpal.R',
    'Hand Left Metacarpal' : 'Metacarpal.L',
    'Hand Right Metacarpal' : 'Metacarpal.R',
    'unused_OPT_Hand_Left_Metacarpal04' : 'Metacarpal.L',
    'unused_OPT_Hand_Right_Metacarpal04' : 'Metacarpal.R',
    'arm left finger 5 base' : 'Metacarpal.L',
    'arm right finger 5 base' : 'Metacarpal.R',
    'arm left metacarpus' : 'Metacarpal.L',
    'arm right metacarpus' : 'Metacarpal.R',
    
    'head eyelid left lower a' : 'Eyelid_Lower_Inner.L',
    'head eyelid left lower 1' : 'Eyelid_Lower_Inner.L',
    'head eyelid left adj' : 'Eyelid_Lower_Inner.L',
    'head eyelid left lower b' : 'Eyelid_Lower_Outer.L',
    'head eyelid left lower 2' : 'Eyelid_Lower_Outer.L',
    
    'head eyelid right lower a' : 'Eyelid_Lower_Inner.R',
    'head eyelid right lower 1' : 'Eyelid_Lower_Inner.R',
    'head eyelid right adj' : 'Eyelid_Lower_Inner.R',
    'head eyelid right lower b' : 'Eyelid_Lower_Outer.R',
    'head eyelid right lower 2' : 'Eyelid_Lower_Outer.R',
    
    'head forehead left' : 'Forehead.L',
    'head left forehead' : 'Forehead.L',
    'head eyebrow left c' : 'Eyebrow_Outer.L',
    'head eyebrow left b' : 'Eyebrow_Middle.L',
    'head eyebrow left a' : 'Eyebrow_Inner.L',
    'head eyebrow left 3' : 'Eyebrow_Outer.L',
    'head eyebrow left 2' : 'Eyebrow_Middle.L',
    'head eyebrow left 1' : 'Eyebrow_Inner.L',
    'head forehead right' : 'Forehead.R',
    'head right forehead' : 'Forehead.R',
    'head eyebrow right c' : 'Eyebrow_Outer.R',
    'head eyebrow right b' : 'Eyebrow_Middle.R',
    'head eyebrow right a' : 'Eyebrow_Inner.R',
    'head eyebrow right 3' : 'Eyebrow_Outer.R',
    'head eyebrow right 2' : 'Eyebrow_Middle.R',
    'head eyebrow right 1' : 'Eyebrow_Inner.R',
    'head eyebrow middle' : 'Eyebrow_Middle',
    'head eyebrow center' : 'Eyebrow_Middle',
    'head jaw' : 'Jaw',
    'head tongue a' : 'Tongue_01',
    'head tongue b' : 'Tongue_02',
    'head tongue 1' : 'Tongue_01',
    'head tongue 2' : 'Tongue_02',
    
    'head lip corner left' : 'Lip_Corner.L',
    'head mouth corner left' : 'Lip_Corner.L',
    'head lip upper left' : 'Lip_Upper.L',
    'head lip lower left' : 'Lip_Lower.L',
    'head lip lower middle' : 'Lip_Lower_Middle',
    'head lip upper middle' : 'Lip_Upper_Middle',
    'head lip corner right' : 'Lip_Corner.R',
    'head mouth corner right' : 'Lip_Corner.R',
    'head lip upper right' : 'Lip_Upper.R',
    'head lip lower right' : 'Lip_Lower.R',
    
    'head eyelid left upper' : 'Eyelid_Upper.L',
    'head eyelid left lower' : 'Eyelid_Lower.L',
    'head eyeball left' : 'Eyeball.L',
    'head eyelid right upper' : 'Eyelid_Upper.R',
    'head eyelid right lower' : 'Eyelid_Lower.R',
    'head eyeball right' : 'Eyeball.R',
    
    'head nose left a' : 'Nose_Upper.L',
    'head nose left 1' : 'Nose_Upper.L',
    'head nostril left 1' : 'Nose_Upper.L',
    'head nose left b' : 'Nostril.L',
    'head nose left 2' : 'Nostril.L',
    'head nostril left 2' : 'Nostril.L',
    'head cheek left c' : 'Cheek_Main.L',
    'head cheek left 3' : 'Cheek_Main.L',
    'head cheek left a' : 'Cheek_Inner.L',
    'head cheek left 1' : 'Cheek_Inner.L',
    'head cheek left b' : 'Cheek_Outer.L',
    'head cheek left 2' : 'Cheek_Outer.L',
    'head nose left c' : 'NoseLine_Inner.L',
    'head nose left d' : 'NoseLine_Outer.L',
    'head nose left 3' : 'NoseLine_Inner.L',
    'head nose left 4' : 'NoseLine_Outer.L',
    
    'head nose right a' : 'Nose_Upper.R',
    'head nose right 1' : 'Nose_Upper.R',
    'head nostril right 2' : 'Nose_Upper.R',
    'head nose right b' : 'Nostril.R',
    'head nose right 2' : 'Nostril.R',
    'head nostril right 2' : 'Nostril.R',
    'head cheek right c' : 'Cheek_Main.R',
    'head cheek right 3' : 'Cheek_Main.R',
    'head cheek right a' : 'Cheek_Inner.R',
    'head cheek right 1' : 'Cheek_Inner.R',
    'head cheek right b' : 'Cheek_Outer.R',
    'head cheek right 2' : 'Cheek_Outer.R',
    'head nose right c' : 'NoseLine_Inner.R',
    'head nose right d' : 'NoseLine_Outer.R',
    'head nose right 3' : 'NoseLine_Inner.R',
    'head nose right 4' : 'NoseLine_Outer.R',
    
    'head nose middle' : 'Nose_Tip',
    'head nose center' : 'Nose_Tip',
    'head nose centre' : 'Nose_Tip',
    'head nostril left' : 'Nostril.L',
    'head nostril right' : 'Nostril.R',
    
    'breast left base' : 'Breast_Base.L',
    'breast left tip' : 'Breast_Tip.L',
    'breast right base' : 'Breast_Base.R',
    'breast right tip' : 'Breast_Tip.R',
    'Breast_1.L' : 'Breast_Base.L',
    'Breast_2.L' : 'Breast_Tip.L',
    'Breast_1.R' : 'Breast_Base.R',
    'Breast_2.R' : 'Breast_Tip.R',
    
    'Breast Left base' : 'Breast_Base.L',
    'Breast Left tip' : 'Breast_Tip.L',
    'Breast Right base' : 'Breast_Base.R',
    'Breast Right tip' : 'Breast_Tip.R',
    'Breast_1.L' : 'Breast_Base.L',
    'Breast_2.L' : 'Breast_Tip.L',
    'Breast_1.R' : 'Breast_Base.R',
    'Breast_2.R' : 'Breast_Tip.R',
    
    'breast left a' : 'Breast_1.L',
    'breast left b' : 'Breast_2.L',
    'breast left c' : 'Breast_3.L',
    'breast left d' : 'Breast_4.L',
    'breast left e' : 'Breast_5.L',
    
    'breast left 1' : 'Breast_1.L',
    'breast left 2' : 'Breast_2.L',
    'breast left 3' : 'Breast_3.L',
    'breast left 4' : 'Breast_4.L',
    'breast left 5' : 'Breast_5.L',
    
    'Breast Left 1' : 'Breast_1.L',
    'Breast Left 2' : 'Breast_2.L',
    'Breast Left 3' : 'Breast_3.L',
    'Breast Left 4' : 'Breast_4.L',
    'Breast Left 5' : 'Breast_5.L',
    
    'breast left 3a' : 'Breast_1.L',
    'breast left 3b' : 'Breast_2.L',
    'breast left 3c' : 'Breast_3.L',
    'breast left 3d' : 'Breast_4.L',
    'breast left 3e' : 'Breast_5.L',
    
    'breast right 3a' : 'Breast_1.R',
    'breast right 3b' : 'Breast_2.R',
    'breast right 3c' : 'Breast_3.R',
    'breast right 3d' : 'Breast_4.R',
    'breast right 3e' : 'Breast_5.R',
    
    'breast right a' : 'Breast_1.R',
    'breast right b' : 'Breast_2.R',
    'breast right c' : 'Breast_3.R',
    'breast right d' : 'Breast_4.R',
    'breast right e' : 'Breast_5.R',
    
    'breast right 1' : 'Breast_1.R',
    'breast right 2' : 'Breast_2.R',
    'breast right 3' : 'Breast_3.R',
    'breast right 4' : 'Breast_4.R',
    'breast right 5' : 'Breast_5.R',
    
    'Breast Right 1' : 'Breast_1.R',
    'Breast Right 2' : 'Breast_2.R',
    'Breast Right 3' : 'Breast_3.R',
    'Breast Right 4' : 'Breast_4.R',
    'Breast Right 5' : 'Breast_5.R',
    
    
    'pussy base' : 'Pussy',
    'pussy left' : 'Pussy.L',
    'pussy right' : 'Pussy.R'
    }     

for bone in myObject.data.bones:
    try: 
        bone.name = jpDict.get(bone.name)
    except TypeError:
        #print("Not found in Bones dict: %s" % bone.name)
        continue
            