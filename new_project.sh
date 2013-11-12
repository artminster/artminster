#!/bin/bash

echo "Hello, "$USER".  This script will create the base ARTMINSTER Django project for you. This should only be done for NEW / EMPTY git projects."
echo "Enter the project name exactly as it appears in Git Hub: "
read projectname
echo

proj_path="${PWD}/${projectname}";

if [ ! -d "${proj_path}" ]; then
	mkdir "${projectname}";
	cd "${projectname}";
	git init;
	git remote add origin "git@github.com:artminster/${projectname}.git";
	git config remote.origin.push refs/heads/master:refs/heads/master;
	git submodule add git@github.com:artminster/artminster.git artminster;
	git submodule add git@github.com:artminster/django-allauth.git allauth;
	cp artminster/core/gitignore .gitignore;
	
	if [ ! -d "${proj_path}/${projectname}" ]; then
		cp -a artminster/example_project/. .;
		mv projectname/apps/projectname_profile projectname/apps/${projectname}_profile;
		mv projectname/apps/projectname/templates/projectname projectname/apps/PROJECTNAME/templates/${projectname};
		mv projectname/apps/projectname projectname/apps/${projectname};
		mv projectname ${projectname};
	
		sed_cmd="s/projectname/${projectname}/g";
		find . -type d \( -name artminster -o -name allauth -o -name .git \) -prune -o -name "*.py" -print -exec sed -i '' -e "$sed_cmd" {} +
		find . -type d \( -name artminster -o -name allauth -o -name .git \) -prune -o -name "*.sh" -print -exec sed -i '' -e "$sed_cmd" {} +
	
		git add .;
		git commit -am 'initial commit';
		git push origin master;
		
		virtualenv "${proj_path}/env";
		source "${proj_path}/env/bin/activate";
		pip install -r "${proj_path}/artminster/core/requirements.txt";
		pip install -r "${proj_path}/artminster/contrib/billing/requirements.txt";
		pip install -r "${proj_path}/allauth/requirements.txt";
		pip install -r "${proj_path}/requirements.txt";
		
		# Create the database
		# createuser -h -d localhost ${projectname}
		# createdb -h localhost -U ${projectname} "${projectname}";
		
		sh "${proj_path}/manage" syncdb --noinput;
		sh "${proj_path}/manage" migrate;
		sh "${proj_path}/manage" loaddata "${proj_path}/allauth/allauth.socialaccount.initial.json";
	fi
fi

echo "Project '${projectname}' successfully created. Others can now clone it locally. Goodbye :)"