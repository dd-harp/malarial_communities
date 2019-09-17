.DEFAULT_GOAL: Africa.shp

Africa_SHP.zip:
	curl -o $@ http://www.maplibrary.org/library/stacks/Africa/Africa_SHP.zip

Africa.shp: Africa_SHP.zip
	unzip $<
