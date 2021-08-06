
class: CommandLineTool
cwlVersion: v1.0

baseCommand: ["bash", "step__next_step__my_workflow__1__1.sh"]

requirements:
   InitialWorkDirRequirement:
      listing:
         - class: File
           location: "step__next_step__my_workflow__1__1.sh"
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
   step__main_step__my_workflow__1__1:
      type: File
   OBC_TOOL_PATH: string
   OBC_DATA_PATH: string
   OBC_WORK_PATH: string



outputs: 
   step__next_step__my_workflow__1__1:
      type: stdout

