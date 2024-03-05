# scripts/prebuild.py

import subprocess

# Install SDL development libraries
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "install", "-y", "libsdl2-dev"])

# Install other dependencies if needed
# subprocess.run(["apt-get", "install", "-y", "other-package"])

# Now, install the Python packages using Poetry
subprocess.run(["poetry", "install"])
