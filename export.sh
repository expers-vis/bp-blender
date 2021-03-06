addon_name="recorder"
addon_dir="blender_addon"
zip_file="${addon_name}_addon.zip"
timestamp=$(date +"%Y-%m-%d %T")

cd ..
rm -fv $zip_file 
zip $zip_file -r $addon_dir -x '*.git*' -x '*PoCs*'

echo "Finished on: ${timestamp}"