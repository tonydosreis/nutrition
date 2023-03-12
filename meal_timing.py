import numpy as np
from scipy import optimize


def dec2time(x):
    hour = int(x)
    minutes = int((300/5)*(x - hour))

    if(hour == 0):
        return f"{minutes:0>2}m"
    else:
        return f"{hour:0>2}:{minutes:0>2}h"


def calc_meal_time_old(t_wake, delta_wake, t_gym,
                       delta_gym, t_sleep, delta_sleep):
    A = np.array([[-1, 2, -1, 0], [0, -1, 2, -1],
                 [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    b = np.array([0, 0, t_wake + delta_wake, t_gym - delta_gym,
                 t_sleep - delta_sleep]).reshape((-1, 1))

    n = A.shape[1]

    def fun(x):
        x = x.reshape((-1, 1))
        return (A@x - b).flatten()

    bounds = ([t_wake + delta_wake, t_wake, t_wake, t_wake],
              [t_sleep, t_sleep, t_sleep, t_sleep])

    res = optimize.least_squares(fun, np.random.uniform(
        low=bounds[0], high=bounds[1], size=(n)), bounds=bounds)
    m = res.x

    return m


def calc_meal_time(t_wake, delta_wake, t_gym, delta_gym,
                   t_sleep, delta_sleep, n_meals):
    """Calculate meal times trying to have equal intervals and other criteria.

    The desired time for first meal is t_wake + delta_wake, for the pregym meal
    is t_gym - delta_gym and for the last meal t_sleep - delta_sleep. The
    solution tries to balance having equal intervals and also being close to
    the desired times.

    Args:
        t_wake: wake up time.
        delta_wake: How much time after waking up is first meal.
        t_gym: gym time.
        delta_gym: How much time before gym to have a meal.
        t_sleep: sleep time.
        delta_sleep: How much time before sleep to have last meal.
        n_meals: number of meals in a day.
    Returns:
        m: meal times.
    """

    assert n_meals >= 3

    # Create A matrix
    A = []
    # Equal intervals constraints
    for i in range(n_meals - 2):
        a_row = []
        for j in range(n_meals):
            if((j == i) or (j == i + 2)):
                a_row.append(-1)
            elif(j == i + 1):
                a_row.append(2)
            else:
                a_row.append(0)
        A.append(a_row)

    # Desired time constraints
    a_row = n_meals*[0]
    a_row[0] = 1
    A.append(a_row)

    # Approximation of which meal will be the pregym meal
    pregym_meal = int((t_gym - delta_gym-t_wake - delta_sleep) /
                      ((t_sleep - delta_sleep - t_wake - delta_sleep)/n_meals))
    a_row = n_meals*[0]
    a_row[pregym_meal] = 1
    A.append(a_row)

    a_row = n_meals*[0]
    a_row[-1] = 1
    A.append(a_row)

    A = np.array(A)

    # Create b
    b = (1+n_meals)*[0]
    b[-1] = t_sleep - delta_sleep
    b[-2] = t_gym - delta_gym
    b[-3] = t_wake + delta_wake

    b = np.array(b).reshape((-1, 1))

    # Bounds
    lb = n_meals*[t_wake]
    lb[0] += delta_wake
    ub = n_meals*[t_sleep]
    bounds = (lb, ub)

    n = A.shape[1]

    def fun(x):
        x = x.reshape((-1, 1))
        return (A@x - b).flatten()

    res = optimize.least_squares(fun, np.random.uniform(
        low=bounds[0], high=bounds[1], size=(n)), bounds=bounds)
    m = res.x

    return m


def display_meal_time(m, t_wake, delta_wake, t_gym,
                      delta_gym, t_sleep, delta_sleep):
    """Format and display useful information returned by cal_meal_time"""

    print("Meal Times:")
    for i, time_dec in enumerate((m)):
        print(f"m{i} = {dec2time(time_dec)}")

    print()

    print("Meal intervals:", end=" ")
    print(f"{[ dec2time(delta) for delta in np.diff(m)]}, "
          f"std = {dec2time(np.std(np.diff(m)))}")

    print("Pregym meal interval:")

    pregym_m_index = np.argmax(m > t_gym) - 1
    print(f"\tDesired = {dec2time(delta_gym)}, "
          f"current = {dec2time(t_gym - m[pregym_m_index])}")

    print("Presleep meal interval:")
    print(f"\tDesired = {dec2time(delta_sleep)}, "
          f"current = {dec2time(t_sleep - m[-1])}")

    print("Postwake meal interval:")
    print(f"\tDesired={dec2time(delta_wake)}, "
          f"current = {dec2time(m[0] - t_wake)}")


if __name__ == "__main__":
    t_wake = 8
    delta_wake = 1/6
    t_gym = 17.5
    delta_gym = 2
    t_sleep = 23
    delta_sleep = 3
    n_meals = 4

    m = calc_meal_time(t_wake, delta_wake, t_gym, delta_gym,
                       t_sleep, delta_sleep, n_meals)
    display_meal_time(m, t_wake, delta_wake, t_gym,
                      delta_gym, t_sleep, delta_sleep)
