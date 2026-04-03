import code_variables as cv

x_cg_TO = 25.61
x_cg_aft = 27.00
x_cg_for = 24.17
x_nosewheels = 9.75
x_mainwheels = 29
W = 56631
H = 5 #COMEBACK need distance between ground and forwardmost cg point
deceleration = 10
g = cv.g

# Moment Arms
Na = x_cg_aft - x_nosewheels
Nf = x_cg_for - x_nosewheels
Ma = x_mainwheels - x_cg_aft
Mf = x_mainwheels - x_cg_for
B = x_mainwheels - x_nosewheels

max_static_load_main = W * Na/B
max_static_load_nose = W * Mf/B
min_static_load_nose = W * Ma/B
dynamic_braking_load_nose = deceleration/g * W * H/B # COMEBACK 0.31 is for 10ft/s decel, we will probably be higher

print(f"\nMax static load (main gear): {max_static_load_main:.2f}")
print(f"Max static load (nose gear): {max_static_load_nose:.2f}")
print(f"Min static load (nose gear): {min_static_load_nose:.2f}")
print(f"Dynamic braking load (nose gear): {dynamic_braking_load_nose:.2f}")
print(Ma/B)      # should be >0.05
print(Mf/B)      # should be <0.20 (0.08-0.15 preferred)

F_mainwheels = W*(x_cg_TO-x_nosewheels)/(x_mainwheels-x_nosewheels)
F_nosewheels = W - F_mainwheels

print(f"\nF main gear: {F_mainwheels:.2f} lbs")
print(f"F nose gear: {F_nosewheels:.2f} lbs")