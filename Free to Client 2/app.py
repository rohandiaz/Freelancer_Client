from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Dummy project data (replace with actual data and logic)
projects = {
    '1': {'title': 'Web Development', 'skills_required': ['JavaScript', 'Web Development'], 'budget': 1000},
    '2': {'title': 'Data Analysis', 'skills_required': ['Python', 'Data Analysis'], 'budget': 1200},
    '3': {'title': 'Machine Learning', 'skills_required': ['Machine Learning', 'Python'], 'budget': 1500},
    '4': {'title': 'Mobile App Development', 'skills_required': ['Android', 'Java', 'Kotlin'], 'budget': 2000},
    '5': {'title': 'Front-end Redesign', 'skills_required': ['HTML', 'CSS', 'JavaScript', 'React'], 'budget': 1300},
    '6': {'title': 'Database Optimization', 'skills_required': ['SQL', 'PostgreSQL'], 'budget': 1400},
    '7': {'title': 'AI Chatbot Development', 'skills_required': ['Python', 'NLP', 'Machine Learning'], 'budget': 2500},
    '8': {'title': 'E-commerce Website', 'skills_required': ['PHP', 'MySQL', 'JavaScript'], 'budget': 1600},
    '9': {'title': 'Data Engineering Pipeline', 'skills_required': ['Python', 'Apache Airflow', 'ETL'], 'budget': 1700},
    '10': {'title': 'Cybersecurity Audit', 'skills_required': ['Network Security', 'Penetration Testing'], 'budget': 2200},
    '11': {'title': 'Cloud Infrastructure Setup', 'skills_required': ['AWS', 'Docker', 'Kubernetes'], 'budget': 3000},
    '12': {'title': 'Blockchain Smart Contract', 'skills_required': ['Solidity', 'Ethereum'], 'budget': 4000},
    '13': {'title': 'SEO Optimization', 'skills_required': ['SEO', 'Marketing'], 'budget': 900},
    '14': {'title': 'Digital Marketing Campaign', 'skills_required': ['Google Ads', 'Facebook Marketing', 'SEO'], 'budget': 800},
    '15': {'title': 'Game Development', 'skills_required': ['Unity', 'C#'], 'budget': 3500},
}

# Route for the main page, rendering the form for freelancer to input skills
@app.route('/')
def index():
    return render_template('index_freelancer.html')

# Function to calculate match score based on skills
def calculate_match_score(freelancer_skills, project_skills):
    matching_skills = set(freelancer_skills) & set(project_skills)
    return len(matching_skills) / len(project_skills)

# Route to handle form submission and provide filtered and sorted project recommendations
@app.route('/recommend_projects', methods=['POST'])
def recommend_projects():
    freelancer_skills = request.form.get('freelancer_skills').split(',')  # Example input: "Python, Data Analysis"
    freelancer_skills = [skill.strip() for skill in freelancer_skills]  # Clean up spaces
    
    # Weights for scoring (match score gets higher priority)
    match_weight = 0.7
    budget_weight = 0.3

    # Filter and score projects by skill match and budget
    scored_projects = []
    for pid, info in projects.items():
        match_score = calculate_match_score(freelancer_skills, info['skills_required'])
        weighted_score = match_weight * match_score + budget_weight * (info['budget'] / 10000)  # Normalize budget score
        scored_projects.append({'title': info['title'], 'skills_required': info['skills_required'], 
                                'budget': info['budget'], 'match_score': match_score, 
                                'weighted_score': weighted_score})

    # Sort projects by weighted score (descending)
    scored_projects.sort(key=lambda x: x['weighted_score'], reverse=True)

    return jsonify(scored_projects)

if __name__ == '__main__':
    app.run(debug=True)
