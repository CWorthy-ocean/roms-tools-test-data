# roms-tools-test-data

Data repository for small versions of source data files for roms-tools automated testing. These files get downloaded and cached when roms-tools runs its test suite. This avoids needing to have access to the full (often large) source datasets during testing.

**Updating process:**
Once the file is updated in a `roms-tools-test-data` branch, the registry needs to be updated in ROMS-Tools to test the data. 

The file's hash in its respective registry needs to be updated in `roms_tools/datasets/download.py`.

Below is an example off one method to get a new hash:
```
import hashlib, urllib.request
base="https://github.com/CWorthy-ocean/roms-tools-test-data/raw/main/"
name = 'WOA_2018_quarterDeg_coarsened.nc'
h = hashlib.sha256()
with urllib.request.urlopen(base + name) as r:
     for chunk in iter(lambda: r.read(1 << 20), b""):
         h.update(chunk)
print(f'"{name}": "sha256:{h.hexdigest()}",')

# It prints this:
# "WOA_2018_quarterDeg_coarsened.nc": "sha256:673ce3c3a98bb386ccd899dbc23eeedf7d9a665b68ea52c96fd69829a4b929a7",         
```

To test the updated `roms-tools-test-data branch`, the `base_url` for the updated registry in `roms_tools/datasets/download.py` needs to match the branch before running `pytest`.

Be sure to change the `base_url` back to the `main` branch before merging the ROMS-Tools PR, assuming the `roms-tools-test-data` branch will be merged into `main`. 
