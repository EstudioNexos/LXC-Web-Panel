all: static-build scanpkg

static-build:
	python rst2html.py ../README.rst > site-src/pages/README.html
	python rst2html.py ../api.rst > site-src/pages/API.html
	cd ..; git log --pretty=format:'%ci;%h;%s' | grep -v Merge > gh-pages/changelog.csv
	md5sum debian/*.deb | sed 's/debian\///g' - > md5sum
	#build after any site-src modification
	cd site-src; cactus build; cd ..
	# prepend complete URI to support sub-directory
	#find . -name '*.html' -exec sed -i 's/\.\/posts/http:\/\/claudyus\.github\.io\/LXC-Web-Panel\/posts/g' \{\} \;
	##find . -name '*.html' -exec sed -i 's/href=\"\//href=\"http:\/\/claudyus.github.io\/LXC-Web-Panel\//g' \{\} \;
	#find . -name '*.html' -exec sed -i 's/src=\"\//src=\"http:\/\/claudyus.github.io\/LXC-Web-Panel\//g' \{\} \;
	cp -r site-src/.build/* .

scanpkg:
	dpkg-scanpackages debian/ /dev/null | gzip -9c > debian/Packages.gz
	dpkg-scanpackages debian-testing/ /dev/null | gzip -9c > debian-testing/Packages.gz
	reprepro includedeb precise debian/$(DEB_PKG)
	reprepro includedeb precise debian/$(DEB_PKG)

serve: all
	cd site-src/; cactus serve
