from flask import Flask, render_template, request
import os
from parser import extract_text_from_file, score_resume

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Job Role to Skills Mapping
ROLE_SKILLS = {
    "Python Developer": ["Python", "Flask", "Django"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python"],
    "Territory Manager": ["Sales", "CRM", "Communication", "Team Management", "Strategic Planning"]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_roles = request.form.getlist('role')
        selected_skills = request.form.getlist('skills')

        # Add role-based skills automatically
        for role in job_roles:
            if role in ROLE_SKILLS:
                selected_skills.extend(ROLE_SKILLS[role])
        selected_skills = list(set(selected_skills))  # Remove duplicates

        uploaded_files = request.files.getlist("resumes")
        results = []

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                extracted_text = extract_text_from_file(file_path)
                score = score_resume(extracted_text, selected_skills)
                results.append((file.filename, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return render_template('index.html', results=results, selected_skills=selected_skills)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
