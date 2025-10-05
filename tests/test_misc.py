import os
import sys
import pandas as pd

# Add the assignment folder to sys.path so we can import misc even though the
# directory name contains a space. This keeps the tests runnable from repo root.
ROOT = os.path.dirname(os.path.dirname(__file__))
ASSIGN_DIR = os.path.join(ROOT, 'assignment _1')
if ASSIGN_DIR not in sys.path:
    sys.path.insert(0, ASSIGN_DIR)

import misc


def test_load_data_columns():
    df = misc.load_data()
    assert isinstance(df, pd.DataFrame)
    expected = set(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS',
                    'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV'])
    assert expected.issubset(set(df.columns))
