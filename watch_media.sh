#!/bin/bash

home=`pwd`

cd static/js
coffee -cmw $home/static &

cd $home
less_file="static/css/core.less";
lessc -ru -x --verbose $less_file ${less_file%.*}.min.css;

while true; do
    files=`find -name "*.less"`;
    inotifywait -qe modify $files;
    lessc -ru -x --verbose $less_file ${less_file%.*}.min.css;
done;
