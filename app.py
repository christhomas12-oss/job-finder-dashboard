import streamlit as st
import requests
import pandas as pd

st.title("🎯 Chris's Automated Job Finder")

keywords = [
    "assistant director international education",
    "director global programs",
    "director international student services",
    "associate director study abroad",
    "director global engagement"
]

sources = [
    "https://www.higheredjobs.com/admin/search.cfm?JobCat=158",
    "https://www.washington.edu/jobs/",
    "https://www.sbctc.edu/about/jobs.aspx"
]

jobs = []

def search_remoteok():
    url = "https://remoteok.com/api"
    try:
        data = requests.get(url).json()
        for job in data[1:]:
            title = job.get("position")
            company = job.get("company")
            link = job.get("url")

            if title:
                if any(k.lower() in title.lower() for k in [
                    "director",
                    "international",
                    "global",
                    "education"
                ]):
                    jobs.append({
                        "Title": title,
                        "Organization": company,
                        "Location": "Remote",
                        "Link": link,
                        "Match Score": 80
                    })
    except:
        pass


def search_higheredjobs():
    try:
        url = "https://www.higheredjobs.com/rss/articleFeed.cfm"
        feed = requests.get(url).text

        lines = feed.split("<title>")

        for line in lines:
            if "director" in line.lower():
                title = line.split("</title>")[0]

                jobs.append({
                    "Title": title,
                    "Organization": "HigherEdJobs listing",
                    "Location": "Various",
                    "Link": "https://www.higheredjobs.com",
                    "Match Score": 75
                })
    except:
        pass


search_remoteok()
search_higheredjobs()

df = pd.DataFrame(jobs)

if len(df) > 0:
    df = df.sort_values("Match Score", ascending=False)

    st.subheader("⭐ Top Job Matches")

    st.dataframe(df.head(5))

    for _, row in df.head(5).iterrows():
        st.markdown(f"""
        **{row['Title']}**

        Organization: {row['Organization']}  
        Location: {row['Location']}  
        Match Score: {row['Match Score']}

        [Apply Here]({row['Link']})

        ---
        """)
else:
    st.write("No jobs found today.")
