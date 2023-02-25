import numpy as np
from scipy import optimize

class Food():
    def __init__(self, name, unit, serving_size, cals, carbs, proteins, fats):
        self.name = name
        self.unit = unit
        self.cals = cals/serving_size
        self.carbs = carbs/serving_size
        self.proteins = proteins/serving_size
        self.fats = fats/serving_size
    
    def __str__(self):
        return f"Name: {self.name:>20}, cals: {self.cals:.2f}/g, carbs: {self.carbs:.2f}/g, proteins: {self.proteins:.2f}/g, fats {self.fats:.2f}/g"

    def get_attr(self, attr_name):
        assert attr_name in ["cals", "carbs", "proteins", "fats", "quantity"]
        if(attr_name == "cals"):
            return self.cals
        elif(attr_name == "carbs"):
            return self.carbs
        elif(attr_name == "proteins"):
            return self.proteins
        elif(attr_name == "fats"):
            return self.fats
        else:
            return 1

class Constraint():
    def __init__(self, property, coef, b):
        assert property in ["cals", "carbs", "proteins", "fats", "quantity"]
        self.property = property
        self.coef = np.array(coef)
        self.b = b

class TotalConstraint(Constraint):
    def __init__(self, foods, property, total):
        coef = len(foods)*[1]
        super().__init__(property, coef,total)

class QuantConstraint(Constraint):
    def __init__(self, foods, food, quant):
        i = foods.index(food)
        coef = len(foods)*[0]
        coef[i]=1
        super().__init__("quantity", coef, quant)

def meal_prop(foods, constraints):
    assert type(foods) == list
    assert type(constraints) == list
    n_foods = len(foods)
    n_constraints = len(constraints)
    
    A = np.zeros((n_constraints,n_foods))
    b = np.zeros((n_constraints, 1))

    for i, constraint in enumerate(constraints):
        A[i,:] = np.array([food.get_attr(constraint.property) for food in foods])*constraint.coef
        b[i] = constraint.b

    bounds = (0, 1000)

    x0 =np.random.uniform(low = bounds[0], high = bounds[1], size=(n_foods))

    def fun(x):
        return (A@x.reshape((-1,1)) - b).flatten()

    out = optimize.least_squares( fun = fun,x0 = x0, bounds = bounds)

    quant = out.x
    res = out.fun

    return quant, res

def get_daily_macros(bodyweight, protein_ratio, fat_ratio):
    daily_protein = bodyweight*protein_ratio
    daily_fats = fat_ratio*bodyweight

    return daily_protein, daily_fats

def get_macros_per_meal(bodyweight, protein_ratio, fat_ratio, daily_cals, n_meals):
    """Calculates the macros for each meal in a day.
    
    Recommended values are for a gaining phase.

    Args:
        Bodyweight: bodyweight in pounds.
        Protein Ratio: 1 is a standard value.
        fat_ration: values between 0.3-0.5 are recommended.
        daily_cals: Depends on experimentation and current weight gaining goal.
        n_meals: Number of meals in a day, at least 4 is recommended.

    Returns:
        cals_per_meal
        protein_per_meal
        fats_per_meal
    """

    daily_protein, daily_fats = get_daily_macros(bodyweight, protein_ratio, fat_ratio)

    cals_per_meal = daily_cals/n_meals
    protein_per_meal = daily_protein/n_meals
    fats_per_meal = daily_fats/n_meals

    return cals_per_meal, protein_per_meal, fats_per_meal

def display_goal(cals_per_meal, protein_per_meal, fats_per_meal):
    print("Goal:")
    print(f"   cals: {cals_per_meal:.0f}, proteins: {protein_per_meal:.0f}g, fats {fats_per_meal:.0f}g" )

def display_meal(foods, quantity):
    calories = 0
    carbs = 0
    proteins = 0
    fats = 0

    print("Meal:")
    for food, quant in zip(foods, quantity):
        print(f"   -{quant:.0f}g of {food.name} ")
        calories += food.cals*quant
        carbs += food.carbs*quant
        proteins += food.proteins*quant
        fats += food.fats*quant

    print("Macros:")
    print(f"   cals: {calories:.0f}, carbs: {carbs:.0f}g, proteins: {proteins:.0f}g, fats {fats:.0f}g" )