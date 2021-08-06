import argparse
import os
import yaml
import tarfile

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
	os.mkdir(temp_folder)
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
			print(list_of_files, extracted_wf_path)
		else:
			raise CWL_ArgoParserException("File: {compressed_workflow_path} does not exist".format(compressed_workflow_path=compressed_workflow_path))		

		self.compressed_workflow_path=compressed_workflow_path
		self.parse_workflow()
		



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
