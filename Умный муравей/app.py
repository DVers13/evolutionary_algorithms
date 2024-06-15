import streamlit as st
import matplotlib.pyplot as plt
import time
from field_generate import generate_field, plot_field
from ga_3 import GA
from ant import Ant
import pandas as pd

def load_field(uploaded_file):
    content = uploaded_file.read().decode('utf-8')
    field = eval(content)
    return field


def main():
    st.title('Ant')
    population_count = st.slider('Population Count', min_value=2, max_value=100, value=20, step=1)
    count_state = st.slider('count_state', min_value=1, max_value=50, value=10, step=1)
    best_solution_count = st.slider('best_solution_count Count', min_value=1, max_value=50, value=5, step=1)
    iterations = st.slider('Iterations', min_value=0, max_value=1000, value=10, step=5)
    coef_m = st.slider('coef_m', min_value=0.01, max_value=1.0, value=0.7, step=0.01)
    coef_c = st.slider('coef_c', min_value=0.01, max_value=1.0, value=0.9, step=0.01)

    if st.button('Generate field'):
        try:
            field = generate_field(32, 32, 89)
            st.session_state.field = field
        except Exception as e:
            st.error(f'Error: {e}')
    field_file = st.file_uploader("Upload field file", type="txt")

    if field_file is not None:
        field = load_field(field_file)
        st.write("Field loaded successfully")
        st.session_state.field = field

    if 'field' in st.session_state:
        st.subheader('Generated Field:')
        plot_field(st.session_state.field)

    if st.button('Run Algorithm'):
        try:
            if 'field' not in st.session_state:
                st.error('Please generate the field first.')
                return
            field = st.session_state.field
            GA_evol = GA(population_count = population_count, count_state = count_state, best_solution_count = best_solution_count, iter = iterations, field = field, coef_m = coef_m, coef_c = coef_c)
            start_time = time.time()
            _, best_automat = GA_evol.run()
            end_time = time.time()
            execution_time = end_time - start_time
            st.write('Best automat:')
            best_automat_df = pd.DataFrame(
                [(i[0], i[1], i[2], 2) for i in best_automat],
                columns=['State_0', 'Action_0', 'State_1', 'Action_1']
            )
            st.table(best_automat_df)
            ant = Ant(field, max_step = 900)
            ant.run_automat(best_automat)
            st.write('Best score:', ant.info()['score'])
            st.write('Execution Time:', execution_time, 'seconds')
            st.write('Use state count:', len(ant.useState))
            st.write('Step count:', ant.info()['step'])
            new_field = ant.field
            plot_field(new_field)
        except Exception as e:
            st.error(f'Error: {e}')

if __name__ == "__main__":
    main()
