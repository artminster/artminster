#!/bin/bash

echo "Hello, "$USER".  This script will clone a ARTMINSTER project to your machine, and set it up locally."
echo "Enter the project name exactly as it appears in Spring Loops: "
read projectname
echo

proj_path="${PWD}/${projectname}";

if [ ! -d "${proj_path}" ]; then
	cd "${projectname}";
	git clone --recursive ssh://sls@slsapp.com:1234/artminster/${projectname}.git;
	
	virtualenv "${proj_path}/env";
	source "${proj_path}/env/bin/activate";
	sudo pip install -r "${proj_path}/artminster/core/requirements.txt";
	sudo pip install -r "${proj_path}/artminster/contrib/billing/requirements.txt";
	sudo pip install -r "${proj_path}/allauth/requirements.txt";
	sudo pip install -r "${proj_path}/requirements.txt";
	
	# Create the database
	createdb -h localhost -U postgres "${projectname}";
	
	sh "${proj_path}/manage" syncdb --noinput;
	sh "${proj_path}/manage" migrate;
	sh "${proj_path}/manage" loaddata "${proj_path}/allauth/allauth.socialaccount.initial.json";
fi

echo "Project '${projectname}' successfully cloned and setup locally. Goodbye :)"