import os 
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

    WORKFLOW_TEMPLATE='''
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: {WORKFLOW_NAME}
spec:
  entrypoint: DAG-{WORKFLOW_NAME}
  templates:
{SCRIPTS}
  - name: DAG-{WORKFLOW_NAME}
    dag:
      tasks:
{DAGS}
'''
#  TODO -> Check about the image for each step
    SCRIPT_TEMPLATE = '''
  - name: {ID}
    script:
      image: debian:9.4 
      env:
{ENVS}
      command: [bash]
      source: |3+
{BASH}
'''
    DAG_TEMPLATE = '''
      - name: {TASK_NAME}
        dependencies: [{DEPENDENCIES}]
        template: {TEMPLATE_NAME}
'''

    VARIABLE_TEMPLATE = '''      - name: {NAME}
        value: "{VALUE}"
'''  # Numerical variables need to be encoded in double quotes (?)  

    def build(self, output, workflow_id=None):
        '''
        Build an argo file according to the cwl workflow
        '''
        print(self.workflow)
