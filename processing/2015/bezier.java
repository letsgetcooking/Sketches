color active_color = color(255, 0, 0);
color passive_color = color(255);
color passive_color_static = color(35);
color bg_color = color(0);

int rad = 10;
int score;
int drawing_mode;

class Point
{
  float xpos, ypos;
  boolean is_active, is_static;

  Point(float x, float y, boolean active_state, boolean static_state)
  {
    xpos = x;
    ypos = y;
    is_active = active_state;
    is_static = static_state;
  }
}

class MCurve
{
  Point a, b, c, d;
  Point[] points;

  MCurve(Point a_point, Point b_point, Point c_point, Point d_point)
  {
    a = a_point;
    b = b_point;
    c = c_point;
    d = d_point;
    
    points = new Point[4];
    points[0] = a_point;
    points[1] = b_point;
    points[2] = c_point;
    points[3] = d_point;
  }
}

ArrayList<MCurve> mcurves;

boolean check()
{
  PGraphics pg = createGraphics(width, height);
  pg.beginDraw();
  pg.background(bg_color);
  pg.noStroke();
  pg.fill(100, 60);
  
  for (MCurve mcurve : mcurves)
  {
    pg.bezier(mcurve.a.xpos, mcurve.a.ypos,
              mcurve.b.xpos, mcurve.b.ypos,
              mcurve.c.xpos, mcurve.c.ypos,
              mcurve.d.xpos, mcurve.d.ypos);
  }
  
  pg.endDraw();
  
  float max_brightness = 0.0;
  pg.loadPixels();
  for (color pixel : pg.pixels)
  {
    float br = brightness(pixel);
    if (br > max_brightness)
      max_brightness = br;
  }
  
  if (max_brightness > 30.0)
    return false;
  else
    return true;
}

void draw_playing()
{
  background(bg_color);
  stroke(255);
  
  for (MCurve mcurve : mcurves)
  {
    noFill();
    bezier(mcurve.a.xpos, mcurve.a.ypos,
           mcurve.b.xpos, mcurve.b.ypos,
           mcurve.c.xpos, mcurve.c.ypos,
           mcurve.d.xpos, mcurve.d.ypos);
           
    for (Point p : mcurve.points)
    {
      if (p.is_active)
        fill(active_color);
      else if (p.is_static)
        fill(passive_color_static);
      else
        fill(passive_color);
      ellipse(p.xpos, p.ypos, rad, rad);
    }
  }
  
  fill(200);
  textSize(18);
  textAlign(LEFT);
  text("SCORE: " + score, 10, height - 35);
  text("PRESS C TO CHECK", 10, height - 15);
  
  if ((frameCount % 6) == 0)
    score += 1;
}

void draw_finished()
{
  background(bg_color);
  stroke(255);
  
  for (MCurve mcurve : mcurves)
  {
    noFill();
    bezier(mcurve.a.xpos, mcurve.a.ypos,
           mcurve.b.xpos, mcurve.b.ypos,
           mcurve.c.xpos, mcurve.c.ypos,
           mcurve.d.xpos, mcurve.d.ypos);
  }
  
  fill(active_color);
  textAlign(CENTER);
  textSize(72);
  text(score, width / 2, height / 2);
  textSize(20);
  text("PRESS N TO START A NEW GAME", width / 2, height / 2 + 25);
}

void keyPressed()
{
  if ((key == 'c') && (check()))
    drawing_mode = (drawing_mode + 1) % 2;
  else if ((key == 'n') && (drawing_mode == 1))
    setup();
}

void mouseDragged()
{
  for (MCurve mcurve : mcurves)
  {
    for (Point p : mcurve.points)
    {
      if (p.is_active)
      {
        p.xpos = constrain(mouseX, rad / 2, width - rad / 2);
        p.ypos = constrain(mouseY, rad / 2, height - rad / 2);
        return;
      }
    }
  }
}

void mousePressed()
{
  for (MCurve mcurve : mcurves)
  {
    for (Point p : mcurve.points)
    {
      if ((sqrt(pow(p.xpos - mouseX, 2) + pow(p.ypos - mouseY, 2)) < rad)
        && !p.is_static)
      {
        p.is_active = true;
        return;
      }
    }
  }
}

void mouseReleased()
{
  for (MCurve mcurve : mcurves)
  {
    mcurve.a.is_active = false;
    mcurve.b.is_active = false;
    mcurve.c.is_active = false;
    mcurve.d.is_active = false;
  }
}

void setup()
{
  size(640, 360);
  
  float n = 12.0;
  int r = 100;
  mcurves = new ArrayList<MCurve>();
  
  float prev_point_x = r * cos(0) + width / 2;
  float prev_point_y = r * sin(0) + height / 2;
  for (int i = 0; i < n; i++)
  {
    float next_point_x = r * cos((i + 1) / n * TWO_PI) + width / 2;
    float next_point_y = r * sin((i + 1) / n * TWO_PI) + height / 2;
    
    Point a = new Point(prev_point_x, prev_point_y, false, true);
    Point b = new Point(random(width - rad) + rad / 2, random(height - rad) + rad / 2, false, false);
    Point c = new Point(random(width - rad) + rad / 2, random(height - rad) + rad / 2, false, false);
    Point d = new Point(next_point_x, next_point_y, false, true);

    MCurve mcurve = new MCurve(a, b, c, d);
    
    mcurves.add(mcurve);
    prev_point_x = next_point_x;
    prev_point_y = next_point_y;
  }
  
  score = 0;
  drawing_mode = 0;
}

void draw()
{
  if (drawing_mode == 0)
  {
    draw_playing();
  }
  else
  {
    draw_finished();
  }
}
