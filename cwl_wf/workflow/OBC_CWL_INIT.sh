for i in "$@"
do
case $i in
  *)
  ;;
esac
done

touch ${OBC_WORK_PATH}/aReFr_inputs.sh




if [ -n "${OBC_WORK_PATH}" ] ; then
    export OBC_REPORT_PATH=${OBC_WORK_PATH}/${OBC_NICE_ID}.html
    export OBC_REPORT_DIR=${OBC_WORK_PATH}/${OBC_NICE_ID}
    mkdir -p ${OBC_REPORT_DIR}
    echo "OBC: Report filename: ${OBC_REPORT_PATH}"

cat > ${OBC_REPORT_PATH} << OBCENDOFFILE
<!DOCTYPE html>
<html lang="en">
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   </head>
   <body>
   <p>
   OpenBio Server: <a href="${OBC_SERVER}">${OBC_SERVER}</a> <br>
   Workflow: <a href="${OBC_SERVER}/w/${OBC_WORKFLOW_NAME}/${OBC_WORKFLOW_EDIT}">${OBC_WORKFLOW_NAME}/${OBC_WORKFLOW_EDIT}</a> <br>

   <p>
   <h3>Intermediate Variables:</h3>
   <ul>
      <!-- {{INTERMEDIATE_VARIABLE}} -->
   </ul>

   <p>
   <h3>Output Variables:</h3>
   <ul>
      <!-- {{OUTPUT_VARIABLE}} -->
   </ul>

   </body>
</html>
OBCENDOFFILE
fi



cat > ${OBC_WORK_PATH}/obc_functions.sh << 'OBCENDOFFILE'



export OBC_REPORT_PATH=${OBC_WORK_PATH}/${OBC_NICE_ID}.html
export OBC_REPORT_DIR=${OBC_WORK_PATH}/${OBC_NICE_ID}

function REPORT() {
    if [ -n "${OBC_WORK_PATH}" ] ; then
        local VAR=$1
        local TIMENOW=$(date)
        local WHOCALLEDME=$(caller 0 | awk '{print $2}')

        if [ -z $3 ] ; then
            local TAG=INTERMEDIATE_VARIABLE
        else
            local TAG=$3
        fi

        if [ ${TAG} == "INTERMEDIATE_VARIABLE" ] ; then
            local EXTRA="${TIMENOW}. Called from: ${WHOCALLEDME}"
        else
            local EXTRA=""
        fi

        local FILEKIND=$(file "${2}")
        # echo "OBC: FILE RESULT ${FILEKIND}"
        if [[ $FILEKIND == *"PNG image data"* ]]; then
           local NEWFILENAME=${OBC_REPORT_DIR}/$(basename ${2})
           local LOCALFILENAME=${OBC_NICE_ID}/$(basename ${2})
           cp ${2} ${NEWFILENAME}
           local HTML="<li>${EXTRA} ${VAR}: <br><img src=\"${LOCALFILENAME}\"></li>\\\\n      <!-- {{${TAG}}} -->\\\\n"
        elif [[ $FILEKIND == *"PDF document"* ]]; then
           local NEWFILENAME=${OBC_REPORT_DIR}/$(basename ${2})
           local LOCALFILENAME=${OBC_NICE_ID}/$(basename ${2})
           cp ${2} ${NEWFILENAME}
           local HTML="<li>${EXTRA} ${VAR}: <br><a href=\"${LOCALFILENAME}\">${LOCALFILENAME}</a></li>\\\\n      <!-- {{${TAG}}} -->\\\\n"
        else
           local VALUE=$(echo "${2}" | sed 's/&/\\\&amp;/g; s/</\\\&lt;/g; s/>/\\\&gt;/g; s/"/\\\&quot;/g; s/'"'"'/\\\&#39;/g')
           local HTML="<li>${EXTRA} ${VAR}=${VALUE}</li>\\\\n      <!-- {{${TAG}}} -->\\\\n"
        fi

        sed -i -e "s|<\!-- {{${TAG}}} -->|${HTML}|" ${OBC_REPORT_PATH}
        sed 's/\\n/\
/g' ${OBC_REPORT_PATH} > ${OBC_REPORT_PATH}.tmp
        mv ${OBC_REPORT_PATH}.tmp ${OBC_REPORT_PATH}
    fi
}



OBCENDOFFILE

