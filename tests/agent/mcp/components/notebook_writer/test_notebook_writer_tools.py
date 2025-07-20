import os
import tempfile
from unittest.mock import patch

import nbformat
import pytest

from agent.mcp.components.notebook_writer.tools import add_cell_to_notebook


class TestAddCellToNotebook:
    def test_add_cell_to_existing_notebook_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "test_notebook.ipynb")

            # Create an existing notebook
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_code_cell("print('existing cell')"))

            with open(notebook_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            # Add a markdown cell
            add_cell_to_notebook(notebook_path, "markdown", "# Test Header")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "code"
            assert result_nb.cells[0].source == "print('existing cell')"
            assert result_nb.cells[1].cell_type == "markdown"
            assert result_nb.cells[1].source == "# Test Header"

    def test_add_cell_to_existing_notebook_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "test_notebook.ipynb")

            # Create an existing notebook
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_markdown_cell("# Existing markdown"))

            with open(notebook_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            # Add a code cell
            add_cell_to_notebook(notebook_path, "code", "import pandas as pd\nprint('hello')")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# Existing markdown"
            assert result_nb.cells[1].cell_type == "code"
            assert result_nb.cells[1].source == "import pandas as pd\nprint('hello')"

    def test_add_cell_to_new_notebook_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "new_notebook.ipynb")

            # File doesn't exist yet
            assert not os.path.exists(notebook_path)

            # Add a markdown cell to new notebook
            add_cell_to_notebook(notebook_path, "markdown", "## New Notebook")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 1
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "## New Notebook"

    def test_add_cell_to_new_notebook_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "new_notebook.ipynb")

            # File doesn't exist yet
            assert not os.path.exists(notebook_path)

            # Add a code cell to new notebook
            add_cell_to_notebook(notebook_path, "code", "x = 1\ny = 2\nprint(x + y)")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 1
            assert result_nb.cells[0].cell_type == "code"
            assert result_nb.cells[0].source == "x = 1\ny = 2\nprint(x + y)"

    def test_add_multiple_cells_to_notebook(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "multi_cell_notebook.ipynb")

            # Add first cell
            add_cell_to_notebook(notebook_path, "markdown", "# Introduction")

            # Add second cell
            add_cell_to_notebook(notebook_path, "code", "import numpy as np")

            # Add third cell
            add_cell_to_notebook(notebook_path, "markdown", "## Analysis")

            # Add fourth cell
            add_cell_to_notebook(notebook_path, "code", "data = np.array([1, 2, 3])\nprint(data)")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 4

            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# Introduction"

            assert result_nb.cells[1].cell_type == "code"
            assert result_nb.cells[1].source == "import numpy as np"

            assert result_nb.cells[2].cell_type == "markdown"
            assert result_nb.cells[2].source == "## Analysis"

            assert result_nb.cells[3].cell_type == "code"
            assert result_nb.cells[3].source == "data = np.array([1, 2, 3])\nprint(data)"

    def test_add_cell_with_special_characters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "special_chars_notebook.ipynb")

            # Test markdown with special characters
            markdown_content = """# データ分析
            
            これは**太字**です。
            
            - リスト1
            - リスト2
            
            ```python
            print("hello")
            ```
            """

            add_cell_to_notebook(notebook_path, "markdown", markdown_content)

            # Test code with special characters
            code_content = """# 日本語のコメント
            text = "これは文字列です"
            print(f"結果: {text}")
            
            # Special characters: @#$%^&*()[]{}|\\:";'<>?,./
            import re
            pattern = r'^[a-zA-Z0-9]+$'
            """

            add_cell_to_notebook(notebook_path, "code", code_content)

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == markdown_content
            assert result_nb.cells[1].cell_type == "code"
            assert result_nb.cells[1].source == code_content

    def test_add_empty_cell(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "empty_cell_notebook.ipynb")

            # Add empty markdown cell
            add_cell_to_notebook(notebook_path, "markdown", "")

            # Add empty code cell
            add_cell_to_notebook(notebook_path, "code", "")

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == ""
            assert result_nb.cells[1].cell_type == "code"
            assert result_nb.cells[1].source == ""

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_add_cell_file_permission_error(self, mock_file):
        with pytest.raises(IOError):
            add_cell_to_notebook("/restricted/path/notebook.ipynb", "code", "test")

    def test_notebook_format_version_consistency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "version_test.ipynb")

            # Add cell to new notebook
            add_cell_to_notebook(notebook_path, "code", "print('version test')")

            # Read the raw JSON to check version
            with open(notebook_path, "r", encoding="utf-8") as f:
                nb_json = nbformat.read(f, as_version=nbformat.NO_CONVERT)

            # Should be version 4
            assert nb_json.nbformat == 4
            assert hasattr(nb_json, "nbformat_minor")

    def test_cell_metadata_structure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = os.path.join(temp_dir, "metadata_test.ipynb")

            # Add cells
            add_cell_to_notebook(notebook_path, "markdown", "# Test")
            add_cell_to_notebook(notebook_path, "code", "x = 1")

            # Read and verify metadata structure
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            for cell in result_nb.cells:
                # Each cell should have proper structure
                assert hasattr(cell, "cell_type")
                assert hasattr(cell, "source")
                assert hasattr(cell, "metadata")

                if cell.cell_type == "code":
                    assert hasattr(cell, "execution_count")
                    assert hasattr(cell, "outputs")
