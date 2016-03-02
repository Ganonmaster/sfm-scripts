import bpy
from bpy import context
import string

print("START")
myObject = bpy.context.object
try:
    myArmature = myObject.modifiers["Armature"].object.data         #Doesn't work if your Armature modifier isn't named Armature. I don't think I care.
except KeyError:
    print("Error: Armature is not named 'Armature'.")
    
    
skDict = {'まばたき' : 'Blink',                                     #ShapeKey Japo->Eng Dictionary
'あ' : 'MouthAh',
'い' : 'MouthSmile',
'う' : 'LipsGape',
'え' : 'MouthGape',
'お' : 'MouthOpen',
'にやり' : 'LipsSmile',
'への字' : 'LipsSad',
'大口' : 'MouthOpen',
'大口舌だし' : 'TongueOut',
'ウィンク' : 'FIXME.Wink.Left',
'ウィンク右' : 'FIXME.Wink.Right',
'困る' : 'EyebrowsWorried',
'真面目' : 'EyebrowsSerious',
'左目細' : 'FIXME.EyeShrinkHorizontal.Left',
'左目縮小' : 'FIXME.EyeShrink.Left',
'右目細' : 'FIXME.EyeShrinkHorizontal.Right',
'右目縮小' : 'FIXME.EyeShrink.Right',
'ほお赤' : 'Blush'}

selectedSK = myObject.active_shape_key_index
myObject.active_shape_key_index = 0
while(type(myObject.active_shape_key) == bpy.types.ShapeKey):
    try:
        key = myObject.active_shape_key
        key.name = skDict[key.name]
    except KeyError:
            #print("Not found in SK dict: %s" % key.name)
            doNothing=0
    myObject.active_shape_key_index += 1
    
flexCount = myObject.active_shape_key_index
myObject.active_shape_key_index = selectedSK

def skCount():                                                      #counts the number of shapekeys on the mesh.
    curIndex = myObject.active_shape_key_index                      #saving the old index
    count = 0
    myObject.active_shape_key_index = 0
    while(type(myObject.active_shape_key) == bpy.types.ShapeKey):   #while shapekey isn't a NoneType(so it exists)
        count+=1
        myObject.active_shape_key_index+=1
    myObject.active_shape_key_index = curIndex                      #setting it back to the old index
    return count
    
removables = []
def newFlex(i1, i2, skName):                                        #combines two flexes into one, leaves active index as it was.
    removables.append(i1)
    removables.append(i2)
    curIndex = myObject.active_shape_key_index
    myObject.active_shape_key_index = i1
    myObject.active_shape_key.value = 1
    myObject.active_shape_key_index = i2
    myObject.active_shape_key.value = 1
    bpy.ops.object.shape_key_add(from_mix=True)
    myObject.active_shape_key_index = skCount()-1
    myObject.active_shape_key.name = skName
    myObject.active_shape_key_index = i2
    myObject.active_shape_key.value = 0
    #bpy.ops.object.shape_key_remove(all=False)
    myObject.active_shape_key_index = i1
    myObject.active_shape_key.value = 0
    #bpy.ops.object.shape_key_remove(all=False)
    myObject.active_shape_key_index = curIndex
    
#combining two-sided flexes into one flex
for i in range(0, flexCount-1):
    print(i)
    myObject.active_shape_key_index = i
    splitStr = myObject.active_shape_key.name.split('.')
    if(splitStr[0] == 'FIXME'):
        for j in range(i+1, flexCount):
            myObject.active_shape_key_index = j
            splitStr2 = myObject.active_shape_key.name.split('.')
            try:
                if(splitStr2[1] == splitStr[1]):
                    print("found match: %s" % splitStr[1])
                    newFlex(i, j, splitStr[1])
                    break
            except IndexError:
                continue
#removing sided shapekeys that we don't need anymore
removables.sort()                                                   #sorts from smallest to biggest
removables.reverse()                                                #iterating through a list while removing stuff from it = pain. This = less pain.
for i in removables:
    myObject.active_shape_key_index = i
    bpy.ops.object.shape_key_remove(all=False)
    
#preparing shapekeys for export, marking stereoflexes




if type(myArmature) is bpy.types.Armature:
    print("Selected object has an Armature, yay!")
    
    jpDict = {'全ての親' : 'Pelvis',
    '下半身' : 'Hips',
    '上半身' : 'Spine0',
    '上半身2' : 'Spine1',
    '上半身２' : 'Spine1',
    '上半身３' : 'Spine2',
    '乳１' : 'Breast',
    '首' : 'Neck',
    '頭' : 'Head',
    '目' : 'Eyeball',
    '肩' : 'Clavicle',
    '腕' : 'UpperArm',
    'ひじ' : 'LowerArm',
    '手首' : 'Hand',
    '親指０' : 'Finger_Thumb_0',
    '親指１' : 'Finger_Thumb_1',
    '親指２' : 'Finger_Thumb_2',
    '人指１' : 'Finger_Point_0',
    '人指２' : 'Finger_Point_1',
    '人指３' : 'Finger_Point_2',
    '中指１' : 'Finger_Middle_0',
    '中指２' : 'Finger_Middle_1',
    '中指３' : 'Finger_Middle_2',
    '薬指１' : 'Finger_Ring_0',
    '薬指２' : 'Finger_Ring_1',
    '薬指３' : 'Finger_Ring_2',
    '小指１' : 'Finger_Little_0',
    '小指２' : 'Finger_Little_1',
    '小指３' : 'Finger_Little_2',
    '足' : 'Thigh',
    'ひざ' : 'Calf',
    '足首' : 'Foot',
    
    'ス前１' : 'Skirt_Front_0',
    'ス前２' : 'Skirt_Front_1',
    'ス前３' : 'Skirt_Front_2',
    'ス横１' : 'Skirt_0',
    'ス横２' : 'Skirt_1',
    'ス横３' : 'Skirt_2',
    'ス後１' : 'Skirt_Back_0',
    'ス後２' : 'Skirt_Back_1',
    'ス後３' : 'Skirt_Back_2'}

    for bone in myArmature.bones:
        try: 
            if bone.name.find('.') != -1:
                #if bone ends with .r or .l (or contains a useless period, in which case this will fuck up.)
                separated = bone.name.split('.')
                bone.name = "%s.%s" % (jpDict.get(separated[0], separated[0]), separated[1])
                continue
            
            bone.name = jpDict.get(bone.name)
        except TypeError:
            #print("Not found in Bones dict: %s" % bone.name)
            continue
            
else:
    print("Error: The modifier named Armature isn't an Armature modifier!")
    
print("END")