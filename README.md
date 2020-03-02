# DataBaseConstruct

Repo to format unstructured infromation saved in a variety of file formats based on a pre-defined structure saved in a JSON under the name CANEVAS_STRUCT.json

**You need the structure saved in JSON format at the root of the repo**

Save your data in the /Data folder with any type of structure you like, the repo will walk through all nested directories

**Create the Conda environment:**

Pre-requisite: Miniconda3 or Anaconda
Conda will use the yml file to install all dependencies
```
conda env create
```

**Run:**

```
python3 main.py
```

If you want to create a table of your metadata to visualize in the shinyapp, add the following argument. The resulting output will be stored in the **Output** folder under metadata.csv

```
python3 main.py df
```
