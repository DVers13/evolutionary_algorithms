import streamlit as st
import matplotlib.pyplot as plt
from differential_evolution import differential_evolution
import time

def plot_route(points, route):
    print(points)
    fig, ax = plt.subplots()
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    ax.plot(x[:], y[:], 'bo')
    ax.plot(x[route[0]], y[route[0]], 'ro')

    for i in range(len(route) - 1):
        ax.plot([x[route[i]], x[route[i + 1]]], [y[route[i]], y[route[i + 1]]], 'r-')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Points and Route')
    ax.grid(True)
    st.pyplot(fig)

def main():
    st.title('Differential Evolution TSP Solver')
    population_count = st.slider('Population Count', min_value=10, max_value=500, value=20, step=1)
    iterations = st.slider('Iterations', min_value=0, max_value=20000, value=10, step=1)
    c = st.slider('C', min_value=0.1, max_value=1.0, value=0.7, step=0.01)
    F = st.slider('F', min_value=0.1, max_value=1.0, value=0.9, step=0.01)

    st.subheader('Upload Data File:')
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        try:
            entry = [list(map(int, line.strip().split())) for line in content.splitlines()]
        except Exception as e:
            st.error(f'Error: {e}')
            return
    if st.button('Run Algorithm'):
        try:
            d_evol = differential_evolution(population_count, iterations, c, F)
            start_time = time.time()
            road, dist = d_evol.run(entry)
            end_time = time.time()
            execution_time = end_time - start_time
            st.write('Best route:', ', '.join(map(str, road)))
            st.write('Distance:', dist)
            st.write('Execution Time:', execution_time, 'seconds')
            plot_route(entry, road)
        except Exception as e:
            st.error(f'Error: {e}')

if __name__ == "__main__":
    main()
