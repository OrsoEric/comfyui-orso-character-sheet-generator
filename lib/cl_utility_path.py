"""
Utility functions for handling file paths in a cross-platform manner.

This module provides utilities for converting lists of path components
into properly formatted OS-specific paths.
"""

import logging
from pathlib import Path
from typing import List, Tuple

def convert_to_path(
    i_ls_path_components: List[str] | Path
) -> Path:
    """
    Convert a list of path components into a cross-platform Path object.

    This function takes a list of string path components and converts them
    into a properly formatted Path object that is compatible with the
    operating system's path conventions.

    Parameters
    ----------
    i_ls_path_components : List[str]
        A list of path components to be joined into a single path.
        Each component should be a string representing a part of the path.

    Returns
    -------
    Path
        A pathlib.Path object representing the joined path components.

    Examples
    --------
    >>> convert_to_path(["src", "data", "file.json"])
    PosixPath('src/data/file.json')  # On Unix-like systems

    >>> convert_to_path(["C:", "Users", "Documents", "file.txt"])
    WindowsPath('C:\\\\Users\\\\Documents\\\\file.txt')  # On Windows
    """
    
    if type(i_ls_path_components) is type(list()):
        # Create a Path object from the list of components
        cl_path: Path = Path(*i_ls_path_components)
    else:
        cl_path = i_ls_path_components
    
    return cl_path

import logging
from pathlib import Path
from typing import Dict, List, Tuple

def find_file_pair_image_json(i_s_folder : str) -> List[Tuple[Path, Path]]:
    """
    Locate matching image / JSON file pairs in a directory.

    The function scans *i_s_folder* for files that share the same stem
    (filename without extension).  If a JSON file is found together with an
    image file (.jpg or .png) it returns the resolved paths of both files as
    a tuple.  Only one image per JSON is returned – the function prefers
    JPEG over PNG if both are present.

    Parameters:
        i_s_folder (str): The absolute or relative path to a directory that
                          contains image and JSON files.

    Returns:
        List[Tuple[Path, Path]]: A list of tuples where each tuple consists of
                                 an image :class:`pathlib.Path` object followed by
                                 the corresponding JSON :class:`pathlib.Path`
                                 object.  The order of tuples is the same as the
                                 iteration order of :func:`pathlib.Path.iterdir`.

    Raises:
        FileNotFoundError: If *i_s_folder* does not exist.
        NotADirectoryError: If *i_s_folder* is not a directory.
    """
    # ------------------------------------------------------------------
    # 1. Resolve and validate the supplied folder path
    # ------------------------------------------------------------------
    cl_path : Path = Path(i_s_folder)

    if not cl_path.exists():
        raise FileNotFoundError(f"Folder not found: {cl_path}")

    if not cl_path.is_dir():
        raise NotADirectoryError(f"Provided path is not a directory: {cl_path}")

    # ------------------------------------------------------------------
    # 2. Build a mapping from file stems to their image/JSON counterparts
    # ------------------------------------------------------------------
    d_stem_to_files : Dict[str, Dict[str, Path | None]] = dict()

    for cl_file_path in cl_path.iterdir():
        if not cl_file_path.is_file():
            continue

        s_ext_lower : str = cl_file_path.suffix.lower()
        logging.debug(f"Inspecting {cl_file_path} (extension: {s_ext_lower})")

        s_stem_without_extension : str = cl_file_path.stem
        d_entry : Dict[str, Path | None] = \
            d_stem_to_files.setdefault(
                s_stem_without_extension,
                {"jpg": None, "png": None, "json": None}
            )

        if s_ext_lower == ".jpg":
            d_entry["jpg"] = cl_file_path.resolve()
        elif s_ext_lower == ".png":
            d_entry["png"] = cl_file_path.resolve()
        elif s_ext_lower == ".json":
            d_entry["json"] = cl_file_path.resolve()

    # ------------------------------------------------------------------
    # 3. Assemble the result list
    # ------------------------------------------------------------------
    lt_image_json_pairs : List[Tuple[Path, Path]] = []

    for s_stem, d_files in d_stem_to_files.items():
        logging.debug(f"Found entry '{s_stem}': {d_files}")

        if d_files["jpg"] and d_files["json"]:
            lt_image_json_pairs.append((d_files["jpg"], d_files["json"]))
        elif d_files["png"] and d_files["json"]:
            lt_image_json_pairs.append((d_files["png"], d_files["json"]))
        # If no matching image/JSON pair exists we simply skip it

    return lt_image_json_pairs

def build_path_output_jpg(output_folder: str, image_path: Path) -> Path:
    """
    Construct a .jpg output path inside `output_folder` using the stem of `image_path`.

    Example:
        image_path = /data/foo/bar/image_001.png
        output_folder = "output"
        -> output/image_001.jpg
    """
    cl_output = Path(output_folder).resolve()
    return cl_output / f"{image_path.stem} sheet.jpg"


# Example usage for testing purposes
if __name__ == "__main__":
    # Basic path conversion
    test_components = ["src", "data", "test.json"]
    result_path = convert_to_path(test_components)
    print(f"Converted path: {result_path}")
