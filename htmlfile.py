HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-4xl p-8">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">WhatsApp Chat Analyzer</h1>

        <div class="mb-8 p-6 bg-blue-50 rounded-lg">
            <h2 class="text-xl font-semibold text-blue-800 mb-2">Instructions</h2>
            <ol class="list-decimal list-inside text-gray-600">
                <li class="mb-1">On your phone, open a WhatsApp chat.</li>
                <li class="mb-1">Tap the three vertical dots (menu) in the top right corner.</li>
                <li class="mb-1">Select `More`, then `Export chat`.</li>
                <li class="mb-1">Choose `WITHOUT MEDIA`.</li>
                <li class="mb-1">Save the `.txt` file to your computer.</li>
                <li class="mb-1">Upload the file below.</li>
            </ol>
        </div>
        
        <form method="post" enctype="multipart/form-data" class="flex flex-col items-center">
            <label for="chat_file" class="block text-gray-700 text-sm font-semibold mb-2">
                Upload your exported chat file (.txt):
            </label>
            <input type="file" name="chat_file" id="chat_file" accept=".txt" required
                   class="mb-4 w-full md:w-auto p-2 border border-gray-300 rounded-lg shadow-sm">
            <button type="submit"
                    class="bg-green-600 text-white font-bold py-2 px-6 rounded-full shadow-lg hover:bg-green-700 transition duration-300">
                Analyze Chat
            </button>
        </form>

        {% if analysis_data %}
            <div class="mt-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Analysis Results</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
                    <div class="bg-blue-500 text-white rounded-lg p-4 shadow-md text-center">
                        <p class="text-sm font-medium opacity-80">Total Messages</p>
                        <p class="text-3xl font-bold">{{ analysis_data.total_messages }}</p>
                    </div>
                    <div class="bg-purple-500 text-white rounded-lg p-4 shadow-md text-center">
                        <p class="text-sm font-medium opacity-80">Total Members</p>
                        <p class="text-3xl font-bold">{{ analysis_data.total_members }}</p>
                    </div>
                    <div class="bg-yellow-500 text-white rounded-lg p-4 shadow-md text-center">
                        <p class="text-sm font-medium opacity-80">Media Messages</p>
                        <p class="text-3xl font-bold">{{ analysis_data.media_messages }}</p>
                    </div>
                </div>

                <div class="flex justify-center">
                    <div class="bg-gray-100 p-6 rounded-lg shadow-inner">
                        <h3 class="text-xl font-semibold text-gray-800 mb-2 text-center">Most Active User</h3>
                        <p class="text-2xl font-bold text-center text-teal-600">{{ analysis_data.most_active_user }}</p>
                        <p class="text-sm text-center text-gray-500 mt-1">with {{ analysis_data.most_active_messages }} messages</p>
                    </div>
                </div>
                
                <div class="mt-8 flex flex-wrap justify-center gap-6">
                    <div class="w-full lg:w-1/2 p-4 bg-gray-50 rounded-lg shadow-inner">
                        <h3 class="text-xl font-semibold text-center mb-4 text-gray-800">Messages Per User</h3>
                        <img src="data:image/png;base64,{{ analysis_data.messages_per_user_chart }}" alt="Messages per user chart" class="w-full h-auto rounded-lg">
                    </div>
                    
                    <div class="w-full lg:w-1/2 p-4 bg-gray-50 rounded-lg shadow-inner">
                        <h3 class="text-xl font-semibold text-center mb-4 text-gray-800">Word Cloud</h3>
                        <img src="data:image/png;base64,{{ analysis_data.word_cloud }}" alt="Word cloud of common words" class="w-full h-auto rounded-lg">
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
