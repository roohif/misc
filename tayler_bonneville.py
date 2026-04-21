from atmosphericgradient import AtmosphericGradientMap # type: ignore
import math
import ISA
from ciddor import n

# https://x.com/taylervee_/status/2045360645403488690/photo/2

earthCurvature = -1 / (2 * 6371) * (180 / math.pi) * 3600 # Arc seconds per kilometre

########################################################################################

def FahrenheitToCelsius(f):

		return 5 / 9 * (f - 32)

########################################################################################

def FeetToMetres(ft):

	return ft * 0.3048

########################################################################################

def InHgToPa(inhg):

	return inhg * 3386.389

########################################################################################

def MilesToKilometres(mi):

	return mi * 1.60934

########################################################################################

def trial(desc, distance, lo, hi):

	gradMap = AtmosphericGradientMap(ISA.toLayers(), interval=20, cutoff=50000, wavelength=0.550, co2=425)

	nLo = n(0.550, lo["temp"], lo.get("pressure", gradMap.pressureAt(lo["elev"])), lo.get("RH", 0.20), 425)
	nHi = n(0.550, hi["temp"], hi.get("pressure", gradMap.pressureAt(hi["elev"])), hi.get("RH", 0.20), 425)

	# gradient
	span = hi["elev"] - lo["elev"]
	gradient = (nHi - nLo) / span * 1000
	lightRadius = 1 / gradient
	lightCurvature = -1 / (2 * lightRadius) * (180 / math.pi) * 3600 # Arc seconds per kilometre

	print()
	print(desc)
	print(F"IOR at Lo: {nLo:.8f}")
	print(F"IOR at Hi: {nHi:.8f}")
	print(f"Refractive Gradient: {gradient:.6f}")
	print(f"Curvature Rate: {(earthCurvature):+.1f}\" per km")
	print(f"Refraction Rate: {(lightCurvature):+.1f}\" per km")

	print()
	print(f"PREDICTIONS (dist: {distance:.2f} km)")
	print(f"GLOBE: {distance * (lightCurvature + earthCurvature):+.1f}\"")
	print(f"FLAT:  {distance * (lightCurvature):+.1f}\"")

	return

########################################################################################

# Trial 1
lo = { "temp": FahrenheitToCelsius(82.7), "elev": FeetToMetres(4222 + 2.5) }
hi = { "temp": FahrenheitToCelsius(84.2), "elev": FeetToMetres(4222 + 5.0) }
trial("TRIAL 1", MilesToKilometres(1.00961), lo, hi)

# Trial 2
lo = { "temp": FahrenheitToCelsius(87.6), "elev": FeetToMetres(4222 + 2.5), "pressure": InHgToPa(25.63), "RH": 0.201 }
hi = { "temp": FahrenheitToCelsius(86.4), "elev": FeetToMetres(4222 + 6.0), "pressure": InHgToPa(25.64), "RH": 0.209 }
trial("TRIAL 2 - Tayler's Pressure", MilesToKilometres(1.00341), lo, hi)

lo = { "temp": FahrenheitToCelsius(87.6), "elev": FeetToMetres(4222 + 2.5), "RH": 0.201 }
hi = { "temp": FahrenheitToCelsius(86.4), "elev": FeetToMetres(4222 + 6.0), "RH": 0.209 }
trial("TRIAL 2 - Standard Pressure", MilesToKilometres(1.00341), lo, hi)

# Trial 3
lo = { "temp": FahrenheitToCelsius(88.4), "elev": FeetToMetres(4222 + 2.5), "pressure": InHgToPa(25.64), "RH": 0.178 }
hi = { "temp": FahrenheitToCelsius(87.2), "elev": FeetToMetres(4222 + 6.0), "pressure": InHgToPa(25.63), "RH": 0.182 }
trial("TRIAL 3", MilesToKilometres(1.01656), lo, hi)

