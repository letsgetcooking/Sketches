#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_COLOR_SHADER

uniform float time;
uniform vec2 resolution;

uniform vec2 size;

varying vec4 vertColor;

vec3 hsvToRgb(vec3 hsv)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(hsv.xxx + K.xyz) * 6.0 - K.www);
    return hsv.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), hsv.y);
}

void main()
{
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    uv.y = 1.0 - uv.y;
    vec2 pos1 = vec2(resolution.x / 4.0, resolution.y / 4.0) / resolution.xy;
    vec2 pos2 = vec2(5.0 * resolution.x / 6.0, resolution.y / 4.0) / resolution.xy;
    vec2 pos3 = vec2(-resolution.x / 6.0, resolution.y / 7.0) / resolution.xy;
    vec2 pos4 = vec2(4.0 * resolution.x / 3.0, resolution.y / 4.0) / resolution.xy;
    vec2 pos5 = vec2(resolution.x / 2.0, 6.0 * resolution.y / 5.0) / resolution.xy;
    vec2 pos6 = vec2(-resolution.x / 9.0, resolution.y / 2.0) / resolution.xy;
    vec2 pos7 = vec2(10.0 * resolution.x / 9.0, resolution.y / 2.0) / resolution.xy;
    
    float dist1 = length(uv.xy - pos1.xy);
    float dist2 = length(uv.xy - pos2.xy);
    float dist3 = length(uv.xy - pos3.xy);
    float dist4 = length(uv.xy - pos4.xy);
    float dist5 = length(uv.xy - pos5.xy);
    float dist6 = length(uv.xy - pos6.xy);
    float dist7 = length(uv.xy - pos7.xy);
    
    float scale = resolution.x / size.x;
    
    vec3 hsv = vec3(mod(dist1 * dist2 / dist3 / dist4 / dist5 / dist6 / dist7 * scale + 0.5 * sin(time) + position1.y, 1.0), 1.0, 1.0);
    vec3 color = hsvToRgb(hsv);
    gl_FragColor = vec4(color, 1.0);
}
