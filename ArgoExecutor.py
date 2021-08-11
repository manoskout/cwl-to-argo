import os 
import sys
import ruamel.yaml
# Use literal of folded scalars i.e. source: |
folded = ruamel.yaml.scalarstring.FoldedScalarString
literal = ruamel.yaml.scalarstring.LiteralScalarString
def str_presenter(dumper, data):
  if len(data.splitlines()) > 1:  # check for multiline string
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml = ruamel.yaml.YAML()

class ExecutorException(Exception):
	'''
	Custom exception
	'''
	pass
class BaseExecutor():
    def __init__(self,workflow):
        '''
        '''
        self.workflow=workflow

class ArgoExecutor(BaseExecutor):
    '''
    https://argoproj.github.io/

    Documentation: 
    https://github.com/argoproj/argo-workflows/blob/master/examples/README.md
    '''

    ARGO_ROOT = os.getcwd()

    def yaml_workflow_builder(self,workflow_name):#,templates=None,tasks=None):
        '''
        A Funtion that return a dict with containing all necessary definitions
        of an argo workflow
        '''
        # if templates is None:
        #     raise ExecutorException("Templates not found")
        # if task is None:
        #     raise ExecutorException("Tasks not found")
            
        return {
            "apiVersion":"argoproj.io/v1alpa1",
            "kind":"Workflow",
            "metadata": {"generateName":workflow_name},
            "spec": {
                "entrypoint": f"DAG-{workflow_name}",   
            }
        }

    def set_workflow_templates(self,name,params,bash,outputs):
        '''
        name: the name of the template
        params: the parameters of the workflow (inputs)
        bash: the bash file of the step
        outputs: the output of the step
        '''
        return {
            "name":name,
            "inputs":{
                "parameters":params
            },
            "script":{
                "image": "debian:9.4",
                "command":'[bash]', # Check how to show that [bash] in workflow rather than '[bash]'
                "source": literal(bash),
            },
            "outputs": outputs
        }
    
    def set_task(self,name,template_name,dep,params):
        '''
        template_name: the name of the template that used in this specific step
        dep: the dependencies of the step
        set the current task and return a dict that will be parsed into yaml file
        '''
        #  - name: step-A 
        # template: step-template-A
        # arguments:
        #   parameters:
        #   - name: template-param-1
        #     value: "{{workflow.parameters.workflow-param-1}}"

        if dep==None:
            return {
            'name': name,
            'template': template_name,
            'arguments':{
                'parameters':[params]
            }
        }
        return {
            'name': name,
            'dependencies': dep,
            'template': template_name,
            'arguments':{
                'parameters':[params]
            } 
        }



    def build(self, workflow_id=None):
        '''
        Build an argo file according to the cwl workflow
        '''
        print(self.workflow.get_wf_info())
        # print(self.workflow.get_step_bash_contents(step,self.workflow.get_wf_bash_files(step)))
        # print(self.workflow.parse_steps(step))
        argo_workflow= self.yaml_workflow_builder(workflow_name='test')
        # argo_workflow['spec']['dag']={"test":"test"}
        # print(argo_workflow)
        yaml.dump(argo_workflow,sys.stdout)    
       
        for index,nodes in enumerate(self.workflow.get_step_dependencies()):
            
            step=dep[0]
            next_step=dep[1]
            print("{step}, {next_step}".format(step=step,next_step=next_step))
        return 0
