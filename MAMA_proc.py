
# coding: utf-8

# In[9]:


from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces import fsl
#from nipype.interfaces.freesurfer import bet
from shutil import copyfile
from subprocess import run, call, CompletedProcess

subject = input('Please enter the subject ID: ')

home = '/Volumes/iang/active/BABIES/BABIES_MAMA'

t1w = home + '/' + subject + '/t1w'
dest = home + '/' + subject + '/anat' 
func1 = home + '/' + subject + '/func/run1'
func2 = home + '/' + subject + '/func/run2'

copyfile((t1w + '/t1w_raw.nii.gz'),(dest + '/t1w_raw.nii.gz'))


# In[10]:


reorient = Node(fsl.Reorient2Std(in_file = (dest +'/t1w_raw.nii.gz'),
                                out_file = (dest +'/spgrorient.nii.gz'),
                                output_type = 'NIFTI_GZ'),
                            name = 'reorient')
reorient.run()


# In[11]:


skullstrip = Node(fsl.BET(in_file = (dest+'/spgrorient.nii.gz'),
                          out_file = (dest+'/spgrbrain.nii.gz'),
                          robust = True,
                          frac= 0.5,
                          vertical_gradient = 0), 
                          name = 'skullstrip')
skullstrip.run()


# In[13]:


#Preprocess functional run1
func_reorient1 = Node(fsl.Reorient2Std(in_file = (func1 + '/' + subject +'_run1raw.nii'),
                                      out_file = (func1 + '/' + subject +'_run1orient.nii.gz'),
                                      output_type = 'NIFTI_GZ'),
                         name = 'func_reorient1')
func_reorient1.run()



# In[14]:


drop1 = Node(fsl.ExtractROI(in_file = (func1 + '/' + subject +'_run1orient.nii.gz'),
                           roi_file = (func1 + '/' + subject +'_run1drop.nii.gz'),
                           output_type = 'NIFTI_GZ',
                           t_min = 4,
                           t_size = 247),
           name = 'drop1')
drop1.run()


# In[15]:


motion_outliers1 = fsl.MotionOutliers(in_file = (func1 + '/' + subject +'_run1drop.nii.gz'),
                                          out_file = (func1 + '/' + subject +'_run1motionoutliers'))
motion_outliers1.run()


# In[16]:


func_strip1 = Node(fsl.BET(in_file = (func1 + '/' + subject +'_run1drop.nii.gz'),
                          out_file = (func1 + '/' + subject +'_run1brain.nii.gz'),
                          frac= 0.3,
                          functional = True), 
                  name = 'func_strip')
func_strip1.run()


# In[17]:


# run1_flow = Workflow(name = 'run1_flow')
# run1_flow.connect([(func_reorient1, drop1,[('in_file','out_file')]),
#                   (drop1, motout1, [('outfile', 'in_file')]),
#                   (motout1, func_strip1[('in_file', 'out_file')])
#                   ])


# In[18]:


#Preprocess functional run2
func_reorient2 = Node(fsl.Reorient2Std(in_file = (func2 + '/' + subject +'_run2raw.nii'),
                                      out_file = (func2 + '/' + subject +'_run2orient.nii.gz'),
                                      output_type = 'NIFTI_GZ'),
                         name = 'reorient2')
func_reorient2.run()


# In[19]:


drop2 = Node(fsl.ExtractROI(in_file = (func2 + '/' + subject +'_run2orient.nii.gz'),
                           roi_file = (func2 + '/' + subject +'_run2drop.nii.gz'),
                           output_type = 'NIFTI_GZ',
                           t_min = 4,
                           t_size = 247),
           name = 'drop2')
drop2.run()


# In[20]:


motion_outliers2 = fsl.MotionOutliers(in_file = (func2 + '/' + subject +'_run2drop.nii.gz'),
                                          out_file = (func2 + '/' + subject +'_run2motionoutliers'))
motion_outliers2.run()


# In[21]:


func_strip2 = Node(fsl.BET(in_file = (func2 + '/' + subject +'_run2drop.nii.gz'),
                          out_file = (func2 + '/' + subject +'_run2brain.nii.gz'),
                          frac= 0.3,
                          functional = True), 
                  name = 'func_strip2')
func_strip2.run()

