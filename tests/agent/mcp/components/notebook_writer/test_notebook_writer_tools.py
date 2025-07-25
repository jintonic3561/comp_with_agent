import os
import tempfile
from unittest.mock import patch

import nbformat
import pytest

from agent.mcp.components.notebook_writer.tools import add_cell_to_notebook


class TestAddCellToNotebook:
    def setup_method(self, method):
        """Set up test environment"""
        self.original_artifact_dir = os.environ.get("ARTIFACT_DIR")
        
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.original_artifact_dir is not None:
            os.environ["ARTIFACT_DIR"] = self.original_artifact_dir
        elif "ARTIFACT_DIR" in os.environ:
            del os.environ["ARTIFACT_DIR"]
    def test_add_cell_to_existing_notebook_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set ARTIFACT_DIR to temp directory
            os.environ["ARTIFACT_DIR"] = temp_dir
            
            notebook_path = os.path.join(temp_dir, "test_notebook.ipynb")

            # Create an existing notebook
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_code_cell("print('existing cell')"))

            with open(notebook_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            # Add a markdown cell
            result = add_cell_to_notebook(notebook_path, "markdown", "# Test Header")
            assert result == "success"

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
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "test_notebook.ipynb")

            # Create an existing notebook
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_markdown_cell("# Existing markdown"))

            with open(notebook_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            # Add a code cell
            result = add_cell_to_notebook(notebook_path, "code", "import pandas as pd\nprint('hello')")
            assert result == "success"

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
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "new_notebook.ipynb")

            # File doesn't exist yet
            assert not os.path.exists(notebook_path)

            # Add a markdown cell to new notebook
            result = add_cell_to_notebook(notebook_path, "markdown", "## New Notebook")
            assert result == "success"

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 1
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "## New Notebook"

    def test_add_cell_to_new_notebook_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "new_notebook.ipynb")

            # File doesn't exist yet
            assert not os.path.exists(notebook_path)

            # Add a code cell to new notebook
            result = add_cell_to_notebook(notebook_path, "code", "x = 1\ny = 2\nprint(x + y)")
            assert result == "success"

            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)

            assert len(result_nb.cells) == 1
            assert result_nb.cells[0].cell_type == "code"
            assert result_nb.cells[0].source == "x = 1\ny = 2\nprint(x + y)"

    def test_add_multiple_cells_to_notebook(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "multi_cell_notebook.ipynb")

            # Add first cell
            result = add_cell_to_notebook(notebook_path, "markdown", "# Introduction")
            assert result == "success"

            # Add second cell
            result = add_cell_to_notebook(notebook_path, "code", "import numpy as np")
            assert result == "success"

            # Add third cell
            result = add_cell_to_notebook(notebook_path, "markdown", "## Analysis")
            assert result == "success"

            # Add fourth cell
            result = add_cell_to_notebook(notebook_path, "code", "data = np.array([1, 2, 3])\nprint(data)")
            assert result == "success"

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
            os.environ["ARTIFACT_DIR"] = temp_dir
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

            result = add_cell_to_notebook(notebook_path, "markdown", markdown_content)
            assert result == "success"

            # Test code with special characters
            code_content = """# 日本語のコメント
text = "これは文字列です"
print(f"結果: {text}")

# Special characters: @#$%^&*()[]{}|\\:";'<>?,./
import re
pattern = r'^[a-zA-Z0-9]+$'
"""

            result = add_cell_to_notebook(notebook_path, "code", code_content)
            assert result == "success"

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
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "empty_cell_notebook.ipynb")

            # Add empty markdown cell
            result = add_cell_to_notebook(notebook_path, "markdown", "")
            assert result == "success"

            # Add empty code cell
            result = add_cell_to_notebook(notebook_path, "code", "")
            assert result == "success"

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
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "version_test.ipynb")

            # Add cell to new notebook
            result = add_cell_to_notebook(notebook_path, "code", "print('version test')")
            assert result == "success"

            # Read the raw JSON to check version
            with open(notebook_path, "r", encoding="utf-8") as f:
                nb_json = nbformat.read(f, as_version=nbformat.NO_CONVERT)

            # Should be version 4
            assert nb_json.nbformat == 4
            assert hasattr(nb_json, "nbformat_minor")

    def test_cell_metadata_structure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "metadata_test.ipynb")

            # Add cells
            result = add_cell_to_notebook(notebook_path, "markdown", "# Test")
            assert result == "success"
            result = add_cell_to_notebook(notebook_path, "code", "x = 1")
            assert result == "success"

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

    def test_add_cell_with_image_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "image_artifact_notebook.ipynb")
            
            # Create a dummy image file
            image_path = os.path.join(temp_dir, "test_image.png")
            with open(image_path, "w") as f:
                f.write("dummy image content")
            
            # Add cell with image artifact
            result = add_cell_to_notebook(
                notebook_path,
                "markdown",
                "# Analysis with Image",
                artifact_paths=[image_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# Analysis with Image"
            
            # Check image display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "matplotlib.pyplot" in result_nb.cells[1].source
            assert "mpimg.imread" in result_nb.cells[1].source
            assert image_path in result_nb.cells[1].source
            assert "test_image.png" in result_nb.cells[1].source
    
    def test_add_cell_with_csv_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "csv_artifact_notebook.ipynb")
            
            # Create a dummy CSV file
            csv_path = os.path.join(temp_dir, "test_data.csv")
            with open(csv_path, "w") as f:
                f.write("col1,col2,col3\n1,2,3\n4,5,6\n")
            
            # Add cell with CSV artifact
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Load and analyze data",
                artifact_paths=[csv_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "code"
            assert result_nb.cells[0].source == "# Load and analyze data"
            
            # Check CSV display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "pandas as pd" in result_nb.cells[1].source
            assert "pd.read_csv" in result_nb.cells[1].source
            assert csv_path in result_nb.cells[1].source
            assert "df.shape" in result_nb.cells[1].source
            assert "df.head(10)" in result_nb.cells[1].source
    
    def test_add_cell_with_multiple_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "multi_artifact_notebook.ipynb")
            
            # Create multiple artifact files
            image_path = os.path.join(temp_dir, "plot.png")
            csv_path = os.path.join(temp_dir, "results.csv")
            txt_path = os.path.join(temp_dir, "notes.txt")
            
            with open(image_path, "w") as f:
                f.write("dummy image")
            with open(csv_path, "w") as f:
                f.write("a,b\n1,2\n")
            with open(txt_path, "w") as f:
                f.write("some notes")
            
            # Add cell with multiple artifacts
            result = add_cell_to_notebook(
                notebook_path,
                "markdown",
                "## Results Summary",
                artifact_paths=[image_path, csv_path, txt_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 4  # 1 main + 3 artifacts
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "## Results Summary"
            
            # Check image display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "matplotlib" in result_nb.cells[1].source
            
            # Check CSV display cell
            assert result_nb.cells[2].cell_type == "code"
            assert "pandas" in result_nb.cells[2].source
            
            # Check text file cell
            assert result_nb.cells[3].cell_type == "code"
            assert "Display text file: notes.txt" in result_nb.cells[3].source
            assert "Content of notes.txt" in result_nb.cells[3].source
    
    def test_add_cell_with_nonexistent_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "nonexistent_artifact_notebook.ipynb")
            
            # Create one existing file
            existing_csv = os.path.join(temp_dir, "exists.csv")
            with open(existing_csv, "w") as f:
                f.write("x,y\n1,2\n")
            
            # Reference both existing and non-existing files
            nonexistent_path = os.path.join(temp_dir, "does_not_exist.png")
            
            # Add cell with mixed existing/non-existing artifacts
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Analysis",
                artifact_paths=[nonexistent_path, existing_csv]
            )
            # Should return error message for non-existent file
            assert "ERROR" in result
            assert "does not exist" in result
            
            # When error occurs, notebook file should not be created
            assert not os.path.exists(notebook_path)
    
    def test_add_cell_with_empty_artifact_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "empty_artifacts_notebook.ipynb")
            
            # Add cell with empty artifact list
            result = add_cell_to_notebook(
                notebook_path,
                "markdown",
                "# No artifacts",
                artifact_paths=[]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            # Should only have the main cell
            assert len(result_nb.cells) == 1
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# No artifacts"
    
    def test_add_cell_with_various_image_extensions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "various_images_notebook.ipynb")
            
            # Create image files with different extensions
            png_path = os.path.join(temp_dir, "image.PNG")  # uppercase
            jpg_path = os.path.join(temp_dir, "photo.jpg")
            jpeg_path = os.path.join(temp_dir, "picture.JPEG")  # uppercase
            
            for path in [png_path, jpg_path, jpeg_path]:
                with open(path, "w") as f:
                    f.write("dummy")
            
            # Add cell with various image formats
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Image Gallery",
                artifact_paths=[png_path, jpg_path, jpeg_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 4  # 1 main + 3 images
            
            # All image cells should use matplotlib
            for i in range(1, 4):
                assert result_nb.cells[i].cell_type == "code"
                assert "matplotlib" in result_nb.cells[i].source
                assert "imshow" in result_nb.cells[i].source
    
    def test_add_cell_with_txt_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "txt_artifact_notebook.ipynb")
            
            # Create a text file with content
            txt_path = os.path.join(temp_dir, "sample.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("This is a sample text file.\nIt has multiple lines.\n日本語も含まれています。")
            
            # Add cell with text artifact
            result = add_cell_to_notebook(
                notebook_path,
                "markdown",
                "# Text File Display Test",
                artifact_paths=[txt_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# Text File Display Test"
            
            # Check text display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "Display text file: sample.txt" in result_nb.cells[1].source
            assert "Content of sample.txt" in result_nb.cells[1].source
            assert txt_path in result_nb.cells[1].source
    
    def test_add_cell_with_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "unsupported_artifact_notebook.ipynb")
            
            # Create files with unsupported extensions
            json_path = os.path.join(temp_dir, "data.json")
            py_path = os.path.join(temp_dir, "script.py")
            
            with open(json_path, "w") as f:
                f.write('{"key": "value"}')
            with open(py_path, "w") as f:
                f.write('print("hello")')
            
            # Add cell with unsupported artifacts
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Test unsupported extensions",
                artifact_paths=[json_path, py_path]
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 3  # 1 main + 2 unsupported files
            
            # Check warning cells
            assert result_nb.cells[1].cell_type == "code"
            assert "Unsupported artifact type: data.json" in result_nb.cells[1].source
            assert "WARNING" in result_nb.cells[1].source
            assert ".json" in result_nb.cells[1].source
            assert "Supported extensions: .png, .jpg, .jpeg, .csv, .txt" in result_nb.cells[1].source
            
            assert result_nb.cells[2].cell_type == "code"
            assert "Unsupported artifact type: script.py" in result_nb.cells[2].source
            assert "WARNING" in result_nb.cells[2].source
            assert ".py" in result_nb.cells[2].source

    def test_add_cell_with_string_artifact_path_single(self):
        """Test artifact_paths as single string path"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "string_artifact_notebook.ipynb")
            
            # Create a CSV file
            csv_path = os.path.join(temp_dir, "data.csv")
            with open(csv_path, "w") as f:
                f.write("x,y\n1,2\n3,4\n")
            
            # Pass artifact_paths as single string (not list)
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Analysis with string path",
                artifact_paths=csv_path  # String instead of list
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 2
            assert result_nb.cells[0].cell_type == "code"
            assert result_nb.cells[0].source == "# Analysis with string path"
            
            # Check CSV display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "pandas as pd" in result_nb.cells[1].source
            assert csv_path in result_nb.cells[1].source

    def test_add_cell_with_json_string_artifact_paths(self):
        """Test artifact_paths as JSON string"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "json_string_artifact_notebook.ipynb")
            
            # Create multiple files
            csv_path = os.path.join(temp_dir, "data.csv")
            txt_path = os.path.join(temp_dir, "notes.txt")
            
            with open(csv_path, "w") as f:
                f.write("a,b\n1,2\n")
            with open(txt_path, "w") as f:
                f.write("Some notes")
            
            # Pass artifact_paths as JSON string
            import json
            paths_json = json.dumps([csv_path, txt_path])
            
            result = add_cell_to_notebook(
                notebook_path,
                "markdown",
                "# Analysis with JSON paths",
                artifact_paths=paths_json  # JSON string
            )
            assert result == "success"
            
            # Read and verify
            with open(notebook_path, "r", encoding="utf-8") as f:
                result_nb = nbformat.read(f, as_version=4)
            
            assert len(result_nb.cells) == 3  # main + csv + txt
            assert result_nb.cells[0].cell_type == "markdown"
            assert result_nb.cells[0].source == "# Analysis with JSON paths"
            
            # Check CSV display cell
            assert result_nb.cells[1].cell_type == "code"
            assert "pandas as pd" in result_nb.cells[1].source
            
            # Check text display cell
            assert result_nb.cells[2].cell_type == "code"
            assert "Display text file: notes.txt" in result_nb.cells[2].source

    def test_add_cell_with_invalid_json_string_artifact_paths(self):
        """Test artifact_paths as invalid JSON string (fallback to single path)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "invalid_json_artifact_notebook.ipynb")
            
            # Create a file
            csv_path = os.path.join(temp_dir, "data.csv")
            with open(csv_path, "w") as f:
                f.write("x,y\n1,2\n")
            
            # Pass artifact_paths as invalid JSON string (should be treated as single path)
            invalid_json = "[invalid json"
            
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Analysis with invalid JSON",
                artifact_paths=invalid_json  # Invalid JSON string
            )
            
            # Should return error because the invalid JSON string is treated as a path
            assert "ERROR" in result
            assert "does not exist" in result

    def test_add_cell_with_nonexistent_string_artifact_path(self):
        """Test artifact_paths as string path that doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["ARTIFACT_DIR"] = temp_dir
            notebook_path = os.path.join(temp_dir, "nonexistent_string_artifact_notebook.ipynb")
            
            nonexistent_path = os.path.join(temp_dir, "does_not_exist.csv")
            
            # Pass non-existent path as string
            result = add_cell_to_notebook(
                notebook_path,
                "code",
                "# Analysis with non-existent path",
                artifact_paths=nonexistent_path
            )
            
            # Should return error message
            assert "ERROR" in result
            assert "does not exist" in result
            assert nonexistent_path in result
