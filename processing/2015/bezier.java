<html>
    <head>
        <title>Bezier Game</title>
        <script type="text/javascript" src="https://cloud.github.com/downloads/processing-js/processing-js/processing-1.4.1.js"></script>

        <script type='text/javascript'>
        var resizeCanvas = function() {
            var canv = Processing.getInstanceById('pjs');
            canv.size(window.innerWidth, window.innerHeight);
        }
        </script>

        <script type="application/processing" data-processing-target="pjs">
        color active_color = color(255, 0, 0);
        color passive_color = color(80);
        color win_color = color(0, 255, 0);
        color bg_color = color(0);
        color text_color = color(200);

        int w = 500;
        int h = 500;
        int rad = 30;
        int score;
        int drawing_mode;
        boolean blinking;
        float blinking_time = 0.0;

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

        Point active_point;
        ArrayList<MCurve> mcurves;

        boolean check()
        {
          PGraphics pg = createGraphics(width, height);
          pg.beginDraw();
          pg.background(0);
          pg.noStroke();
          pg.fill(100, 60);
          
          for (MCurve mcurve : mcurves)
          {
            pg.bezier(mcurve.a.xpos + width / 2, mcurve.a.ypos + height / 2,
                   mcurve.b.xpos + width / 2, mcurve.b.ypos + height / 2,
                   mcurve.c.xpos + width / 2, mcurve.c.ypos + height / 2,
                   mcurve.d.xpos + width / 2, mcurve.d.ypos + height / 2);
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
          return true;
        }

        void draw_playing()
        {
          background(bg_color);
          noStroke();
          
          for (MCurve mcurve : mcurves)
          {
            for (Point p : mcurve.points)
            {
              if (p.is_active)
              {
                fill(active_color);
                ellipse(p.xpos + width / 2, p.ypos + height / 2, rad, rad);
              }
              else if (!p.is_static)
              {
                fill(passive_color);
                ellipse(p.xpos + width / 2, p.ypos + height / 2, rad, rad);
              }
            }
          }

          stroke(255);
          for (MCurve mcurve : mcurves)
          {
            noFill();
            bezier(mcurve.a.xpos + width / 2, mcurve.a.ypos + height / 2,
                   mcurve.b.xpos + width / 2, mcurve.b.ypos + height / 2,
                   mcurve.c.xpos + width / 2, mcurve.c.ypos + height / 2,
                   mcurve.d.xpos + width / 2, mcurve.d.ypos + height / 2);
          }
          
          fill(text_color);
          textAlign(CENTER);
          textSize(30);
          text("UNTANGLE IT", width / 2, 40);
          textSize(20);
          text("TIME: " + score, width / 2, height - 35);
          if (blinking)
          {
            fill(active_color);
            blinking_time -= 1 / frameRate;
            if (blinking_time < 0)
            {
              blinking_time = 0.0;
              blinking = false;
            }
          }
          text("PRESS C TO CHECK", width / 2, height - 15);
          
          if ((frameCount % 6) == 0)
            score += 1;
        }

        void draw_finished()
        {
          background(bg_color);
          stroke(255);

          pushMatrix();
          translate(width / 2, height / 2);
          rotate((frameCount % 800.0) / 800.0 * TWO_PI);
          
          for (MCurve mcurve : mcurves)
          {
            noFill();
            bezier(mcurve.a.xpos, mcurve.a.ypos,
                   mcurve.b.xpos, mcurve.b.ypos,
                   mcurve.c.xpos, mcurve.c.ypos,
                   mcurve.d.xpos, mcurve.d.ypos);
          }
          popMatrix();
          
          fill(win_color);
          textAlign(CENTER);
          textSize(30);
          text("CONGRATULATIONS!", width / 2, 40);
          textSize(20);
          text("YOUR BEST TIME: " + score, width / 2, height - 35);
          text("PRESS N TO START A NEW GAME", width / 2, height - 15);
        }

        void reset_all()
        {
          float n = 12.0;
          int r = 100;
          mcurves = new ArrayList<MCurve>();
          
          float prev_point_x = r * cos(0);
          float prev_point_y = r * sin(0);
          for (int i = 0; i < n; i++)
          {
            float next_point_x = r * cos((i + 1) / n * TWO_PI);
            float next_point_y = r * sin((i + 1) / n * TWO_PI);
            
            Point a = new Point(prev_point_x, prev_point_y, false, true);
            Point b = new Point(random(w - rad) + rad / 2 - w / 2, random(h - rad) + rad / 2 - h / 2, false, false);
            Point c = new Point(random(w - rad) + rad / 2 - w / 2, random(h - rad) + rad / 2 - h / 2, false, false);
            Point d = new Point(next_point_x, next_point_y, false, true);

            MCurve mcurve = new MCurve(a, b, c, d);
            
            mcurves.add(mcurve);
            prev_point_x = next_point_x;
            prev_point_y = next_point_y;
          }
          
          score = 0;
          drawing_mode = 0;
          blinking = false;
        }

        void keyPressed()
        {
          if ((key == 'c') && (drawing_mode == 0))
            {
              if (check())
                drawing_mode = (drawing_mode + 1) % 2;
              else
              {
                blinking = true;
                blinking_time = 3.0;
              }
            }
          else if ((key == 'n') && (drawing_mode == 1))
            reset_all();
        }

        void mouseDragged()
        {
          if (active_point != null)
          {
            active_point.xpos = constrain(mouseX, rad / 2, width - rad / 2) - width / 2;
            active_point.ypos = constrain(mouseY, rad / 2, height - rad / 2) - height / 2;
          }
        }

        void mousePressed()
        {
          Point closest = null;
          float min_dist = 99999999.9;
          for (MCurve mcurve : mcurves)
          {
            for (Point p : mcurve.points)
            {
              float dist = sqrt(pow(p.xpos - mouseX + width / 2, 2) + pow(p.ypos - mouseY + height / 2, 2));
              if ((dist < rad) && !p.is_static && dist < min_dist)
              {
                min_dist = dist;
                closest = p;
              }
            }
          }
          if (closest != null)
          {
            closest.is_active = true;
            active_point = closest;
          }
        }

        void mouseReleased()
        {
          if (active_point != null)
          {
            active_point.is_active = false;
            active_point = null;
          }
        }

        void setup()
        {
          size(640, 360);
          reset_all();
        }

        void draw()
        {
          if (drawing_mode == 0)
            draw_playing();
          else
            draw_finished();
        }
        </script>
    </head>
    <body onload="resizeCanvas();" onresize="resizeCanvas();" style="margin: 0;padding: 0;">
        <canvas id="pjs"></canvas>
    </body>
</html>
