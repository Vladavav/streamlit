import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

uploaded_file = st.file_uploader("tips")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)
    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)
    
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

tips = pd.read_csv('/Users/uladzislauyermakou/streamlit/tips.csv')

st.subheader("Данные")
tips

st.subheader("Данные с датой")
tips['time_order'] = np.random.choice(pd.date_range('2023-01-01', '2023-01-31'), 244)
tips

st.subheader("График показывающий динамику чаевых за январь")
tips1 = tips.groupby('time_order', as_index = False).agg({'tip':'sum'}).sort_values('time_order', ascending = True)
st.line_chart(tips1, x='time_order', y='tip', use_container_width=True)

st.subheader("Гистограмма `total_bill`")
sns.histplot(data=tips, x="total_bill")
st.pyplot(plt)

st.subheader("Scatterplot, показывающий связь между `total_bill` and `tip`")
sns.scatterplot(data=tips, x="total_bill", y="tip")
st.pyplot(plt)


st.subheader("Scatterplot, связывающий `total_bill`, `tip`, и `size`")
sns.relplot(data = tips, x = 'total_bill', y = 'tip',hue = 'size')
st.pyplot(plt)

st.subheader("Покажите связь между днем недели и размером счета")
sns.relplot(data = tips, x = 'day', y = 'total_bill')
st.pyplot(plt)

st.subheader("`scatter plot` с днем недели по оси **Y**, чаевыми по оси **X**, и цветом по полу")
sns.scatterplot(data = tips, x = 'day', y = 'tip', hue = 'sex')
st.pyplot(plt)

st.subheader("`box plot` c суммой всех счетов за каждый день, разбивая по `time` (Dinner/Lunch)")
total = tips.groupby(['day','time'], as_index = False).agg({'total_bill':'sum'}).sort_values('day')
sns.boxplot(data = total, x="day", y="total_bill")
st.pyplot(plt)

st.subheader("Нарисуйте 2 гистограммы чаевых на обед и ланч. Расположите их рядом по горизонтали.")
fig, axes = plt.subplots(1, 2,figsize=(12, 4))

tips[tips['time'] == 'Dinner']['tip'].hist(ax=axes[0])
axes[0].set_title('Чаевые за ужин')
axes[0].set_xlabel('Размер чаевых')
axes[0].set_ylabel('Частота')

tips[tips['time'] == 'Lunch']['tip'].hist(ax=axes[1])
axes[1].set_title('Чаевые за ланч')
axes[1].set_xlabel('Размер чаевых')
axes[1].set_ylabel('Частота')

sns.boxplot(data=tips, x="day", y="total_bill")
st.pyplot(plt)

st.subheader("2 scatterplots (для мужчин и женщин), связанные размером счета и чаевых, а также разбитые по курящим/некурящим.")

g = sns.FacetGrid(tips, col="sex", hue="smoker")
g.map(plt.scatter, "total_bill", "tip")
g.add_legend()
st.pyplot(plt)

st.subheader("Тепловая карта зависимостей численных переменных")
numeric_cols = tips.select_dtypes(include=[np.number]).columns
df = tips[numeric_cols]
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f')
st.pyplot(plt)

@st.cache_data

def convert_df(df):
    return df.to_csv().encode("utf-8")

csv = convert_df(tips)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="tips.csv",
    mime="сsv"
)
