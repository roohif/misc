import math
import argparse

EARTH_RADIUS=6371000
DEFAULT_RADIUS_MULTIPLIER = 1.20

# Create the parser
parser = argparse.ArgumentParser(description="Curve Calculator")

parser.add_argument("-o", "--observer", type=float, required=True, help="Observer height (default: metres)")
parser.add_argument("-d", "--distance", type=float, required=True, help="Target Distance (default: metres)")

ref_group = parser.add_mutually_exclusive_group()
ref_group.add_argument("-kv", type=float, help="k-value - ratio of earth radius to light radius. e.g. 0.15")
ref_group.add_argument("-rm", type=float, help="Radius Multiplier. Typical value of 1.2")
ref_group.add_argument("-lr", type=float, help="Light Radius in *KILOMETRES* not metres. Typical value of 40000")

args = parser.parse_args()

################################################################################

# Now look through the arguments to figure out refraction
if (args.kv is not None):
	light_radius = EARTH_RADIUS / args.kv
	effective_radius = 1 / (1 / EARTH_RADIUS - 1 / light_radius)
elif (args.rm is not None):
	effective_radius = EARTH_RADIUS * args.rm
elif (args.lr is not None):
	effective_radius = 1 / (1 / EARTH_RADIUS - 1 / (args.lr * 1000))
else:
	effective_radius = EARTH_RADIUS * DEFAULT_RADIUS_MULTIPLIER

print(f"Effective Radius: {effective_radius:.2f} m")

################################################################################


# Step 1. Calculate the distance to the horizon from the observer
central_angle = math.acos(effective_radius / (effective_radius + args.observer))
horizon_distance = central_angle * effective_radius

print(f"Horizon Distance: {horizon_distance:.2f} m")

# Step 2. How much distance remains, and how high is the tangent at that distance?
if (args.distance < horizon_distance):
	print(f"Target is in front of the horizon. Zero hidden")
	quit()

remaining_distance = args.distance - horizon_distance
central_angle = remaining_distance / effective_radius
hidden_height = (effective_radius - effective_radius * math.cos(central_angle)) / math.cos(central_angle)

print(f"Hidden Height: {hidden_height:.2f} m")



