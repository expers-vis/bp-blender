addon_dir="blender_addon"
zip_file="${addon_dir}.zip"
datetime=$(date +"%Y-%m-%d %T")

cd ..
rm -fv $zip_file 
zip $zip_file -r $addon_dir

echo "Finished on: ${datetime}"