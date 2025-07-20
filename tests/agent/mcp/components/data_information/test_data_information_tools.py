import pytest

from agent.mcp.components.data_information.tools import (
    get_data_description,
    get_join_keys_info,
    get_problem_formulation,
    list_available_data,
)


class TestListAvailableData:
    def test_list_available_data_returns_correct_list(self):
        result = list_available_data()
        expected = ["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]
        assert result == expected
        assert isinstance(result, list)
        assert len(result) == 4

    def test_list_available_data_returns_strings(self):
        result = list_available_data()
        for item in result:
            assert isinstance(item, str)


class TestGetDataDescription:
    def test_get_data_description_timeseries(self):
        result = get_data_description("timeseries")
        assert isinstance(result, str)

    def test_get_data_description_soil_data(self):
        result = get_data_description("soil_data")
        assert isinstance(result, str)

    def test_get_data_description_invalid_type(self):
        with pytest.raises(ValueError) as exc_info:
            get_data_description("invalid_type")
        assert "無効なデータ種別です" in str(exc_info.value)


class TestGetJoinKeysInfo:
    def test_get_join_keys_info_returns_string(self):
        result = get_join_keys_info()
        assert isinstance(result, str)


class TestGetProblemFormulation:
    def test_get_problem_formulation_returns_string(self):
        result = get_problem_formulation()
        assert isinstance(result, str)
