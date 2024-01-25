""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    res_test = {
        "files": 10,
        "subdirectories": 5,
        ".csv files": 8,
        ".txt files": 0,
        ".npy files": 2,
        ".md files": 0,
        "other files": 0,
    }

    # Compare the dictionay obtained from get_diagnostics and the manually counted res_test
    # Establish if the test is passed or not, if not specify which elements are not correct
    res = get_diagnostics(example_config)
    assert res['files'] == res_test['files'], f"{res['files']} total files but expected {res_test['files']}"
    assert res['subdirectories'] == res_test[
        'subdirectories'], f"{res['subdirectories']} total subdirectories but expected {res_test['subdirectories']}"
    assert res['.csv files'] == res_test[
        '.csv files'], f"{res['.csv files']} .csv files but expected {res_test['.csv files']}"
    assert res['.txt files'] == res_test[
        '.txt files'], f"{res['.txt files']} .txt files but expected {res_test['.txt files']}"
    assert res['.npy files'] == res_test[
        '.npy files'], f"{res['.npy files']} .npy files but expected {res_test['.npy files']}"
    assert res['.md files'] == res_test[
        '.md files'], f"{res['.md files']} .md files but expected {res_test['.md files']}"
    assert res['other files'] == res_test[
        'other files'], f"{res['other files']} other files but expected {res_test['other files']}"


@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        # add more combinations of (exception, dir) here
        (NotADirectoryError, "Not_a_real_directory"),
        (NotADirectoryError, Path("/Non_existent_directory")),
        (TypeError, 12),
        (TypeError, True),
    ],
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """

    with pytest.raises(exception) as excinfo:
        get_diagnostics(dir)

    # Check if the correct exception was raised and assert accordingly
    if exception == NotADirectoryError:
        assert isinstance(
            excinfo.value, NotADirectoryError), "The exception should be a NotADirectoryError"
        assert str(excinfo.value) == "The provided path must be a directory" or str(
            excinfo.value) == "The provided path must exist", "The exception message does not match"
    elif exception == TypeError:
        assert isinstance(
            excinfo.value, TypeError), "The exception should be a TypeError"
        assert str(
            excinfo.value) == "The provided path must be a str or Path object", "The exception message does not match"


@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """
    assert is_gas_csv("ch4.csv") == False, "Not passed"
    assert is_gas_csv("h2o.csv") == False, "Not passed"
    assert is_gas_csv("co2.csv") == False, "Not passed"
    assert is_gas_csv("h3.csv") == False, "Not passed"
    assert is_gas_csv("gas.csv") == False, "Not passed"
    assert is_gas_csv("N2o.csv") == False, "Not passed"
    assert is_gas_csv("CO2.csv") == True, "Not passed"
    assert is_gas_csv("CH4.csv") == True, "Not passed"
    assert is_gas_csv("N2O.csv") == True, "Not passed"
    assert is_gas_csv("SF6.csv") == True, "Not passed"
    assert is_gas_csv("H2.csv") == True, "Not passed"


@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        # TODO: finish this task ?
        (ValueError, Path(__file__).parent.absolute()),
        (ValueError, Path("/home/yourusername/files/file2.doc")),
        (TypeError, 15),
        (TypeError, True),
        # add more combinations of (exception, path) here
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """
    with pytest.raises(exception) as excinfo:
        is_gas_csv(path)

    # #assert is_gas_csv("example.txt") == False, f"(Not Passed)"
    # #assert is_gas_csv("/home/yourusername/files/file2.doc") == False, f"(Not Passed)"
    # #assert is_gas_csv("/Projects/2023/repOrt.pdf") == False, f"(Not Passed)"
    # #assert is_gas_csv("/var/www/html/images/image.CsV") == False, f"(Not Passed)"
    # #assert is_gas_csv("/home/yourusername/files/file2.csv") == True, f"(Not Passed)"
    # assert is_gas_csv("/mnt/data/archive.csv") == True, f"(Not Passed)"
    # assert is_gas_csv("/files/myfile.csv") == True, f"(Not Passed)"
    # assert is_gas_csv("/home/yourUsername//mnt/data/archive/fIlE.csv") == True, f"(Not Passed)"
    # Check if the correct exception was raised and assert accordingly
    if exception == ValueError:
        assert isinstance(
            excinfo.value, ValueError), "The exception should be a ValueError"
        assert str(
            excinfo.value) == "Expected path to a .cvs file, got something else instead", "The exception message does not match"
    elif exception == TypeError:
        assert isinstance(
            excinfo.value, TypeError), "The exception should be a TypeError"
        assert str(
            excinfo.value) == "The provided path must be a str or Path object", "The exception message does not match"
    # typeerror


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
    dest_parent = example_config / "pollution_data_restructured" / "by_gas"
    dest_parent.mkdir(parents=True, exist_ok=True)

    by_src_dir = example_config / "pollution_data" / "by_src"
    argriculture_dir = by_src_dir / "src_agriculture"
    airtraffic_dir = by_src_dir / "src_airtraffic"
    oil_and_gass_dir = by_src_dir / "src_oil_and_gass"

    file_path = [argriculture_dir / "H2.csv", airtraffic_dir / "CO2.csv",
                 oil_and_gass_dir / "CH4.csv", oil_and_gass_dir / "CO2.csv"]
    f0 = get_dest_dir_from_csv_file(dest_parent, file_path[0])
    f1 = get_dest_dir_from_csv_file(dest_parent, file_path[1])
    f2 = get_dest_dir_from_csv_file(dest_parent, file_path[2])
    f3 = get_dest_dir_from_csv_file(dest_parent, file_path[3])
    assert f0 == dest_parent / \
        "gas_H2", f'Wrong destination directory: got {f0} instead of {dest_parent / "gas_H2"}'
    assert f1 == dest_parent / \
        "gas_CO2", f'Wrong destination directory: got {f1} instead of {dest_parent / "gas_CO2"}'
    assert f2 == dest_parent / \
        "gas_CH4", f'Wrong destination directory: got {f2} instead of {dest_parent / "gas_CH4"}'
    assert f3 == dest_parent / \
        "gas_CO2", f'Wrong destination directory: got {f3} instead of {dest_parent / "gas_CO2"}'


@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        (ValueError, Path(__file__).parent.absolute(), "foo.csv"),
        (ValueError, Path(__file__).parent.absolute(), 'foo'),
        (TypeError, 15, "foo.txt"),
        (TypeError, 15, 30),
        (TypeError, Path(__file__).parent.absolute(), 30),
        (TypeError, True, False),
        (NotADirectoryError, "foo/foofoo", "foo.txt"),
        (NotADirectoryError, "foo.txt", "foo.txt"),
        # add more combinations of (exception, dest_parent, file_path) here
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """
    with pytest.raises(exception) as excinfo:
        get_dest_dir_from_csv_file(dest_parent, file_path)

    if exception == ValueError:
        assert isinstance(
            excinfo.value, ValueError), "The exception should be a ValueError"
        assert "Expected path to a" in str(
            excinfo.value), "The exception message does not match"
    if exception == TypeError:
        assert isinstance(
            excinfo.value, TypeError), "The exception should be a TypeError"
        assert "The provided path must be a str or Path object" in str(
            excinfo.value), "The exception message does not match"
    if exception == NotADirectoryError:
        assert isinstance(
            excinfo.value, NotADirectoryError), "The exception should be a NotADirectoryError"
        assert str(
            excinfo.value) == "Expected dest_parent to be a existing directory", "The exception message does not match"


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """
    assert merge_parent_and_basename(
        '/User/.../assignment2/pollution_data/by_src/src_agriculture/CO2.csv') == 'src_agriculture_CO2.csv', "Wrong merged basename"
    assert merge_parent_and_basename(
        'some_dir/some_sub_dir') == 'some_dir_some_sub_dir', "Wrong merged basename"
    assert merge_parent_and_basename(
        'some_dir/some_file.txt') == 'some_dir_some_file.txt', "Wrong merged basename"


@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (TypeError, True),
        (ValueError, 'some_file.txt'),
        (ValueError, 'some_file'),
        # add more combinations of (exception, path) here
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    with pytest.raises(exception) as excinfo:
        merge_parent_and_basename(path)

    if exception == TypeError:
        assert isinstance(
            excinfo.value, TypeError), "The exception should be a TypeError"
        assert str(
            excinfo.value) == "The provided path must be a str or Path object", "The exception message does not match"
    if exception == ValueError:
        assert isinstance(
            excinfo.value, ValueError), "The exception should be a ValueError"
        assert str(
            excinfo.value) == "Missing filename or parent_name in the path", "The exception message does not match"
