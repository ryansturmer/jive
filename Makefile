get-bootstrap:
	python scripts/get_sdk.py

get-nodejs:
	cd deps; sudo npm install recess connect uglify-js jshint -g

bootstrap:
	cd deps/bootstrap; make bootstrap; cp -R bootstrap ../../static

environment: get-bootstrap get-nodejs 

