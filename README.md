# -whatsappdeep

💡 Project OverviewThis project is a powerful and interactive tool designed to extract meaningful insights and visualizations from your exported WhatsApp chat files (.txt). By leveraging [Mention main technique, e.g., Data Analysis, NLP, Machine Learning] techniques, it provides a deep dive into communication patterns, activity trends, and sentiment within individual or group conversations.The primary goal is to transform raw, unstructured chat data into a clear, visual story, answering questions like:Who are the most active participants?What are the most frequent words and emojis?What is the overall sentiment of the conversation?When is the group or individual most active?

📲 How to Export Your Chat
To use this analyzer, you first need to export your chat from WhatsApp:Open the individual or group chat you wish to analyze.Tap on the three-dot menu (⋮) in the top-right corner.Select More > Export chat.Crucially, choose "WITHOUT MEDIA" to generate the required .txt file.Save the file to your local machine.

Note: The tool requires a specific date format in the exported file. If you encounter errors, you may need to adjust the date-time parsing logic in the pre-processing script.
⚙️ Installation and Setup
Follow these steps to get your development environment running:PrerequisitesPython 3.8+pip (Python package installer)
Step-by-StepClone the repository:Bashgit clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName
Create a virtual environment (Recommended):Bashpython -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows
Install dependencies:Bashpip install -r requirements.txt

🚀 Usage
If your project is a script or a web app (like Streamlit):Running the Streamlit Web ApplicationEnsure you have completed the Installation and Setup.Run the main application file:Bashstreamlit run app.py
The application will open automatically in your web browser (usually at http://localhost:8501).Use the file uploader in the sidebar to upload your exported WhatsApp chat .txt file.

Select a user (or the overall chat) from the dropdown 
Running as a Jupyter/Colab Notebook
Open the notebook (whatsapp_analysis.ipynb) in your environment.Follow the instructions within the notebook to upload your chat file.Run the cells sequentially to perform data cleaning, analysis, and visualization.
