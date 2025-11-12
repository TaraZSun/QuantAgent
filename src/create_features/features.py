import pandas as pd
import pandas_ta as ta

import pathlib
import const

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create technical indicator features for the given DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame with OHLCV data.

    Returns:
    pd.DataFrame: DataFrame with added technical indicator features.
    """
    # Ensure the DataFrame has the required columns
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"DataFrame must contain '{col}' column.")

    # Iterate over the indicators defined in const.INDICATORS
    for indicator, params in const.INDICATORS:
        try:
            # Dynamically get the function from pandas_ta
            ta_function = getattr(ta, indicator)
            # Calculate the indicator and add it to the DataFrame
            indicator_values = ta_function(
                high=df['high'],
                low=df['low'],
                close=df['close'],
                volume=df['volume'],
                **params
            )
            # If the result is a DataFrame (multiple columns), concatenate it
            if isinstance(indicator_values, pd.DataFrame):
                df = pd.concat([df, indicator_values], axis=1)
            else:
                df[indicator] = indicator_values
        except Exception as e:
            print(f"Error calculating {indicator} with params {params}: {e}")

    return df
