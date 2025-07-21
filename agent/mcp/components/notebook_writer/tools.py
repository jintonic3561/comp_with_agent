import os
import textwrap
from typing import List, Literal

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def add_cell_to_notebook(
    file_name: str, cell_type: Literal["markdown", "code"], contents: str, artifact_paths: List[str] | None = None
) -> None:
    """
    Jupyter Notebookファイルにセルを追加します。

    引数:
        file_name (str): ノートブックファイルのファイル名。新しいファイルでもOK。
        cell_type (Literal["markdown", "code"]): 追加するセルの種類。
        contents (str): セルに追加する内容。
        artifact_paths (List[str] | None):
            表示するアーティファクトファイルのpathのリスト。
            分析で何らかのファイル出力を行った場合は、必ずそのすべてのpathを指定する。

    戻り値:
        なし
    """
    # Check if the file exists
    artifact_dir = os.environ.get("ARTIFACT_DIR", "/work/artifacts")
    os.makedirs(artifact_dir, exist_ok=True)

    # Handle both absolute paths and filenames
    if os.path.isabs(file_name):
        path = file_name
    else:
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

    # Add artifact display cells if artifact_paths is provided
    if artifact_paths:
        for artifact_path in artifact_paths:
            if not os.path.exists(artifact_path):
                print(f"WARNING: The artifact path '{artifact_path}' does not exist. Skipping.")
                continue

            # Determine file type and create appropriate display code
            artifact_name = os.path.basename(artifact_path)
            if artifact_path.lower().endswith((".png", ".jpg", ".jpeg")):
                # Image file - display with matplotlib
                display_code = textwrap.dedent(f"""\
                    import matplotlib.pyplot as plt
                    import matplotlib.image as mpimg
                    
                    # Display image: {artifact_name}
                    img = mpimg.imread('{artifact_path}')
                    plt.figure(figsize=(10, 8))
                    plt.imshow(img)
                    plt.axis('off')
                    plt.title('{artifact_name}')
                    plt.show()
                    """)
            elif artifact_path.lower().endswith(".csv"):
                # CSV file - display as DataFrame
                display_code = textwrap.dedent(f"""\
                    import pandas as pd
                    
                    # Display CSV: {artifact_name}
                    df = pd.read_csv('{artifact_path}')
                    print(f"Shape: {{df.shape}}")
                    print(f"\\nColumns: {{list(df.columns)}}")
                    print(f"\\nFirst 10 rows:")
                    display(df.head(10))
                    """)
            elif artifact_path.lower().endswith(".txt"):
                # Text file - display contents
                display_code = textwrap.dedent(f"""\
                    # Display text file: {artifact_name}
                    with open('{artifact_path}', 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    print(f"=== Content of {artifact_name} ===")
                    print(content)
                    print(f"=== End of {artifact_name} ===")
                    """)
            else:
                # For unsupported file types, show warning
                extension = os.path.splitext(artifact_path)[1]
                display_code = textwrap.dedent(f"""\
                    # Unsupported artifact type: {artifact_name}
                    print("WARNING: The file '{artifact_name}' with extension '{extension}' is not supported for display.")
                    print("Supported extensions: .png, .jpg, .jpeg, .csv, .txt")
                    print(f"File path: {artifact_path}")
                    """)

            # Create and add the display cell
            display_cell = new_code_cell(display_code)
            nb.cells.append(display_cell)

    # Write the notebook to file
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
