# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 11:21:02 2025

@author: feyzullah çonkar
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data(file_name="oyuncular.xlsx"):
    """Aynı klasördeki Excel dosyasından verileri yükler."""
    try:
        df = pd.read_excel(file_name)
        return df
    except FileNotFoundError:
        st.error(f"{file_name} dosyası bulunamadı!")
        return None

def create_radar_chart(df, player1, player2, stats):
    """İki oyuncu için radar grafiği oluşturur."""
    fig = go.Figure()

    colors = ['blue', 'red'] # Renkleri istediğiniz gibi değiştirebilirsiniz

    for i, player in enumerate([player1, player2]):
        values = df[df['Oyuncular'] == player][stats].values.flatten().tolist()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=stats,
            fill='toself',
            name=player,
            marker=dict(color=colors[i]) # Renk ayarı
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(df[stats].max())]  # Eksen aralığını değiştirmedik
            )),
        showlegend=True,
        width=680,  # Grafiğin genişliğini artırdık
        height=680  # Grafiğin yüksekliğini artırdık
    )
    return fig

def main():
    st.title("Oyuncu İstatistikleri Radar Grafiği")

    df = load_data()

    if df is not None:
        players = df['Oyuncular'].tolist()
        stats = df.columns[1:].tolist()  # İlk sütun (Oyuncular) hariç tüm sütunlar

        player1 = st.selectbox("Oyuncu 1 Seçin", players)
        player2 = st.selectbox("Oyuncu 2 Seçin", players)

        if player1 != player2:
            fig = create_radar_chart(df, player1, player2, stats)
            st.plotly_chart(fig)
        else:
            st.warning("Lütfen farklı iki oyuncu seçin.")

if __name__ == "__main__":
    main()