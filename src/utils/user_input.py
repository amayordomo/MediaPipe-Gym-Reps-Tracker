SUPPORTED_EXERCISES = ["curls", "squats"]

def get_valid_exercise():
    while True:
        exercise = input("Enter the exercise you are doing (e.g., curls): ").lower()
        if exercise in SUPPORTED_EXERCISES:
            return exercise
        else:
            print("\tInvalid exercise. Please enter a valid exercise.")

def get_valid_reps():
    while True:
        try:
            target_reps = int(input("Enter the number of reps you want to do: "))
            if target_reps > 0:
                return target_reps
            else:
                print("\tPlease enter a positive number.")
        except ValueError:
            print("\tInvalid input. Please enter a valid number.")
