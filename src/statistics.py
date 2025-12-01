import numpy as np
from scipy import stats


class SPRT:
    """
    Sequential Probability Ratio Test (SPRT) for A/B Testing

    This class implements the statistical engine that allows you to
    monitor A/B tests continuously without inflating Type I error.
    """

    def __init__(self, alpha=0.05, beta=0.20, mde=0.02):
        """
        Initialize SPRT with test parameters

        Args:
            alpha: Significance level (Type I error rate)
            beta: Type II error rate (1 - power)
            mde: Minimum Detectable Effect (relative difference)
        """
        self.alpha = alpha
        self.beta = beta
        self.mde = mde

        self.upper_boundary = np.log((1 - beta) / alpha)
        self.lower_boundary = np.log(beta / (1 - alpha))

    def calculate_log_likelihood_ratio(self, conversions_a, trials_a, conversions_b, trials_b):
        """
        Calculate the log likelihood ratio for current data

        Args:
            conversions_a: Number of conversions in group A
            trials_a: Number of trials in group A
            conversions_b: Number of conversions in group B
            trials_b: Number of trials in group B

        Returns:
            Log likelihood ratio statistic
        """
        p_a = conversions_a / trials_a
        p_b = conversions_b / trials_b
        pooled_conversion_rate = (conversions_a + conversions_b) / (trials_a + trials_b)
        p_b_alt = pooled_conversion_rate * (1 + mde)
        pass

    def get_decision(self, llr):
        """
        Determine whether to continue, stop and declare winner, or stop and declare no effect

        Args:
            llr: Log likelihood ratio

        Returns:
            Decision: "CONTINUE", "STOP_B_WINS", or "STOP_NO_EFFECT"
        """
        if llr >= self.upper_boundary:
            return "STOP_B_WINS"
        elif llr <= self.lower_boundary:
            return "STOP_NO_EFFECT"
        else:
            return "CONTINUE"
