import streamlit as st
import numpy as np
import pandas as pd
import tooltip_function as tt
import conv_functions as cv
from list_func import cost_list_func, park_cost_list_func

with st.sidebar:
    st.write("Contact:")
    st.write("platformbve@gmail.com")

st.header("VerhuurDashboard Transparq", divider = "gray")

st.session_state.total_cost = 0
st.session_state.total_cost_park = 0
st.session_state.total_cost_priv = 0
st.session_state.total_cost_gov = 0

with st.container(border=True):
    st.subheader("Kosten van de Eigenaar Dashboard", divider="gray")
    with st.expander("Kosten van de Eigenaar"):
        tab1, tab2, tab3 = st.tabs(["Parkbijdrage", "Eigenaarskosten Investering", "Overheidskosten"])
        with tab1:
            names_park = cost_list_func()
            len_list = len(names_park)
            std_cost_park = np.zeros(len_list)
            cost_park = np.zeros(len_list)

            all_zero = st.checkbox("Zelf totaal invullen (Pas op! Als u dit aanklikt verdwijnen alle individuele ingevulde velden.)")
            if all_zero:
                st.session_state.total_cost_park = st.number_input("Totale kosten aan park per jaar", min_value = 0, key = "total_cost_park_self")
            else:
                for i in range(len_list):
                    key_str = "cost_park_" + str(i)
                    cost_park[i] = st.number_input(names_park[i], value = std_cost_park[i], min_value = 0.0, key = key_str)
                st.session_state.total_cost_park = cost_park.sum()

        with tab2:
            st.write("Alle kosten eigenaar prive aankoop")
            names_priv = np.array(["Rente lening","Afschrijving inboedel","Afschrijving huisje", "Extra 1", "Extra 2", "Extra 3"])
            cost_priv = np.zeros(len(names_priv))
            for i in range(len(names_priv)):
                key_str = "cost_priv_" + str(i)
                cost_priv[i] = st.number_input(names_priv[i], min_value = 0, key = key_str)
            tot_cost_priv = cost_priv.sum()

        with tab3:
            st.write("Alle kosten overheid")
            names_gov = np.array(["Box 3","WOZ", "Extra 1", "Extra 2", "Extra 3"])
            cost_gov = np.zeros(len(names_gov))
            for i in range(len(names_gov)):
                key_str = "cost_gov_" + str(i)
                cost_gov[i] = st.number_input(names_gov[i], min_value = 0, key = key_str)
            tot_cost_gov = cost_gov.sum()

    st.session_state.total_cost = st.session_state.total_cost_park + tot_cost_priv + tot_cost_gov

    col1,col2 = st.columns([0.7,1])
    h = 305
    with col1:
        with st.container(border = True, height=h-20):
            st.subheader("Kosten overzicht", divider="gray")
            st.write("Alle kosten aan park: ", round(st.session_state.total_cost_park,2), "€")
            st.write("Alle kosten eigenaar: ", round(tot_cost_priv,2), "€")
            st.write("Alle kosten aan overheid: ", round(tot_cost_gov,2), "€")
            st.write("Totale kosten: ", round(st.session_state.total_cost,2), "€")

    with col2:
        with st.container(border = False, height=h, vertical_alignment = "center"):
            percent = np.array([20, 30, 45, 65, 70, 80, 90])
            table_data = np.zeros(len(percent))
            for i in range(len(percent)):
                table_data[i] = round(st.session_state.total_cost / ((percent[i]/100) * 365),2)

            df = pd.DataFrame({'Percentage bezetting chalet (%)':percent,'Kosten per nacht (€)':table_data})
            st.dataframe(df, hide_index=True, width="stretch")


with st.container(border = True):
    st.subheader("Huursom Dashboard", divider="gray")
    col1,col2 = st.columns([2,1])
    h = 80
    with col1:
        #st.write("Bezetting chalet")
        with st.container(height = h, vertical_alignment = "center", border = False):
            col1_1,col1_2 = st.columns(2)
            with col1_1:
                occupancy = st.number_input("Percentage bezetting chalet", key = "occ_perc", value = 65.00, min_value = 0.01, max_value = 100.00, on_change=cv.perc_to_days)
            with col1_2:
                occupancy_days = st.number_input("Dagen bezetting chalet", key = "occ_day", value = 65 * 365 / 100,min_value =0.01, max_value = 365.00, on_change=cv.days_to_perc )
            cost_per_night = st.session_state.total_cost / ((occupancy/100) * 365)

    with col2:
        with st.container(height = h-15, vertical_alignment="bottom", border = False):
            cost_per_night = st.session_state.total_cost / ((occupancy/100) * 365)
            st.write("Kosten per nacht voor eigenaar:\n ", round(cost_per_night,2)," €")


    def pc_priv_park():
        st.session_state.pc_park = 100 - st.session_state.pc_priv

    def pc_park_priv():
        st.session_state.pc_priv = 100 - st.session_state.pc_park

    col1, col2, col3 = st.columns(3)

    with col1:
        intr = st.number_input("Winst marge eigenaar (%)", min_value = 0, value = 10)

    with col2:
        park_perc = st.number_input("Percentage huursom aan park", key = "pc_priv", min_value = 0.01, max_value = 99.99, value = 32.7, on_change=pc_priv_park)

    with col3:
        priv_perc = st.number_input("Percentage huursom aan eigenaar", key = "pc_park", min_value = 0.01, max_value = 99.99, value = 67.3, on_change=pc_park_priv)

    rent_sum_per_night = (cost_per_night*(1 + intr/100))/(priv_perc/100)


    col1, col2, col3 = st.columns(3)

    with col1:
        rent_sum_per_night = (cost_per_night*(1 + intr/100))/(priv_perc/100)
        st.write("Huursom per nacht: ", round(rent_sum_per_night,2), " €")

    with col2:
        share_park = park_perc/100 * rent_sum_per_night
        st.write("Opbrengst park: ", round(share_park,2), " €")

    with col3:
        share_priv = priv_perc/100 * rent_sum_per_night
        st.write("Opbrengst eigenaar: ", round(share_priv,2), " €")

    col1, col2 = st.columns([1,0.01])
    with col2:
        tt.tooltip("Met deze dashboard kunt u aan de hand van bepaalde gegevens zien wat\
         de huursom voor een nacht van het chalet zou moeten zijn onder aanpassing van\
         bezettings percentage/dagen chalet, huursom verdeling tussen park en eigenaar.\
         Ook kunt u hier als eigenaar uw gewenste winstmarge aangeven over uw totale \
         investering/kosten.", width = 400)

with st.expander("Tabel huursom en opbrengsten"):
    percent = np.array([20, 30, 45, 65, 70, 80, 90])
    table_data = np.zeros(len(percent)*3).reshape(3,len(percent))
    for i in range(len(percent)):
        cost_per_night_per_percentage = st.session_state.total_cost / ((percent[i]/100) * 365)
        rent_sum_per_night_per_percentage = (cost_per_night_per_percentage*(1 + intr/100))/(priv_perc/100)
        share_park_per_percentage = park_perc/100 * rent_sum_per_night_per_percentage
        share_priv_per_percentage = priv_perc/100 * rent_sum_per_night_per_percentage
        table_data[0][i] = round(rent_sum_per_night_per_percentage,2)
        table_data[1][i] = round(share_park_per_percentage,2)
        table_data[2][i] = round(share_priv_per_percentage,2)

    df = pd.DataFrame({'Percentage bezetting (%)':percent,'Huursom per nacht (€)':table_data[0],
    'Opbrengst park (€)': table_data[1], 'Opbrengst eigenaar (€)': table_data[2]})
    st.dataframe(df, hide_index=True)



with st.container(border = True):
    st.subheader("Boekingsprijs Dashboard", divider = "gray")
    with st.expander("Kosten van het park"):
        
        park_cost_names_list = park_cost_list_func()
        len_list = len(park_cost_names_list)
        #park_cost_price_list = np.array([84,35,15,12.5,0,0])
        park_cost_price_list = np.zeros(len_list)
        park_cost = np.zeros(len_list)

        park_cost_all_zero = st.checkbox("Zelf totaal invullen (Pas op! Als u dit aanklikt verdwijnen alle individuele ingevulde velden.)", key="self_2")
        if park_cost_all_zero:
            st.session_state.park_cost = st.number_input("Kosten van het park per boeking", min_value = 0, key = "park_cost_self")
        else:
            for i in range(len_list):
                key_str = "park_cost" + str(i)
                park_cost[i] = st.number_input(park_cost_names_list[i], value = park_cost_price_list[i], min_value = 0.0, key = key_str)
            st.session_state.park_cost = park_cost.sum()
    
    col1_1, col1_2 = st.columns(2)
    col2_1, col2_2 = st.columns(2)
    col3_1, col3_2 = st.columns(2)
    h = 80
    with col1_1:
        with st.container(border = False, vertical_alignment = "bottom", height = h - 15):
            st.write("Kosten van het park per boeking: ", st.session_state.park_cost, " €")
    with col1_2:
        with st.container(border = False, vertical_alignment = "center", height = h):
            duration_stay = st.number_input("Aantal nachten per boeking", min_value=2, max_value=21)
    total_price_stay = duration_stay * rent_sum_per_night + st.session_state.park_cost
    price_per_night_stay = total_price_stay / duration_stay
    with col2_1:
        with st.container(border = False, vertical_alignment = "center"):
            st.write("Totaal prijs boeking: ", round(total_price_stay,2)," €")
    with col2_2:
        with st.container(border = False, vertical_alignment = "center"):
            st.write("Prijs per nacht voor boeking: ", round(price_per_night_stay,2)," €")
    with col3_1:
        cost_priv_stay = duration_stay * cost_per_night
        with st.container(border = False, vertical_alignment = "center"):
            st.write("Kosten eigenaar per boeking: ", round(cost_priv_stay,2), "€")
    with col3_2:
        share_priv_stay = share_priv * duration_stay
        with st.container(border = False, vertical_alignment = "center"):
            st.write("Opbrengst eigenaar per boeking: ", round(share_priv_stay,2)," €")

    col1, col2 = st.columns([1,0.01])
    with col2:
        tt.tooltip("Met de Boekingsprijs Dashboard wordt het verschil inzichtelijk\
         gemaakt tussen wat de klant betaalt voor de totale boeking ten opzichte\
         van de huursom in de \"Huursom Dashboard\".", width = 400)

col1,col2 = st.columns(2)
def snow_func():
    st.snow()

def party_func():
    st.balloons()

with col1:
    with st.container(horizontal_alignment = "left", vertical_alignment = "bottom"):
        snow_button = st.button("Let It Snow", on_click=snow_func)

with col2:
    with st.container(horizontal_alignment = "right", vertical_alignment = "bottom"):
        party_button = st.button("Let's Party", on_click=party_func)

