#!/bin/bash

home=`pwd`

cd static/js
coffee -cmw *.coffee &

cd $home
less_file="static/css/core.less";
lessc -x --verbose $less_file ${less_file%.*}.min.css;

while true; do
    files=`find -name "*.less"`;
    inotifywait -qe modify $files;
    lessc -x --verbose $less_file ${less_file%.*}.min.css;
done;
