"""
CIDE Web Application
====================
Flask-based web interface for Code Integrity Detection Engine.
Provides visual interface for code similarity analysis and plagiarism detection.
"""

from flask import Flask, render_template, request, jsonify, session, send_file, make_response
from werkzeug.utils import secure_filename
import os
import difflib
from pathlib import Path
import json
from datetime import datetime
from io import BytesIO

# Import our analyzers
from code_similarity import CodeSimilarityAnalyzer
from ast_analyzer import HybridSimilarityAnalyzer
from report_generator import generate_report
from batch_comparator import BatchComparator

app = Flask(__name__)

# Use environment variable for secret key in production
import os
app.secret_key = os.environ.get('SECRET_KEY', 'cide-secret-key-change-in-production')

# Admin credentials (in production, use database with hashed passwords)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# In-memory storage for analyses (replace with database in production)
analyses_db = []

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'py', 'java', 'js', 'cpp', 'c', 'h', 'txt'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_file_language(filename):
    """Detect programming language from file extension."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'txt'
    language_map = {
        'py': 'python',
        'java': 'java',
        'js': 'javascript',
        'cpp': 'cpp',
        'c': 'c',
        'h': 'c',
        'txt': 'text'
    }
    return language_map.get(ext, 'text')


def generate_diff_html(code1, code2, filename1='File 1', filename2='File 2'):
    """Generate HTML for side-by-side diff view."""
    differ = difflib.HtmlDiff(wrapcolumn=80)
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()
    
    diff_html = differ.make_table(
        code1_lines,
        code2_lines,
        fromdesc=filename1,
        todesc=filename2,
        context=True,
        numlines=3
    )
    
    return diff_html


@app.route('/')
def index():
    """Home page with file upload form."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded files for similarity."""
    try:
        # Check if files were uploaded
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Both files are required'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Check if files have names
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Both files must be selected'}), 400
        
        # Validate file types
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': f'Allowed file types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400
        
        # Read file contents
        code1 = file1.read().decode('utf-8')
        code2 = file2.read().decode('utf-8')
        
        # Get analysis mode from form
        mode = request.form.get('mode', 'hybrid')
        
        # Detect language
        language = get_file_language(file1.filename)
        
        # Initialize analyzers
        basic_analyzer = CodeSimilarityAnalyzer()
        
        # Perform analysis based on mode
        if mode == 'hybrid' and language == 'python':
            # Use hybrid analyzer for Python
            hybrid_analyzer = HybridSimilarityAnalyzer()
            ast_result = hybrid_analyzer.analyze(code1, code2)
            
            result = {
                'mode': 'hybrid',
                'language': language,
                'weighted_score': ast_result['weighted_score'],
                'weighted_percentage': ast_result['weighted_percentage'],
                'structure_similarity': ast_result['structure_similarity'],
                'sequence_similarity': ast_result['sequence_similarity'],
                'feature_similarity': ast_result['feature_similarity'],
                'identical_structure': ast_result['identical_structure'],
                'features1': ast_result['features1'],
                'features2': ast_result['features2'],
                'error': ast_result.get('error')
            }
            
            # Check for plagiarism
            plagiarism_result = hybrid_analyzer.detect_plagiarism(code1, code2, threshold=0.75)
            result['plagiarism'] = {
                'is_plagiarism': plagiarism_result['is_plagiarism'],
                'confidence': plagiarism_result['confidence'],
                'confidence_percentage': plagiarism_result['confidence_percentage'],
                'plagiarism_type': plagiarism_result['plagiarism_type']
            }
        else:
            # Use basic analyzer
            basic_result = basic_analyzer.analyze(code1, code2, mode='basic', language=language)
            
            result = {
                'mode': 'basic',
                'language': language,
                'similarity_score': basic_result['similarity_score'],
                'similarity_percentage': basic_result['similarity_percentage'],
                'code1_length': basic_result['code1_length'],
                'code2_length': basic_result['code2_length']
            }
        
        # Generate diff view
        diff_html = generate_diff_html(code1, code2, file1.filename, file2.filename)
        
        # Add metadata
        result['file1_name'] = file1.filename
        result['file2_name'] = file2.filename
        result['code1_lines'] = len(code1.splitlines())
        result['code2_lines'] = len(code2.splitlines())
        result['timestamp'] = datetime.now().isoformat()
        result['diff_html'] = diff_html
        
        # Store analysis result in session for report generation
        session['last_analysis'] = result
        
        # Store in analyses database
        analysis_record = {
            'id': len(analyses_db) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'files': f"{file1.filename}, {file2.filename}",
            'language': language,
            'mode': mode,
            'similarity': result.get('weighted_percentage', result.get('similarity_percentage', 0)),
            'file_count': 2,
            'result': result
        }
        analyses_db.append(analysis_record)
        
        return jsonify(result)
    
    except UnicodeDecodeError:
        return jsonify({'error': 'Unable to decode file. Please ensure files are text-based.'}), 400
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500


@app.route('/about')
def about():
    """About page with information about the tool."""
    return render_template('about.html')


@app.route('/batch', methods=['GET', 'POST'])
def batch():
    """Batch comparison page and endpoint."""
    if request.method == 'GET':
        return render_template('batch.html')
    
    try:
        # Get uploaded files
        files_data = []
        
        for key in request.files:
            file = request.files[key]
            
            if file.filename == '' or not allowed_file(file.filename):
                continue
            
            content = file.read().decode('utf-8')
            files_data.append({
                'name': file.filename,
                'content': content
            })
        
        if len(files_data) < 2:
            return jsonify({'error': 'At least 2 files are required for batch comparison'}), 400
        
        # Get mode and language
        mode = request.form.get('mode', 'hybrid')
        language = get_file_language(files_data[0]['name'])
        
        # Perform batch comparison
        comparator = BatchComparator(mode=mode)
        result = comparator.compare_all_pairs(files_data, language)
        
        # Store in session
        session['last_batch_analysis'] = result
        
        # Store batch analysis in database
        file_names = ', '.join([f['name'] for f in files_data])
        avg_similarity = sum([r['similarity'] for r in result['results']]) / len(result['results']) if result['results'] else 0
        
        analysis_record = {
            'id': len(analyses_db) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'files': file_names,
            'language': language,
            'mode': mode,
            'similarity': avg_similarity,
            'file_count': len(files_data),
            'result': result
        }
        analyses_db.append(analysis_record)
        
        return jsonify(result)
    
    except UnicodeDecodeError:
        return jsonify({'error': 'Unable to decode files. Please ensure all files are text-based.'}), 400
    except Exception as e:
        return jsonify({'error': f'Batch analysis error: {str(e)}'}), 500


@app.route('/download/report/<format_type>')
def download_report(format_type):
    """Download analysis report in specified format."""
    try:
        # Get the last analysis result from session
        analysis_result = session.get('last_analysis')
        
        if not analysis_result:
            return jsonify({'error': 'No analysis result available. Please run an analysis first.'}), 400
        
        # Remove diff_html from report (too large for downloads)
        report_data = {k: v for k, v in analysis_result.items() if k != 'diff_html'}
        
        # Generate report based on format
        if format_type == 'text':
            report_content = generate_report(report_data, 'text')
            
            # Create response
            response = make_response(report_content)
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=cide_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            
            return response
        
        elif format_type == 'json':
            report_content = generate_report(report_data, 'json')
            
            response = make_response(report_content)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=cide_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            return response
        
        elif format_type == 'html':
            report_content = generate_report(report_data, 'html')
            
            response = make_response(report_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=cide_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            
            return response
        
        else:
            return jsonify({'error': f'Unsupported format: {format_type}. Use text, json, or html.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Report generation error: {str(e)}'}), 500


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'features': ['basic', 'ast', 'hybrid', 'plagiarism_detection', 'report_generation']
    })


# ==================== Admin Routes ====================

def require_admin():
    """Check if user is logged in as admin."""
    if not session.get('admin_logged_in'):
        return False
    return True


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard page."""
    if not require_admin():
        return render_template('admin_login.html')
    
    return render_template('admin.html')


@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_logged_in', None)
    return render_template('admin_login.html', message='Logged out successfully')


@app.route('/api/admin/analyses')
def get_analyses():
    """Get all analyses (admin only)."""
    if not require_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Return analyses without the full result details (too large)
    simplified_analyses = [
        {
            'id': a['id'],
            'timestamp': a['timestamp'],
            'files': a['files'],
            'language': a['language'],
            'mode': a['mode'],
            'similarity': a['similarity'],
            'file_count': a['file_count']
        }
        for a in analyses_db
    ]
    
    return jsonify({
        'success': True,
        'analyses': simplified_analyses
    })


@app.route('/api/admin/analysis/<int:analysis_id>')
def get_analysis_detail(analysis_id):
    """Get detailed analysis result (admin only)."""
    if not require_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    analysis = next((a for a in analyses_db if a['id'] == analysis_id), None)
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })


@app.route('/api/admin/analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete an analysis (admin only)."""
    if not require_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global analyses_db
    analyses_db = [a for a in analyses_db if a['id'] != analysis_id]
    
    return jsonify({
        'success': True,
        'message': 'Analysis deleted'
    })


@app.route('/api/admin/stats')
def get_admin_stats():
    """Get statistics for admin dashboard."""
    if not require_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    total_analyses = len(analyses_db)
    
    if total_analyses == 0:
        return jsonify({
            'success': True,
            'stats': {
                'total_analyses': 0,
                'avg_similarity': 0,
                'high_risk_count': 0,
                'total_files': 0,
                'language_distribution': {},
                'trend_data': []
            }
        })
    
    # Calculate statistics
    avg_similarity = sum(a['similarity'] for a in analyses_db) / total_analyses
    high_risk_count = sum(1 for a in analyses_db if a['similarity'] >= 80)
    total_files = sum(a['file_count'] for a in analyses_db)
    
    # Language distribution
    lang_dist = {}
    for a in analyses_db:
        lang = a['language']
        lang_dist[lang] = lang_dist.get(lang, 0) + 1
    
    # Trend data (last 7 days)
    from collections import defaultdict
    trend_data = defaultdict(int)
    
    for a in analyses_db:
        date = a['timestamp'].split(' ')[0]  # Get date part
        trend_data[date] += 1
    
    return jsonify({
        'success': True,
        'stats': {
            'total_analyses': total_analyses,
            'avg_similarity': round(avg_similarity, 1),
            'high_risk_count': high_risk_count,
            'total_files': total_files,
            'language_distribution': lang_dist,
            'trend_data': dict(trend_data)
        }
    })


if __name__ == '__main__':
    # Check if running in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    
    if not is_production:
        print("=" * 70)
        print("🚀 CIDE - Code Integrity Detection Engine")
        print("=" * 70)
        print("Starting web server...")
        print("Access the application at: http://localhost:5000")
        print("=" * 70)
    
    # Run with appropriate settings
    app.run(
        debug=not is_production,
        host='0.0.0.0',
        port=port
    )
