
class: CommandLineTool
cwlVersion: v1.0

baseCommand: ["bash", "OBC_CWL_INIT.sh"]

requirements:
   InitialWorkDirRequirement:
      listing:
         - class: File
           location: "OBC_CWL_INIT.sh"
   InlineJavascriptRequirement: {} 
   EnvVarRequirement:
       envDef:
         OBC_TOOL_PATH: $(inputs.OBC_TOOL_PATH)
         OBC_DATA_PATH: $(inputs.OBC_DATA_PATH)
         OBC_WORK_PATH: $(inputs.OBC_WORK_PATH)
         OBC_WORKFLOW_NAME: "my_workflow"
         OBC_WORKFLOW_EDIT: "1"
         OBC_NICE_ID: "my_workflow__1"

inputs: 
   OBC_TOOL_PATH: string
   OBC_DATA_PATH: string
   OBC_WORK_PATH: string



outputs: 
   OBC_CWL_INIT:
      type: stdout

