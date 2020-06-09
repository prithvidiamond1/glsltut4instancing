#version 330 core

// varying variables need to be in/out in core context
in vec3 v_position;
in vec4 v_color;

// output variables are required as variables like gl_FragColor is deprecated in core context
out vec4 FragColor;

void main() {
    float xy = min(abs(v_position.x), abs(v_position.y));
    float xz = min(abs(v_position.x), abs(v_position.z));
    float yz = min(abs(v_position.y), abs(v_position.z));

    float b_width1 = 0.04;
    float b_width2 = 0.04;
    float c_width = 0.22;

    float border1 = 1-b_width1;
    float border2 = (1-(b_width1+c_width));
    float border3 = (1-(b_width1+b_width2+c_width));

    if ((xy > border1) || (xz > border1) || (yz > border1)) {
        FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
    else if ((xy > border2) || (xz > border2) || (yz > border2)) {
        FragColor = v_color;
    }
    else if ((xy > border3) || (xz > border3) || (yz > border3)) {
        FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
    else {
        discard;
    }
}