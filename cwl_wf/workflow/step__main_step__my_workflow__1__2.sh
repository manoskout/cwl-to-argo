. ${OBC_WORK_PATH}/aReFr_inputs.sh
. ${OBC_WORK_PATH}/step__main_step__my_workflow__1__1_VARS.sh
. ${OBC_WORK_PATH}/step__next_step__my_workflow__1__1_VARS.sh
. ${OBC_WORK_PATH}/obc_functions.sh
OBC_START=$(eval "declare")

OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=" | sort) <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=" | sort) > ${OBC_WORK_PATH}/step__main_step__my_workflow__1__2_VARS.sh
