#!/usr/bin/env python
# coding: utf-8

# In[65]:


#!/usr/bin/env python3
import PIL
import dateutil.parser as dp
import datetime
from IPython.display import Image
from PIL import ImageFont
from collections import defaultdict


# In[76]:


life_expectancy = 80
weeks_in_life = 52 * life_expectancy
birth = dp.parse('1989-12-02')
elapsed = datetime.datetime.now() - birth
elapsed_weeks = int(elapsed.days / 7)


# # Define milestones

# In[106]:


milestone_list = [
    ("born", "1989-12-02"),
    ("start uni", "2012-09-20"),
    ("bought house", "2019-09-26"),
    ("turned 30", "2019-12-02")
]
milestones = defaultdict(list)
for thing, when in milestone_list:
    when_weekno = int(((dp.parse(when) - birth).days) / 7)
    milestones[when_weekno].append((thing, when))

milestones


# # Define calendar parameters

# In[114]:


weeks_per_row = 52 # 1 'season', 3 months
num_rows = int(weeks_in_life / weeks_per_row)

cube_size = 10 # px
offset = 50 # Margin top, right, bottom ,left

def size_calc(size, n_items, padding, offset):
    # *2 as we're using 'SIZE' as padding
    # so it's ... offset + [SIZEsize x N] + offset ...
    # minus one cube (as we don't need padding after final cube)
    item_size = (size * n_items * 2) - size
    return int(offset + item_size + offset)

calendar_width = size_calc(cube_size, weeks_per_row, padding, offset)
calendar_height = size_calc(cube_size, num_rows, padding, offset)

num_milestone_rows = len(milestones.keys())
calendar_height += int(num_milestone_rows * 15 + (num_milestone_rows - 1) * 15)

print(f"{calendar_width}x{calendar_height}")


# In[115]:


font = ImageFont.truetype('nas/archive/CaslonAntique.ttf', 30)
font_small = ImageFont.truetype('nas/archive/CaslonAntique.ttf', 24)


# # Draw calendar

# In[118]:


bg = (240, 240, 240)
im = PIL.Image.new('RGB', (calendar_width, calendar_height), bg)
draw = PIL.ImageDraw.Draw(im)

colour_milestone = [(182, 30, 252), (80, 0, 117)]
colour_done = [(100, 100, 100), None]
colour_todo = [(255,255,255), (100, 100, 100)]

i = 0
for row in range(num_rows):
    for col in range(weeks_per_row):
        x = offset + (col * cube_size) + (col * padding)
        y = offset + (row * cube_size) + (row * padding)
        if i in milestones:
            draw.rectangle((x, y, x+cube_size, y+cube_size), fill=colour_milestone[0], outline=colour_milestone[1])
        else:
            if i < elapsed_weeks:
                draw.line((x, y, x+cube_size+1, y+cube_size), fill=colour_done[0], width=1)
                draw.line((x+cube_size, y, x, y+cube_size), fill=colour_done[0], width=1)
            else:
                draw.rectangle((x, y, x+cube_size, y+cube_size), fill=colour_todo[0], outline=colour_todo[1])
        i += 1
#     break
y_text_offset = offset + (num_rows * cube_size) + (num_rows * padding) + 15
for i, weekno in enumerate(sorted(milestones.keys())):
    stuff = milestones[weekno]
    text = ', '.join([' '.join([date, thing]) for thing, date in stuff])
    y = y_text_offset + (i * 24)
    x = offset
    draw.text((x, y), text, font=font_small, align="Left", fill=(0, 0, 0))
draw.text((offset, 5), "Weeks of Life Calendar - Chris Davison", font=font, align="Left", fill=(0,0,0))
display(im)

im.save('life-calendar.png')

