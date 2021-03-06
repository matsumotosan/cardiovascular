
test_name="coronarytree.stl"
test_name="remove-faces.vtp"

python=python
python=python3

## Write a 1D solver input file.
#
# Centerlines are read from a file.
# 
if [ $test_name  == "coronarytree.stl" ]; then
    surface_file=coronarytree.stl
    ${python} extract_faces.py \
        --surface-file ${surface_file} \
        --use-feature-angle true \
        --angle 60.0               

elif [ $test_name  == "remove-faces.vtp" ]; then
    surface_file=remove-faces.vtp
    ${python} extract_faces.py \
        --surface-file ${surface_file} 

fi



