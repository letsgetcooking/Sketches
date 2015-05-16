#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXTURE_SHADER


uniform sampler2D texture;
uniform vec2 resolution;

varying vec4 vertColor;
varying vec4 vertTexCoord;


float bump(float x) {
    return abs(x) > 1.0 ? 0.0 : 1.0 - x * x;
}

void main()
{
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    
    float c = 3.0;
    vec3 color = vec3(1.0);
    color.x = bump(c * (uv.x - 0.885));
    color.y = bump(c * (uv.x - 0.5));
    color.z = bump(c * (uv.x - 0.115));
    
    float line = abs(0.01 / abs(0.5-uv.y) );
    uv.y = abs( uv.y - 0.5 );
    
    vec4 soundWave =  texture2D( texture, vec2(uv.x, 0.5 - uv.y) );
    color *= line * (1.0 - 2.0 * abs( 0.5 - uv.xxx ) + pow( soundWave.y, 10.0 ) * 30.0 );
    
    gl_FragColor = vec4(color, 1.0);
}
