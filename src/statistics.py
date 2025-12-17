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
        # Check if there is data
        if trials_a == 0 or trials_b == 0:
            return 0.0
        
        # Check if there is enough data
        MIN_SAMPLES = 5
        if trials_a < MIN_SAMPLES or trials_b < MIN_SAMPLES:
            return 0.0

        epsilon = 1e-10
        pooled_conversion_rate = np.clip(
            (conversions_a + conversions_b) / (trials_a + trials_b),
            epsilon, 1 - epsilon
        )
        # Clip p_b_alt to ensure it's a valid probability
        p_b_alt = np.clip(
            pooled_conversion_rate * (1 + self.mde),
            epsilon, 1 - epsilon
        )
        
        # Log Likelihood under H0: both groups have pooled rate
        ll_null = (
            conversions_a * np.log(pooled_conversion_rate) +
            (trials_a - conversions_a) * np.log(1 - pooled_conversion_rate) +
            conversions_b * np.log(pooled_conversion_rate) +
            (trials_b - conversions_b) * np.log(1 - pooled_conversion_rate)
        )

        # Log Likelihood under H1: A has pooled rate, B has higher rate
        ll_alt = (
            conversions_a * np.log(pooled_conversion_rate) +
            (trials_a - conversions_a) * np.log(1 - pooled_conversion_rate) +
            conversions_b * np.log(p_b_alt) +
            (trials_b - conversions_b) * np.log(1 - p_b_alt)
        )
        
        return ll_alt - ll_null

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
