import os
import tempfile
import textwrap
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from agent.mcp.components.analysis_executor.tools import (
    _execute_function,
    _load_data,
    _load_with_cache,
    execute_all_data_analysis,
    execute_soil_analysis,
    execute_timeseries_analysis,
    get_data_sample,
    get_data_summary,
)


class TestExecuteTimeseriesAnalysis:
    def test_execute_timeseries_analysis_valid_function_train_single_path(self):
        func_string = textwrap.dedent("""
            def test_analysis(df):
                result_path = '/work/artifacts/csv/test_result.csv'
                df.head().to_csv(result_path, index=False)
                return result_path
        """)
        with patch("agent.mcp.components.analysis_executor.tools._load_data"):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN") as mock_train:
                mock_train.head.return_value.to_csv = MagicMock()
                with patch("os.path.exists", return_value=True):
                    result = execute_timeseries_analysis(func_string, "train")
                    assert result == "/work/artifacts/csv/test_result.csv"

    def test_execute_timeseries_analysis_valid_function_train_list_paths(self):
        func_string = textwrap.dedent("""
            def test_analysis(df):
                result_paths = ['/work/artifacts/csv/test_result1.csv', '/work/artifacts/csv/test_result2.csv']
                df.head().to_csv(result_paths[0], index=False)
                df.tail().to_csv(result_paths[1], index=False)
                return result_paths
        """)
        with patch("agent.mcp.components.analysis_executor.tools._load_data"):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN") as mock_train:
                mock_train.head.return_value.to_csv = MagicMock()
                mock_train.tail.return_value.to_csv = MagicMock()
                with patch("os.path.exists", return_value=True):
                    result = execute_timeseries_analysis(func_string, "train")
                    assert result == ["/work/artifacts/csv/test_result1.csv", "/work/artifacts/csv/test_result2.csv"]

    def test_execute_timeseries_analysis_invalid_data_type(self):
        func_string = "def test_func(df): return 'test'"
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            result = execute_timeseries_analysis(func_string, "invalid")
            assert "Error: Invalid data type specified" in result

    def test_execute_timeseries_analysis_function_error(self):
        func_string = textwrap.dedent("""
            def test_analysis(df):
                raise ValueError("Test error")
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN", pd.DataFrame()):
                result = execute_timeseries_analysis(func_string, "train")
                assert "ValueError: Test error" in result

    def test_execute_timeseries_analysis_missing_function(self):
        func_string = "x = 1"
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            result = execute_timeseries_analysis(func_string, "train")
            assert "Error: No function definition found" in result

    def test_execute_timeseries_analysis_multiple_functions(self):
        func_string = textwrap.dedent("""
            def func1(df): return 'test1'
            def func2(df): return 'test2'
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            result = execute_timeseries_analysis(func_string, "train")
            assert "Error: Multiple function definitions found" in result


class TestExecuteSoilAnalysis:
    def test_execute_soil_analysis_valid_function_single_path(self):
        func_string = textwrap.dedent("""
            def soil_analysis(df):
                result_path = '/work/artifacts/csv/soil_result.csv'
                df.head().to_csv(result_path, index=False)
                return result_path
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA") as mock_soil:
                mock_soil.head.return_value.to_csv = MagicMock()
                with patch("os.path.exists", return_value=True):
                    result = execute_soil_analysis(func_string)
                    assert result == "/work/artifacts/csv/soil_result.csv"

    def test_execute_soil_analysis_valid_function_list_paths(self):
        func_string = textwrap.dedent("""
            def soil_analysis(df):
                result_paths = ['/work/artifacts/csv/soil_result1.csv', '/work/artifacts/png/soil_plot.png']
                df.head().to_csv(result_paths[0], index=False)
                # Mock saving plot
                return result_paths
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA") as mock_soil:
                mock_soil.head.return_value.to_csv = MagicMock()
                with patch("os.path.exists", return_value=True):
                    result = execute_soil_analysis(func_string)
                    assert result == ["/work/artifacts/csv/soil_result1.csv", "/work/artifacts/png/soil_plot.png"]

    def test_execute_soil_analysis_function_error(self):
        func_string = textwrap.dedent("""
            def soil_analysis(df):
                raise RuntimeError("Soil analysis error")
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", pd.DataFrame()):
                result = execute_soil_analysis(func_string)
                assert "RuntimeError: Soil analysis error" in result


class TestExecuteAllDataAnalysis:
    def test_execute_all_data_analysis_valid_function_single_path(self):
        func_string = textwrap.dedent("""
            def all_data_analysis(train, validation, test, soil):
                import os
                result_path = '/work/artifacts/csv/all_data_result.csv'
                train.head().to_csv(result_path, index=False)
                return result_path
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN") as mock_train:
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", pd.DataFrame()):
                    with patch("agent.mcp.components.analysis_executor.tools.TEST", pd.DataFrame()):
                        with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", pd.DataFrame()):
                            mock_train.head.return_value.to_csv = MagicMock()
                            with patch("os.path.exists", return_value=True):
                                result = execute_all_data_analysis(func_string)
                                assert result == "/work/artifacts/csv/all_data_result.csv"

    def test_execute_all_data_analysis_valid_function_list_paths(self):
        func_string = textwrap.dedent("""
            def all_data_analysis(train, validation, test, soil):
                import os
                result_paths = ['/work/artifacts/csv/all_data_result.csv', '/work/artifacts/png/all_data_plot.png']
                train.head().to_csv(result_paths[0], index=False)
                # Mock saving plot
                return result_paths
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN") as mock_train:
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", pd.DataFrame()):
                    with patch("agent.mcp.components.analysis_executor.tools.TEST", pd.DataFrame()):
                        with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", pd.DataFrame()):
                            mock_train.head.return_value.to_csv = MagicMock()
                            with patch("os.path.exists", return_value=True):
                                result = execute_all_data_analysis(func_string)
                                assert result == ["/work/artifacts/csv/all_data_result.csv", "/work/artifacts/png/all_data_plot.png"]

    def test_execute_all_data_analysis_function_error(self):
        func_string = textwrap.dedent("""
            def all_analysis(train, validation, test, soil):
                raise IndexError("All data analysis error")
            """)
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with patch("agent.mcp.components.analysis_executor.tools.TRAIN", pd.DataFrame()):
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", pd.DataFrame()):
                    with patch("agent.mcp.components.analysis_executor.tools.TEST", pd.DataFrame()):
                        with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", pd.DataFrame()):
                            result = execute_all_data_analysis(func_string)
                            assert "IndexError: All data analysis error" in result


class TestExecuteFunction:
    def test_execute_function_valid_return_type_single_path(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return '/work/artifacts/other/valid_path.txt'
            """)
        with patch("os.path.exists", return_value=True):
            result = _execute_function(func_string, pd.DataFrame())
            assert result == "/work/artifacts/other/valid_path.txt"

    def test_execute_function_valid_return_type_list_paths(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return ['/work/artifacts/other/valid_path1.txt', '/work/artifacts/other/valid_path2.txt']
            """)
        with patch("os.path.exists", return_value=True):
            result = _execute_function(func_string, pd.DataFrame())
            assert result == ["/work/artifacts/other/valid_path1.txt", "/work/artifacts/other/valid_path2.txt"]

    def test_execute_function_invalid_return_type_number(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return 123
            """)
        result = _execute_function(func_string, pd.DataFrame())
        assert "Error: The function must return a string path or list of string paths. Got int instead." in result

    def test_execute_function_invalid_return_type_mixed_list(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return [123, '/work/artifacts/other/valid_path.txt']
            """)
        # Put the invalid type first so it's checked before any path existence validation
        result = _execute_function(func_string, pd.DataFrame())
        assert "Error: The function must return a string path or list of string paths. Got int instead." in result

    def test_execute_function_nonexistent_path_single(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return '/nonexistent/path.txt'
            """)
        with patch("os.path.exists", return_value=False):
            result = _execute_function(func_string, pd.DataFrame())
            assert "Error: The specified result path '/nonexistent/path.txt' does not exist" in result

    def test_execute_function_nonexistent_path_in_list(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                return ['/work/artifacts/other/valid_path.txt', '/nonexistent/path.txt']
            """)
        def mock_exists(path):
            return path == '/work/artifacts/other/valid_path.txt'
        with patch("os.path.exists", side_effect=mock_exists):
            result = _execute_function(func_string, pd.DataFrame())
            assert "Error: The specified result path '/nonexistent/path.txt' does not exist" in result

    def test_execute_function_syntax_error(self):
        func_string = "def invalid_syntax("
        result = _execute_function(func_string, pd.DataFrame())
        assert "SyntaxError" in result

    def test_execute_function_helper_functions_ignored(self):
        func_string = textwrap.dedent("""
            def _helper_function():
                return "helper"

            def main_function(data):
                return '/work/artifacts/other/main_result.txt'
            """)
        with patch("os.path.exists", return_value=True):
            result = _execute_function(func_string, pd.DataFrame())
            assert result == "/work/artifacts/other/main_result.txt"

    def test_execute_function_helper_functions_ignored_with_list_return(self):
        func_string = textwrap.dedent("""
            def _helper_function():
                return ["helper1", "helper2"]

            def main_function(data):
                return ['/work/artifacts/other/main_result1.txt', '/work/artifacts/other/main_result2.txt']
            """)
        with patch("os.path.exists", return_value=True):
            result = _execute_function(func_string, pd.DataFrame())
            assert result == ["/work/artifacts/other/main_result1.txt", "/work/artifacts/other/main_result2.txt"]

    def test_execute_function_scope_includes_libraries(self):
        func_string = textwrap.dedent("""
            def test_function(data):
                # Test that required libraries are available
                assert pd is not None
                assert np is not None
                assert plt is not None
                assert sns is not None
                assert sklearn is not None
                assert os is not None
                assert math is not None
                return '/work/artifacts/other/scope_test.txt'
            """)
        with patch("os.path.exists", return_value=True):
            result = _execute_function(func_string, pd.DataFrame())
            assert result == "/work/artifacts/other/scope_test.txt"


class TestLoadWithCache:
    def test_load_with_cache_parquet_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test_data")
            parquet_path = f"{test_path}.parquet"
            # Create test parquet file
            test_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            test_df.to_parquet(parquet_path, index=False)

            result = _load_with_cache(test_path)
            pd.testing.assert_frame_equal(result, test_df)

    def test_load_with_cache_csv_exists_creates_parquet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test_data")
            parquet_path = f"{test_path}.parquet"
            csv_path = f"{test_path}.csv"

            # Create test CSV file
            test_df = pd.DataFrame({"x": [7, 8, 9], "y": [10, 11, 12]})
            test_df.to_csv(csv_path, index=False)

            result = _load_with_cache(test_path)
            pd.testing.assert_frame_equal(result, test_df)

            # Check that parquet file was created
            assert os.path.exists(parquet_path)

    def test_load_with_cache_file_not_found(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "nonexistent")

            with pytest.raises(FileNotFoundError) as exc_info:
                _load_with_cache(test_path)

            assert "Neither" in str(exc_info.value)
            assert "nonexistent.parquet" in str(exc_info.value)
            assert "nonexistent.csv" in str(exc_info.value)


class TestLoadData:
    @patch("agent.mcp.components.analysis_executor.tools._load_with_cache")
    def test_load_data_initializes_all_data(self, mock_load):
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            # Mock return values for each dataset
            mock_train = pd.DataFrame({"train": [1, 2, 3]})
            mock_validation = pd.DataFrame({"validation": [4, 5, 6]})
            mock_test = pd.DataFrame({"test": [7, 8, 9]})
            mock_soil = pd.DataFrame({"soil": [10, 11, 12]})

            mock_load.side_effect = [mock_train, mock_validation, mock_test, mock_soil]

            with patch("agent.mcp.components.analysis_executor.tools.TRAIN", None):
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", None):
                    with patch("agent.mcp.components.analysis_executor.tools.TEST", None):
                        with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", None):
                            _load_data()

            # Verify that _load_with_cache was called with correct paths
            expected_calls = [
                ("/work/data/train_timeseries/train_timeseries",),
                ("/work/data/validation_timeseries/validation_timeseries",),
                ("/work/data/test_timeseries/test_timeseries",),
                ("/work/data/soil_data",),
            ]
            actual_calls = [call[0] for call in mock_load.call_args_list]
            assert actual_calls == expected_calls

    @patch("agent.mcp.components.analysis_executor.tools._load_with_cache")
    def test_load_data_skips_already_loaded(self, mock_load):
        with patch("agent.mcp.components.analysis_executor.tools.TRAIN", pd.DataFrame()):
            with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", None):
                with patch("agent.mcp.components.analysis_executor.tools.TEST", None):
                    with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", None):
                        _load_data()

        # Should only load the three that were None
        assert mock_load.call_count == 3


class TestGetDataSample:
    def test_get_data_sample_train_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'date': pd.date_range('2000-01-01', periods=10),
            'PRECTOT': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0],
            'score': [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TRAIN", mock_data):
                    result = get_data_sample("train_timeseries")
                    
                    # Check that CSV string is returned
                    assert isinstance(result, str)
                    
                    # Parse the CSV to check content
                    import io
                    result_df = pd.read_csv(io.StringIO(result))
                    
                    # Should have 10 rows (head 5 + tail 5)
                    assert len(result_df) == 10
                    
                    # Check that we have the right columns
                    assert 'fips' in result_df.columns
                    assert 'PRECTOT' in result_df.columns
                    
                    # Check that values are from head and tail
                    assert result_df.iloc[0]['fips'] == 1  # First row from head
                    assert result_df.iloc[9]['fips'] == 10  # Last row from tail

    def test_get_data_sample_soil_data(self):
        mock_soil = pd.DataFrame({
            'fips': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
            'lat': [40.1, 40.2, 40.3, 40.4, 40.5, 40.6, 40.7, 40.8, 40.9, 41.0],
            'lon': [-120.1, -120.2, -120.3, -120.4, -120.5, -120.6, -120.7, -120.8, -120.9, -121.0],
            'elevation': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", mock_soil):
                    result = get_data_sample("soil_data")
                    
                    # Check that CSV string is returned
                    assert isinstance(result, str)
                    
                    # Parse the CSV to check content
                    import io
                    result_df = pd.read_csv(io.StringIO(result))
                    
                    # Should have 10 rows (head 5 + tail 5)
                    assert len(result_df) == 10
                    
                    # Check that we have the right columns
                    assert 'fips' in result_df.columns
                    assert 'lat' in result_df.columns
                    assert 'elevation' in result_df.columns

    def test_get_data_sample_invalid_data_type(self):
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with pytest.raises(ValueError) as exc_info:
                get_data_sample("invalid_type")
            
            assert "Invalid data type: invalid_type" in str(exc_info.value)
            assert "'train_timeseries', 'validation_timeseries', 'test_timeseries', or 'soil_data'" in str(exc_info.value)

    def test_get_data_sample_small_dataset(self):
        # Test with dataset smaller than 10 rows
        mock_data = pd.DataFrame({
            'fips': [1, 2, 3],
            'score': [0, 1, 2]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TRAIN", mock_data):
                    result = get_data_sample("train_timeseries")
                    
                    import io
                    result_df = pd.read_csv(io.StringIO(result))
                    
                    # Should have 6 rows for small dataset (head 3 + tail 3)
                    assert len(result_df) == 6

    def test_get_data_sample_validation_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [11, 12, 13],
            'PRECTOT': [2.1, 2.2, 2.3],
            'score': [1, 2, 1]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", mock_data):
                    result = get_data_sample("validation_timeseries")
                    
                    assert isinstance(result, str)
                    import io
                    result_df = pd.read_csv(io.StringIO(result))
                    assert len(result_df) == 6  # head 3 + tail 3

    def test_get_data_sample_test_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [21, 22, 23, 24],
            'PRECTOT': [3.1, 3.2, 3.3, 3.4],
            'score': [2, 3, 2, 1]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TEST", mock_data):
                    result = get_data_sample("test_timeseries")
                    
                    assert isinstance(result, str)
                    import io
                    result_df = pd.read_csv(io.StringIO(result))
                    assert len(result_df) == 8  # head 4 + tail 4


class TestGetDataSummary:
    def test_get_data_summary_train_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [1, 2, 3, 4, 5],
            'PRECTOT': [1.1, 2.2, 3.3, 4.4, 5.5],
            'PS': [100.1, 100.2, 100.3, 100.4, 100.5],
            'score': [0, 1, 2, 3, 4]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TRAIN", mock_data):
                    result = get_data_summary("train_timeseries")
                    
                    # Check that result is a dict
                    assert isinstance(result, dict)
                    
                    # Check required keys
                    assert "row_count" in result
                    assert "column_count" in result
                    assert "describe_csv" in result
                    
                    # Check values
                    assert result["row_count"] == 5
                    assert result["column_count"] == 4
                    
                    # Check that describe_csv is valid CSV
                    assert isinstance(result["describe_csv"], str)
                    import io
                    describe_df = pd.read_csv(io.StringIO(result["describe_csv"]), index_col=0)
                    
                    # describe() should have statistics like count, mean, std, etc.
                    assert 'count' in describe_df.index
                    assert 'mean' in describe_df.index

    def test_get_data_summary_soil_data(self):
        mock_soil = pd.DataFrame({
            'fips': [100, 200, 300],
            'lat': [40.1, 40.2, 40.3],
            'lon': [-120.1, -120.2, -120.3],
            'elevation': [100, 200, 300],
            'slope1': [0.1, 0.2, 0.3]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.SOIL_DATA", mock_soil):
                    result = get_data_summary("soil_data")
                    
                    # Check that result is a dict
                    assert isinstance(result, dict)
                    
                    # Check required keys
                    assert "row_count" in result
                    assert "column_count" in result
                    assert "describe_csv" in result
                    
                    # Check values
                    assert result["row_count"] == 3
                    assert result["column_count"] == 5
                    
                    # Check that describe_csv is valid CSV
                    assert isinstance(result["describe_csv"], str)

    def test_get_data_summary_invalid_data_type(self):
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", True):
            with pytest.raises(ValueError) as exc_info:
                get_data_summary("invalid_type")
            
            assert "Invalid data type: invalid_type" in str(exc_info.value)
            assert "'train_timeseries', 'validation_timeseries', 'test_timeseries', or 'soil_data'" in str(exc_info.value)

    def test_get_data_summary_with_non_numeric_columns(self):
        # Test with mixed numeric and non-numeric columns
        mock_data = pd.DataFrame({
            'fips': [1, 2, 3],
            'category': ['A', 'B', 'C'],  # Non-numeric column
            'value': [10.5, 20.5, 30.5]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TRAIN", mock_data):
                    result = get_data_summary("train_timeseries")
                    
                    assert result["row_count"] == 3
                    assert result["column_count"] == 3
                    
                    # describe() will only include numeric columns by default
                    import io
                    describe_df = pd.read_csv(io.StringIO(result["describe_csv"]), index_col=0)
                    assert 'fips' in describe_df.columns
                    assert 'value' in describe_df.columns
                    # 'category' should not be in describe output as it's non-numeric

    def test_get_data_summary_validation_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [11, 12, 13],
            'PRECTOT': [2.1, 2.2, 2.3],
            'score': [1, 2, 1]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.VALIDATION", mock_data):
                    result = get_data_summary("validation_timeseries")
                    
                    assert isinstance(result, dict)
                    assert result["row_count"] == 3
                    assert result["column_count"] == 3

    def test_get_data_summary_test_timeseries(self):
        mock_data = pd.DataFrame({
            'fips': [21, 22, 23, 24],
            'PRECTOT': [3.1, 3.2, 3.3, 3.4],
            'score': [2, 3, 2, 1]
        })
        
        with patch("agent.mcp.components.analysis_executor.tools.INITIALIZED", False):
            with patch("agent.mcp.components.analysis_executor.tools._load_data") as mock_load:
                with patch("agent.mcp.components.analysis_executor.tools.TEST", mock_data):
                    result = get_data_summary("test_timeseries")
                    
                    assert isinstance(result, dict)
                    assert result["row_count"] == 4
                    assert result["column_count"] == 3
