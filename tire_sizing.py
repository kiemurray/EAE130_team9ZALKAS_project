import code_variables as cv

x_cg_TO = 25.61
x_cg_aft = 27.00
x_cg_for = 24.17
x_nosewheels = 8
x_mainwheels = 28

g = cv.g
W = 56631
H = 5 #COMEBACK need distance between ground and forwardmost cg point
deceleration = 10 #keeping at 10 for normal landing, arrestor hooks on carrier will make landing easier on nose gear


# Moment Arms
Na = x_cg_aft - x_nosewheels
Nf = x_cg_for - x_nosewheels
Ma = x_mainwheels - x_cg_aft
Mf = x_mainwheels - x_cg_for
B = x_mainwheels - x_nosewheels

# Caclulating max static loads
max_static_load_main = W * Na/B 
max_static_load_nose = W * Mf/B 
min_static_load_nose = W * Ma/B
dynamic_braking_load_nose = deceleration/g * W * H/B 
total_dynamic_load_nose = max_static_load_nose + dynamic_braking_load_nose

# Add Safety Margin of 7%, divide by 2 because 2 wheels
max_static_load_main *= 1.07
max_static_load_main_perwheel = max_static_load_main / 2
max_static_load_nose_perwheel = max_static_load_nose*1.07/2
dynamic_braking_load_nose *= (1.07/2)
breakload_nose = dynamic_braking_load_nose + max_static_load_nose_perwheel

print(f"\nMax static load per wheel (main gear): {max_static_load_main_perwheel:.2f} lbs")
# print(f"Max static load (nose gear): {max_static_load_nose:.2f} lbs")
# print(f"Min static load (nose gear): {min_static_load_nose:.2f} lbs")
# print(f"Dynamic braking load (nose gear): {dynamic_braking_load_nose:.2f} lbs")
#print(f"Total dynamic load (nose gear): {total_dynamic_load_nose:.2f} lbs")
print(f"Static value load per wheel (nose gear): {max_static_load_nose_perwheel:.2f} lbs")
print(f"Braking value load per wheel (nose gear): {breakload_nose:.2f} lbs")
print(Ma/B)      # should be >0.05
print(Mf/B)      # should be <0.20 (0.08-0.15 preferred)




# Sizing tire diameter and width
diameter_main = 1.59 * (max_static_load_main_perwheel)**0.302
width_main = 0.0980 * (max_static_load_main_perwheel)**0.467
print(f"\nTire Diameter (main gear): {diameter_main:.2f} inches")
print(f"Tire Width (main gear):    {width_main:.2f} inches")



#percent on each wheels
F_mainwheels = W*(x_cg_TO-x_nosewheels)/(x_mainwheels-x_nosewheels)
F_nosewheels = W - F_mainwheels

F_mainwheelsF = W*(x_cg_for-x_nosewheels)/(x_mainwheels-x_nosewheels)
F_nosewheelsF = W - F_mainwheelsF

F_mainwheelsA = W*(x_cg_aft-x_nosewheels)/(x_mainwheels-x_nosewheels)
F_nosewheelsA = W - F_mainwheelsA

print(f"\nPercent weight on main gear: {F_mainwheels/W:.2f} lbs")
print(f"Percent weight on nose gear: {F_nosewheels/W:.2f} lbs")

print(f"\nPercent weight on main gear (fore CG): {F_mainwheelsF/W:.2f} lbs")
print(f"Percent weight on nose gear (fore CG): {F_nosewheelsF/W:.2f} lbs")

print(f"\nPercent weight on main gear (aft CG): {F_mainwheelsA/W:.2f} lbs")
print(f"Percent weight on nose gear (aft CG): {F_nosewheelsA/W:.2f} lbs")