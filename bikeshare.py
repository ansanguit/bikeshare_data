import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by to apply no month filter
        (str) day - name of the day of week to filter by to apply no day filter
    """
    print('Hello! Welcome to the amazing world of bikeshare. Let\'s explore some US bikeshare data!')
    print('\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('What city do you want to explore? Please enter: Chicago, New York City or Washington:\n').lower()

    while city not in ('chicago', 'new york city', 'washington'):
       city = input("Sorry, that is not a valid option. Enter again: ").lower()

    print('\n')

    # TO DO: get user input for month (all, January, February, ... , June)
    filter_month = input('Would you like to filter by month? y or n:\n').lower()
    while filter_month not in ('y','n'):
        filter_month = input('Sorry, I did not get that, enter y or n:\n').lower()
    if filter_month == 'y':
        month = input('Please, select the month you want to filter by : January, February, March, ...June \n').lower()
        while month not in ('january', 'february', 'march', 'april', 'june'):
            month = input('Sorry, that is not a valid month, try again:\n').lower()
    else:
        month = 'all'
        print('You have chosen no filter per month')

    print('\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    filter_day = input('Now last one, promised! Would you like to filter by day? y or n:\n').lower()
    while filter_day not in ('y','n'):
        filter_day = input('Sorry, I did not get that, enter y or n:\n').lower()
    if filter_day == 'y':
        day = input('Please, select the day you want to filter by : Monday, Tuesday, etc \n').lower()
        while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            day = input('Sorry, that is not a valid day, try again:\n').lower()
    else:
        day = 'all'
        print('You have chosen no filtering per day')

    print('\n')

    print('-'*70)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    pd.set_option("display.precision", 2)

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print('-'*70)
    return df

def general_stats(df):
    """
    Loads general descriptive statistics from the selected city, day, months.
    Prompts the user with a message to see a selection of raw data.

    """
    print('Here some stats, but no worries,we will cover a bit more in detail later')
    print('\n')
    print(df.describe(include=[np.number]))

    raw_data = input('Would you like to a sample of the raw data? y or n \n').lower()
    if raw_data == 'y':
        rows= int(input('Ok, how may rows do you want to see? enter a number \n'))
        pd.set_option('display.max_columns',400)
        print(df.head(rows))
    else:
        pass

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        print('The most common month is {}'.format(most_common_month))
    else:
        print('You have chosen {} as month.'.format(month))
    # TO DO: display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print('The most common day of the week is {}'.format(most_common_day))
    else:
        print('You have chosen {} as day.'.format(day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour  {}'.format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station was  {}'.format(most_common_start_station))

    # TO DO: display most commonly used end station

    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station was  {}'.format(most_common_end_station))


    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most common trip was  {}'.format(most_common_trip))

    # Round trips

    df['Round'] = np.where(df['Start Station'] == df['End Station'], 1 , 0)
    round_trips = int(df['Round'].sum())
    total_trips = int(df.shape[0])
    percent = "{:.2f}".format((round_trips/total_trips)*100)


    print('The total trips returning to the same station are {} which represents {} %'.format(round_trips, percent))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_seconds = df['Trip Duration'].sum()
    total_travel_minutes = "{:.2f}".format((total_travel_seconds)/60)
    print('The total time in minutes for the period chosen was {}'.format(total_travel_minutes))

    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()
    mean_min = "{:.2f}".format((mean)/60)
    print('The average time in minutes for the period chosen was {}'.format(mean_min))

    # The longest ride:

    longest = int(((df['Trip Duration'].max())/60)/60)
    print('The longest ride  was {} hours'.format(longest))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if city == 'washington':
        print('We are sorry, we do not have these details for the city selected')
        pass
    else:
        gender = df['Gender'].value_counts()
        print(gender)
    # TO DO: Display earliest, most recent, and most common year of birth
        dob_old = int(df['Birth Year'].min())
        dob_young = int(df['Birth Year'].max())
        dob_mode = int(df['Birth Year'].mode()[0])
        print('The oldest riders were born in {}, the youngest in {} and the most frequent date of birth is {}'.format(dob_old,dob_young,dob_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        general_stats(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        while restart not in ('y', 'n'):
           restart = input("Sorry, that is not a valid option. Enter again y or n: ")
        if restart.lower() == 'n':
            break




if __name__ == "__main__":
	main()
