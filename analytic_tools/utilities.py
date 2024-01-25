"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
from pathlib import Path
from typing import Dict, List


def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """

    # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    # Check if directory is of type str or Path, otherwise raise TypeError
    if not isinstance(dir, (str, Path)):
        raise TypeError(f"The provided path must be a str or Path object")

    # Will raise TypeError if path is not str or Path
    path = Path(dir)

    # Check if the given path exists
    # The exercise requested to raise a NotADirectoryError but it is usually used when a directory operation is requested on something which is not a directory
    # I think FileNotFoundError is more appropriate here as it is raised when a file or directory is requested but doesn’t exist.
    if not path.exists():
        raise NotADirectoryError("The provided path must exist")

    # Check if the given path is a directory otherwaise raise NotADirectoryError
    if not path.is_dir():
        raise NotADirectoryError("The provided path must be a directory")

    # Traverse the directory and find its contents
    contents = path.rglob('*')

    # Iterate over all Path objects present in the given directory and increment the appropriate dictionary counter
    for item in contents:
        if item.is_dir():
            res["subdirectories"] += 1
        elif item.is_file():              # elif and not simply else, as there could be other types of content in the directory (i.e. symbolic links, mount points, and sockets)
            res["files"] += 1
            if item.suffix == '.csv':
                res[".csv files"] += 1
            elif item.suffix == '.txt':
                res[".txt files"] += 1
            elif item.suffix == '.npy':
                res[".npy files"] += 1
            elif item.suffix == '.md':
                res[".md files"] += 1
            else:
                res["other files"] += 1

    return res


def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """

    # Check if directory is of type str or Path, otherwise raise TypeError
    if not isinstance(dir, (str, Path)):
        raise TypeError(f"The provided path must be a str or Path object")

    # Will raise TypeError if path is not str or Path
    path = Path(dir)

    # Check if the given path exists
    # The exercise requested to raise a NotADirectoryError but it is usually used when a directory operation is requested on something which is not a directory
    # I think FileNotFoundError is more appropriate here as it is raised when a file or directory is requested but doesn’t exist.
    if not path.exists():
        raise NotADirectoryError("The provided path must exist")

    # Check if the given path is a directory otherwaise raise NotADirectoryError
    if not path.is_dir():
        raise NotADirectoryError("The provided path must be a directory")

    # Check if contents is a dictionary otherwaise raise TypeError
    if type(contents) is not dict:
        raise TypeError(f"Expected a dictionary but received {type(contents)}")

    # Print the summary to the terminal
    # Display the path to the directory of interest
    print(f"Diagnostics for: {str(path)} ")
    print("----------------------------------------------")
    # Display each key in the dictionary and its corresponding value
    print(f"Number of files: {contents['files']}")
    print(f"Number of subdirectories: {contents['subdirectories']}")
    print(f"Number of .csv files: {contents['.csv files']}")
    print(f"Number of .txt files: {contents['.txt files']}")
    print(f"Number of .npy files: {contents['.npy files']}")
    print(f"Number of .md files: {contents['.md files']}")
    print(f"Number of other files: {contents['other files']}")
    print("----------------------------------------------")


def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """

    # Validate the path
    if not isinstance(dir, (str, Path)):
        raise TypeError(f"The provided path must be a str or Path object")
    # Will raise TypeError if path is not str or Path
    path = Path(dir)
    # Check path existence
    if not path.exists():
        raise NotADirectoryError(
            f"The provided path {str(path)} does not exist")
    # Check if path is a directory
    if not path.is_dir():
        raise NotADirectoryError(
            f"The provided path {str(path)} is not a directory")

    # Validate maxfiles
    if not isinstance(maxfiles, int):
        raise TypeError("Maxfiles must be an integer")
    if maxfiles < 1:
        raise ValueError("Maxfiles must be greater or equal to 1")

    # Declere recursive function to traverse the directory
    def recursive_display(current_path: [str | Path], indent: str = "") -> None:
        """Takes as input the current directory and how much indentation is required to display.
            Returns nothing.
        """
        # If the current path is a file, display it
        if current_path.is_file():
            print(f"{indent}- {current_path.name}")
        # If the current path is a directory, diaplay its name and files up to maxfiles
        elif current_path.is_dir():
            print(f"{indent}{current_path.stem}/")
            files = list(current_path.iterdir())
            displayed_files = min(maxfiles, len(files))
            for i in range(displayed_files):
                recursive_display(files[i], indent + "    ")
            if len(files) > maxfiles:
                print(f"{indent}    ...")

    # Display the root directory and start the recursive tree traversal
    print(f"{path.stem}/")
    for item in path.iterdir():
        recursive_display(item, "    ")


def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """

    # Do correct error handling first
    # Extract the filename from the .csv file and check if it is a valid greenhouse gas

    # Check if directory is of type str or Path, otherwise raise TypeError
    if not isinstance(path, (str, Path)):
        raise TypeError(f"The provided path must be a str or Path object")
    # Will raise TypeError if path is not str or Path
    path = Path(path)

    # Check if it is a absolute path

    # Check if path to .cvs flie, if not, raise ValueError
    if path.suffix != ".csv":
        # {print(path.suffix) if path.suffix else print('a dir')}
        raise ValueError(
            f"Expected path to a .cvs file, got something else instead")

    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]

    # Return if the file satisfies the [gas_formula].csv pattern
    return True if path.stem in gasses else False


def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """

    # Do correct error handling first

    # Check if dest_parent directory is of type str or Path, otherwise raise TypeError
    if not isinstance(dest_parent, (str, Path)):
        raise TypeError("The provided path must be a str or Path object")
    # Check if file_path directory is of type str or Path, otherwise raise TypeError
    if not isinstance(file_path, (str, Path)):
        raise TypeError("The provided path must be a str or Path object")

    # Will raise TypeError if path is not str or Path
    file_path = Path(file_path)
    # Will raise TypeError if path is not str or Path
    dest_parent = Path(dest_parent)

    # Check dest_parent exists and is a directory, otherwise raise NotADirectoryError
    if not dest_parent.is_dir() and not dest_parent.exists():
        raise NotADirectoryError(
            "Expected dest_parent to be a existing directory")

    # Check file_path is a path to a file, otherwise raise ValueError
    if not file_path.suffix:
        raise ValueError("Expected path to a file")
    # Check file_path is a path to a original .cvs file, otherwise raise ValueError
    if file_path.suffix != '.cvs' and not file_path.exists():
        # if not is_gas_csv(file_path):
        raise ValueError("Expected path to an original gas .cvs file")

    # If the input file is valid:
    # Derive the name of the directory, pattern: gas_[gas_formula] directory
    dest_name = f"gas_{file_path.stem}"

    # Derive its absolute path
    # Concatenate the dest_parent and the dest_name
    dest_path = dest_parent / dest_name

    # Check if the directory already exists, and create one of not
    if dest_path.exists():
        return dest_path
    # Should you have done something with .is_absolute() ?
    else:
        dest_path.mkdir()
        return dest_path


def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """
    # Check if directory is of type str or Path, otherwise raise TypeError
    if not isinstance(path, (str, Path)):
        raise TypeError("The provided path must be a str or Path object")
    # Will raise TypeError if path is not str or Path
    path = Path(path)

    # Check if there is filename and parent_name in the path, otherwise raise ValueError
    # or path.name != '': # verifica se è un file, ma non ne ho necessita)
    if path.parents[0].stem == '':
        raise ValueError("Missing filename or parent_name in the path")

    # new_base = path.parents[1] / Path(str(path.parents[0].stem) + "_" + str(path.stem))

    # New, merged, basename of the path, which will be the new filename
    if path.name:
        new_base = path.parents[0].stem + "_" + path.name
    else:
        new_base = path.parents[0].stem + "_" + path.stem
    return new_base


def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    # NOTE: This is an optional task, no points assigned. If you are skipping it, remove `raise NotImplementedError` in the function body
    ...
