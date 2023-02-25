class Food():

    def __init__(self, name,base_grams, tot_cal, tot_carb, tot_prot, tot_fat):

        self.name = name

        #all values are per gram
        self.cal = tot_cal/ (float)(base_grams)
        self.carb = tot_carb/ (float)(base_grams)
        self.prot = tot_prot/ (float)(base_grams)
        self.fat = tot_fat / (float)(base_grams)

    
    def get_info(self):
        print(f"Food: {self.name}")
        print(f"Calories: {self.cal:.2f}/g")
        print(f"Carbohydrates: {self.carb:.2f}/g")
        print(f"Proteins: {self.prot:.2f}/g")
        print(f"Fats: {self.fat:.2f}/g")

class FoodList():

    def __init__(self, food_list):
        self.food_list = food_list

    def get_info(self):
        for food in self.food_list:
            print()
            food.get_info()

class Meal():

    def __init__(self, meal_name, ingredients):

        self.meal_name = meal_name
        #ingredintes is a list of tuples, each tuple is a pair (grams, Food)
        self.ingredients = ingredients
            
        self.tot_cal = 0
        self.tot_carb = 0
        self.tot_prot = 0
        self.tot_fat = 0

        for (gram, food) in ingredients:
            self.tot_cal += gram * food.cal
            self.tot_carb += gram * food.carb
            self.tot_prot += gram * food.prot
            self.tot_fat += gram * food.fat

    def meal_info(self):
        print()
        print("Meal: " + self.meal_name)
        print("Ingredients: ")
        for (gram, food) in self.ingredients:
            print(f" - {gram}g of " + food.name)
        print("Info:")
        print(f"Total calories: {self.tot_cal:.2f} kcal")
        print(f"Total carbohydrates: {self.tot_carb:.2f}g")
        print(f"Total Protein: {self.tot_prot:.2f}g")
        print(f"Total Fat: {self.tot_fat:.2f}g")

if __name__ == '__main__':

    oatmeal = Food("Nestle Oatmeal", 30, 103, 16, 4.6, 2.3)
    greek_yogurt = Food("Itambe greek yogurt", 200, 256, 32,9.8,9.9)

    whole_bread = Food("Di Napoli Whole Bread", 50,118,23,5,0.75)
    ham = Food("Seara Ham", 40, 102, 2, 5.6, 8)
    cheese = Food("Piracanjuba Prato Cheese", 30, 101, 0, 6.8, 8.2)

    list1 = FoodList([oatmeal, greek_yogurt, whole_bread])
    list1.get_info()

    meal1 = Meal("Yogurt n oatmeal", [(100, greek_yogurt), (30, oatmeal)])
    meal2 = Meal("Ham and cheese sandwich", [(50, whole_bread), (20, ham), (15, cheese)])

    meal1.meal_info()
    meal2.meal_info()