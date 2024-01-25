"""This is the mane script orchestrating the restructuring and plotting of the content of the pollution_data directory.
"""

# Import necessary packages here
from pathlib import Path
import shutil
from analytic_tools.utilities import (
    display_diagnostics,
    display_directory_tree,
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)
from analytic_tools.plotting import (
    plot_pollution_data,
)


def restructure_pollution_data(pollution_dir: str | Path, dest_dir: str | Path) -> None:
    """This function searches the tree of pollution_data directory pointed to by pollution_dir for .csv files
        that satisfy the criteria described in the assignment. It then moves a renamed copy of these files to gas-specific
        sub-directories in dest_dir, which will be created based on the gasses present in pollution_data directory.

    Parameters:
        - pollution_dir (str or pathlib.Path) : The absolute path to pollution_data directory
        - dest_dir (str or pathlib.Path) : The absolute path to new directory where gas-specific subdirectories will
                                     be created, which must be pollution_data_restructured/by_gas

    Returns:
    None

    Pseudocode:
    1. Iterate through the contents of `pollution_dir`
    2. Find valid .csv files for gasses ([`[gas_formula].csv` files of correct gas types).
    3. Create/assign new directory to store them under `dest_dir` using `get_dest_dir_from_csv_file`
    4. Assign a new name using `merge_parent_and_basename` and copy the file to the new destination.
       If the file happens already to exist there, it should be overwritten.
    """

    # Check that pollution_dir and dest_dir are path-like objects
    if not isinstance(pollution_dir, (str, Path)) or not isinstance(dest_dir, (str, Path)):
        raise TypeError("The provided path must be a str or Path object")

    pollution_dir = Path(pollution_dir)
    dest_dir = Path(dest_dir)

    # Check that pollution_dir and dest_dir are existing directories
    if not pollution_dir.exists():
        raise NotADirectoryError("The provided path must exist")
    if not dest_dir.exists():
        raise NotADirectoryError("The provided path must exist")
    if not pollution_dir.is_dir() or not dest_dir.is_dir():
        raise NotADirectoryError("The provided path must be a directory")

    # Contents of pollution_data tree
    contents = pollution_dir.glob('**/*.csv')

    # Iterate through the contents of `pollution_dir
    for path in contents:
        # Find valid .csv files
        if is_gas_csv(path):
            # Create/assign new directory to store them using `get_dest_dir_from_csv_file`
            destination = get_dest_dir_from_csv_file(dest_dir, path)
            # Assign new name using `merge_parent_and_basename`
            new_file = destination / Path(merge_parent_and_basename(path))
            # Create new_file if new_file does not exists
            if not new_file.exists():
                new_file.touch()
            # Copy file to the new destination, overwrite it if it already exists
            shutil.copy(path, new_file)  # Replaces existing file


def analyze_pollution_data(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data and plot
       the statistics showing emissions of each gas as function of all the corresponding
       sources. The new structure and the plots are saved in a separate directory under work_dir

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the new directories will be created

    Returns:
    None

    Pseudocode:
    - Create pollution_data_restructured in work_dir
    - Populate it with a by_gas subdirectory
    - Make a call to restructure_pollution_data
    - Populate pollution_data_restructured with a subdirectory named figures
    - Make a call to plot_pollution_data
    """

    # Check that work_dir is a path-like object
    if not isinstance(work_dir, (str, Path)):
        raise TypeError("The provided path must be a str or Path object")

    work_dir = Path(work_dir)

    # Check that work_dir exists
    if not work_dir.exists() or not work_dir.is_dir():
        raise NotADirectoryError(
            "Work directory must be an existing directory")

    # Create pollution_data_restructured in work_dir
    pollution_dir = work_dir / "pollution_data"
    restructured_dir = work_dir / "pollution_data_restructured"
    if not pollution_dir.exists():
        pollution_dir.mkdir(parents=True)

    # Make a call to display_diagnostics and display_directory_tree
    display_diagnostics(pollution_dir, get_diagnostics(pollution_dir))
    display_directory_tree(pollution_dir, maxfiles=3)

    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_dir / "by_gas"
    if not by_gas_dir.exists():
        by_gas_dir.mkdir(parents=True)

    # Make a call to restructure_pollution_data
    restructure_pollution_data(pollution_dir, by_gas_dir)

    # Populate pollution_data_restructured with a sub folder named figures
    figures_dir = restructured_dir / "figures"
    if not figures_dir.exists():
        figures_dir.mkdir(parents=True)

    # Make a call to plot_pollution_data
    plot_pollution_data(by_gas_dir, figures_dir)


def analyze_pollution_data_tmp(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data in a temporary directory and create the figures
       showing emissions of each gas as function of all the corresponding
       sources. The new figures are saved in a real directory under work_dir.

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the figures will be saved

    Returns:
    None

    Pseudocode:
    - Create a temporary directory and copy pollution_data directory to it
    - Perform the same operations as in analyze_pollution_data
    - Copy (or directly save) the figures to a directory named `figures` under the original working directory pointed to by `work_dir`
    """

    # NOTE: This is a bonus task, if you are skipping it, remove `raise NotImplementedError()`
    # in the function body
    ...


if __name__ == "__main__":
    # Create a variable holding the path to your working directory
    work_dir = "C:/Users/crist/OneDrive/Desktop/IN3110/IN3110-cristila/assignment2"
    # Make a call to analyze_pollution_data
    analyze_pollution_data(work_dir)
