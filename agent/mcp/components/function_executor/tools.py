import ast
import math
import os
import traceback
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn

TRAIN = pd.read_csv("/work/data/train_timeseries/train_timeseries.csv")
VALIDATION = pd.read_csv("/work/data/validation_timeseries/validation_timeseries.csv")
TEST = pd.read_csv("/work/data/test_timeseries/test_timeseries.csv")
SOIL_DATA = pd.read_csv("/work/data/soil_data.csv")


def execute_timeseries_analysis(func_string: str, data_type: Literal["train", "validation", "test"]) -> str:
    """
    与えられた単一の時系列データを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `df: pd.DataFrame` のみを取ること
        - dfには `{data_type}_timeseries.csv` の内容が格納される
        - 分析結果をcsvまたはpng形式で関数内で保存すること
        - 返り値は保存した分析結果のpathとすること
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
        - 成功した場合: 関数の返り値である成果物のpath。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """
    if data_type == "train":
        df = TRAIN
    elif data_type == "validation":
        df = VALIDATION
    elif data_type == "test":
        df = TEST
    else:
        return "Error: Invalid data type specified. Use 'train', 'validation', or 'test'."

    return _execute_function(func_string, df)


def execute_soil_analysis(func_string: str) -> str:
    """
    与えられた土壌データを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `df: pd.DataFrame` のみを取ること
        - dfには `soil_data.csv` の内容が格納される
        - 分析結果をcsvまたはpng形式で関数内で保存すること
        - 返り値は保存した分析結果のpathとすること
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
        - 成功した場合: 関数の返り値である成果物のpath。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """

    return _execute_function(func_string, SOIL_DATA)


def execute_all_data_analysis(func_string: str) -> str:
    """
    与えられた任意のデータを分析するためのPython関数定義を文字列として受け取り、その実行結果またはエラーを返す。
    関数定義は以下の要件を満たすように実装する：
        - 関数名は任意
        - 引数として `train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame, soil: pd.DataFrame` の4つを取ること
        - それぞれの引数には `{data_type}_timeseries.csv` もしくは `soil_data.csv` の内容が格納される
        - すべてのデータを利用する必要はなく、必要なデータのみを選んで使用してよい
        - 分析結果をcsvまたはpng形式で関数内で保存すること
        - 返り値は保存した分析結果のpathとすること
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
        - 成功した場合: 関数の返り値である成果物のpath。
        - 失敗した場合: エラーのトレースバック情報（文字列）。
    """
    return _execute_function(func_string, TRAIN, VALIDATION, TEST, SOIL_DATA)


def _execute_function(func_string: str, *data) -> str:
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
        exec(func_string, globals=global_scope, locals=local_scope)

        # 4. 定義された関数オブジェクトを取得
        analysis_func = local_scope[func_name]

        # 5. 関数を実行し、結果を取得
        try:
            result = analysis_func(*data)
            if not isinstance(result, str):
                return f"Error: The function must return a string path to the saved result. Got {type(result).__name__} instead."
            else:
                # 6. 結果のパスが存在するか確認
                if not os.path.exists(result):
                    return f"Error: The specified result path '{result}' does not exist."
                else:
                    return result
        except Exception:
            return traceback.format_exc()

    except Exception:
        return traceback.format_exc()
