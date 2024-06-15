import random
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import matplotlib.patches as patches

def generate_field(width, height, num_special_cells):

    field = np.array([['.' for _ in range(width)] for _ in range(height)])
    apple = random.choices([(i, j) for i in range(width) for j in range(height)], k = num_special_cells)
    for y, x in apple:
        field[y][x] = "S"
    return field

def plot_field(field):
    color_map = {
    '.': [255,255,255],
    'S': [245, 2, 19],
    'R': [192,192,192],
    'M' : [156, 123, 3],
    '*': [0,0,0]}
    field_color = np.array([[color_map[cell] for cell in row] for row in field])
    fig, ax = plt.subplots()
    ax.imshow(field_color, aspect='equal')
    rows, cols = len(field), len(field[0])
    for i in range(rows):
        for j in range(cols):
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=1, edgecolor='gray', facecolor='none')
            ax.add_patch(rect)
    ax.axis('off')
    st.pyplot(fig)