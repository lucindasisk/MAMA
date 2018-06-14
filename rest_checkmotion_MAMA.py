
# coding: utf-8

# In[1]:

#import packages
from os import listdir, path
from nipype.interfaces.io import DataSink, SelectFiles
from nipype.interfaces.utility import IdentityInterface
from nipype.pipeline.engine import Node, Workflow
from nipype.interfaces.fsl.preprocess import MCFLIRT
from nipype.interfaces.fsl import PlotMotionParams

# Set study variables
studyhome = '/Volumes/iang/active/BABIES/'
subject_data = studyhome + '/BABIES_MAMA' #path to folder containing individual subject folders
output_dir = studyhome + 'BABIES_MAMA/rest_motion' #path to new folder where motion plot will be exported
workflow_dir = studyhome + '/BABIES_rest/workflows'
subjects_list = ['065-MAMA', '075-MAMA', '076-MAMA', '087-MAMA', '088-MAMA'] #[f for f in listdir(subject_data) if not f.startswith('.')] #skips hidden files

proc_cores = 4 # number of cores of processing for the workflows

for file in subjects_list:
   print (file)


# In[2]:

## File handling Nodes

# Identity node- select subjects and pe
infosource = Node(IdentityInterface(fields=['subject_id']),
                     name="infosource")
infosource.iterables = [('subject_id', subjects_list)]

# Data grabber- select fMRI
templates = {'func': subject_data + '/{subject_id}/rest/rest.nii'}

selectfiles = Node(SelectFiles(templates), name='selectfiles')

# Datasink- where our select outputs will go
datasink = Node(DataSink(), name ='datasink')
datasink.inputs.base_directory = output_dir
datasink.inputs.container = output_dir


# In[3]:

#Node to check motion
motion_correct = Node(MCFLIRT(save_plots = True,
                              mean_vol = True),
                      name = 'motion_correct')

plot_motion = Node(PlotMotionParams(in_source = "fsl",
                                    plot_type = "displacement"),
                   name = 'plot_motion')


# In[4]:

#Define workflow

# workflowname.connect([(node1,node2,[('node1output','node2input')]),
#                       (node2,node3,[('node2output','node3input')])
#                     ])
checkmotion_wf = Workflow(name = 'checkmotion_wf')

checkmotion_wf.connect([(infosource, selectfiles,[('subject_id','subject_id')]),
                        (selectfiles, motion_correct, [('func', 'in_file')]),
                        (motion_correct, plot_motion, [('par_file','in_file')]),

                       (plot_motion, datasink, [('out_file', 'motion_plot')])])


# In[5]:

#Run workflow
checkmotion_wf.base_dir = workflow_dir
checkmotion_wf.run('MultiProc', plugin_args={'n_procs': proc_cores})


# In[ ]:
