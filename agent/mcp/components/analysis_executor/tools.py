import ast
import math
import os
import traceback
from typing import List, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn

INITIALIZED = False
TRAIN = None
VALIDATION = None
TEST = None
SOIL_DATA = None
os.environ["ARTIFACT_DIR"] = "/work/artifacts"


def execute_timeseries_analysis(func_string: str, data_type: Literal["train", "validation", "test"]) -> str | List[str]:
    """
    与えられた単一の時系列データを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `df: pd.DataFrame` のみを取ること
        - dfには `{data_type}_timeseries.csv` の内容が格納される
        - csvまたはpng形式の分析結果を関数内で `os.environ["ARTIFACT_DIR"]` 内に保存すること
        - 関数の返り値は保存した分析結果のpath、またはそのリストとすること
        - 以下のライブラリはimport済みとしてよい
            - pandas as pd
            - numpy as np
            - math
            - matplotlib.pyplot as plt
            - seaborn as sns
            - sklearn
            - os
        - その他のライブラリは必要に応じてimportしてもよい
        - `_`で始まるヘルパー関数を複数定義してもよいが、実行したい関数はトップレベルで一つだけ定義すること
    このツールを呼び出した後は、必ず返り値のpathを使用して分析結果をすべて読み込み、考察を行うこと

    Args:
        func_string (str): 実行したいPythonの関数定義文字列。
        data_type (Literal["train", "validation", "test"]): 使用するデータのタイプ。'train', 'validation', 'test' のいずれかを指定。

    Returns:
        - 成功した場合: 関数の返り値である成果物のpathまたはそのリスト。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """
    if not INITIALIZED:
        _load_data()

    if data_type == "train":
        df = TRAIN
    elif data_type == "validation":
        df = VALIDATION
    elif data_type == "test":
        df = TEST
    else:
        return "Error: Invalid data type specified. Use 'train', 'validation', or 'test'."

    return _execute_function(func_string, df)


def execute_soil_analysis(func_string: str) -> str | List[str]:
    """
    与えられた土壌データを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `df: pd.DataFrame` のみを取ること
        - dfには `soil_data.csv` の内容が格納される
        - 分析結果をcsvまたはpng形式で関数内で保存すること
        - csvまたはpng形式の分析結果を関数内で `os.environ["ARTIFACT_DIR"]` 内に保存すること
        - 関数の返り値は保存した分析結果のpath、またはそのリストとすること
        - 以下のライブラリはimport済みとしてよい
            - pandas as pd
            - numpy as np
            - math
            - matplotlib.pyplot as plt
            - seaborn as sns
            - sklearn
            - os
        - その他のライブラリは必要に応じてimportしてもよい
        - `_`で始まるヘルパー関数を複数定義してもよいが、実行したい関数はトップレベルで一つだけ定義すること
    このツールを呼び出した後は、必ず返り値のpathを使用して分析結果をすべて読み込み、考察を行うこと

    Args:
        func_string (str): 実行したいPythonの関数定義文字列。

    Returns:
        - 成功した場合: 関数の返り値である成果物のpathまたはそのリスト。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """
    if not INITIALIZED:
        _load_data()

    return _execute_function(func_string, SOIL_DATA)


def execute_all_data_analysis(func_string: str) -> str | List[str]:
    """
    与えられた任意のデータを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame, soil: pd.DataFrame` の4つを取ること
        - それぞれの引数には `{data_type}_timeseries.csv` もしくは `soil_data.csv` の内容が格納される
        - すべてのデータを利用する必要はなく、必要なデータのみを選んで使用してよい
        - 分析結果をcsvまたはpng形式で関数内で保存すること
        - csvまたはpng形式の分析結果を関数内で `os.environ["ARTIFACT_DIR"]` 内に保存すること
        - 関数の返り値は保存した分析結果のpath、またはそのリストとすること
        - 以下のライブラリはimport済みとしてよい
            - pandas as pd
            - numpy as np
            - math
            - matplotlib.pyplot as plt
            - seaborn as sns
            - sklearn
            - os
        - その他のライブラリは必要に応じてimportしてもよい
        - `_`で始まるヘルパー関数を複数定義してもよいが、実行したい関数はトップレベルで一つだけ定義すること
    このツールを呼び出した後は、必ず返り値のpathを使用して分析結果をすべて読み込み、考察を行うこと

    Args:
        func_string (str): 実行したいPythonの関数定義文字列。

    Returns:
        - 成功した場合: 関数の返り値である成果物のpathまたはそのリスト。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """
    if not INITIALIZED:
        _load_data()

    return _execute_function(func_string, TRAIN, VALIDATION, TEST, SOIL_DATA)


def _execute_function(func_string: str, *data) -> str | List[str]:
    try:
        # 1. 文字列からAST（抽象構文木）を生成し、関数名を取得
        tree = ast.parse(func_string)
        # ファイルのトップレベルにある関数定義を探す
        func_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")]
        if not func_defs:
            return "Error: No function definition found in the provided string."
        elif len(func_defs) > 1:
            return "Error: Multiple function definitions found. Please define only one top-level function."
        else:
            func_name = func_defs[0].name

        # 2. execのためのスコープを準備
        global_scope = {
            "pd": pd,
            "np": np,
            "math": math,
            "plt": plt,
            "sns": sns,
            "sklearn": sklearn,
            "os": os,
        }
        local_scope = {}

        # 3. 文字列のコードを実行して、スコープ内に関数を定義
        exec(func_string, global_scope, local_scope)

        # 4. 定義された関数オブジェクトを取得
        analysis_func = local_scope[func_name]

        # 5. 関数を実行し、結果を取得
        try:
            result = analysis_func(*data)

            paths = result if isinstance(result, list) else [result]
            for path in paths:
                if not isinstance(path, str):
                    return f"Error: The function must return a string path or list of string paths. Got {type(path).__name__} instead."
                if not os.path.exists(path):
                    return f"Error: The specified result path '{path}' does not exist."

            return result
        except Exception:
            return traceback.format_exc()

    except Exception:
        return traceback.format_exc()


def _load_with_cache(path_without_extension: str) -> pd.DataFrame:
    parquet_path = f"{path_without_extension}.parquet"
    csv_path = f"{path_without_extension}.csv"

    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path, index=False)
        return df
    else:
        raise FileNotFoundError(f"Neither {parquet_path} nor {csv_path} exists")


def _load_data() -> None:
    global TRAIN, VALIDATION, TEST, SOIL_DATA

    if TRAIN is None:
        TRAIN = _load_with_cache("/work/data/train_timeseries/train_timeseries")
    if VALIDATION is None:
        VALIDATION = _load_with_cache("/work/data/validation_timeseries/validation_timeseries")
    if TEST is None:
        TEST = _load_with_cache("/work/data/test_timeseries/test_timeseries")
    if SOIL_DATA is None:
        SOIL_DATA = _load_with_cache("/work/data/soil_data")


def get_data_sample(data_type: Literal["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]) -> str:
    """
    データ種別を引数に、データのhead(5), tail(5)を結合したサンプルデータをcsv形式文字列で返す関数

    Args:
        data_type (Literal["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]): データ種別名

    Returns:
        str: head(5)とtail(5)を結合したCSV形式の文字列

    Raises:
        ValueError: 無効なデータ種別が指定された場合
    """
    global INITIALIZED, TRAIN, VALIDATION, TEST, SOIL_DATA
    if not INITIALIZED:
        _load_data()
        INITIALIZED = True
    
    if data_type == "train_timeseries":
        df = TRAIN
    elif data_type == "validation_timeseries":
        df = VALIDATION
    elif data_type == "test_timeseries":
        df = TEST
    elif data_type == "soil_data":
        df = SOIL_DATA
    else:
        raise ValueError(f"Invalid data type: {data_type}. Use 'train_timeseries', 'validation_timeseries', 'test_timeseries', or 'soil_data'.")
    
    # head(5)とtail(5)を取得
    head_df = df.head(5)
    tail_df = df.tail(5)
    
    # 結合してCSV形式で返す
    combined_df = pd.concat([head_df, tail_df], ignore_index=True)
    return combined_df.to_csv(index=False)


def get_data_summary(data_type: Literal["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]) -> dict:
    """
    データ種別を引数に、データの行数、列数、df.describe()のcsv形式文字列をdictで返す関数

    Args:
        data_type (Literal["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]): データ種別名

    Returns:
        dict: {"row_count": int, "column_count": int, "describe_csv": str}

    Raises:
        ValueError: 無効なデータ種別が指定された場合
    """
    global INITIALIZED, TRAIN, VALIDATION, TEST, SOIL_DATA
    if not INITIALIZED:
        _load_data()
        INITIALIZED = True
    
    if data_type == "train_timeseries":
        df = TRAIN
    elif data_type == "validation_timeseries":
        df = VALIDATION
    elif data_type == "test_timeseries":
        df = TEST
    elif data_type == "soil_data":
        df = SOIL_DATA
    else:
        raise ValueError(f"Invalid data type: {data_type}. Use 'train_timeseries', 'validation_timeseries', 'test_timeseries', or 'soil_data'.")
    
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "describe_csv": df.describe().to_csv()
    }
