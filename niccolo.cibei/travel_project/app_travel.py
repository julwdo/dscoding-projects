import streamlit as st
from travel_project.data import TravelData
from travel_project.methods import TravelGraphBidirectional, TravelGraphRight, TravelGraphLeft
from travel_project.plotting import Plotting


def create_bidirectional_graph(df):
    return TravelGraphBidirectional(df)


def create_right_graph(df):
    return TravelGraphRight(df)


def create_left_graph(df):
    return TravelGraphLeft(df)


path = r"C:\Users\cibei\Downloads\worldcities.xlsx"

page_options = ["Bidirectional Graph", "Right Graph", "Left Graph", "Dataset Info"]
page_selection = st.sidebar.selectbox("Select a page", page_options)

st.title("Travel Data Web App")

travel_data = TravelData(path=path,
                         admin=True,
                         primary=True,
                         minor=False,
                         num_rows=0,
                         num=300
                         )
df_city = travel_data.df

plotting = Plotting(df_city)

if page_selection == "Bidirectional Graph":
    travel_graph = create_bidirectional_graph(df_city)
elif page_selection == "Right Graph":
    travel_graph = create_right_graph(df_city)
elif page_selection == "Left Graph":
    travel_graph = create_left_graph(df_city)
else:
    travel_graph = None

if travel_graph is not None:
    st.header("Select the starting and target cities")

    city_names = df_city['city_ascii'].tolist()
    starting_city = st.selectbox("Select the starting city", city_names)
    target_city = st.selectbox("Select the target city", city_names)
    speed = st.slider("Select the speed (km/h)", 0, 1000, 100)

    result_short_path = travel_graph.shortest_path(source_city_name=starting_city,
                                                   target_city_name=target_city
                                                   )
    result_time = travel_graph.travel_time(path=result_short_path,
                                           speed=speed
                                           )
    st.subheader("Shortest Path Result")

    if result_short_path:
        st.write(f"The shortest path between {starting_city} and {target_city} is: ")
        st.write(result_short_path)
        st.write(result_time)
        st.subheader("3D Globe Plot of the Path")

        mapping = plotting.map_3d(cities_path=result_short_path)
        st.plotly_chart(mapping)
    else:
        st.sidebar.warning("Please select valid starting and target cities.")
else:
    st.header("Some info about the dataset")

    num_countries = st.slider("Select the number of countries to plot", 0, 20, 10)
    plot1 = plotting.plot_top_countries(n=num_countries)
    st.plotly_chart(plot1)

    plot2 = plotting.plot_population_by_continent()
    st.plotly_chart(plot2)

    plot3 = plotting.plot_density_map()
    st.plotly_chart(plot3)
