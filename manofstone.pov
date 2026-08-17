#version 3.7;

global_settings {
    assumed_gamma 1.0
    max_trace_level 100
    ambient_light rgb <1, 1, 1>
}

#include "colors.inc"
#include "stones.inc"

// Place the shadow wall a few metres away
#declare SHADOW_WALL_DISTANCE = 6;

// How tall is the observer
#declare OBSERVER_HEIGHT = 1.6;

#declare WINDOW_CENTRE = 2.5;

#declare to_radians = function (x) { x * pi / 180 };

// Floor
plane {
	y, 0
	texture { T_Grnt0 }
}

// Place the "vertex" wall at the origin
difference {
	box {
		<-2, 0, -0.1>,	// Bottom left
		<2, 4, 0.1> // Top right 		
	}
	
	box {
		<-0.5, WINDOW_CENTRE - 0.5, -0.2>,
		<0.5, WINDOW_CENTRE + 0.5, 0.2>
	}

	texture {
		pigment { color rgb <0.8, 0.8, 0.8> }
	}
}


// cylinders for the cross-frame
cylinder {
	<-0.5, WINDOW_CENTRE, 0>,
	<0.5, WINDOW_CENTRE, 0>,
	0.02
    
	texture {
		pigment { color rgb <0.8, 0.8, 0.8> }
    }
}

cylinder {
	<0, WINDOW_CENTRE - 0.5, 0>,
	<0, WINDOW_CENTRE + 0.5, 0>,
	0.02
    
	texture {
		pigment { color rgb <0.8, 0.8, 0.8> }
    }
}

box {
	<-2, 0, SHADOW_WALL_DISTANCE>,
	<2, 4, SHADOW_WALL_DISTANCE + 0.2>
	
	texture {
		pigment { color rgb <0.8, 0.8, 0.8> }
	}
}

// Tiny red line on the wall
cylinder {
	<-2, WINDOW_CENTRE - 0.5, SHADOW_WALL_DISTANCE>,
	<2, WINDOW_CENTRE - 0.5, SHADOW_WALL_DISTANCE>,
	0.01
	
	texture {
		pigment { rgb <1, 0, 0> }
	}
}  

// Place Stone's 16m obstruction, 1390 metres away
box {
	<-1, 0, -1390>,
	<1, 16, -1389>
	
	texture {
		pigment { color rgb <1, 1, 1> }
	}
}

// Using the clock, I want to move the sun from say five degrees
// down to horizontal.
#local sun_angle = 1.0 - (clock * 0.5); // 1.0 down to 0.5 degrees
#local sun_distance = 2000;
#local sun_height = sun_distance * tan(to_radians(sun_angle));
#debug concat("\n\n\n\nSun: ", str(sun_height, 0, 3), "\n\n\n\n")


// I can either use the "parallel" keyword, or increase the intensity
// of light by using "rgb <100, 100, 100>". Same effect
light_source {
	<0, sun_height, -sun_distance>,
	color rgb <1, 1, 1> // Intensity AND colour
	parallel
}

camera {
    location <10, OBSERVER_HEIGHT, -5>
    look_at <0, OBSERVER_HEIGHT, SHADOW_WALL_DISTANCE / 2>
    angle 60
}
 
//Set a background color
background { color rgb <0.5, 0.5, 0.9> }
