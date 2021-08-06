#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs: 
   OBC_TOOL_PATH: string
   OBC_DATA_PATH: string
   OBC_WORK_PATH: string


outputs: 
   OBC_FINAL_REPORT:
      type: File
      outputSource: OBC_CWL_FINAL/OBC_FINAL_REPORT



steps:
   step__main_step__my_workflow__1__1:
      run: step__main_step__my_workflow__1__1.cwl
      in: 
         OBC_TOOL_PATH: OBC_TOOL_PATH
         OBC_DATA_PATH: OBC_DATA_PATH
         OBC_WORK_PATH: OBC_WORK_PATH
         OBC_CWL_INIT: OBC_CWL_INIT/OBC_CWL_INIT

      out: [step__main_step__my_workflow__1__1]


   step__next_step__my_workflow__1__1:
      run: step__next_step__my_workflow__1__1.cwl
      in: 
         OBC_TOOL_PATH: OBC_TOOL_PATH
         OBC_DATA_PATH: OBC_DATA_PATH
         OBC_WORK_PATH: OBC_WORK_PATH
         step__main_step__my_workflow__1__1: step__main_step__my_workflow__1__1/step__main_step__my_workflow__1__1

      out: [step__next_step__my_workflow__1__1]


   OBC_CWL_INIT:
      run: OBC_CWL_INIT.cwl
      in: 
         OBC_TOOL_PATH: OBC_TOOL_PATH
         OBC_DATA_PATH: OBC_DATA_PATH
         OBC_WORK_PATH: OBC_WORK_PATH

      out: [OBC_CWL_INIT]


   step__main_step__my_workflow__1__2:
      run: step__main_step__my_workflow__1__2.cwl
      in: 
         OBC_TOOL_PATH: OBC_TOOL_PATH
         OBC_DATA_PATH: OBC_DATA_PATH
         OBC_WORK_PATH: OBC_WORK_PATH
         step__next_step__my_workflow__1__1: step__next_step__my_workflow__1__1/step__next_step__my_workflow__1__1

      out: [step__main_step__my_workflow__1__2]


   OBC_CWL_FINAL:
      run: OBC_CWL_FINAL.cwl
      in: 
         OBC_TOOL_PATH: OBC_TOOL_PATH
         OBC_DATA_PATH: OBC_DATA_PATH
         OBC_WORK_PATH: OBC_WORK_PATH
         step__main_step__my_workflow__1__2: step__main_step__my_workflow__1__2/step__main_step__my_workflow__1__2

      out: [OBC_FINAL_REPORT]



