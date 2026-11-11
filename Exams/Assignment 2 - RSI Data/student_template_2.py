import numpy as np
from os import path
import scipy.constants as constants
from scipy.stats import ttest_rel
from scipy.stats import norm, chisquare
import matplotlib.pyplot as plt
import pandas as pd

"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""


def main(filepath):

    #setup File Paths and Gather Data
    if not path.exists(filepath):
            print("File does not exist", filepath)
    
        # load the data from the file
    mydata = np.loadtxt(filepath, delimiter=",", skiprows=1, dtype=str)

    #seperate the data into the two columns of interest

    forceplatersi = mydata[:, 1].astype(float)
    accelrsi = mydata[:, 2].astype(float)


    # print("data sample: ", mydata[:5, :])


    """Task 1: For the new dataset of RSI values (all_participant_data_rsi.csv), conduct a paired t-test
    comparing all the force plate and accelerometer RSI values. Clearly report the t-value, p-value, null 
    and alternative hypotheses, and decide whether the null hypothesis can be rejected or not.
    In your report: What can we conclude about the two measurement methods?
    """

    #with our separated data, we can now conduct a paired t-test to compare the two measurement methods
    #print out test specifications
    print("Paired t-test comparing force plate and accelerometer RSI values:")
    print("Null Hypothesis: There is no significant difference between the RSI values measured by the force plate and accelerometer.")
    print("Alternative Hypothesis: There is a significant difference between the RSI values measured by the force plate and accelerometer.")
    print("Significance Level: 0.05\n")

    t_stat, p_value = ttest_rel(forceplatersi, accelrsi)
    #print out results
    print("Paired t-test results:")
    print("t-statistic:", t_stat)
    print("p-value:", p_value)
    #print out conclusion based on p-value
    if p_value < 0.05:
        print("Reject the null hypothesis. There is a significant difference between the two measurement methods.")
    else:
        print("Fail to reject the null hypothesis. There is no significant difference between the two measurement methods.")

    """
    Task 2: For the RSI values gathered using an accelerometer, fit a normal distribution and conduct a
    Chi2 Goodness of Fit Test. Clearly print out the chi2 stat, p-value, and an indication of whether it is
    a good fit or not. Plot a histogram of the accelerometer data with the normal distribution curve overlaid.
    In your report: what factors in the data cause this to be a good fit or not?
    """
    #step 1: fit the accelerometer RSI data to a normal distribution
    accel_mean, accel_std = norm.fit(accelrsi)

    bincount = len(accelrsi)//5  #number of bins for the histogram and expected counts, with at least 5 samples per bin

    #step 2: create bins for the histogram and expected counts
    bins = np.r_[-np.inf, np.linspace(accel_mean - 2 * accel_std, accel_mean + 2 * accel_std, bincount), np.inf]

    # Step 3: bin the samples with np.histogram() to get the observed counts
    observed_counts = np.histogram(accelrsi, bins=bins)[0]

    # Step 4: get the expected counts with your expected_normal_counts()
    expected_prob = np.diff(norm.cdf(bins, loc=accel_mean, scale=accel_std))
    expected_counts = expected_prob * len(accelrsi)

    # Step 5: run chisquare() with ddof=2, because the mean and standard deviation were estimated from the samples
    chi_stat, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
    reject = (p_value < 0.05)

    #print out results
    print("\nChi-Square Goodness of Fit Test results:")
    print("Chi-Square Statistic:", chi_stat)
    print("p-value:", p_value)
    if reject:
        print("Reject the null hypothesis. The accelerometer RSI values do not follow a normal distribution.")
    else:
        print("Fail to reject the null hypothesis. The accelerometer RSI values follow a normal distribution.")

    #now, plot a histogram of the accelerometer data with the normal distribution curve overlaid
    plot_bins = np.linspace(accelrsi.min(), accelrsi.max(), bincount)
    plt.hist(accelrsi, bins=plot_bins, density=True, alpha=0.7,
         label="Accelerometer RSI")
    x = np.linspace(accel_mean - 2 * accel_std, accel_mean + 2 * accel_std, 100)
    plt.plot(x, norm.pdf(x, loc=accel_mean, scale=accel_std), 'r-', label='Normal Distribution')
    plt.xlabel('RSI Values')
    plt.ylabel('Density')
    plt.title('Chi-Square Goodness of Fit Test for Accelerometer RSI')
    plt.legend()
    plt.show()

    """
    Task 3: From the force plate and accelerometer-based RSI data for all participants, create and print()
    a dataframe containing only the trials from Participant ‘F’. Calculate the 95% confidence intervals
    for Participant F’s RSI for both the force plate and accelerometer measurements. 
    In your report: What can we conclude about the two measurement methods from these?
    """

    #create a dataframe from the data
    pandas_data = pd.DataFrame(mydata, columns=['Trial', 'Force_Plate_RSI', 'Accelerometer_RSI', 'Error'])

    #filter for Participant 'F'
    participant_f_data = pandas_data[pandas_data['Trial'].str.startswith('F')]

    #calculate the 95% confidence intervals for both measurement methods using data frame
    force_plate_rsi = participant_f_data['Force_Plate_RSI'].astype(float)
    accel_rsi = participant_f_data['Accelerometer_RSI'].astype(float)

    force_plate_mean = force_plate_rsi.mean()
    force_plate_std = force_plate_rsi.std()
    accel_mean = accel_rsi.mean()
    accel_std = accel_rsi.std()

    #confidence intervals
    force_plate_ci = (force_plate_mean - 1.96 * force_plate_std / np.sqrt(len(force_plate_rsi)),
                      force_plate_mean + 1.96 * force_plate_std / np.sqrt(len(force_plate_rsi)))   
    accel_ci = (accel_mean - 1.96 * accel_std / np.sqrt(len(accel_rsi)),
                  accel_mean + 1.96 * accel_std / np.sqrt(len(accel_rsi))) 

    #print out results
    print("\nParticipant F's RSI Data:\n")
    print("Mean Force Plate RSI:", force_plate_mean)
    print("Standard deviation of Force Plate RSI:", force_plate_std)
    print("95% Confidence Interval for Force Plate RSI:", tuple(float(x) for x in force_plate_ci), "\n")
    print("Mean Accelerometer RSI:", accel_mean)
    print("standard deviation of Accelerometer RSI:", accel_std)
    print("95% Confidence Interval for Accelerometer RSI:", tuple(float(x) for x in accel_ci))

    return


if __name__ == "__main__":
    filepath = "data/drop-jump/all_participant_data_rsi.csv"


    main(filepath)