sentence = 'there is a bird in the tall tree in front of my houes .'
screen_width = 80;
text_width = len(sentence)
box_width = text_width + 6
left_margin = (screen_width - box_width)//2
print('')
print( ' ' * left_margin + '+'  + '-' * (box_width-4) +  '+')
print( ' ' * left_margin + '| ' + ' ' * text_width    + ' |')
print( ' ' * left_margin + '| ' +       sentence      + ' |')
print( ' ' * left_margin + '| ' + ' ' * text_width    + ' |')
print( ' ' * left_margin + '+'  + '-' * (box_width-4) +  '+')
print('')
