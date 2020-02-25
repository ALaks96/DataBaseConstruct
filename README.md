# DataBaseConstruct

Repo to format unstructured infromation saved in a variety of file formats based on a pre-defined structure saved in a JSON under the name CANEVAS_STRUCT.json

**You need the structure saved in json format at the root of the repo**

Save your data in the /Data folder with any type of structure you like, the repo will walk through all nested directories

**To run:**

```
python3 -m pip install requirements.txt

python3 main.py
```

If you want to create a table of your metadata to visualize in the shinyapp, add the following argument. The resulting output will be stored in the **Output** folder under metadata.csv

```
python3 main.py df
```
