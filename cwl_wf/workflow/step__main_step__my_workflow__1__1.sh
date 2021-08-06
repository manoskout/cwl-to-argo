. ${OBC_WORK_PATH}/aReFr_inputs.sh
. ${OBC_WORK_PATH}/obc_functions.sh
OBC_START=$(eval "declare")
:
# Insert the BASH commands for this step.
# You can use the variable ${OBC_WORK_PATH} as your working directory.
# Also read the Documentation about the REPORT and the PARALLEL commands.

echo "Hello from main_step"

OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=" | sort) <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=" | sort) > ${OBC_WORK_PATH}/step__main_step__my_workflow__1__1_VARS.sh
