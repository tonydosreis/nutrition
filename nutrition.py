import numpy as np
from scipy import optimize

MIN_QUANT = 0
MAX_QUANT = 10**4 #10kg

class Food():

    ATTR_NAMES = ["cals", "carbs", "proteins", "fats", "quantity"]

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
        assert attr_name in Food.ATTR_NAMES
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
        
class MealSolver():
    def __init__(self, foods):
        self.foods = foods
        self.n_foods = len(foods)
        self.quant_bounds = (MIN_QUANT*np.ones(self.n_foods), MAX_QUANT*np.ones(self.n_foods))
        self.n_equations = 0
        self.A = []
        self.B = []

    def add_equation(self, a,b):
        assert len(a) == self.n_foods
        assert type(b) in [float, int]
        self.A.append(a)
        self.B.append(b)
        self.n_equations += 1

    def add_total_constraint(self, property, quant):
        assert property in Food.ATTR_NAMES
        assert quant >= 0
        a = [food.get_attr(property) for food in self.foods]
        b = quant
        self.add_equation(a,b)

    def add_quant_constraint(self, food, quant):
        assert food in self.foods
        assert quant >= 0
        a = [0]*self.n_foods
        i = self.foods.index(food)
        a[i] = 1
        b = quant
        self.add_equation(a,b)

    def solve(self):
        assert self.n_equations > 0
        A = np.array(self.A)
        B = np.array(self.B).reshape(-1,1)
        bounds = self.quant_bounds
        x0 =np.random.uniform(low = bounds[0], high = bounds[1], size=(self.n_foods))
        def fun(x):
            return (A@x.reshape((-1,1)) - B).flatten()
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

if __name__ =="__main__":
    rice = Food("Rice", "grams", serving_size=47, cals =170, carbs=37, proteins=3, fats=0)
    vegetables = Food("Vegetables", "grams", serving_size=100, cals=28, carbs=3, proteins=3, fats=0.5)
    chicken = Food("Chicken breast", "grams", serving_size=112, cals=100, carbs=0, proteins=24, fats=0.5 )
    oil = Food("Canola oil", "grams", serving_size=14, cals=120, carbs =0, proteins=0,fats=14)

    foods = [rice, vegetables, chicken, oil]

    bodyweight = 150
    protein_ratio = 1
    fat_ratio = .4

    daily_cals = 2200
    n_meals = 4

    cals_per_meal, protein_per_meal, fats_per_meal = get_macros_per_meal(bodyweight, protein_ratio, fat_ratio, daily_cals, n_meals)
    display_goal(cals_per_meal, protein_per_meal, fats_per_meal)

    solver = MealSolver(foods)
    solver.add_total_constraint("proteins", protein_per_meal)
    solver.add_total_constraint("cals", cals_per_meal)
    solver.add_total_constraint("fats", fats_per_meal)
    solver.add_quant_constraint(vegetables, 100)

    quant, res = solver.solve()

    display_meal(foods, quant)