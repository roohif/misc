import math
import keyboard

# Three body simulator: Sun, Earth, Moon
# Ignore the sun - it's orders of magnitude larger in mass

# Big G
G = 6.674008E-11

# Three three bodies
SUN = { "M": 1.989E+30, "X": 0.0, "Y": 0.0, "Vx": 0.0, "Vy": 0.0 } # Start the sun at the Centre
EARTH = { "M": 5.972E+24, "X": 1.521E+11, "Y": 0.0, "Vx": 0.0, "Vy": 2.9295E+4 } # Approx 30 km/s

# Place the moon in relation to the earth
MOON = {
	"M": 7.348E+22,
	"X": EARTH["X"] + 4.11E+8, # 3.844E+8,
	"Y": 0.0, # Start when all three bodies are in perfect alignment (2D)
	"Vx": 0.0,
	"Vy": EARTH["Vy"] + 9.65E+2 # 1.022E+3
}

################################################################################

def distance(a, b):

	x_dist = a["X"] - b["X"]
	y_dist = a["Y"] - b["Y"]

	return math.sqrt(x_dist**2 + y_dist**2)

################################################################################

def acceleration(a, b):

	# What is the acceleration vector that A exerts on B
	d = distance(a, b)
	
	dX = a["X"] - b["X"]
	dY = a["Y"] - b["Y"]

	# Return an X/Y acceleration tuple
	magnitude = G * a["M"] / d**2
	polarAngle = math.atan2(dY, dX)

	return (magnitude * math.cos(polarAngle), magnitude * math.sin(polarAngle))

################################################################################

timer = 0 # Seconds
interval = 60 # Every X seconds

while (True):

	# What forces are exerted on the EARTH
	SunEarthAcc = acceleration(SUN, EARTH)
	MoonEarthAcc = acceleration(MOON, EARTH)

	TotalAcc = (SunEarthAcc[0] + MoonEarthAcc[0], SunEarthAcc[1] + MoonEarthAcc[1])

	# Apply this acceleration to the velocity of the EARTH
	EARTH["Vx"] = EARTH["Vx"] + (TotalAcc[0] * interval)
	EARTH["Vy"] = EARTH["Vy"] + (TotalAcc[1] * interval)

	# Apply the velocity to the position
	EARTH["X"] = EARTH["X"] + EARTH["Vx"] * interval
	EARTH["Y"] = EARTH["Y"] + EARTH["Vy"] * interval


	# What forces are exerted on the MOON
	SunMoonAcc = acceleration(SUN, MOON)
	EarthMoonAcc = acceleration(EARTH, MOON)

	TotalAcc = (SunMoonAcc[0] + EarthMoonAcc[0], SunMoonAcc[1] + EarthMoonAcc[1])

	# Apply this acceleration to the velocity of the MOON
	MOON["Vx"] = MOON["Vx"] + (TotalAcc[0] * interval)
	MOON["Vy"] = MOON["Vy"] + (TotalAcc[1] * interval)

	# Apply the velocity to the position
	MOON["X"] = MOON["X"] + MOON["Vx"] * interval
	MOON["Y"] = MOON["Y"] + MOON["Vy"] * interval

	# Print the new positions, velocities, etc.
	sunDist = distance(SUN, EARTH) / 1E+9
	moonDist = distance(MOON, EARTH) / 1E+6
	moonDistSun = distance(SUN, MOON) / 1E+9

	speed = math.sqrt(EARTH["Vx"]**2 + EARTH["Vy"]**2)
	days = timer / 60 / 60 / 24

	print(f"\r*EARTH* Distance: {sunDist:5.2f}M km Speed: {speed:5.2f} m/s {days:4.2f} days    *MOON* Distance {moonDist:5.2f}k km {moonDistSun:5.2f}M km", end="")

	if keyboard.is_pressed('esc'):
		print("\nExiting...")
		break

	timer += interval

