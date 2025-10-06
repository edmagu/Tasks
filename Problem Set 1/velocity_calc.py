import math #Normal one

def velocity_calc():
    
    distance = float(input("What is the distance the ball has traveled in meters: "))
    time = float(input("How long did it take the ball to travel that distance in seconds: "))

    d = distance
    t = time
    velocity = d/t
    print(f"The velocity of the ball is {round(velocity, 2)}m/s")

if __name__ == "__main__":
    velocity_calc()


