import numpy as np
import matplotlib.pyplot as plt

# Mission profile points
range_nmi = np.array([0, 20, 100, 800, 825, 875, 955, 1655, 1675, 1725, 1750, 1800])
altitude_ft = np.array([0, 0, 30000, 30000, 0, 0, 30000, 30000, 10000, 10000, 0, 0])

fig, ax = plt.subplots(figsize=(10,5))

# Plot mission profile
ax.plot(range_nmi, altitude_ft, color='black', linewidth=2)

# Phase definitions
phases = [
    (0, 20,  "#C2F0C1", "Taxi & Takeoff"),
    (20, 100,"#0B9910", "Climb"),
    (100, 800, "#61F17B", "Cruise"),
    (800, 825, "#187035", "Descent"),
    (825, 875, "#07200C", "Strike"),
    (875, 955, "#0B9910", "Climb"),
    (955, 1655, "#61F17B", "Cruise"),
    (1655, 1675, "#187035", "Descent"),
    (1675, 1725, "#23BB86", "Loiter"),
    (1725,1750, "#187035", "Descent"),
    (1750, 1800, "#C4FFF9", "Landing")
]

# Fill from x-axis to the mission line
for start, end, color, label in phases:
    mask = (range_nmi >= start) & (range_nmi <= end)
    ax.fill_between(range_nmi[mask],
                    altitude_ft[mask],
                    -1000,
                    color=color,
                    alpha=0.75,
                    label=label)

# Labels
ax.set_yticks([0,10000,20000,30000])
ax.set_yticklabels(["Sea Level","10k","20k","30k"])
ax.set_xlabel("Range (nmi)")
ax.set_ylabel("Altitude (ft)")
ax.set_title("Aircraft Strike Mission Profile")

# Remove duplicate legend labels
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), loc="upper right")
plt.ylim(-1000,33000)
ax.axhline(y=0, color='k', linestyle='--', linewidth=1)
ax.axhline(y=10000, color='k', linestyle='--', linewidth=1)
ax.axhline(y=30000, color='k', linestyle='--', linewidth=1)

# Add label
plt.show()