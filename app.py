import emoji
import matplotlib.pyplot as plt
import streamlit as st
import preprocess,helper
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat File", type=["txt"])

if uploaded_file is not None:
    data=uploaded_file.getvalue().decode("utf-8")
    df=preprocess.preprocess_data(data)
   
    users=df['user'].unique().tolist()
    # users.remove("group_notification", None)

    users.sort()
    st.sidebar.title("Select User")
    users.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Select User", users)

    if st.sidebar.button("Show Analysis"):
        num_messages,total_words,no_of_media,no_links=helper.fetch_stats(selected_user,df)
## Stats Area
        st.title("Top Statistics:-")

        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            st.markdown("### Total Messages")
            st.write(f"## {num_messages}")

        with col2:
            st.markdown("### Total Words")
            st.write(f"## {total_words}")

        with col3:
            st.markdown("### Media Shared")
            st.write(f"## {no_of_media}")

        with col4:
            st.markdown("### Links Shared")
            st.write(f"## {no_links}")
## TimeLine Analysis
        st.title("Monthly Timeline") 
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        ### Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)  
## Activity Map
        cols1, cols2 = st.columns(2)
        with cols1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with cols2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weekly Activity Heatmap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

## Finding The Busiest Users IN Group (Overall)
        if selected_user == 'Overall':
            st.title("Most Busy Users")

            x,new_df = helper.fetch_busy_users(df)

            cols1, cols2 = st.columns(2)

            with cols1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values,color='red')
                ax.set_xticklabels(x.index, rotation=90)
                st.pyplot(fig)
            with cols2:
                st.dataframe(new_df)
## WordCloud
        st.title("Word Analysis")
        df_wc = helper.create_wordcloud(selected_user, df)
        st.pyplot(df_wc)

## Most Common Words
        st.title("Most Common Words")
        mcdf=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(mcdf[0],mcdf[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

## Emoji Analysis

        st.title("Emoji Analysis")
        emoji_df=helper.emoji_helper(selected_user,df)
        cols1, cols2 = st.columns(2)
        with cols1:
            st.dataframe(emoji_df)
        with cols2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)