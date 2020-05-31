import os


DATASET_PATH = "absolute_path"

for i, (dirpath, dirnames, filenames) in enumerate(os.walk(DATASET_PATH)):
    if dirpath is not DATASET_PATH:
        semantic_label = dirpath.split("/")[-1]
        print("\nProcessing: {}".format(semantic_label))

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.getsize(file_path) != 2646044:
                print(file_path)
            else:
                print("验证通过 / No error")
