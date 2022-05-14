import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

BODY = "loan_body"
PAYMENT = "payment"
INTEREST_PAYMENT = "interest_payment"
BODY_PAYMENT = "body_payment"


class Annuity:
    def __init__(self, amount, period, rate):
        self.amount = amount
        self.period = period
        self.rate = rate

        self._monthly_rate = self.rate / 12
        self._annuity_coef = self._calculate_annuity_coef()

    def _calculate_annuity_coef(self):
        m_rate = self._monthly_rate
        return (m_rate * (1 + m_rate) ** self.period) / (
            (1 + m_rate) ** self.period - 1
        )

    def payment_table(self):

        payment = self._annuity_coef * self.amount

        table = pd.DataFrame(
            {PAYMENT: [payment] * self.period, BODY: np.nan, INTEREST_PAYMENT: np.nan}
        )

        rate = self._monthly_rate

        # made with loops because depends on previous row calculations
        for i in range(table.shape[0]):
            if i == 0:
                table.loc[i, BODY] = self.amount
                table.loc[i, INTEREST_PAYMENT] = table.loc[i, BODY] * rate
            else:
                table.loc[i, BODY] = table.loc[i - 1, BODY] - (
                    table.loc[i - 1, PAYMENT] - table.loc[i - 1, INTEREST_PAYMENT]
                )
                table.loc[i, INTEREST_PAYMENT] = table.loc[i - 1, BODY] * rate

        table[BODY_PAYMENT] = table[PAYMENT] - table[INTEREST_PAYMENT]

        table.index = pd.period_range(start="2022-06", periods=self.period, freq="M")

        return table

    def plot_loan_body_change(self):
        table = self.payment_table()

        fig, ax = plt.subplots()
        ax.plot(table.index.strftime("%Y-%m"), table[BODY].values)
        plt.xticks(rotation=90)

        return fig
