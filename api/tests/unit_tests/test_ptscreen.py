from unittest import TestCase

import pandas as pd

from snow import ptscreen


class PatientScreeningTransformationTests(TestCase):
    def test_ymca_columns_rounded_up(self):
        data = pd.DataFrame(data={
            'patient_num': [1, 2, 3, 4],
            'ymca_fulton': [1.7, 2.3, 4.0, 3.9],
        })

        data = ptscreen._pre_process(data)
        self.assertSequenceEqual(data.ymca_fulton.tolist(), [2, 3, 4, 4])
