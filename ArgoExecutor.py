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

    def yaml_workflow_builder(self,workflow_name,templates=None,tasks=None):
        '''
        A Funtion that return a dict with containing all necessary definitions
        of an argo workflow
        '''
        if templates is None:
            raise ExecutorException("Templates not found")
        if task is None:
            raise ExecutorException("Tasks not found")
            
        return {
            "apiVersion":"argoproj.io/v1alpa1",
            "kind":"Workflow",
            "metadata": {"generateName":workflow_name},
            "spec": {
                "entrypoint": f"DAG-{workflow_name}",   
                "templates": [templates],
                "dag":{
                    "tasks":[tasks]
                }
            }
        }

    def set_workflow_templates(self,id,bash,outputs):
        return {
            "name":id,
            "script":{
                "image": "debian:9.4",
                "command":'[bash]', # Check how to show that [bash] in workflow rather than '[bash]'
                "source": literal(bash),
            },
            outputs: outputs
        }
    
    def set_task(self,name,source):
        return {
            'name': name,
            'template': {
                'image': 'debian:9.4', 
                'command': "[bash]", 
                'source':literal(source), 
            }
        }



    def build(self, workflow_id=None):
        '''
        Build an argo file according to the cwl workflow
        '''
        print(self.workflow.get_wf_info())
        return 0
