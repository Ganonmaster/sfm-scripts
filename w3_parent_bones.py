import bpy
from pprint import pprint

def script():
    armature = bpy.context.object
    parent_dict = {
        # spine
        'pelvis': 'torso',
        'torso2': 'torso',
        'torso3': 'torso2',
        'neck': 'torso3',
        'head': 'neck',
        
        # breasts
        'l_boob': 'torso3',
        'r_boob': 'torso3',
        
        #right leg
        'r_thigh': 'torso',
        'r_legRoll': 'torso',
        'r_legRoll2': 'torso',
        'r_shin': 'r_thigh',
        'r_kneeRoll': 'r_shin',
        'r_foot': 'r_shin',
        'r_toe': 'r_foot',
        
        #right arm
        'r_shoulder': 'torso3',
        'r_shoulderRoll': 'r_shoulder',
        'r_bicep': 'r_shoulder',
        'r_bicep2': 'r_bicep',
        'r_elbowRoll': 'r_bicep',
        'r_forearmRoll1': 'r_elbowRoll',
        'r_forearmRoll2': 'r_elbowRoll',
        'r_handRoll': 'r_elbowRoll',
        
        #right hand
        'r_hand': 'r_elbowRoll',
        'r_pinky0': 'r_hand',
        
        'r_thumb1': 'r_hand',
        'r_thumb_roll': 'r_hand',
        'r_thumb2': 'r_thumb1',
        'r_thumb3': 'r_thumb2',
        
        'r_index_knuckleRoll': 'r_hand',
        'r_index1': 'r_hand',
        'r_index2': 'r_index1',
        'r_index3': 'r_index2',
        
        'r_middle_knuckleRoll': 'r_hand',
        'r_middle1': 'r_hand',
        'r_middle2': 'r_middle1',
        'r_middle3': 'r_middle2',
        
        'r_ring_knuckleRoll': 'r_hand',
        'r_ring1': 'r_hand',
        'r_ring2': 'r_ring1',
        'r_ring3': 'r_ring2',
        
        'r_pinky_knuckleRoll': 'r_hand',
        'r_pinky1': 'r_hand',
        'r_pinky2': 'r_pinky1',
        'r_pinky3': 'r_pinky2',
        
        #left leg
        'l_thigh': 'torso',
        'l_legRoll': 'torso',
        'l_legRoll2': 'torso',
        'l_shin': 'l_thigh',
        'l_kneeRoll': 'l_shin',
        'l_foot': 'l_shin',
        'l_toe': 'l_foot',
        
        #left arm
        'l_shoulder': 'torso3',
        'l_shoulderRoll': 'l_shoulder',
        'l_bicep': 'l_shoulder',
        'l_bicep2': 'l_bicep',
        'l_elbowRoll': 'l_bicep',
        'l_forearmRoll1': 'l_elbowRoll',
        'l_forearmRoll2': 'l_elbowRoll',
        'l_handRoll': 'l_elbowRoll',
        
        #left hand
        'l_hand': 'l_elbowRoll',
        'l_pinky0': 'l_hand',
        
        'l_thumb1': 'l_hand',
        'l_thumb_roll': 'l_hand',
        'l_thumb2': 'l_thumb1',
        'l_thumb3': 'l_thumb2',
        
        'l_index_knuckleRoll': 'l_hand',
        'l_index1': 'l_hand',
        'l_index2': 'l_index1',
        'l_index3': 'l_index2',
        
        'l_middle_knuckleRoll': 'l_hand',
        'l_middle1': 'l_hand',
        'l_middle2': 'l_middle1',
        'l_middle3': 'l_middle2',
        
        'l_ring_knuckleRoll': 'l_hand',
        'l_ring1': 'l_hand',
        'l_ring2': 'l_ring1',
        'l_ring3': 'l_ring2',
        
        'l_pinky_knuckleRoll': 'l_hand',
        'l_pinky1': 'l_hand',
        'l_pinky2': 'l_pinky1',
        'l_pinky3': 'l_pinky2',
        
        
        #head / face
        'thyroid': 'head',
        'hroll': 'neck',
        'jaw': 'head',
        'ears': 'head',
        'nose': 'head',
        'nose_base': 'head',
        'lowwer_lip': 'head',
        'upper_lip': 'head',
        'chin': 'head',
        
        'right_temple': 'head',
        'right_forehead': 'head',
        'right_chick1': 'head',
        'right_chick2': 'head',
        'right_chick3': 'head',
        'right_chick4': 'head',
        'right_nose1': 'head',
        'right_nose2': 'head',
        'right_nose3': 'head',
        'right_eyebrow1': 'head',
        'right_eyebrow2': 'head',
        'right_eyebrow3': 'head',
        'right_eye': 'head',
        
        'upper_right_eyelid1': 'head',
        'upper_right_eyelid2': 'head',
        'upper_right_eyelid3': 'head',
        'upper_right_eyelid_fold': 'head',
        'lowwer_right_eyelid1': 'head',
        'lowwer_right_eyelid2': 'head',
        'lowwer_right_eyelid3': 'head',
        'lowwer_right_eyelid_fold': 'head',
        
        'right_chick2': 'head',
        'right_chick3': 'head',
        'right_mouth_fold1': 'jaw',
        'right_mouth2': 'head',
        'right_mouth1': 'jaw',
        'upper_right_lip': 'head',
        'lowwer_right_lip': 'jaw',
        'right_corner_lip2': 'jaw',
        'right_corner_lip1': 'head',
        'right_mouth3': 'head',
        'right_mouth4': 'head',
        'right_mouth_fold2': 'head',
        'right_mouth_fold3': 'head',
        'right_mouth_fold4': 'head',
        
        'left_temple': 'head',
        'left_forehead': 'head',
        'left_chick1': 'head',
        'left_chick2': 'head',
        'left_chick3': 'head',
        'left_chick4': 'head',
        'left_nose1': 'head',
        'left_nose2': 'head',
        'left_nose3': 'head',
        'left_eyebrow1': 'head',
        'left_eyebrow2': 'head',
        'left_eyebrow3': 'head',
        'left_eye': 'head',
        
        'upper_left_eyelid1': 'head',
        'upper_left_eyelid2': 'head',
        'upper_left_eyelid3': 'head',
        'upper_left_eyelid_fold': 'head',
        'lowwer_left_eyelid1': 'head',
        'lowwer_left_eyelid2': 'head',
        'lowwer_left_eyelid3': 'head',
        'lowwer_left_eyelid_fold': 'head',
        
        'left_chick2': 'head',
        'left_chick3': 'head',
        'left_mouth_fold1': 'jaw',
        'left_mouth2': 'head',
        'left_mouth1': 'jaw',
        'upper_left_lip': 'head',
        'lowwer_left_lip': 'jaw',
        'left_corner_lip2': 'jaw',
        'left_corner_lip1': 'head',
        'left_mouth3': 'head',
        'left_mouth4': 'head',
        'left_mouth_fold2': 'head',
        'left_mouth_fold3': 'head',
        'left_mouth_fold4': 'head',
    }

    # Create bones
    bpy.ops.object.mode_set(mode='EDIT')
    
    for bone in armature.data.edit_bones:
        pprint(bone)
        parent_name = parent_dict.get(bone.name)
        if not parent_name:
            print('no parent for %s', bone.name)
            continue

        parent = armature.data.edit_bones.get(parent_name, None)
        if parent:
            bone.parent = parent
            bone.use_connect = False
            pprint(parent)
        else:
            print('parent not found')
        
    bpy.ops.object.mode_set(mode='OBJECT')

script()
