import streamlit as st

import streamlit as st
from wordcloud import WordCloud,STOPWORDS
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import jieba.posseg
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
stwlist=[line.strip() for line in open('stopwords.txt','r',encoding='utf-8').readlines()]
drop_list = ['r', 'f', 's', 'i', 'q', 'ad', 'z', 'u', 'd', 'c', 'ul', 't','o','m']

@st.cache()
def plotly_wordcloud(text):
    colors = ["#000000", "#111111", "#101010", "#121212", "#212121", "#222222"]
    cmap = LinearSegmentedColormap.from_list("mycmap", colors)
    wc = WordCloud(stopwords = set(STOPWORDS.union(set(stwlist))),
                   max_words = 300,
                   max_font_size = 120,
                   colormap=cmap,
                   random_state = 0,
                   )
    wc.generate(text)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append((i*150+8))
    # new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(plot_bgcolor='#D3DFE2')
    return fig

# #D3DFE2 #303640 #DDBEA9

def plot_word2(text):
    wordcloud = WordCloud(
        stopwords = STOPWORDS.union(set(stwlist)),
        max_words = 200,
        max_font_size = 120,
        font_path="simsun.ttf",
        random_state = 0,
    ).generate(text)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()
@st.cache()
def get_data():
    file_ID = '1JA4vvS-hXexGN7bizBcXsFxx8g5Is1Ps'
    df = pd.read_excel(f'https://drive.google.com/uc?export=download&id={file_ID}')
    return df

@st.cache()
def process_data(df,data_col):
    # df = df.sample(5000).copy() #test mode
    dt = df_raw.copy()
    dt.dropna(subset=[data_col],inplace=True)
    dt['cutted'] = dt[data_col].apply(lambda x:list(jieba.posseg.cut((str(x)))))
    return dt

df =get_data()

data_col = 'content'
# df = process_data(df_raw,data_col)




def write(df):
    """Used to write the page in the app.py file"""
    dt = process_data(df,data_col)

    with st.spinner("Loading 词云工具 ..."):
        st.title('词云工具')
        # raw_text = st.text_area('')
        check = st.checkbox('是否去除非重要词性语料')
        click = st.button('点击生成词云')

        if click:
            if check:
                pro_text=''
                for item in dt.cutted:
                    for i in item:
                        if not (i.flag in drop_list):
                            pro_text+= (' '+i.word)
            else:
                pro_text=''
                for item in dt.cutted:
                    for i in item:
                        pro_text+= (' '+i.word)
            # raw_text = pro_text
            st.markdown('文字预览：')
            st.write(pro_text[:500])
            st.markdown('## 词云预览：')
            plot_word2(pro_text)
            st.markdown('## 详细词云（放大观看）：')
            st.plotly_chart(plotly_wordcloud(pro_text))
        else:
            st.warning('非重要词性包括拟声词、副词、连词等等')


if __name__ == "__main__":
    write(df)

