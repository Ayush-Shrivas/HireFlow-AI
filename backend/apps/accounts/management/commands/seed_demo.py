from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.companies.models import Company, CompanyMembership
from apps.jobs.models import Job, JobSkill, Skill

class Command(BaseCommand):
    help = "Create repeatable local demo users, company, skills, and 50+ published opportunities."

    OPPORTUNITIES = [
        ("Product Engineer", "Python,Django,React", "Remote"),
        ("Senior Backend Engineer", "Python,Django,PostgreSQL", "Bengaluru"),
        ("Frontend Engineer", "React,TypeScript,CSS", "Remote"),
        ("Full Stack Developer", "React,Node.js,PostgreSQL", "Hyderabad"),
        ("Machine Learning Engineer", "Python,TensorFlow,SQL", "Pune"),
        ("Data Scientist", "Python,SQL,Statistics", "Remote"),
        ("Data Analyst", "SQL,Python,Tableau", "Mumbai"),
        ("DevOps Engineer", "Docker,Kubernetes,AWS", "Chennai"),
        ("Cloud Solutions Architect", "AWS,Docker,Kubernetes", "Remote"),
        ("Site Reliability Engineer", "Kubernetes,Linux,Python", "Bengaluru"),
        ("Mobile App Developer", "React Native,TypeScript,Android", "Remote"),
        ("iOS Engineer", "Swift,iOS,Git", "Mumbai"),
        ("Android Engineer", "Kotlin,Android,REST", "Delhi"),
        ("QA Automation Engineer", "Selenium,Python,API Testing", "Hyderabad"),
        ("Test Engineer", "Cypress,JavaScript,Git", "Remote"),
        ("Security Engineer", "Python,Linux,AWS", "Bengaluru"),
        ("Application Security Analyst", "Security,Python,SQL", "Pune"),
        ("Solutions Engineer", "Python,REST,SQL", "Remote"),
        ("Technical Product Manager", "Agile,SQL,Analytics", "Bengaluru"),
        ("Product Designer", "Figma,UX Research,Design", "Remote"),
        ("UX Researcher", "UX Research,Analytics,Design", "Mumbai"),
        ("UI Designer", "Figma,CSS,Design", "Remote"),
        ("Technical Writer", "Documentation,API,Git", "Remote"),
        ("Developer Advocate", "Python,JavaScript,Documentation", "Remote"),
        ("Engineering Manager", "Leadership,Agile,Python", "Bengaluru"),
        ("Scrum Master", "Agile,Leadership,Communication", "Hyderabad"),
        ("Project Manager", "Agile,Planning,Communication", "Remote"),
        ("Business Analyst", "SQL,Analytics,Communication", "Mumbai"),
        ("Marketing Data Analyst", "SQL,Tableau,Analytics", "Delhi"),
        ("Growth Product Manager", "Analytics,SQL,Marketing", "Remote"),
        ("Customer Success Manager", "Communication,Analytics,CRM", "Pune"),
        ("Technical Support Engineer", "Linux,Python,SQL", "Chennai"),
        ("Database Administrator", "PostgreSQL,SQL,Linux", "Bengaluru"),
        ("Database Reliability Engineer", "PostgreSQL,Python,Docker", "Remote"),
        ("Platform Engineer", "Kubernetes,AWS,Python", "Hyderabad"),
        ("Infrastructure Engineer", "Linux,Docker,AWS", "Mumbai"),
        ("Network Engineer", "Linux,Security,AWS", "Delhi"),
        ("AI Research Engineer", "Python,TensorFlow,Statistics", "Bengaluru"),
        ("NLP Engineer", "Python,Machine Learning,SQL", "Remote"),
        ("Computer Vision Engineer", "Python,TensorFlow,OpenCV", "Pune"),
        ("Robotics Software Engineer", "Python,C++,Linux", "Chennai"),
        ("Blockchain Developer", "Python,JavaScript,Security", "Remote"),
        ("API Platform Developer", "Python,FastAPI,PostgreSQL", "Bengaluru"),
        ("Node.js Engineer", "Node.js,TypeScript,PostgreSQL", "Hyderabad"),
        ("Java Backend Engineer", "Java,Spring,SQL", "Mumbai"),
        ("Go Backend Engineer", "Go,Docker,Kubernetes", "Remote"),
        ("Ruby on Rails Engineer", "Ruby,PostgreSQL,Git", "Pune"),
        ("Technical Recruiter", "Recruiting,Communication,Analytics", "Bengaluru"),
        ("People Operations Specialist", "Communication,Planning,Analytics", "Remote"),
        ("Finance Systems Analyst", "SQL,Analytics,Excel", "Delhi"),
        ("Operations Analyst", "Analytics,SQL,Planning", "Mumbai"),
        ("Research Analyst", "Statistics,SQL,Research", "Remote"),
    ]

    def handle(self, *args, **options):
        recruiter, _ = User.objects.get_or_create(email="demo.recruiter@example.com", defaults={"role": User.Role.RECRUITER})
        recruiter.role = User.Role.RECRUITER
        recruiter.set_password("DemoPass123!")
        recruiter.save()
        candidate, _ = User.objects.get_or_create(email="demo.candidate@example.com", defaults={"role": User.Role.CANDIDATE})
        candidate.role = User.Role.CANDIDATE
        candidate.set_password("DemoPass123!")
        candidate.save()
        company, _ = Company.objects.get_or_create(slug="astrea-demo", defaults={"name": "Astrea Demo", "created_by": recruiter, "description": "Demo hiring workspace"})
        CompanyMembership.objects.get_or_create(company=company, user=recruiter, defaults={"role": CompanyMembership.Role.OWNER})
        created = 0
        for title, skill_names, location in self.OPPORTUNITIES:
            skills = [Skill.objects.get_or_create(name=name, defaults={"slug": name.lower().replace(" ", "-").replace(".", "")})[0] for name in skill_names.split(",")]
            job, was_created = Job.objects.get_or_create(company=company, title=title, defaults={"created_by": recruiter, "description": f"Join Astrea Demo as a {title} and build meaningful products with a collaborative team.", "location": location, "status": Job.Status.PUBLISHED, "min_experience": 2})
            if was_created:
                created += 1
            if job.status != Job.Status.PUBLISHED:
                job.status = Job.Status.PUBLISHED
                job.save(update_fields=("status", "updated_at"))
            for skill in skills:
                JobSkill.objects.get_or_create(job=job, skill=skill)
        self.stdout.write(self.style.SUCCESS(f"Demo data ready: {len(self.OPPORTUNITIES)} opportunities available; {created} created this run."))
        self.stdout.write("Login: demo.candidate@example.com / DemoPass123!")