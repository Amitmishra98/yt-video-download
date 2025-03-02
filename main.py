
import yt_dlp
import os
from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Download best quality video & audio
        "merge_output_format": "mp4",  # Merge output as MP4
        "skip_download": True,  # Only extract info, don't download
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    video_info = None
    
    if request.method == 'POST':
        video_url = request.form.get('url')
        if video_url:
            try:
                video_info = get_video_info(video_url)
                result = f"Video found: {video_info.get('title', 'Video')}"
            except Exception as e:
                error = f"Error: {str(e)}"
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Video Downloader</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            h1 {
                color: #ff4545;
                text-align: center;
                margin-bottom: 30px;
                font-weight: 700;
                font-size: 2.2rem;
                letter-spacing: 0.5px;
                text-shadow: 0 2px 10px rgba(255, 69, 69, 0.2);
                position: relative;
                padding-bottom: 12px;
                animation: titlePulse 2s infinite alternate, fadeIn 1s ease;
            }
            
            @keyframes titlePulse {
                0% { text-shadow: 0 2px 10px rgba(255, 69, 69, 0.2); }
                100% { text-shadow: 0 2px 20px rgba(255, 69, 69, 0.6); }
            }
            
            h1::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80px;
                height: 3px;
                background: linear-gradient(to right, transparent, #ff4545, transparent);
                animation: lineWidth 3s infinite alternate;
            }
            
            @keyframes lineWidth {
                0% { width: 40px; opacity: 0.6; }
                100% { width: 120px; opacity: 1; }
            }
            
            .container {
                background: rgba(30, 30, 40, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                width: 100%;
                max-width: 800px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                animation: containerFadeIn 0.8s ease-out, floatContainer 6s ease-in-out infinite;
                transform-origin: center;
            }
            
            @keyframes containerFadeIn {
                0% { opacity: 0; transform: translateY(30px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes floatContainer {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            .form-group {
                margin-bottom: 24px;
            }
            
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: 500;
                color: #d0d0d0;
                font-size: 0.95rem;
                letter-spacing: 0.5px;
            }
            
            input[type="text"] {
                width: 100%;
                padding: 14px 18px;
                box-sizing: border-box;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 16px;
                background-color: rgba(45, 45, 60, 0.5);
                color: #f0f0f0;
                transition: all 0.3s ease;
                font-family: 'Poppins', sans-serif;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
                animation: inputPulse 2s infinite alternate;
            }
            
            @keyframes inputPulse {
                0% { border-color: rgba(255, 255, 255, 0.1); }
                100% { border-color: rgba(255, 69, 69, 0.3); }
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: rgba(255, 69, 69, 0.5);
                box-shadow: 0 0 0 3px rgba(255, 69, 69, 0.2);
                animation: none;
            }
            
            input[type="text"]::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }
            
            button {
                background: linear-gradient(135deg, #ff4545, #ff7676);
                background-size: 200% 200%;
                animation: gradientShift 3s ease infinite;
                color: white;
                border: none;
                padding: 14px 24px;
                cursor: pointer;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(255, 69, 69, 0.3);
                letter-spacing: 0.5px;
                position: relative;
                overflow: hidden;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            button:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 6px 20px rgba(255, 69, 69, 0.4);
            }
            
            button:active {
                transform: translateY(1px) scale(0.98);
            }
            
            button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transition: 0.5s;
            }
            
            button:hover::before {
                left: 100%;
                animation: shimmer 1.5s infinite;
            }
            
            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            .success {
                color: #4caf50;
                margin-top: 20px;
                padding: 15px;
                background-color: rgba(76, 175, 80, 0.1);
                border-radius: 8px;
                border-left: 4px solid #4caf50;
                font-weight: 500;
            }
            
            .error {
                color: #f44336;
                margin-top: 20px;
                padding: 15px;
                background-color: rgba(244, 67, 54, 0.1);
                border-radius: 8px;
                border-left: 4px solid #f44336;
                font-weight: 500;
            }
            
            .downloads {
                margin-top: 35px;
                animation: fadeIn 0.5s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .downloads h2 {
                color: #d0d0d0;
                font-size: 1.3rem;
                margin-bottom: 15px;
                font-weight: 600;
                position: relative;
                display: inline-block;
                padding-bottom: 8px;
            }
            
            .downloads h2::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(to right, #4CAF50, transparent);
            }
            
            .download-instruction {
                color: #a0a0a0;
                font-size: 14px;
                margin-bottom: 20px;
                font-style: italic;
                line-height: 1.5;
            }
            
            .download-list {
                list-style-type: none;
                padding: 0;
            }
            
            .download-item {
                padding: 18px;
                background-color: rgba(61, 61, 81, 0.6);
                margin-bottom: 12px;
                border-radius: 10px;
                display: flex;
                flex-direction: column;
                gap: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.05);
                animation: slideIn 0.5s ease;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            .download-item span {
                font-weight: 500;
                word-break: break-word;
                line-height: 1.4;
                font-size: 1.05rem;
                color: #e0e0e0;
            }
            
            .download-buttons {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }
            
            .download-button {
                background: linear-gradient(135deg, #4CAF50, #2E7D32);
                background-size: 200% 200%;
                animation: dlBtnGradient 4s ease infinite;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s ease;
                font-weight: 500;
                flex: 1;
                text-align: center;
                min-width: 140px;
                box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                position: relative;
                overflow: hidden;
            }
            
            @keyframes dlBtnGradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .download-button:hover {
                transform: translateY(-2px) scale(1.03);
                box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
            }
            
            .download-button:active {
                transform: translateY(1px) scale(0.98);
            }
            
            .download-button::after {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                transition: 0.5s;
            }
            
            .download-button:hover::after {
                left: 100%;
                animation: dlBtnShimmer 1.5s infinite;
            }
            
            @keyframes dlBtnShimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            .download-button svg {
                animation: iconBounce 2s ease infinite;
            }
            
            @keyframes iconBounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-3px); }
            }
            
            .download-button[style*="7249d1"] {
                background: linear-gradient(135deg, #7249d1, #5834a3);
                background-size: 200% 200%;
                animation: mp3BtnGradient 4s ease infinite;
                box-shadow: 0 4px 12px rgba(114, 73, 209, 0.2);
            }
            
            @keyframes mp3BtnGradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .download-button[style*="7249d1"]:hover {
                box-shadow: 0 6px 15px rgba(114, 73, 209, 0.3);
            }
            
            .loading {
                display: none;
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                animation: loadingPulse 2s infinite alternate;
            }
            
            @keyframes loadingPulse {
                0% { box-shadow: 0 0 5px rgba(255, 69, 69, 0.2); }
                100% { box-shadow: 0 0 20px rgba(255, 69, 69, 0.6); }
            }
            
            .spinner {
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-top: 3px solid #ff4545;
                border-right: 3px solid #ff4545;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .loading p {
                animation: textFade 1.5s infinite alternate;
            }
            
            @keyframes textFade {
                0% { opacity: 0.7; }
                100% { opacity: 1; }
            }
            
            @media (max-width: 600px) {
                body {
                    padding: 15px;
                }
                
                .container {
                    padding: 20px;
                }
                
                h1 {
                    font-size: 1.8rem;
                }
                
                .download-item {
                    padding: 15px;
                }
                
                .download-buttons {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>YouTube Video Downloader</h1>
            
            <form method="post" id="downloadForm">
                <div class="form-group">
                    <label for="url">Enter YouTube URL:</label>
                    <input type="text" id="url" name="url" required placeholder="https://www.youtube.com/watch?v=...">
                </div>
                <button type="submit" id="submitBtn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
                    Find Video
                </button>
            </form>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Finding video... Please wait a moment.</p>
            </div>
            
            {% if result %}
            <div class="success">{{ result }}</div>
            {% endif %}
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            
            {% if video_info %}
            <div class="downloads">
                <h2>Video Found</h2>
                <div class="download-item">
                    <span>{{ video_info.get('title', 'Video') }}</span>
                    <div class="download-buttons">
                        <a href="{{ url_for('download_video', url=request.form.get('url'), format='mp4') }}" class="download-button">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Download MP4
                        </a>
                        <a href="{{ url_for('download_video', url=request.form.get('url'), format='mp3') }}" class="download-button" style="background-color: #7249d1;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>
                            Download MP3
                        </a>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
        
        <script>
            document.getElementById('downloadForm').addEventListener('submit', function() {
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('loading').style.display = 'block';
            });
            
            // Add animation to elements when they appear
            document.addEventListener('DOMContentLoaded', function() {
                // Add animation to success/error messages if they exist
                const successMessage = document.querySelector('.success');
                const errorMessage = document.querySelector('.error');
                const downloadsSection = document.querySelector('.downloads');
                
                if (successMessage) {
                    successMessage.style.animation = 'fadeInSlideUp 0.5s ease-out forwards';
                }
                
                if (errorMessage) {
                    errorMessage.style.animation = 'fadeInSlideUp 0.5s ease-out forwards';
                }
                
                if (downloadsSection) {
                    downloadsSection.style.animation = 'fadeInScale 0.6s ease-out forwards';
                }
            });
            
            // Define the animations in CSS
            const styleSheet = document.createElement("style");
            styleSheet.textContent = `
                @keyframes fadeInSlideUp {
                    0% { opacity: 0; transform: translateY(20px); }
                    100% { opacity: 1; transform: translateY(0); }
                }
                
                @keyframes fadeInScale {
                    0% { opacity: 0; transform: scale(0.9); }
                    100% { opacity: 1; transform: scale(1); }
                }
            `;
            document.head.appendChild(styleSheet);
        </script>
    </body>
    </html>
    ''', result=result, error=error, video_info=video_info)

@app.route('/download_video')
def download_video():
    video_url = request.args.get('url')
    format_type = request.args.get('format', 'mp4')
    if not video_url:
        return "No URL provided", 400
    
    try:
        if format_type == 'mp3':
            # Get audio in mp3 format
            with yt_dlp.YoutubeDL({
                "format": "bestaudio",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            }) as ydl:
                info = ydl.extract_info(video_url, download=False)
                # For mp3, we need to get the direct URL to the audio
                for format in info.get('formats', []):
                    if format.get('ext') == 'm4a' and format.get('acodec') != 'none':
                        audio_url = format['url']
                        title = info.get('title', 'audio')
                        
                        # Create response with appropriate headers for download
                        response = redirect(audio_url)
                        response.headers['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
                        return response
                return "Could not find suitable audio format", 404
        else:
            # Default mp4 video download
            with yt_dlp.YoutubeDL({"format": "best"}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                video_url = info['url']
                title = info.get('title', 'video')
                
                # Create response with appropriate headers for download
                response = redirect(video_url)
                response.headers['Content-Disposition'] = f'attachment; filename="{title}.mp4"'
                return response
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use PORT from env, default to 8080
    app.run(host='0.0.0.0', port=port, debug=False)  # Debug=False for production
