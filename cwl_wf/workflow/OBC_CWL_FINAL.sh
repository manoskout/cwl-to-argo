. ${OBC_WORK_PATH}/step__main_step__my_workflow__1__1_VARS.sh
. ${OBC_WORK_PATH}/step__next_step__my_workflow__1__1_VARS.sh
. ${OBC_WORK_PATH}/step__main_step__my_workflow__1__2_VARS.sh
. ${OBC_WORK_PATH}/obc_functions.sh


OBC_REPORT_TGZ=${OBC_WORK_PATH}/${OBC_NICE_ID}.tgz

#echo "RUNNING: "
#echo "tar zcf ${OBC_REPORT_TGZ} -C ${OBC_WORK_PATH} ${OBC_NICE_ID}.html ${OBC_NICE_ID}/"

tar zcf ${OBC_REPORT_TGZ} -C ${OBC_WORK_PATH} ${OBC_NICE_ID}.html ${OBC_NICE_ID}/

echo "{}"
