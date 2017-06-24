import pip, os, time

for package in pip.get_installed_distributions():
     print "%s: %s" % (package, time.ctime(os.path.getctime(package.location)))
