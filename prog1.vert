#version 330 core

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

in vec4 color;
in vec3 position;
in mat4 translation;

// varying variables need to be in/out in core context
out vec3 v_position;
out vec4 v_color;

mat4 pvm = projection*view*translation*model;

void main() {
    gl_Position = pvm*vec4(position, 1.0);
    v_color = color;
    v_position = position;
}