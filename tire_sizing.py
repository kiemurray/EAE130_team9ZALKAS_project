x_cg_TO = 25.61
x_cg_aft = 27.00
x_cg_for = 24.17
x_nosewheel = 9.75
x_mainwheels = 29
W = 56631

F_mainwheels = W*(x_cg_TO-x_nosewheel)/(x_mainwheels-x_nosewheel)
F_nosewheels = W - F_mainwheels

print(f"\nF main gear: {F_mainwheels:.2f} lbs")
print(f"F nose gear: {F_nosewheels:.2f} lbs")