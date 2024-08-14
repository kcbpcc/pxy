[app]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (e.g. org.test)
package.domain = org.example

# (str) Path to the main .py file
# Make sure this matches your file name
main.py = ztestskc.py

# (str) Application version
# You can set this to the version of your app
version = 1.0

# (list) List of inclusions using glob patterns.
include_exts = py,png,jpg,kv,atlas

# (list) List of source files to include in the package.
source.include_patterns = ztestskc.py

# (list) List of requirements to install with the app
requirements = python3,kivy
