#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_COLOR_SHADER

uniform vec2 resolution;
uniform float time;

varying vec4 vertColor;

void main()
{
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    uv.y = 1.0 - uv.y;
    float offset = 200.0;
    vec2 pos1 = vec2((resolution.x / 2.0 + offset) * time - offset, resolution.y / 2.0) / resolution.xy;
    vec2 pos2 = vec2((resolution.x / 2.0 + offset) * (1 - time) + resolution.x / 2.0, resolution.y / 2.0) / resolution.xy;

    float r1 = (dot(uv - pos1, uv - pos1)) * (8.0 - 7.0 * pow(time, 4.0));
    float r2 = (dot(uv - pos2, uv - pos2)) * (8.0 - 7.0 * pow(time, 4.0));
    float metaball = (1.0 / r1 + 1.0 / r2);
    float col = pow(metaball, 16.0);

    gl_FragColor = vec4(col, col, col, 1.0);
}
