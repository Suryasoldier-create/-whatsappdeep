"""
Copyright - Deepak 
Amrapali University Haldwani
2025
"""



import re
import pandas as pd
from flask import Flask, render_template_string, request
import matplotlib
matplotlib.use('Agg') # Set the backend for Matplotlib
import matplotlib.pyplot as plt
import io
import base64
from wordcloud import WordCloud, STOPWORDS
import emoji
from htmlfile import HTML_TEMPLATE

app = Flask(__name__)


MESSAGE_PATTERN = re.compile(
    r'^\[?(\d{1,2}/\d{1,2}/\d{2,4}),\s*'            
    r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)' 
    r'\]?\s*-\s*(.+)$'                             
)

def parse_chat(file_content: bytes) -> pd.DataFrame:
    lines = file_content.decode('utf-8', errors='ignore').splitlines()
    data = []

    for line in lines:
        m = re.match(MESSAGE_PATTERN, line)
        if m:
            date = m.group(1).strip()
            time = m.group(2).strip()
            rest = m.group(3).strip()
         
            if ': ' in rest:
                author, message = rest.split(': ', 1)
                author = author.strip()
                message = message.strip()

            data.append([date, time, author, message])
        else:
            
            if data:
                data[-1][3] += ' ' + line.strip()

    if not data:
      
        return pd.DataFrame(columns=['Date', 'Time', 'Author', 'Message', 'datetime'])

    df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Message'])

  
    df['datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        errors='coerce',
        dayfirst=True,
        infer_datetime_format=True
    )

    if df['datetime'].isna().any():
        mask = df['datetime'].isna()
        try:
            df.loc[mask, 'datetime'] = pd.to_datetime(
                df.loc[mask, 'Date'] + ' ' + df.loc[mask, 'Time'],
                errors='coerce',
                dayfirst=False,
                infer_datetime_format=True
            )
        except Exception:
         
            pass

    df.dropna(subset=['datetime'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_messages_per_user_chart(df: pd.DataFrame) -> str:
    counts = df['Author'].value_counts()
    if counts.empty:
      
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return _fig_to_base64(fig)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind='bar', ax=ax)
    ax.set_title('Messages Sent Per User', fontsize=16, fontweight='bold')
    ax.set_xlabel('User', fontsize=12)
    ax.set_ylabel('Number of Messages', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return _fig_to_base64(fig)

def generate_word_cloud(df: pd.DataFrame) -> str:

    mask_media = df['Message'].str.contains(r'<media omitted>', case=False, na=False)
    text = " ".join(df.loc[~mask_media, 'Message'].astype(str).tolist())
    text = re.sub(r'http\S+', '', text)  
    text = emoji.demojize(text)

    stopwords = set(STOPWORDS)
 
    stopwords.update({'omitted', 'media', 'image', 'video', 'sticker'})

    if not text.strip():
       
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, "No text to generate word cloud", ha='center', va='center', fontsize=18)
        ax.axis('off')
        return _fig_to_base64(fig)

    wc = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, min_font_size=10)
    wordcloud = wc.generate(text)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return _fig_to_base64(fig)

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis_data = None
    if request.method == 'POST':
        if 'chat_file' not in request.files:
            return "No file part", 400
        file = request.files['chat_file']
        if not file or file.filename == '':
            return "No selected file", 400
        if not file.filename.lower().endswith('.txt'):
            return "Only .txt files accepted", 400

        file_bytes = file.read()
        df = parse_chat(file_bytes)

        if df.empty:
            analysis_data = None
        else:
            total_messages = int(len(df))
            total_members = int(df['Author'].nunique())
            media_messages = int(df['Message'].str.contains(r'<media omitted>', case=False, na=False).sum())

            messages_per_user = df['Author'].value_counts()
            most_active_user = messages_per_user.index[0] if not messages_per_user.empty else 'N/A'
            most_active_messages = int(messages_per_user.iloc[0]) if not messages_per_user.empty else 0

            analysis_data = {
                'total_messages': total_messages,
                'total_members': total_members,
                'media_messages': media_messages,
                'most_active_user': most_active_user,
                'most_active_messages': most_active_messages,
                'messages_per_user_chart': generate_messages_per_user_chart(df),
                'word_cloud': generate_word_cloud(df)
            }

    return render_template_string(HTML_TEMPLATE, title="WhatsApp Chat Analyzer", analysis_data=analysis_data)

if __name__ == '__main__':
    app.run(debug=True)