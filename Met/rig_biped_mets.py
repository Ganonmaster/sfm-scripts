#Version B6.1
#Dva
#2016.02.29

#I'll document this shit later. If you want to see the magic, go to def regexGroup()

import vs
import random
import re

#The script is not finished yet. When it will be, I'll release it as an individual SFMLab upload.

#TODO - search for all the TODO's and do them. Delete legacy code, clean up actual code, refactor variable names, document with consistent comment placement and correct grammar
#TODO - implement removal of single-controller groups.
#TODO - consider if it would possibly be easier to collect the hierarcy into a storage first before actually creating it, and rather than fixing single-control groups, prevent them.
#TODO - make it compatible with as many models and conventions as possible - skyrim, XNA, etc.
#TODO - upgrade the way rig bones are listed and found, just like the spine works so gloriously. also, did I implement that for the neck and head? I think not. do that too.
#TODO - make toes optional, however the autorigger guy did it.
#TODO - clavicles even^
#TODO - all kinds of bad shit happens when the rig gets re-applied after getting removed. flexes fuck up, groups get duplicated

#Global Variables - These should be accessible from anywhere in the script
shot = sfm.GetCurrentShot()
animSet = sfm.GetCurrentAnimationSet()
gameModel = animSet.gameModel
rootGroup = animSet.GetRootControlGroup()
rootBone = gameModel.children[0]
controlGroups = animSet.rootControlGroup.children

topLevelColor = vs.Color( 0, 128, 255, 255 )
RightColor = vs.Color( 255, 0, 0, 255 )
LeftColor = vs.Color( 0, 255, 0, 255 )
CustomColor = vs.Color( 15, 128, 55, 255 )
CustomColor2 = vs.Color( 30, 185, 85, 255 )
GenitalColor = vs.Color( 230, 30, 200, 255 )

def AddValidObjectToList( objectList, obj ):		#TODO - Valve's worthless function, never used, delete it
	if ( obj != None ): objectList.append( obj )

def HideControlGroups( rig, rootGroup, *groupNames ):	#TODO - similar to the above, but used once.
	for name in groupNames:	
		group = rootGroup.FindChildByName( name, False )
		if ( group != None ):
			rig.HideControlGroup( group )

#==================================================================================================
# Create the reverse foot control and operators for the foot on the specified side
#==================================================================================================
def CreateReverseFoot( controlName, sideName, gameModel, animSet, shot, helperControlGroup, footControlGroup ) :
	
	# Cannot create foot controls without heel position, so check for that first
	heelAttachName = "pvt_heel_" + sideName
	if ( gameModel.FindAttachment( heelAttachName ) == 0 ):
		#print "Could not create foot control " + controlName + ", model is missing heel attachment point: " + heelAttachName;
		return None
	
	footRollDefault = 0.5
	rotationAxis = vs.Vector( 1, 0, 0 )
		
	# Construct the name of the dag nodes of the foot and toe for the specified side
	footName = "rig_foot_" + sideName
	toeName = "rig_toe_" + sideName	
	
	# Get the world space position and orientation of the foot and toe
	footPos = sfm.GetPosition( footName )
	footRot = sfm.GetRotation( footName )
	toePos = sfm.GetPosition( toeName )
	
	# Setup the reverse foot hierarchy such that the foot is the parent of all the foot transforms, the 
	# reverse heel is the parent of the heel, so it can be used for rotations around the ball of the 
	# foot that will move the heel, the heel is the parent of the foot IK handle so that it can perform
	# rotations around the heel and move the foot IK handle, resulting in moving all the foot bones.
	# root
	#   + rig_foot_R
	#	   + rig_knee_R
	#	   + rig_reverseHeel_R
	#		   + rig_heel_R
	#			   + rig_footIK_R
	
	# Construct the reverse heel joint this will be used to rotate the heel around the toe, and as
	# such is positioned at the toe, but using the rotation of the foot which will be its parent, 
	# so that it has no local rotation once parented to the foot.
	reverseHeelName = "rig_reverseHeel_" + sideName
	reverseHeelDag = sfm.CreateRigHandle( reverseHeelName, pos=toePos, rot=footRot, rotControl=False )
	sfmUtils.Parent( reverseHeelName, footName, vs.REPARENT_LOGS_OVERWRITE )
	
	# Construct the heel joint, this will be used to rotate the foot around the back of the heel so it 
	# is created at the heel location (offset from the foot) and also given the rotation of its parent.
	heelName = "rig_heel_" + sideName
	vecHeelPos = gameModel.ComputeAttachmentPosition( heelAttachName )
	heelPos = [ vecHeelPos.x, vecHeelPos.y, vecHeelPos.z ]	 
	heelRot = sfm.GetRotation( reverseHeelName )
	heelDag = sfm.CreateRigHandle( heelName, pos=heelPos, rot=heelRot, posControl=True, rotControl=False )
	sfmUtils.Parent( heelName, reverseHeelName, vs.REPARENT_LOGS_OVERWRITE )
	
	# Create the ik handle which will be used as the target for the ik chain for the leg
	ikHandleName = "rig_footIK_" + sideName   
	ikHandleDag = sfmUtils.CreateHandleAt( ikHandleName, footName )
	sfmUtils.Parent( ikHandleName, heelName, vs.REPARENT_LOGS_OVERWRITE )
					
	# Create an orient constraint which causes the toe's orientation to match the foot's orientation
	footRollControlName = controlName + "_" + sideName
	toeOrientTarget = sfm.OrientConstraint( footName, toeName, mo=True, controls=False )
	footRollControl, footRollValue = sfmUtils.CreateControlledValue( footRollControlName, "value", vs.AT_FLOAT, footRollDefault, animSet, shot )
	
	# Create the expressions to re-map the footroll slider value for use in the constraint and rotation operators
	toeOrientExprName = "expr_toeOrientEnable_" + sideName	
	toeOrientExpr = sfmUtils.CreateExpression( toeOrientExprName, "inrange( footRoll, 0.5001, 1.0 )", animSet )
	toeOrientExpr.SetValue( "footRoll", footRollDefault )
	
	toeRotateExprName = "expr_toeRotation_" + sideName
	toeRotateExpr = sfmUtils.CreateExpression( toeRotateExprName, "max( 0, (footRoll - 0.5) ) * 140", animSet )
	toeRotateExpr.SetValue( "footRoll", footRollDefault )
							
	heelRotateExprName = "expr_heelRotation_" + sideName
	heelRotateExpr = sfmUtils.CreateExpression( heelRotateExprName, "max( 0, (0.5 - footRoll) ) * -100", animSet )
	heelRotateExpr.SetValue( "footRoll", footRollDefault )
		
	# Create a connection from the footroll value to all of the expressions that require it
	footRollConnName = "conn_footRoll_" + sideName
	footRollConn = sfmUtils.CreateConnection( footRollConnName, footRollValue, "value", animSet )
	footRollConn.AddOutput( toeOrientExpr, "footRoll" )
	footRollConn.AddOutput( toeRotateExpr, "footRoll" )
	footRollConn.AddOutput( heelRotateExpr, "footRoll" )
	
	# Create the connection from the toe orientation enable expression to the target weight of the 
	# toe orientation constraint, this will turn the constraint on an off based on the footRoll value
	toeOrientConnName = "conn_toeOrientExpr_" + sideName;
	toeOrientConn = sfmUtils.CreateConnection( toeOrientConnName, toeOrientExpr, "result", animSet )
	toeOrientConn.AddOutput( toeOrientTarget, "targetWeight" )
	
	# Create a rotation constraint to drive the toe rotation and connect its input to the 
	# toe rotation expression and connect its output to the reverse heel dag's orientation
	toeRotateConstraintName = "rotationConstraint_toe_" + sideName
	toeRotateConstraint = sfmUtils.CreateRotationConstraint( toeRotateConstraintName, rotationAxis, reverseHeelDag, animSet )
	
	toeRotateExprConnName = "conn_toeRotateExpr_" + sideName
	toeRotateExprConn = sfmUtils.CreateConnection( toeRotateExprConnName, toeRotateExpr, "result", animSet )
	toeRotateExprConn.AddOutput( toeRotateConstraint, "rotations", 0 );

	# Create a rotation constraint to drive the heel rotation and connect its input to the 
	# heel rotation expression and connect its output to the heel dag's orientation 
	heelRotateConstraintName = "rotationConstraint_heel_" + sideName
	heelRotateConstraint = sfmUtils.CreateRotationConstraint( heelRotateConstraintName, rotationAxis, heelDag, animSet )
	
	heelRotateExprConnName = "conn_heelRotateExpr_" + sideName
	heelRotateExprConn = sfmUtils.CreateConnection( heelRotateExprConnName, heelRotateExpr, "result", animSet )
	heelRotateExprConn.AddOutput( heelRotateConstraint, "rotations", 0 )
	
	if ( helperControlGroup != None ):
		sfmUtils.AddDagControlsToGroup( helperControlGroup, reverseHeelDag, ikHandleDag, heelDag )	   
	
	if ( footControlGroup != None ):
		footControlGroup.AddControl( footRollControl )
		
	return ikHandleDag

#==================================================================================================
# Compute the direction from boneA to boneB
#==================================================================================================
def ComputeVectorBetweenBones( boneA, boneB, scaleFactor ):
	
	vPosA = vs.Vector( 0, 0, 0 )
	boneA.GetAbsPosition( vPosA )
	
	vPosB = vs.Vector( 0, 0, 0 )
	boneB.GetAbsPosition( vPosB )
	
	vDir = vs.Vector( 0, 0, 0 )
	vs.mathlib.VectorSubtract( vPosB, vPosA, vDir )
	vDir.NormalizeInPlace()
	
	vScaledDir = vs.Vector( 0, 0, 0 )
	vs.mathlib.VectorScale( vDir, scaleFactor, vScaledDir )	
	
	return vScaledDir
   
#==================================================================================================
# Add a list of bones to a group, if they exist. If not, fine!
#==================================================================================================
'''
def AddFlexesToGroup(group, *flexNames):	#TODO: this shit with regex. maybe merge this functionality with the two regex functions.
	for g in controlGroups:
		for dmEle in g.controls: #bones are not in .controls, but under .children, so now we are only iterating through flexes and constraints this way.
			dmName = str(dmEle.name)
			if "Constraint" not in dmName:
				for n in flexNames:
					if n == str(dmName):
						#print("found flex: %s" %n)
						group.controls.append(dmEle)	#adding the flex to the group that was passed in
						
'''
	
def regexGroup(groupName, parentGroup, groupColor, regex, selectable=True):
	rei = re.compile(regex, re.I)
	retGroup = parentGroup.CreateControlGroup( groupName )
	
	for b in allBones:
		if re.search(rei, str(b.name)):
			sfmUtils.AddDagControlsToGroup( retGroup, b )
	
	
	#TODO - this fucks up when trying to re-apply the rig from a model that it was earlier on.
	
	if("unnamed" not in str(parentGroup.name) and False):
		for g in controlGroups:
			for dmEle in g.controls: #bones are not in .controls, but under .children, so now we are only iterating through flexes and constraints this way.
				if re.search(rei, str(dmEle.name)) and type(dmEle) is not None:
					retGroup.controls.append(dmEle)
	
	retGroup.SetGroupColor( groupColor, False )
	retGroup.SetSelectable(selectable)
	return retGroup
'''
def stereoRegexGroup(groupName, regex, parentGL, parentGR):	#TODO - could avoid some duplicate code by calling regexGroup() twice in this function.
	reiL = re.compile("((?=.*"+regex+"))(?=.*( L|\.L|left|_L))", re.I)
	reiR = re.compile("((?=.*"+regex+"))(?=.*( R|\.R|right|_R)(?!oot))", re.I)	#excludes "hair.root" "hair_root", etc.
	
	GroupL = parentGL.CreateControlGroup( "Left "+groupName )
	GroupR = parentGR.CreateControlGroup( "Right "+groupName )
	for b in allBones:
		if re.search(reiL, str(b.name)):
			sfmUtils.AddDagControlsToGroup( GroupL, b )
		if re.search(reiR, str(b.name)):
			sfmUtils.AddDagControlsToGroup( GroupR, b )
	
	GroupL.SetGroupColor( LeftColor, False )
	GroupR.SetGroupColor( RightColor, False )
	
	ret = [GroupL, GroupR]
	return ret
'''
def stereoRegexGroup(groupName, regex, parentGL, parentGR, selectable=False):	#TODO - could avoid some duplicate code by calling regexGroup() twice in this function.
	reL = "((?=.*"+regex+"))(?=.*( L|\.L|left|_L))"
	reR = "((?=.*"+regex+"))(?=.*( R|\.R|right|_R)(?!oot))"	#excludes "hair.root" "hair_root", etc.
	
	GroupL = regexGroup( "Left %s" %groupName, parentGL, LeftColor, reL, selectable )
	GroupR = regexGroup( "Right %s" %groupName, parentGR, RightColor, reR, selectable )
	
	ret = [GroupL, GroupR]
	return ret
'''
def CreateGroup(groupName, parentGroup, groupColor, selectable=True, boneNames=[]):	#TODO delete this, it's shite.
	actualBones = []
	#print("making group: %s" % groupName)
	
	for bn in boneNames:
		bone = sfmUtils.FindFirstDag( [bn], False )
		if( bone != None ):
			actualBones.append(bone)
			continue #no need to do the next parts then. (we assume regular bone names don't include '#' or end with '_'
		
		names = [bn]
		splitName = bn.split('#')
		if( len( splitName ) > 2): #numbers
			count = int(splitName[1]) #second element should be the part between the hashtags, aka the count.
			names.append(splitName[0]+splitName[2]) #without the zero
			for i in range(0, 9):
				names.append( splitName[0]+str(0)+str(i)+splitName[2] ) #man this is filthy - TODO
			for i in range(0, count+1):
				names.append( splitName[0]+str(i)+splitName[2] )
				
		for n in names: #left and right
			if("//" in n):
				names.append( n.replace("//", "L"))
				names.append( n.replace("//", "R"))
		
		newNames = names[:] #making a copy rather than a reference, otherwise this infinite loops, or crashes for some other reason, I have no idea.
		for n in names: #letters
			alphabet = "abcdefghijklmno"
			for l in alphabet:
				newNames.append( n.replace('$', l) )
				
		for n in newNames: #finding bones
			bone = sfmUtils.FindFirstDag( [n], False )
			if( bone != None ):
				actualBones.append(bone)
		
	controlGroup = parentGroup.CreateControlGroup( groupName )
	controlGroup.SetGroupColor( groupColor, False )
	controlGroup.SetSelectable( selectable )
	for b in actualBones:
		sfmUtils.AddDagControlsToGroup( controlGroup, b )
	return controlGroup
		
#TODO: function AddBonesToGroup - should be used by CreateGroup
#combineGroups(g1, g2) - for combining left and right groups that don't have enough elements to warrant a separate group.
'''
	
'''
def getChildren(dag): #this one's shit, I forgot why. TODO delete
	#return a list of bones that are the children of the parameter
	bones = []
	for i in dag.children:
		if i.children : #if its not empty
			getChildren(i)
		for j in i.controls:
			bones.append(j)
	return bones
'''

def getChildren2(dag):	#Why did I need this again? I'm sure I needed it for something. I think I would need it for avoiding the creation of 1-2-controller groups.
	bones = []
	#print("children: %s" %dag.children)
	for i in dag.children:
		bones += [i]
		if i.children : 		#if it's not empty
			bones += getChildren2(i)
	return bones

allBones = getChildren2(rootBone)

'''
def CleanUp(dag):	#IM A FUCKING IDIOT. THERE IS ALREADY A FUNCTION FOR THIS. DmeControlGroup.DestroyEmptyChildren()
	bones = []
	crap = True
	
	if dag.children: #if it has sub-groups
		for d in dag.children:
			crap = not CleanUp(d)
			#print("is %s crap? %s" %(str(dag.name), crap))
	if dag.controls: #if it has bones
		for j in dag.controls:
			bones.append(j)
		crap = False
		
	if(crap == True):
		print("this is shit: %s" %str(dag.name))
		return True
	return bones
'''
	

def FindChildBySubStr(bone, regex):
	rei = re.compile(regex, re.I)
	for b in bone.children:
		if re.search(rei, str(b)):
			return b
	return None
	
#==================================================================================================
# Build a simple ik rig for the currently selected animation set
#==================================================================================================
def BuildRig():
	# Get the currently selected animation set and shot
	#bones = getChildren(gameModel.children[0], 0)
	
	# Start the biped rig to which all of the controls and constraints will be added
	rig = sfm.BeginRig( "rig_biped_" + animSet.GetName() + str(random.randint(0, 10000)));
	if ( rig == None ):
		return
	
	# Change the operation mode to passthrough so changes chan be made temporarily
	sfm.SetOperationMode( "Pass" )
	
	# Move everything into the reference pose
	sfm.SelectAll()
	sfm.SetReferencePose()
	
	#Finding bones for the IK rig: - TODO
	#Pelvis
		#Spine
			#SpineX
				#Neck
					#Head
				#Clavicle L
					#Shoulder L
						#Hand L
				#Clavicle R
					#Shoulder R
						#Hand R
		#Thigh L
			#Knee L
				#Foot L
		#Thigh R
			#Knee R
				#Foot R
	
	#shit that needs to be done for a rig bone:
	#find the bone by name - DONE
	#create constrained handle rig
	
	#add rig handle to an array that we'll use to generate samples and shit
	#after the above step would you only parent them
	
	#OR INSTEAD what we could do, is parent the rig right after it is created, and generate samples and shit later.
	#After the new rig handles have their hierarchy down, parent them to their bones with pointorientconstraint.

	bonePelvis = FindChildBySubStr(rootBone, "Pelvis")
	if(bonePelvis == None):
		bonePelvis = rootBone
	
	boneSpines = []
	boneSpines.append(bonePelvis)
	#print(str(bonePelvis.name))
	
	while(True):	#I also like to live dangerously
		boneSpine = FindChildBySubStr(boneSpines[len(boneSpines)-1], "^(?!.*adjust.*).*spine.*$")
		if(boneSpine != None):
			#print("found: %s" %str(boneSpine.name))
			boneSpines.append(boneSpine)
			#print("found %s" %str(boneSpine.name))
		else:break
	
	#==============================================================================================
	# Find the dag nodes for all of the bones in the model which will be used by the script
	#==============================================================================================
	
	boneRoot	  = sfmUtils.FindFirstDag( [ "RootTransform" ], True )
	#boneSpine0	= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine",		"Bip01_Spine",		"bip_spine_0", "Spine" ], True )
	#boneSpine1	= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine1",		"Bip01_Spine1",		"bip_spine_1", "Spine" ], True )
	#boneLastSpine	= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine2",		"Bip01_Spine2",		"bip_spine_2", "Spine1" ], True )
	boneNeck	  = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Neck",		"Bip01_Neck",		"bip_neck_0",	"bip_neck", "ValveBiped.Bip01_Neck1", "Neck" ], True )
	boneHead	  = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Head",		"Bip01_Head",		"bip_head",		"ValveBiped.Bip01_Head1", "Head", "Head1" ], True )
	
	boneUpperLegR = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Thigh",	"Bip01_R_Thigh",	"bip_hip_R", "Thigh.R", "UpperLeg.R" ], True )
	boneLowerLegR = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Calf",	 "Bip01_R_Calf",	 "bip_knee_R", "Calf.R", "LowerLeg.R", "Shin.R" ], True )
	boneFootR	 = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Foot",	 "Bip01_R_Foot",	 "bip_foot_R", "Foot.R" ], True )
	boneToeR	  = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Toe0", "ValveBiped.Bip01_R_Toe",	 "Bip01_R_Toe0",	 "bip_toe_R", "Toe.R" ], True ) 
	boneCollarR   = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Clavicle", "Bip01_R_Clavicle", "bip_collar_R", "Clavicle.R", "Clav.R", "Collar.R" ], True )   
	boneUpperArmR = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_UpperArm", "Bip01_R_UpperArm", "bip_upperArm_R", "UpperArm.R", "Shoulder.R" ], True ) 
	boneLowerArmR = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Forearm",  "Bip01_R_Forearm",  "bip_lowerArm_R", "Forearm.R", "LowerArm.R", "Elbow.R" ], True )
	boneHandR	 = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Hand",	 "Bip01_R_Hand",	 "bip_hand_R", "Hand.R" ], True )
   
	boneUpperLegL = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Thigh",	"Bip01_L_Thigh",	"bip_hip_L", "Thigh.L", "UpperLeg.L" ], True )
	boneLowerLegL = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Calf",	 "Bip01_L_Calf",	 "bip_knee_L", "Calf.L", "LowerLeg.L", "Shin.L" ], True )
	boneFootL	 = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Foot",	 "Bip01_L_Foot",	 "bip_foot_L", "Foot.L" ], True )
	boneToeL	  = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Toe0", "ValveBiped.Bip01_L_Toe",	 "Bip01_L_Toe0",	 "bip_toe_L", "Toe.L" ], True ) 
	boneCollarL   = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Clavicle", "Bip01_L_Clavicle", "bip_collar_L", "Clavicle.L", "Clav.L", "Collar.L" ], True )		
	boneUpperArmL = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_UpperArm", "Bip01_L_UpperArm", "bip_upperArm_L", "UpperArm.L", "Shoulder.L" ], True ) 
	boneLowerArmL = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Forearm",  "Bip01_L_Forearm",  "bip_lowerArm_L", "Forearm.L", "LowerArm.L", "Elbow.L" ], True ) 
	boneHandL	 = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Hand",	 "Bip01_L_Hand",	 "bip_hand_L", "Hand.L" ], True )

	#==============================================================================================
	# Create the rig handles and constrain them to existing bones
	#==============================================================================================
	rigRoot	= sfmUtils.CreateConstrainedHandle( "rig_root",	 boneRoot,	bCreateControls=False )
	rigPelvis	= sfmUtils.CreateConstrainedHandle( "rig_pelvis",	 bonePelvis,	bCreateControls=False )
	
	rigNeck	= sfmUtils.CreateConstrainedHandle( "rig_neck",	 boneNeck,	bCreateControls=False )
	rigHead	= sfmUtils.CreateConstrainedHandle( "rig_head",	 boneHead,	bCreateControls=False )
	
	rigFootR   = sfmUtils.CreateConstrainedHandle( "rig_foot_R",   boneFootR,   bCreateControls=False )
	rigToeR	= sfmUtils.CreateConstrainedHandle( "rig_toe_R",	boneToeR,	bCreateControls=False )
	rigCollarR = sfmUtils.CreateConstrainedHandle( "rig_collar_R", boneCollarR, bCreateControls=False )
	rigHandR   = sfmUtils.CreateConstrainedHandle( "rig_hand_R",   boneHandR,   bCreateControls=False )
	rigFootL   = sfmUtils.CreateConstrainedHandle( "rig_foot_L",   boneFootL,   bCreateControls=False )
	rigToeL	= sfmUtils.CreateConstrainedHandle( "rig_toe_L",	boneToeL,	bCreateControls=False )
	rigCollarL = sfmUtils.CreateConstrainedHandle( "rig_collar_L", boneCollarL, bCreateControls=False )
	rigHandL   = sfmUtils.CreateConstrainedHandle( "rig_hand_L",   boneHandL,   bCreateControls=False )
	
	# Use the direction from the heel to the toe to compute the knee offsets, 
	# this makes the knee offset indpendent of the inital orientation of the model.
	vKneeOffsetR = ComputeVectorBetweenBones( boneFootR, boneToeR, 10 )
	vKneeOffsetL = ComputeVectorBetweenBones( boneFootL, boneToeL, 10 )
	
	rigKneeR   = sfmUtils.CreateOffsetHandle( "rig_knee_R",  boneLowerLegR, vKneeOffsetR,  bCreateControls=False )   
	rigKneeL   = sfmUtils.CreateOffsetHandle( "rig_knee_L",  boneLowerLegL, vKneeOffsetL,  bCreateControls=False )
	rigElbowR  = sfmUtils.CreateOffsetHandle( "rig_elbow_R", boneLowerArmR, -vKneeOffsetR,  bCreateControls=False )
	rigElbowL  = sfmUtils.CreateOffsetHandle( "rig_elbow_L", boneLowerArmL, -vKneeOffsetL,  bCreateControls=False )
	
	# Create a helper handle which will remain constrained to the each foot position that can be used for parenting.
	rigFootHelperR = sfmUtils.CreateConstrainedHandle( "rig_footHelper_R", boneFootR, bCreateControls=False )
	rigFootHelperL = sfmUtils.CreateConstrainedHandle( "rig_footHelper_L", boneFootL, bCreateControls=False )
	
	# Create a list of all of the rig dags
	allRigHandles = [ rigRoot, rigNeck, rigHead,
					  rigCollarR, rigElbowR, rigHandR, rigKneeR, rigFootR, rigToeR,
					  rigCollarL, rigElbowL, rigHandL, rigKneeL, rigFootL, rigToeL ];
	
	rigSpines = []
	rigSpines.append(rigPelvis)
	
	for i in range(1, len(boneSpines)):
		rigSpine = sfmUtils.CreateConstrainedHandle( "rig_spine_%s" %i,  boneSpines[i],  bCreateControls=False )
		rigSpines.append(rigSpine)
		#print("rig spine added: %s" %rigSpine)
	
	for r in rigSpines:
		allRigHandles.append(r)
	
	#==============================================================================================
	# Generate the world space logs for the rig handles and remove the constraints
	#==============================================================================================
	sfm.ClearSelection()
	sfmUtils.SelectDagList( allRigHandles )
	sfm.GenerateSamples()
	sfm.RemoveConstraints()	
	
	#==============================================================================================
	# Build the rig handle hierarchy
	#==============================================================================================
	sfmUtils.ParentMaintainWorld( rigSpines[0],		rigRoot ) #runs without this, so what if I just called the pelvis bone explicitly
	
	for i in range(1, len(rigSpines)):
		sfmUtils.ParentMaintainWorld( rigSpines[i],	rigSpines[i-1] )
		
	sfmUtils.ParentMaintainWorld( rigNeck,		  rigSpines[len(rigSpines)-1] )
	sfmUtils.ParentMaintainWorld( rigHead,		  rigNeck )
	
	sfmUtils.ParentMaintainWorld( rigFootHelperR,   rigRoot )
	sfmUtils.ParentMaintainWorld( rigFootHelperL,   rigRoot )
	sfmUtils.ParentMaintainWorld( rigFootR,		 rigRoot )
	sfmUtils.ParentMaintainWorld( rigFootL,		 rigRoot )
	sfmUtils.ParentMaintainWorld( rigKneeR,		 rigFootR )
	sfmUtils.ParentMaintainWorld( rigKneeL,		 rigFootL )
	sfmUtils.ParentMaintainWorld( rigToeR,		  rigFootHelperR )
	sfmUtils.ParentMaintainWorld( rigToeL,		  rigFootHelperL )
	
	sfmUtils.ParentMaintainWorld( rigCollarR,	   rigSpines[len(rigSpines)-1] )
	sfmUtils.ParentMaintainWorld( rigElbowR,		rigCollarR )
	sfmUtils.ParentMaintainWorld( rigHandR,		rigRoot )
	sfmUtils.ParentMaintainWorld( rigCollarL,	   rigSpines[len(rigSpines)-1] )
	sfmUtils.ParentMaintainWorld( rigElbowL,		rigCollarL )
	sfmUtils.ParentMaintainWorld( rigHandL,		rigRoot )
	
	# Create the hips control, this allows a pelvis rotation that does not effect the spine,
	# it is only used for rotation so a position control is not created. Additionally add the
	# new control to the selection so the that set default call operates on it too.
	rigHips = sfmUtils.CreateHandleAt( "rig_hips", rigPelvis, False, True )
	sfmUtils.Parent( rigHips, rigPelvis, vs.REPARENT_LOGS_OVERWRITE )
	sfm.SelectDag( rigHips )

	# Set the defaults of the rig transforms to the current locations. Defaults are stored in local
	# space, so while the parent operation tries to preserve default values it is cleaner to just
	# set them once the final hierarchy is constructed.
	sfm.SetDefault()
	
	#==============================================================================================
	# Create the reverse foot controls for both the left and right foot
	#==============================================================================================
	rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
	rigHelpersGroup = rootGroup.CreateControlGroup( "RigHelpers" )
	rigHelpersGroup.SetVisible( False )
	rigHelpersGroup.SetSnappable( False )
	
	footIKTargetR = rigFootR
	footIkTargetL = rigFootL
	
	if ( gameModel != None ) :
		footRollIkTargetR = CreateReverseFoot( "rig_footRoll", "R", gameModel, animSet, shot, rigHelpersGroup, rigLegsGroup )
		footRollIkTargetL = CreateReverseFoot( "rig_footRoll", "L", gameModel, animSet, shot, rigHelpersGroup, rigLegsGroup )
		if ( footRollIkTargetR != None ) :
			footIKTargetR = footRollIkTargetR
		if ( footRollIkTargetL != None ) :
			footIkTargetL = footRollIkTargetL
	
	#==============================================================================================
	# Create constraints to drive the bone transforms using the rig handles
	#==============================================================================================
	
	# The following bones are simply constrained directly to a rig handle
	sfmUtils.CreatePointOrientConstraint( rigRoot,	  boneRoot		)
	sfmUtils.CreatePointOrientConstraint( rigHips,	  bonePelvis	  )
	for k in range(1, len(rigSpines)):
		sfmUtils.CreatePointOrientConstraint( rigSpines[k], boneSpines[k])
		#print("constraining rig %s to bone %s" %(rigSpines[k], boneSpines[k]))
	#sfmUtils.CreatePointOrientConstraint( rigSpine0,	boneSpine0	  )
	#sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1	  )
	#sfmUtils.CreatePointOrientConstraint( rigSpines[len(rigSpines)-1],	boneSpines[len(boneSpines)-1]	  )
	sfmUtils.CreatePointOrientConstraint( rigNeck,	  boneNeck		)
	sfmUtils.CreatePointOrientConstraint( rigHead,	  boneHead		)
	sfmUtils.CreatePointOrientConstraint( rigCollarR,   boneCollarR	 )
	sfmUtils.CreatePointOrientConstraint( rigCollarL,   boneCollarL	 )
	sfmUtils.CreatePointOrientConstraint( rigToeR,	  boneToeR		)
	sfmUtils.CreatePointOrientConstraint( rigToeL,	  boneToeL		)
	
	# Create ik constraints for the arms and legs that will control the rotation of the hip / knee and 
	# upper arm / elbow joints based on the position of the foot and hand respectively.
	sfmUtils.BuildArmLeg( rigKneeR,  footIKTargetR, boneUpperLegR,  boneFootR, True )
	sfmUtils.BuildArmLeg( rigKneeL,  footIkTargetL, boneUpperLegL,  boneFootL, True )
	sfmUtils.BuildArmLeg( rigElbowR, rigHandR,	  boneUpperArmR,  boneHandR, True )
	sfmUtils.BuildArmLeg( rigElbowL, rigHandL,	  boneUpperArmL,  boneHandL, True )
	
	#==============================================================================================
	# Create handles for the important attachment points 
	#==============================================================================================	
	attachmentGroup = rootGroup.CreateControlGroup( "Attachments" )  
	attachmentGroup.SetVisible( False )
	
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_heel_R",	   attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_toe_R",		attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_outerFoot_R",  attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_innerFoot_R",  attachmentGroup )
	
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_heel_L",	   attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_toe_L",		attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_outerFoot_L",  attachmentGroup )
	sfmUtils.CreateAttachmentHandleInGroup( "pvt_innerFoot_L",  attachmentGroup )
	
	#==============================================================================================
	# Re-organize the selection groups
	#==============================================================================================  
	
	rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
	rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
	
	BodyGroup = regexGroup( "Body", rootGroup, topLevelColor, "head|neck|spine|pelvis|hip")
	LegsGroup = regexGroup( "Legs", BodyGroup, topLevelColor, "leg|thigh|calf|upperleg|knee|foot|shin" )
	ArmsGroup = regexGroup( "Arms", BodyGroup, topLevelColor, "clav|collar|shoulder|upperarm|forearm|lowerarm|elbow|hand" )
	'''
	LegsGroup = CreateGroup( "Legs", BodyGroup, topLevelColor, selectable=False, boneNames=[ 
		"ValveBiped.Bip01_//_Thigh",	"Bip01_//_Thigh",	"bip_hip_//", "Thigh.//" , "UpperLeg.//",
		"ValveBiped.Bip01_//_Calf",	 "Bip01_//_Calf",	 "bip_knee_//", "Calf.//" , "LowerLeg.//",
		"ValveBiped.Bip01_//_Foot",	 "Bip01_//_Foot",	 "bip_foot_//", "Foot.//",
		"ValveBiped.Bip01_//_Toe0", "ValveBiped.Bip01_//_Toe",	 "Bip01_//_Toe0",	 "bip_toe_//", "Toe.//",
	] )
	ArmsGroup = CreateGroup( "Arms", BodyGroup, topLevelColor, selectable=False, boneNames=[ 
		"ValveBiped.Bip01_//_Clavicle", "Bip01_//_Clavicle", "bip_collar_//", "Clavicle.//", "Clav.//",
		"ValveBiped.Bip01_//_UpperArm", "Bip01_//_UpperArm", "bip_upperArm_//", "UpperArm.//", "Shoulder.//", "UpperArm.//",
		"ValveBiped.Bip01_//_Forearm",  "Bip01_//_Forearm",  "bip_lowerArm_//", "Forearm.//", "LowerArm.//", "LowerArm.//",
		"ValveBiped.Bip01_//_Hand",	 "Bip01_//_Hand",	 "bip_hand_//", "Hand.//", "Elbow.//"
	] )
	BodyGroup = CreateGroup( "Body", rootGroup, topLevelColor, selectable=False, boneNames=[ "ValveBiped.Bip01_Pelvis",	"Bip01_Pelvis",		"bip_pelvis", "Pelvis" , "Hips", "ValveBiped.Bip01_Hips",
		"ValveBiped.Bip01_Spine1",		"Bip01_Spine1",		"bip_spine_1", "Spine#4#", 
		"ValveBiped.Bip01_Spine2",		"Bip01_Spine2",		"bip_spine_2", "Spine.#4#", 
		"ValveBiped.Bip01_Neck",		"Bip01_Neck",		"bip_neck_0",	"bip_neck", "ValveBiped.Bip01_Neck1", "Neck",
		"ValveBiped.Bip01_Head",		"Bip01_Head",		"bip_head",		"ValveBiped.Bip01_Head1", "Head", "Head1", "Head.//"	] )
	'''
	BodyGroup.AddChild( rigHelpersGroup )
	
	RightArmGroup = rootGroup.CreateControlGroup( "RightArm" )
	LeftArmGroup = rootGroup.CreateControlGroup(  "LeftArm" )
	RightLegGroup = rootGroup.CreateControlGroup(  "RightLeg" )
	LeftLegGroup = rootGroup.CreateControlGroup(  "LeftLeg" )   
	
	################################
	ArmTwistLRGroups = stereoRegexGroup( "Arm Adjust", "(?=.*(twist|adjust|FK))(?=.*(arm|elbow|shoulder|clav|collar|wrist))|carpal", LeftArmGroup, RightArmGroup, selectable=False )
	LegTwistLRGroups = stereoRegexGroup( "Leg Adjust", "(?=.*(twist|adjust|FK))(?=.*(leg|thigh|knee|calf|ankle))|tarsal|heel|achil", LeftLegGroup, RightLegGroup, selectable=False )
	
	ToesLRGroup = stereoRegexGroup( "Toes", "toe|(?=.*(toe))(?=.*(big|index|middle|ring|pinky))", LeftLegGroup, RightLegGroup )
	
	FingerLRGroups = stereoRegexGroup( "Fingers",  "(finger|index|thumb|ring|pinky)|(?=.*(middle))(?=.*(finger))", LeftArmGroup, RightArmGroup ) #I can't assume everything that has "middle" in it is a finger, but everything that has both "middle" and "finger" in it should hopefully get matched.
	
	GenitalsGroup = regexGroup( "Genitals", rootGroup, topLevelColor, "vag|butt|ass" ,False)
	BreastsLRGroup = stereoRegexGroup ( "Breast", "breast|pec", GenitalsGroup, GenitalsGroup, True )
	VaginaGroup = regexGroup( "Vagina", GenitalsGroup, GenitalColor, "vag|(?<!naso)labia|bulge" ) #don't fucking catch nasolabial mouth bones
	PenisGroup = regexGroup( "Penis", GenitalsGroup, GenitalColor, "penis|ball|sack" )
	AnusGroup = regexGroup( "Anus", GenitalsGroup, GenitalColor, "anus" )
	
	WingsGroup = regexGroup( "Wings", rootGroup, topLevelColor, "wing" )
	WingsLRGroup = stereoRegexGroup( "Wing", "wing", WingsGroup, WingsGroup )
	
	TailGroup = regexGroup( "Tail", rootGroup, topLevelColor, "tail" )
	
	'''
	AddFlexesToGroup( VaginaGroup, "Vagina" )
	AddFlexesToGroup( AnusGroup, "Anus" )
	
	ToesLGroup = CreateGroup( "Left Toes", LeftLegGroup, LeftColor, selectable=False, boneNames=["Toe#50#.L"] )
	ToesRGroup = CreateGroup( "Right Toes", RightLegGroup, RightColor, selectable=False, boneNames=["Toe#50#.R"] )
	LegTwistLGroup = CreateGroup( "Left Leg Twist", LeftLegGroup, LeftColor, selectable=False, boneNames=["Twist_Thigh.L", "Twist_Thigh_2.L", "Adjust_Thigh.L", "Adjust_Knee.L", "Twist_Knee.L", "UpperLeg_FK.L", "LowerLeg_FK.L", "Calf_FK.L"] )
	LegTwistRGroup = CreateGroup( "Right Leg Twist", RightLegGroup, RightColor, selectable=False, boneNames=["Twist_Thigh.R", "Twist_Thigh_2.R", "Adjust_Thigh.R", "Adjust_Knee.R", "Twist_Knee.R", "UpperLeg_FK.R", "LowerLeg_FK.R", "Calf_FK.R"] )
	#FingersLGroup = CreateGroup( "LeftFingers", LeftArmGroup, LeftColor, selectable=False, boneNames=["ValveBiped.Bip01_L_Finger#50#", "Finger#50#.L"] )#who needs defaultanimationgroups.txt? pssh.
	#FingersRGroup = CreateGroup( "RightFingers", RightArmGroup, RightColor, selectable=False, boneNames=["ValveBiped.Bip01_R_Finger#50#", "Finger#50#.R"] )
	GenitalsGroup = CreateGroup( "Erogenous", rootGroup, topLevelColor, selectable=False, boneNames=["Butt.//", "Pussy.//"] )
	BreastsLGroup = CreateGroup( "Left Breast", GenitalsGroup, LeftColor, boneNames=["Breast.L", "Breast_Base_Parent.L", "Breast_Base.L", "Breast_Tip.L", "Breast_#5#.L"] )
	BreastsRGroup = CreateGroup( "Right Breast", GenitalsGroup, RightColor, boneNames=["Breast.R", "Breast_Base_Parent.R", "Breast_Base.R", "Breast_Tip.R", "Breast_#5#.R"] )
	AnusGroup = CreateGroup( "Anus", GenitalsGroup, GenitalColor, boneNames=["Root_Anus", "anus.#5#", "Anus.//.#5#"] )
	LabiaGroup = CreateGroup( "Labia", GenitalsGroup, GenitalColor, boneNames=["Root_Labia", "Labia_#6#.//"] )
	VaginaGroup = CreateGroup( "Vagina", GenitalsGroup, GenitalColor, boneNames=["Root_Vagina", "Root_Vagoo", "vagina.#5#", "Vagina_#6#.//"] )
	#WingsLGroup = CreateGroup( "Left Wings", WingsGroup, LeftColor, boneNames=["Wing_Root.L", "Wing_#21#.L", "Wing.L", "Wing.L.#5#"] )
	#WingsRGroup = CreateGroup( "Right Wings", WingsGroup, RightColor, boneNames=["Wing_Root.R", "Wing_#21#.R","Wing.R",  "Wing.R.#5#"] )
	TailGroup = CreateGroup( "Tail", rootGroup, topLevelColor, boneNames=["tail", "tail #13#", "Tail.#50#"] )
	'''
	
	HairGroup = regexGroup( "Hair", rootGroup, topLevelColor, "hair", False )
	HairBackGroup = regexGroup( "Back", HairGroup, CustomColor2, "(?=.*(hair))(?=.*(tail|back))" )
	HairFrontGroup = regexGroup( "Front", HairGroup, CustomColor2, "(?=.*(hair))(?=.*(fringe|front|bang))" )
	HairLRGroups = stereoRegexGroup( "Hair", "hair|kanzashi", HairGroup, HairGroup ,True)
	
	FaceGroup = regexGroup( "Face", rootGroup, topLevelColor, "face|teeth|throat", False )
	TongueGroup = regexGroup( "Tongue", FaceGroup, CustomColor, "tongue")
	EyesGroup = regexGroup( "Eyes", FaceGroup, CustomColor, "eye" ) #fuck it, might as well, just make sure this stays Before "eye"brows and "eye"lids, etc.
	EyebrowsGroup = regexGroup( "Eyebrows", EyesGroup, CustomColor2, "brow" )
	LowerEyelidsGroup = regexGroup( "Lower Eyelids", EyesGroup, CustomColor2, "(?=.*(eyelid))(?=.*(lower))" )
	UpperEyelidsGroup = regexGroup( "Upper Eyelids", EyesGroup, CustomColor2, "(?=.*(eyelid))(?=.*(upper))" )
	
	
	ForeHeadGroup = regexGroup( "Forehead", FaceGroup, CustomColor, "forehead" )
	NoseGroup = regexGroup( "Nose", FaceGroup, CustomColor, "nose|nostril" )
	CheeksGroup = regexGroup( "Cheek", FaceGroup, CustomColor, "cheek|squint")
	JawGroup = regexGroup( "Jaw", FaceGroup, CustomColor, "jaw|chin|nasola" )	#It is awkwardly important that this stays below the Vagina group definition.
	
	LipsGroup = regexGroup( "Lips", FaceGroup, CustomColor, "lip|smile|pucker" ) #yolo
	
	EarsGroup = regexGroup( "Ears", FaceGroup, CustomColor, "(?<!for)ear" )	#don't fucking catch forearms.
	
	'''
	AddFlexesToGroup( LipsGroup, "LowerLipFold", "UpperLipFold", "LipsForward", "LipsShrink", "LipUpperDown", "LipLowerUp", "MouthSmile", "MouthSmile2" ) #TODO remove mouthsmile2, use syntax
	AddFlexesToGroup( JawGroup, "MouthOpen", "Throat" )	#attempting to add these to FaceGroup crashes SFM, don't know why, don't care
	AddFlexesToGroup( CheeksGroup, "CheeksPuff", "CheeksRaise", "CheeksDeflate" )
	AddFlexesToGroup( NoseGroup, "NoseFlare" )
	AddFlexesToGroup( EyesGroup, "EyesBlink", "EyesBlinkHappy", "EyesOpen")
	AddFlexesToGroup( EyebrowsGroup, "EyebrowsInnerUp", "EyebrowsInnerDown", "EyebrowsOuterDown", "EyebrowsOuterUp" )
	FaceGroup = CreateGroup( "Face", rootGroup, topLevelColor, boneNames=["Root_Face", "Jaw", "lowerJaw", "Teeth.T", "upperTeeth", "Teeth.B", "lowerTeeth", "throat", "Eyelids", "Eyebrows"] )
	EyesGroup = CreateGroup( "Eyes", FaceGroup, CustomColor, boneNames=["Eyeball.//", "eye.//"] )
	EyebrowsGroup = CreateGroup( "Eyebrows", EyesGroup, CustomColor2, boneNames=["Eyebrow_Outer.//", "Eyebrow_Middle.//", "Eyebrow_Inner.//", "Eyebrow_Middle", "brow.T.//", "brow.T.//.#5#", "Eyebrow.//", "Eyebrow.//.#5#", "Eyebrow_Devil.//"] )
	LowerEyelidsGroup = CreateGroup( "Lower Eyelids", EyesGroup, CustomColor2, boneNames=["Eyelid_Lower.//", "Eyelid_Lower_Outer.//", "Eyelid_Lower_Inner.//", "lid.B.//", "lid.B.//.#5#", "LowerEyelid.//"] ) #dunno if I want left/right in these. 
	UpperEyelidsGroup = CreateGroup( "Upper Eyelids", EyesGroup, CustomColor2, boneNames=["Eyelid_Upper.//", "lid.T.//", "lid.T.//.#5#", "UpperEyelid.//"] )
	#LowerEyebrowsGroup = CreateGroup ("Lower Eyebrows", EyesGroup, CustomColor2, boneNames=["Eyebrow_Lower_Root.//", "brow.B.//", "brow.B.//.#5#"] ) #I think only Motoko ever used this, so fuck it.
	NoseGroup = CreateGroup( "Nose", FaceGroup, CustomColor, boneNames=["Nose_Upper.//", "Nose_Lower.//", "Nose_Tip", "Nostril.//", "nose.//", "nose", "nose.#4#", "nose.//.#2#"])
	CheeksGroup = CreateGroup( "Cheeks", FaceGroup, CustomColor, boneNames=["Cheek_Outer.//", "Cheek_Inner.//", "Cheek_Main.//", "NoseLine_Inner.//", "NoseLine_Outer.//", "cheek.T.//", "cheek.T.//.#3#", "cheek.B.//", "cheek.B.//.#3#", "Cheek.//", "Cheek.//.#2#"] )
	JawGroup = CreateGroup( "Jaw", FaceGroup, CustomColor, boneNames=["jaw", "jaw.//", "jaw.//.#2#", "chin", "chin.#2#", "chin.//", "NasolabialLower.//", "Chin#3#", "Chin", "Chin.//"] )
	LipsGroup = CreateGroup( "Lips", FaceGroup, CustomColor, boneNames=["Lip_Corner.//", "Lip_Upper.//", "Lip_Lower.//", "Lip_Lower_Middle", "Lip_Upper_Middle", "lip.T.//", "lip.T.//.#3#", "lip.B.//", "lip.B.//.#3#", "Lip_Top", "Lip_Top.//", "Lip_Bottom", "Lip_Bottom.//", "Mouth_Corner.//", "Lip_Bot.//", "Lip_Bot_Mid", "Lip_Top_Mid"] )
	EarsGroup = CreateGroup( "Ears", FaceGroup, CustomColor, boneNames=["ear.//", "ear.//.#6#"] )
	'''
	
	ClothesGroup = regexGroup( "Clothes", rootGroup, topLevelColor, "weapon|shade|glass|gun|headband|cloth|mask|flower|hairpiece|bunny|gear|pouch|mag|pistol|zip|backpad|fit(arm|leg|tit|breast|butt|chest|torso|upper|lower|bikini|top)|chestcompress|visor|wibbly|timeywimey|jacket" , False)
	ClothesLRGroups = stereoRegexGroup( "Clothes", "fringe", ClothesGroup, ClothesGroup )
	ClothesFrontGroup = regexGroup( "Front Clothes", ClothesGroup, CustomColor,"(?=.*(cloth))(?=.*(front))")
	ClothesBackGroup = regexGroup( "Back Clothes", ClothesGroup, CustomColor, "(?=.*(cloth))(?=.*(back))")
	
	RibbonsGroup = regexGroup( "Ribbons", ClothesGroup, CustomColor, "ribbon" )
	SkirtGroup = regexGroup( "Skirt", ClothesGroup, CustomColor, "skirt" )
	MercySkirtGroup = regexGroup ( "Devil Skirt", SkirtGroup, CustomColor, "skirt_d" )
	
	FuckedGroup = regexGroup( "STRAY_VERTS", rootGroup, RightColor, "blender_implicit")
	
	
	'''
	FlexesGroup = CreateGroup( "Flexes", ClothesGroup, CustomColor, boneNames=[] )
	AddFlexesToGroup( FlexesGroup, "ChestCompress", "ChestCompress2", "FitArms", "FitLegs", "FitFeet", "FitTits", "ValButt", "FitBikini" )
	
	ClothesGroup = CreateGroup( "Clothes", rootGroup, topLevelColor, boneNames=["Weapon", "shades", "glasses", "MediGun", "Medigun.#3#", "HeadBand", "cloth top.//.#3#", "cloth back #5#.//", "cloth top.//.#5#", "Mask1", "Flower1", "HairPiece_Root"])
	ClothesFrontGroup = CreateGroup( "Front Clothes", ClothesGroup, CustomColor, boneNames=["Cloth_Front.#10#"])
	ClothesBackGroup = CreateGroup( "Back Clothes", ClothesGroup, CustomColor, boneNames=["Cloth_Back.#10#"])
	RibbonsGroup = CreateGroup( "Ribbons", ClothesGroup, CustomColor, boneNames=["ribbon back #20#", "ribbon #5# ", "BikiniString_Root", "BikiniString.//", "Ribbon_Back_Root", "ribbon back.//.#5#", "ribbon back top.//.#5#", "ribbon wrist $ #5#", "Ribbon.//.#5#", "Ribbon_Back_Top.#5#", "Ribbon_Back.#5#"] )
	SkirtGroup = CreateGroup( "Skirt", ClothesGroup, CustomColor, boneNames=["skirt #20#$", "Skirt.//.#4#", "skirt front.#5#", "skirt back.#5#", "skirt.#5#"] )
	'''
	'''
	###MODEL SPECIFIC SHIT - which kind of shouldn't be necessary. Or maybe it is. Definitely needs cleanup. TODO
	FuckedGroup = CreateGroup( "YOU FUCKED UP", rootGroup, CustomColor, boneNames=["blender_implicit"])
	#Met's Motoko
	MotokoGroup = CreateGroup( "Motoko Gear", ClothesGroup, CustomColor, boneNames=["ThighGear", "Pouch_Big", "Pouch_Small", "Mag1", "Mag2", "Pouch_Belt", "Pistol", "Zip_Root", "Zip", "BackPad.//"] )
	CollarGroup = CreateGroup( "Collar", ClothesGroup, CustomColor, boneNames=["Collar_Back", "Collar.//"] )
	#Met's DoA5 5Tina
	FringeArmLeftGroup = CreateGroup( "Arm Left Fringe", LeftArmGroup, LeftColor, selectable=False, boneNames=["Fringe_Arm_#5#.L", "Fringe_Wrist.L"] )
	FringeLegLeftGroup = CreateGroup( "Leg Left Fringe", LeftLegGroup, LeftColor, selectable=False, boneNames=["Fringe_Leg_#5#.L"] )
	FringeArmRightGroup = CreateGroup( "Arm Right Fringe", RightArmGroup, RightColor, selectable=False, boneNames=["Fringe_Arm_#5#.R", "Fringe_Wrist.R"] )
	FringeLegRightGroup = CreateGroup( "Leg Right Fringe", RightLegGroup, RightColor, selectable=False, boneNames=["Fringe_Leg_#5#.R"] )
	LassoGroup = CreateGroup( "Lasso", ClothesGroup, CustomColor, selectable=False, boneNames=["lasso root", "lasso #5#"] )
	#Met's Tracer
	TracerGroup = CreateGroup( "Tracer", ClothesGroup, CustomColor, selectable=False, boneNames=["TracerVisor", "ShoulderGear.//", "Visor", "WibblyWobbly", "TimeyWimey", "JacketCollar.//", "JacketCollar_Back", "Jacket.//"] )
	AddFlexesToGroup( TracerGroup, "FitJacket", "FitLegsUpper", "FitLegsLower", "KirbyLeggings", "SmoothBody" )
	#Met's Mercy
	MercySkirtGroup = CreateGroup( "Devil Skirt", SkirtGroup, CustomColor, boneNames=["Skirt_D.//", "Skirt_D.//.#5#", "Skirt_D_B.//", "Skirt_D_B.//.#5#"])
	'''
	
	################################
	sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigHips, rigPelvis )
	for r in rigSpines:
		sfmUtils.AddDagControlsToGroup(rigBodyGroup, r)
	sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigNeck, rigHead )
	  
	rigArmsGroup.AddChild( RightArmGroup )
	rigArmsGroup.AddChild( LeftArmGroup )
	sfmUtils.AddDagControlsToGroup( RightArmGroup,  rigHandR, rigElbowR, rigCollarR )
	sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigHandL, rigElbowL, rigCollarL )
	
	rigLegsGroup.AddChild( RightLegGroup )
	rigLegsGroup.AddChild( LeftLegGroup )
	sfmUtils.AddDagControlsToGroup( RightLegGroup, rigKneeR, rigFootR, rigToeR )
	sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigKneeL, rigFootL, rigToeL )
	
	sfmUtils.MoveControlGroup( "rig_footRoll_L", rigLegsGroup, LeftLegGroup )
	sfmUtils.MoveControlGroup( "rig_footRoll_R", rigLegsGroup, RightLegGroup )

	sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigFootHelperR, rigFootHelperL )

	# Set the control group visiblity, this is done through the rig so it can track which
	# groups it hid, so they can be set back to being visible when the rig is detached.
	HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )	  
		
	#Re-order the groups
	fingersGroup = rootGroup.FindChildByName( "Fingers", False ) 
	rootGroup.MoveChildToBottom( rigBodyGroup )
	rootGroup.MoveChildToBottom( rigLegsGroup )	
	rootGroup.MoveChildToBottom( rigArmsGroup )	  
	rootGroup.MoveChildToBottom( fingersGroup )  
	   
	rightFingersGroup = rootGroup.FindChildByName( "RightFingers", True ) 
	if ( rightFingersGroup != None ):
		RightArmGroup.AddChild( rightFingersGroup )
		rightFingersGroup.SetSelectable( False )
								
	leftFingersGroup = rootGroup.FindChildByName( "LeftFingers", True ) 
	if ( leftFingersGroup != None ):
		LeftArmGroup.AddChild( leftFingersGroup )
		leftFingersGroup.SetSelectable( False )
		

	#==============================================================================================
	# Set the selection groups colors
	#==============================================================================================
	rigBodyGroup.SetGroupColor( topLevelColor, False )
	rigArmsGroup.SetGroupColor( topLevelColor, False )
	rigLegsGroup.SetGroupColor( topLevelColor, False )
	attachmentGroup.SetGroupColor( topLevelColor, False )
	rigHelpersGroup.SetGroupColor( topLevelColor, False )
	
	RightArmGroup.SetGroupColor( RightColor, False )
	LeftArmGroup.SetGroupColor( LeftColor, False )
	RightLegGroup.SetGroupColor( RightColor, False )
	LeftLegGroup.SetGroupColor( LeftColor, False )
	
	#deleting empty and near-empty groups #TODO near empty*
	rootGroup.DestroyEmptyChildren()
	
	print("RIG DONE")	#TODO could print some extra info or some shit.
	# End the rig definition
	sfm.EndRig()
	return
	
#==================================================================================================
# Script entry
#==================================================================================================

# Construct the rig for the selected animation set
BuildRig();