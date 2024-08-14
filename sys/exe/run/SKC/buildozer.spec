[app]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (e.g. org.test)
package.domain = org.example

# (str) Path to the main .py file
main.py = ztestskc.py

# (str) Application version
version = 1.0

# (list) List of inclusions using glob patterns.
include_exts = py,png,jpg,kv,atlas

# (list) List of source files to include in the package.
source.include_patterns = ztestskc.py

# (str) Directory where the source files are located
source.dir = .

# (list) List of requirements to install with the app
requirements = python3,kivy
