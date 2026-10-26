from flask import Flask, render_template, request, jsonify, send_file
import os
import logging
from src.resume_tailor import ResumeTailor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

resume_tailor = None
logger.info("🔧 Initializing ResumeTailor...")
try:
    resume_tailor = ResumeTailor()
    logger.info("✅ ResumeTailor initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize ResumeTailor: {e}")
    import traceback
    logger.error(traceback.format_exc())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tailor', methods=['POST'])
def tailor_resume():
    logger.info("🎯 /tailor endpoint called")
    try:
        data = request.get_json()
        logger.info(f"📥 Received data keys: {list(data.keys()) if data else 'None'}")
        
        # Extract data from request
        job_description = data.get('job_description', '')
        projects_data = data.get('projects', [])
        latex_resume = data.get('latex_resume', '')
        
        logger.info(f"📋 Job description length: {len(job_description)}")
        logger.info(f"📋 Projects count: {len(projects_data)}")
        logger.info(f"📋 LaTeX resume length: {len(latex_resume)}")
        
        if not job_description or not latex_resume:
            logger.error("❌ Missing required data")
            return jsonify({'error': 'Job description and LaTeX resume are required'}), 400
        
        if resume_tailor is None:
            logger.error("❌ ResumeTailor not initialized")
            return jsonify({'error': 'ResumeTailor not initialized'}), 500
        
        # Use the new modular approach
        logger.info("🔧 Calling resume_tailor.tailor_resume...")
        result = resume_tailor.tailor_resume(job_description, latex_resume, projects_data)
        logger.info(f"📊 Result keys: {list(result.keys()) if result else 'None'}")
        logger.info(f"📊 PDF result: {result.get('pdf_result')}")
        
        if result['pdf_result']:
            return jsonify({
                'success': True,
                'keywords': result['keywords'],
                'modified_resume': result['modified_resume'],
                'pdf_path': result['pdf_result']['filename'],
                'is_single_page': result['pdf_result']['is_single_page'],
                'page_count': result['pdf_result']['page_count']
            })
        else:
            return jsonify({'error': 'Failed to compile LaTeX resume'}), 500
            
    except Exception as e:
        logger.error(f"❌ Error in /tailor endpoint: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        temp_dir = os.environ.get('TEMP_DIR', 'temp')
        file_path = f'{temp_dir}/{filename}'
        logger.info(f"📥 Download request for: {file_path}")
        logger.info(f"📁 File exists: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            logger.info(f"📄 File size: {os.path.getsize(file_path)} bytes")
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        logger.error(f"❌ File not found: {filename}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create temp directory if it doesn't exist
    temp_dir = os.environ.get('TEMP_DIR', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # In Codespaces, always run in debug mode for better development experience
    debug = True
    
    print(f"🚀 Starting Resume Tailor on port {port}")
    print(f"📁 Temp directory: {temp_dir}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌐 Access the application at: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 