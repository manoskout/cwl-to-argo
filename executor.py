import argparse
import os
import yaml
from yaml.loader import SafeLoader
import tarfile
import shutil
import logging
from ArgoExecutor import ArgoExecutor
logging.basicConfig(level=logging.DEBUG)

def log_info(message):
    '''
    '''
    logging.info(message)

class CWL_ArgoParserException(Exception):
	'''
	Custom exception
	'''
	pass
def extract_file(file_path, temp_folder):
	'''
	Extract a tar.gz file into a specific directory
	Returns a list of extracted files and the folder that exists
	'''
	workflow_tar = tarfile.open(file_path)
	try:
		os.mkdir(temp_folder)
	except FileExistsError:
		# TODO --> Delete this exception the file should be removed if the parsing have been achieved
		print("File Exists")
	wf_path= os.path.join(os.getcwd(),temp_folder)
	workflow_tar.extractall(temp_folder)
	wf_list=os.listdir(temp_folder)
	return wf_list, wf_path
	
class Workflow:
	'''
	'''
	def __init__(self,compressed_workflow_path=None):
		'''
		all related workflow files (i.e. steps, variables etc)
		workflow_path: The tar.gz file that contains all of the workflow files
		wf_inputs: the file that contains all the inputs of the workflow
		'''
		if os.path.exists(compressed_workflow_path):
			print("File found")
			list_of_files, extracted_wf_path = extract_file(compressed_workflow_path, "tmp_folder")
			# print(list_of_files, extracted_wf_path)
		else:
			raise CWL_ArgoParserException("File: {compressed_workflow_path} does not exist".format(compressed_workflow_path=compressed_workflow_path))		

		self.compressed_workflow_path=compressed_workflow_path
		self.extracted_wf_path=extracted_wf_path
		self.workflow_files=list_of_files
		self.parse_workflow()

	def get_workflow_path(self):
		'''
		Return the full path of workflow
		'''
		return self.extracted_wf_path

	def get_steps(self):
		'''
		Return the steps of the workflow if the key "test" exists into the CWL file
		'''
		try:
			return list(self.cwl_wf['steps'].keys())
		except KeyError:
			print("Error 01: steps are not defined into the workflow.cwl")
			return []
	def get_step_path(self):
		'''
		Return a specific directory of the workflow
		'''

	def get_step_dependencies(self):
		'''
		Return a dict that the key is the step that depends on its value.
		Also there are two more keys (main,final) that are the first and the final respectively
		'''
		step_dependencies=[]
		# Get all the dependenies of each step
		for step in self.wf_steps:
			for dep in list(self.cwl_wf["steps"][step]["in"].keys()):
				if dep in self.wf_steps:
					step_dependencies.append((dep,step))
		return step_dependencies

	def is_cmd_tool(self,step):
		'''
		Checks if the step is a CommandLineTool
		more info : https://www.commonwl.org/v1.0/CommandLineTool.html
		'''
		return True if step=="CommandLineTool" else False


	def get_wf_file_path(self,step):
		'''
		Returns the full file path of cwl steps file 
		'''
		print(step)
		return os.path.join(self.extracted_wf_path,self.cwl_wf["steps"][step]['run'])
	
	def get_wf_bash_files(self,step):
		'''
		returns the list of files that a specific step contains 
		TODO: In cwl we are able to pass multiple bash files 
		check how we could get all the bash file from the listing arguement 
		'''
		list_of_files = self.parse_step(step)['requirements']['InitialWorkDirRequirement']['listing']
		return list_of_files
	def parse_step(self,step):
		'''
		'''
		with open(self.get_wf_file_path(step)) as f:
			cwl_file_step = yaml.load(f, Loader=SafeLoader)
		# print(cwl_file_step)
		return cwl_file_step

	def get_wf_info(self):
		'''
		'''
		log_info("Workflow inputs: ")
		log_info(self.wf_inputs)
		log_info("Workflow outputs:")
		log_info(self.wf_outputs)
		log_info("Workflow dependencies: ")
		log_info(self.step_dependencies)
		# for step in self.step_dependencies:
			# log_info(self.get_wf_file_path(step))
		# print(self.cwl_wf)

	def get_step_bash_contents(self,step,step_files):
		'''
		step: a string which is a name of the step
		step_files: a list of dicts that contains all files of a specific step
		Get tha bash file to pass it into the argo yaml file
		In our case we have just one file
		TODO -> Check how we can work in multiple files in argo workflow !
		Return a list that each line is a value of a list
		'''
		
		if not self.is_cmd_tool(self.parse_step(step)["class"]):
			raise CWL_ArgoParserException("Step {step} is not contains bash file".format(step=step))
		for step_file in step_files:
			if step_file['class'] == 'File':
				# print(os.path.join(self.extracted_wf_path,step_file['location']))
				if os.path.exists(os.path.join(self.extracted_wf_path,step_file['location'])):
					with open(os.path.join(self.extracted_wf_path,step_file['location']),'r') as f:
						bash_content=f.read()
		# else:
			# raise CWL_ArgoParserException("File {step} does not extists".format(step=step))
		# print(bash_content)
		return bash_content

	def get_step_inputs(self,step):
		'''
		Return a dict that contain the inputs and their types of the cwl workflow
		'''
		return self.parse_step(step)['inputs']
	def get_step_outputs(self,step):
		'''
		Return a dict that contain the outputs and their types of the cwl workflow
		'''
		return self.parse_step('OBC_CWL_INIT')['outputs']

	def parse_workflow(self):
		'''
		'''
		# Open the file and load the file
		if "workflow.cwl" in self.workflow_files:
			workflow_file_path = os.path.join(self.extracted_wf_path,"workflow.cwl")
		with open(workflow_file_path) as f:
			self.cwl_wf = yaml.load(f, Loader=SafeLoader)
		self.wf_inputs=self.cwl_wf["inputs"]
		self.wf_outputs=self.cwl_wf["outputs"]
		self.wf_steps = self.get_steps()
		self.step_dependencies = self.get_step_dependencies()
		# self.get_wf_info()
		# print(self.parse_step('OBC_CWL_INIT')['inputs'])



if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='CWL to Argo workflow parser'
		)
	parser.add_argument(
		'-W', 
		'--workflow', 
		dest='workflow_filename', 
		help='CWL workflow file', 
		required=True
		)

	parser.add_argument(
		'-O', 
		'--output',
		dest='output', 
		help="The output filename [Default : workflow.yaml]", 
		default='workflow'
		)
	
	args = parser.parse_args()
	print('Given inputs: \n\tworkflow_filename:{workflow_name} \n\toutput:{output}'.format(workflow_name=args.workflow_filename, output=args.output))
	workflow = Workflow(compressed_workflow_path=args.workflow_filename)
	# Delete the extracted workflow path
	e = ArgoExecutor(workflow)
	output= e.build()
	# print(output)
	shutil.rmtree(workflow.get_workflow_path())