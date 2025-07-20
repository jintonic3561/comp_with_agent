import os
from typing import Literal

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def add_cell_to_notebook(file_name: str, cell_type: Literal["markdown", "code"], contents: str) -> None:
    """
    Jupyter Notebookファイルにセルを追加します。

    引数:
        file_name (str): ノートブックファイルのファイル名。新しいファイルでもOK。
        cell_type (Literal["markdown", "code"]): 追加するセルの種類。
        contents (str): セルに追加する内容。

    戻り値:
        なし
    """
    # Check if the file exists
    artifact_dir = "/work/artifacts"
    os.makedirs(artifact_dir, exist_ok=True)
    path = os.path.join(artifact_dir, file_name)
    if os.path.exists(path):
        # Load existing notebook
        with open(path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    else:
        # Create a new notebook
        nb = new_notebook()

    # Create and add the new cell
    if cell_type == "markdown":
        cell = new_markdown_cell(contents)
    else:  # cell_type == "code"
        cell = new_code_cell(contents)

    # Add the cell to the notebook
    nb.cells.append(cell)

    # Write the notebook to file
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
