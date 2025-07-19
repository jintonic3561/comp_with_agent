from typing import List, Literal


def list_available_data() -> List[str]:
    """
    利用可能なデータ一覧を返す関数

    Returns:
        List[str]: 利用可能なデータファイルのリスト
    """
    available_data = ["train_timeseries", "validation_timeseries", "test_timeseries", "soil_data"]

    return available_data


def get_data_description(data_type: Literal["timeseries", "soil_data"]) -> str:
    """
    データ種別の説明をマークダウン形式で返す関数

    Args:
        data_type (str): データ種別名 ("timeseries" または "soil_data")

    Returns:
        str: データ全体の説明、各列名と型・説明

    Raises:
        ValueError: 無効なデータ種別が指定された場合
    """
    if data_type == "timeseries":
        return """
        # 時系列データ（train_timeseries.csv, validation_timeseries.csv, test_timeseries.csv）

        ## データ概要
        米国の干ばつレベルの時系列データと気象指標のデータセットです。日々の気象データと週次の干ばつスコアを含みます。
        干ばつスコアがない日はNaN値となっています。
        train, validation, testの3つのデータセットがあり、各データセットの期間が重複せず、リークしないように設計されています。
        各データのスキーマは同一です。

        ## 列の説明

        | 列名 | データ型 | 説明 |
        |------|---------|------|
        | fips | int | 米国郡のFIPSコード（地域識別子） |
        | date | datetime | 観測日 |
        | PRECTOT | float | 降水量 (mm/日) |
        | PS | float | 地表面気圧 (kPa) |
        | QV2M | float | 地上2メートルでの比湿 (g/kg) |
        | T2M | float | 地上2メートルでの気温 (C) |
        | T2MDEW | float | 地上2メートルでの露点/霜点 (C) |
        | T2MWET | float | 地上2メートルでの湿球温度 (C) |
        | T2M_MAX | float | 地上2メートルでの最高気温 (C) |
        | T2M_MIN | float | 地上2メートルでの最低気温 (C) |
        | T2M_RANGE | float | 地上2メートルでの気温範囲 (C) |
        | TS | float | 地表面温度 (C) |
        | WS10M | float | 地上10メートルでの風速 (m/s) |
        | WS10M_MAX | float | 地上10メートルでの最大風速 (m/s) |
        | WS10M_MIN | float | 地上10メートルでの最小風速 (m/s) |
        | WS10M_RANGE | float | 地上10メートルでの風速範囲 (m/s) |
        | WS50M | float | 地上50メートルでの風速 (m/s) |
        | WS50M_MAX | float | 地上50メートルでの最大風速 (m/s) |
        | WS50M_MIN | float | 地上50メートルでの最小風速 (m/s) |
        | WS50M_RANGE | float | 地上50メートルでの風速範囲 (m/s) |
        | score | float | 干ばつの度合い（0:干ばつなし、1:D0、2:D1、3:D2、4:D3、5:D4） |

        ## 干ばつスコアの説明
        - 0: 干ばつなし (None)
        - 1: D0 (異常な乾燥)
        - 2: D1 (中程度の干ばつ)
        - 3: D2 (重度の干ばつ)
        - 4: D3 (極度の干ばつ)
        - 5: D4 (例外的な干ばつ)
        """
    elif data_type == "soil_data":
        return """
        # 土壌データ (soil_data.csv)

        ## データ概要
        米国郡ごとの地形、土壌特性に関するデータです。Harmonized World Soil Database から取得された情報を含みます。

        ## 列の説明

        | 列名 | データ型 | 説明 |
        |------|---------|------|
        | fips | int | 米国郡のFIPSコード（地域識別子） |
        | lat | float | 緯度 |
        | lon | float | 経度 |
        | elevation | float | 中央値の標高 (メートル) |
        | slope1 | float | 傾斜 0% ≤ 傾斜 ≤ 0.5% の土地の割合 |
        | slope2 | float | 傾斜 0.5% ≤ 傾斜 ≤ 2% の土地の割合 |
        | slope3 | float | 傾斜 2% ≤ 傾斜 ≤ 5% の土地の割合 |
        | slope4 | float | 傾斜 5% ≤ 傾斜 ≤ 10% の土地の割合 |
        | slope5 | float | 傾斜 10% ≤ 傾斜 ≤ 15% の土地の割合 |
        | slope6 | float | 傾斜 15% ≤ 傾斜 ≤ 30% の土地の割合 |
        | slope7 | float | 傾斜 30% ≤ 傾斜 ≤ 45% の土地の割合 |
        | slope8 | float | 傾斜 > 45% の土地の割合 |
        | aspectN | float | 北向き: 0˚< 方位 ≤45˚ または 315˚< 方位 ≤360˚ の土地の割合 |
        | aspectE | float | 東向き: 45˚ < 方位 ≤ 135˚ の土地の割合 |
        | aspectS | float | 南向き: 135˚ < 方位 ≤ 225˚ の土地の割合 |
        | aspectW | float | 西向き: 225˚ < 方位 ≤ 315˚ の土地の割合 |
        | aspectUnknown | float | 未定義: 傾斜方位が未定義、または傾斜勾配が2%未満の格子の割合 |
        | WAT_LAND | float | 水域の割合 |
        | NVG_LAND | float | 不毛/非常に疎らな植生地の割合 |
        | URB_LAND | float | 建造地（住宅・インフラ）の割合 |
        | GRS_LAND | float | 草地/低木/森林の割合 |
        | FOR_LAND | float | 森林地、FRA2000土地統計にキャリブレーション済みの割合 |
        | CULTRF_LAND | float | 降水依存型耕作地の割合 |
        | CULTIR_LAND | float | 灌漑耕作地の割合 (GMIA 4.0に基づく) |
        | CULT_LAND | float | 総耕作地の割合 |
        | SQ1 | float | 栄養素の利用可能性 |
        | SQ2 | float | 栄養素保持能力 |
        | SQ3 | float | 根の条件 |
        | SQ4 | float | 根への酸素の利用可能性 |
        | SQ5 | float | 過剰塩分 |
        | SQ6 | float | 毒性 |
        | SQ7 | float | 作業性（圃場管理の制約） |
        """
    else:
        raise ValueError("無効なデータ種別です。'timeseries' または 'soil_data' を指定してください。")


def get_join_keys_info() -> str:
    """
    各データの結合キー情報をマークダウン形式で返す関数

    Returns:
        str: 結合キーの詳細情報
    """
    return """
    # データ結合キー情報

    ## 共通結合キー: fips

    ### fips (Federal Information Processing Standards code)
    - **データ型**: int
    - **説明**: 米国郡のFIPSコード（地域識別子）
    
    ### 結合方法
    timeseriesデータ（train_timeseries, validation_timeseries, test_timeseries）とsoil_dataは、
    共通のfipsコードで結合することができます。

    ```python
    # 結合例
    import pandas as pd

    # データ読み込み
    timeseries_df = pd.read_csv('train_timeseries.csv')
    soil_df = pd.read_csv('soil_data.csv')

    # fipsで結合
    merged_df = timeseries_df.merge(soil_df, on='fips', how='left')
    ```

    ### 注意点
    - timeseriesデータは時系列データ（日次）であり、同一fipsに対して複数の日付データが存在します
    - soil_dataは静的データ（郡ごと）であり、各fipsに対して1つのレコードのみ存在します
    - 結合時は通常left joinを使用し、timeseriesデータの各レコードにsoil_dataの情報を付加します
    - fipsコードが両データセットに存在しない場合も想定し、データの欠損に注意してください

    ### データ関係性
    - **1対多の関係**: 1つのfips（soil_data）に対して、複数の日付データ（timeseries）が対応
    - **時間軸**: timeseriesデータは時間軸を持つが、soil_dataは時間軸を持たない静的データ
    """


def get_problem_formulation() -> str:
    """
    取り組む問題の問題設計をマークダウン形式で返す関数

    Returns:
        str: 問題設計
    """
    return """
    # 問題設計
    ## About Dataset
    Update (14/12/21): Kaggle Tasks are being deprecated, so I moved the current results on this dataset here:

    | User | Model/Notebook | Macro F1 Mean | MAE Mean |
    |------|----------------|---------------|----------|
    | @cdminix | LSTM Baseline | 0.639 | 0.277 |
    | @epistoteles | Ridge Regression (default features) | 0.579 | 0.255 |
    | @epistoteles | Ridge Regression (MiniROCKET features) | 0.444 | 0.372 |

    ```
    On NaN values: The drought scores are available weekly while the meteorological data points are available daily. To make using previous drought scores for prediction easier (e.g. by interpolating), I merged them into one file and set the drought scores to NaN were not available.
    ```

    ### Context
    The US drought monitor is a measure of drought across the US manually created by experts using a wide range of data.
    This datasets' aim is to help investigate if droughts could be predicted using only meteorological data, potentially leading to generalization of US predictions to other areas of the world.

    ### Content
    This is a classification dataset over six levels of drought, which is no drought (None in the dataset), and five drought levels shown below.
    Each entry is a drought level at a specific point in time in a specific US county, accompanied by the last 90 days of 18 meteorological indicators shown in the bottom of this description.

    D0 (Abnormally Dry)
    D1 (Moderate Drought)
    D2 (Severe Drought)
    D3 (Extreme Drought)
    D4 (Exceptional Drought)

    ![drought level](/work/assets/inbox_2055480_f5ad8544ab11d043972fb9209a874dd3_levels.png)

    To avoid data leakage, the data has been split into the following subsets.

    | Split | Year Range (inclusive) | Percentage (approximate) |
    |-------|------------------------|--------------------------|
    | Train | 2000-2009 | 47% |
    | Validation | 2010-2011 | 10% |
    | Test | 2012-2020 | 43% |

    ### Dataset Imbalance
    The dataset is imbalanced, as can be seen in the following graph.

    ![dataset imbalance](/work/assets/inbox_2055480_9b1753b67845d5e6fe81156350db5191_imbalance.png)

    ### Acknowledgements
    This dataset would not exist without the open data offered by the NASA POWER Project and the authors of the US Drought Monitor.

    These data were obtained from the NASA Langley Research Center (LaRC) POWER Project funded through the NASA Earth Science/Applied Science Program.
    The U.S. Drought Monitor is produced through a partnership between the National Drought Mitigation Center at the University of Nebraska-Lincoln, the United States Department of Agriculture, and the National Oceanic and Atmospheric Administration.
    This dataset utilizes the Harmonized World Soil Database by Fischer, G., F. Nachtergaele, S. Prieler, H.T. van Velthuizen, L. Verelst, D. Wiberg, 2008. Global Agro-ecological Zones Assessment for Agriculture (GAEZ 2008). IIASA, Laxenburg, Austria and FAO, Rome, Italy.

    ### Meteorological Indicators
    Indicator	Description
    WS10M_MIN	Minimum Wind Speed at 10 Meters (m/s)
    QV2M	Specific Humidity at 2 Meters (g/kg)
    T2M_RANGE	Temperature Range at 2 Meters (C)
    WS10M	Wind Speed at 10 Meters (m/s)
    T2M	Temperature at 2 Meters (C)
    WS50M_MIN	Minimum Wind Speed at 50 Meters (m/s)
    T2M_MAX	Maximum Temperature at 2 Meters (C)
    WS50M	Wind Speed at 50 Meters (m/s)
    TS	Earth Skin Temperature (C)
    WS50M_RANGE	Wind Speed Range at 50 Meters (m/s)
    WS50M_MAX	Maximum Wind Speed at 50 Meters (m/s)
    WS10M_MAX	Maximum Wind Speed at 10 Meters (m/s)
    WS10M_RANGE	Wind Speed Range at 10 Meters (m/s)
    PS	Surface Pressure (kPa)
    T2MDEW	Dew/Frost Point at 2 Meters (C)
    T2M_MIN	Minimum Temperature at 2 Meters (C)
    T2MWET	Wet Bulb Temperature at 2 Meters (C)
    PRECTOT	Precipitation (mm day-1)

    ### Previous Updates
    Update (23/07/21): The prediction task is now finalised. The starter and baseline notebooks have been updated. We now use a 180-day window of past data for predictions, and include previous drought values, static data, and meteorological data from the year prior. We also now evaluate on 6 future weeks of predictions. While the baseline model is still very simple, it performs much better using this additional input data.

    Update (03/03/21): the new version adds features from the harmonized world soil database.

    ### Data
    - train_timeseries/train_timeseries.csv
    - validation_timeseries/validation_timeseries.csv
    - test_timeseries/test_timeseries.csv
    - soil_data.csv
    """
