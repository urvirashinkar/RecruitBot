# dummy_candidate.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from sqlalchemy import create_engine, text
from embedding_utils import flatten_candidate, get_embedding

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_CANDIDATES_COLLECTION = os.getenv("MONGO_CANDIDATES_COLLECTION", "candidates")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
candidates_col = mongo_db[MONGO_CANDIDATES_COLLECTION]

dummy_candidates = [
    {
        "personal_info": {
            "full_name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "+1234567890",
            "linkedin": "https://linkedin.com/in/alicesmith",
            "github": "https://github.com/alicesmith",
            "portfolio": "https://alicesmith.dev",
            "address": "123 Main St, City, Country",
            "summary": "Experienced data scientist with a passion for NLP and ML."
        },
        "education": [
            {
                "degree": "MSc",
                "major": "Computer Science",
                "university": "Tech University",
                "location": "City, Country",
                "start_date": "2018-09",
                "end_date": "2020-06",
                "gpa": "3.9"
            }
        ],
        "experience": [
            {
                "job_title": "Data Scientist",
                "company": "DataCorp",
                "location": "City, Country",
                "start_date": "2020-07",
                "end_date": "Present",
                "responsibilities": [
                    "Developed NLP models for text classification",
                    "Led a team of 4 data analysts",
                    "Deployed ML models to production"
                ],
                "technologies_used": ["Python", "TensorFlow", "scikit-learn"]
            }
        ],
        "projects": [
            {
                "project_name": "Resume Parser",
                "description": "Built a resume parser using spaCy and FastAPI.",
                "technologies": ["spaCy", "FastAPI"],
                "link": "https://github.com/alicesmith/resume-parser"
            }
        ],
        "skills": {
            "technical": ["Python", "ML", "NLP", "SQL"],
            "soft": ["Leadership", "Communication"],
            "languages": ["English", "Spanish"]
        },
        "certifications": [
            {
                "name": "TensorFlow Developer",
                "issuing_organization": "Google",
                "issue_date": "2021-03",
                "expiration_date": None,
                "credential_id": "12345",
                "credential_url": "https://google.com/cert/12345"
            }
        ],
        "achievements": ["Kaggle Competition Winner", "Published 3 papers"],
        "publications": [
            {
                "title": "Deep Learning for NLP",
                "journal": "AI Journal",
                "date": "2022-01",
                "url": "https://aijournal.com/dl-nlp"
            }
        ],
        "additional_info": {
            "interests": ["Hiking", "Chess"],
            "volunteer_experience": [
                {
                    "role": "Mentor",
                    "organization": "Tech4Good",
                    "start_date": "2021-01",
                    "end_date": "2022-01",
                    "description": "Mentored students in data science."
                }
            ]
        }
    },
    {
        "personal_info": {
            "full_name": "Bob Lee",
            "email": "bob@example.com",
            "phone": "+1987654321",
            "linkedin": "https://linkedin.com/in/boblee",
            "github": "https://github.com/boblee",
            "portfolio": "https://boblee.dev",
            "address": "456 Side St, City, Country",
            "summary": "Frontend engineer specializing in React and UI/UX design."
        },
        "education": [
            {
                "degree": "BSc",
                "major": "Information Technology",
                "university": "Design College",
                "location": "City, Country",
                "start_date": "2015-09",
                "end_date": "2019-06",
                "gpa": "3.7"
            }
        ],
        "experience": [
            {
                "job_title": "Frontend Engineer",
                "company": "Webify",
                "location": "City, Country",
                "start_date": "2019-07",
                "end_date": "Present",
                "responsibilities": [
                    "Built responsive web apps with React",
                    "Collaborated with designers for UI/UX",
                    "Optimized performance for large-scale apps"
                ],
                "technologies_used": ["JavaScript", "React", "TypeScript", "CSS"]
            }
        ],
        "projects": [
            {
                "project_name": "UI Component Library",
                "description": "Developed a reusable React component library.",
                "technologies": ["React", "Storybook"],
                "link": "https://github.com/boblee/ui-library"
            }
        ],
        "skills": {
            "technical": ["JavaScript", "React", "TypeScript", "CSS"],
            "soft": ["Teamwork", "Creativity"],
            "languages": ["English", "French"]
        },
        "certifications": [
            {
                "name": "React Professional",
                "issuing_organization": "Meta",
                "issue_date": "2022-05",
                "expiration_date": None,
                "credential_id": "67890",
                "credential_url": "https://meta.com/cert/67890"
            }
        ],
        "achievements": ["Hackathon Winner"],
        "publications": [],
        "additional_info": {
            "interests": ["Photography", "Travel"],
            "volunteer_experience": []
        }
    },
    {
        "personal_info": {
            "full_name": "Carol Zhang",
            "email": "carol@example.com",
            "phone": "+1122334455",
            "linkedin": "https://linkedin.com/in/carolzhang",
            "github": "https://github.com/carolzhang",
            "portfolio": "https://carolzhang.dev",
            "address": "789 High St, City, Country",
            "summary": "Product manager with a background in SaaS and agile teams."
        },
        "education": [
            {
                "degree": "MBA",
                "major": "Business Administration",
                "university": "Business School",
                "location": "City, Country",
                "start_date": "2016-09",
                "end_date": "2018-06",
                "gpa": "3.8"
            }
        ],
        "experience": [
            {
                "job_title": "Product Manager",
                "company": "SaaSify",
                "location": "City, Country",
                "start_date": "2018-07",
                "end_date": "Present",
                "responsibilities": [
                    "Led product roadmap for SaaS platform",
                    "Coordinated cross-functional teams",
                    "Launched new features based on user feedback"
                ],
                "technologies_used": ["Jira", "Figma", "SQL"]
            }
        ],
        "projects": [
            {
                "project_name": "User Analytics Dashboard",
                "description": "Launched analytics dashboard for SaaS customers.",
                "technologies": ["SQL", "Figma"],
                "link": "https://github.com/carolzhang/analytics-dashboard"
            }
        ],
        "skills": {
            "technical": ["SQL", "Figma", "Jira"],
            "soft": ["Leadership", "Strategic Thinking"],
            "languages": ["English", "Mandarin"]
        },
        "certifications": [
            {
                "name": "Certified Scrum Master",
                "issuing_organization": "Scrum Alliance",
                "issue_date": "2019-02",
                "expiration_date": None,
                "credential_id": "54321",
                "credential_url": "https://scrumalliance.org/cert/54321"
            }
        ],
        "achievements": ["Launched 3 SaaS products"],
        "publications": [],
        "additional_info": {
            "interests": ["Cooking", "Yoga"],
            "volunteer_experience": [
                {
                    "role": "Organizer",
                    "organization": "Women in Tech",
                    "start_date": "2020-01",
                    "end_date": "2021-01",
                    "description": "Organized networking events for women in tech."
                }
            ]
        }
    },
    {
    "personal_info": {
        "full_name": "David Johnson",
        "email": "david@example.com",
        "phone": "+1415123456",
        "linkedin": "https://linkedin.com/in/davidjohnson",
        "github": "https://github.com/davidjohnson",
        "portfolio": "https://davidjohnson.dev",
        "address": "101 River Rd, City, Country",
        "summary": "Backend developer with expertise in microservices and distributed systems."
    },
    "education": [
        {
            "degree": "BEng",
            "major": "Software Engineering",
            "university": "Tech Institute",
            "location": "City, Country",
            "start_date": "2014-09",
            "end_date": "2018-06",
            "gpa": "3.6"
        }
    ],
    "experience": [
        {
            "job_title": "Backend Developer",
            "company": "CloudNet",
            "location": "City, Country",
            "start_date": "2018-07",
            "end_date": "Present",
            "responsibilities": [
                "Designed RESTful APIs for SaaS platform",
                "Implemented CI/CD pipelines",
                "Worked on scalable distributed systems"
            ],
            "technologies_used": ["Java", "Spring Boot", "Docker", "Kubernetes"]
        }
    ],
    "projects": [
        {
            "project_name": "Scalable API Gateway",
            "description": "Built an API gateway to handle millions of requests.",
            "technologies": ["Java", "Spring Boot", "Kubernetes"],
            "link": "https://github.com/davidjohnson/api-gateway"
        }
    ],
    "skills": {
        "technical": ["Java", "Spring Boot", "Docker", "Kubernetes"],
        "soft": ["Problem-Solving", "Collaboration"],
        "languages": ["English", "German"]
    },
    "certifications": [
        {
            "name": "AWS Solutions Architect",
            "issuing_organization": "Amazon",
            "issue_date": "2021-08",
            "expiration_date": None,
            "credential_id": "11223",
            "credential_url": "https://aws.amazon.com/cert/11223"
        }
    ],
    "achievements": ["Built microservices architecture at scale"],
    "publications": [],
    "additional_info": {
        "interests": ["Cycling", "Gaming"],
        "volunteer_experience": []
    }
},
{
    "personal_info": {
        "full_name": "Emma Davis",
        "email": "emma@example.com",
        "phone": "+1987001122",
        "linkedin": "https://linkedin.com/in/emmadavis",
        "github": "https://github.com/emmadavis",
        "portfolio": "https://emmadavis.dev",
        "address": "202 Ocean Blvd, City, Country",
        "summary": "UX/UI designer passionate about creating intuitive digital products."
    },
    "education": [
        {
            "degree": "BA",
            "major": "Graphic Design",
            "university": "Design University",
            "location": "City, Country",
            "start_date": "2013-09",
            "end_date": "2017-06",
            "gpa": "3.8"
        }
    ],
    "experience": [
        {
            "job_title": "UX/UI Designer",
            "company": "Creatify",
            "location": "City, Country",
            "start_date": "2017-07",
            "end_date": "Present",
            "responsibilities": [
                "Designed mobile and web user interfaces",
                "Conducted user research and usability testing",
                "Collaborated with developers on design implementation"
            ],
            "technologies_used": ["Figma", "Adobe XD", "Sketch"]
        }
    ],
    "projects": [
        {
            "project_name": "Mobile Banking App Redesign",
            "description": "Led redesign of a banking app to improve usability.",
            "technologies": ["Figma", "Adobe XD"],
            "link": "https://dribbble.com/emmadavis"
        }
    ],
    "skills": {
        "technical": ["Figma", "Adobe XD", "Sketch"],
        "soft": ["Creativity", "Empathy"],
        "languages": ["English", "Italian"]
    },
    "certifications": [
        {
            "name": "Certified UX Designer",
            "issuing_organization": "NN/g",
            "issue_date": "2020-11",
            "expiration_date": None,
            "credential_id": "44556",
            "credential_url": "https://nngroup.com/cert/44556"
        }
    ],
    "achievements": ["Redesigned apps with 30% increase in engagement"],
    "publications": [],
    "additional_info": {
        "interests": ["Art", "Travel"],
        "volunteer_experience": []
    }
},
{
    "personal_info": {
        "full_name": "Frank Miller",
        "email": "frank@example.com",
        "phone": "+1555777888",
        "linkedin": "https://linkedin.com/in/frankmiller",
        "github": "https://github.com/frankmiller",
        "portfolio": "https://frankmiller.dev",
        "address": "303 Mountain Rd, City, Country",
        "summary": "DevOps engineer experienced in automation and cloud infrastructure."
    },
    "education": [
        {
            "degree": "MSc",
            "major": "Information Systems",
            "university": "Tech University",
            "location": "City, Country",
            "start_date": "2016-09",
            "end_date": "2018-06",
            "gpa": "3.7"
        }
    ],
    "experience": [
        {
            "job_title": "DevOps Engineer",
            "company": "InfraTech",
            "location": "City, Country",
            "start_date": "2018-07",
            "end_date": "Present",
            "responsibilities": [
                "Automated infrastructure provisioning with Terraform",
                "Managed CI/CD pipelines",
                "Monitored system performance and uptime"
            ],
            "technologies_used": ["Terraform", "AWS", "Jenkins", "Docker"]
        }
    ],
    "projects": [
        {
            "project_name": "CI/CD Automation",
            "description": "Implemented automated deployment pipelines.",
            "technologies": ["Jenkins", "Terraform"],
            "link": "https://github.com/frankmiller/cicd-automation"
        }
    ],
    "skills": {
        "technical": ["Terraform", "AWS", "Jenkins", "Docker"],
        "soft": ["Attention to Detail", "Collaboration"],
        "languages": ["English"]
    },
    "certifications": [
        {
            "name": "Certified Kubernetes Administrator",
            "issuing_organization": "CNCF",
            "issue_date": "2021-02",
            "expiration_date": "2024-02",
            "credential_id": "98765",
            "credential_url": "https://cncf.io/cert/98765"
        }
    ],
    "achievements": ["Reduced deployment time by 40%"],
    "publications": [],
    "additional_info": {
        "interests": ["Hiking", "Photography"],
        "volunteer_experience": []
    }
},
{
    "personal_info": {
        "full_name": "Grace Kim",
        "email": "grace@example.com",
        "phone": "+1222333444",
        "linkedin": "https://linkedin.com/in/gracekim",
        "github": "https://github.com/gracekim",
        "portfolio": "https://gracekim.dev",
        "address": "404 Lake View, City, Country",
        "summary": "AI researcher focused on computer vision and deep learning."
    },
    "education": [
        {
            "degree": "PhD",
            "major": "Artificial Intelligence",
            "university": "AI Research University",
            "location": "City, Country",
            "start_date": "2015-09",
            "end_date": "2020-06",
            "gpa": "4.0"
        }
    ],
    "experience": [
        {
            "job_title": "AI Research Scientist",
            "company": "VisionAI Labs",
            "location": "City, Country",
            "start_date": "2020-07",
            "end_date": "Present",
            "responsibilities": [
                "Published research papers on deep learning",
                "Built image classification and detection models",
                "Collaborated with universities on joint research"
            ],
            "technologies_used": ["Python", "PyTorch", "TensorFlow", "OpenCV"]
        }
    ],
    "projects": [
        {
            "project_name": "Medical Imaging AI",
            "description": "Developed AI for early cancer detection in scans.",
            "technologies": ["PyTorch", "OpenCV"],
            "link": "https://github.com/gracekim/medical-imaging-ai"
        }
    ],
    "skills": {
        "technical": ["Python", "PyTorch", "TensorFlow", "OpenCV"],
        "soft": ["Research", "Critical Thinking"],
        "languages": ["English", "Korean"]
    },
    "certifications": [],
    "achievements": ["Published 5+ papers in top AI journals"],
    "publications": [
        {
            "title": "Deep Learning in Medical Imaging",
            "journal": "Nature AI",
            "date": "2021-05",
            "url": "https://nature.com/ai/medical-imaging"
        }
    ],
    "additional_info": {
        "interests": ["Reading", "Swimming"],
        "volunteer_experience": []
    }
},
{
    "personal_info": {
        "full_name": "Henry Wilson",
        "email": "henry@example.com",
        "phone": "+1333444555",
        "linkedin": "https://linkedin.com/in/henrywilson",
        "github": "https://github.com/henrywilson",
        "portfolio": "https://henrywilson.dev",
        "address": "505 Central Ave, City, Country",
        "summary": "Full-stack developer experienced in building scalable SaaS applications."
    },
    "education": [
        {
            "degree": "BSc",
            "major": "Computer Science",
            "university": "Global Tech University",
            "location": "City, Country",
            "start_date": "2012-09",
            "end_date": "2016-06",
            "gpa": "3.5"
        }
    ],
    "experience": [
        {
            "job_title": "Full-stack Developer",
            "company": "SaaSPro",
            "location": "City, Country",
            "start_date": "2016-07",
            "end_date": "Present",
            "responsibilities": [
                "Built end-to-end SaaS applications",
                "Integrated payment gateways",
                "Optimized databases for performance"
            ],
            "technologies_used": ["Node.js", "React", "PostgreSQL", "AWS"]
        }
    ],
    "projects": [
        {
            "project_name": "E-commerce Platform",
            "description": "Developed a scalable e-commerce platform.",
            "technologies": ["Node.js", "React", "PostgreSQL"],
            "link": "https://github.com/henrywilson/ecommerce-platform"
        }
    ],
    "skills": {
        "technical": ["Node.js", "React", "PostgreSQL", "AWS"],
        "soft": ["Time Management", "Leadership"],
        "languages": ["English", "Spanish"]
    },
    "certifications": [
        {
            "name": "Google Cloud Professional Developer",
            "issuing_organization": "Google",
            "issue_date": "2022-06",
            "expiration_date": None,
            "credential_id": "224466",
            "credential_url": "https://cloud.google.com/cert/224466"
        }
    ],
    "achievements": ["Built SaaS apps serving 100k+ users"],
    "publications": [],
    "additional_info": {
        "interests": ["Basketball", "Music"],
        "volunteer_experience": []
    }
}

]


POSTGRES_URI = os.getenv("POSTGRES_URI")
pg_engine = create_engine(POSTGRES_URI)

if __name__ == "__main__":
    for candidate in dummy_candidates:
        result = candidates_col.insert_one(candidate)
        mongo_id = str(result.inserted_id)
        print(f"Inserted candidate with _id: {mongo_id}")
        flat = flatten_candidate(candidate)
        emb = get_embedding(flat)
        with pg_engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO candidates (candidate_id, content, embedding)
                VALUES (:cid, :content, :embedding)
            """), {"cid": mongo_id, "content": flat, "embedding": emb})
        print(f"Embedded and stored in NeonDB with candidate_id: {mongo_id}")
