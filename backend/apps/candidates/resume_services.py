import json
import re
import urllib.error
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings
from pypdf import PdfReader


def extract_resume_text(resume):
    extension = Path(resume.original_filename).suffix.lower()
    resume.file.open("rb")
    try:
        content = resume.file.read()
    finally:
        resume.file.close()
    if extension == ".txt":
        return content.decode("utf-8", errors="replace").strip()
    if extension == ".docx":
        with zipfile.ZipFile(BytesIO(content)) as document:
            xml = document.read("word/document.xml").decode("utf-8", errors="ignore")
        return re.sub(r"<[^>]+>", " ", xml).replace("&amp;", "&").strip()
    if extension == ".pdf":
        try:
            return " ".join((page.extract_text() or "") for page in PdfReader(BytesIO(content)).pages).strip()
        except Exception:
            return ""
    return ""


def analyze_with_ai(text, filename):
    payload = json.dumps({"text": text, "filename": filename}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if getattr(settings, "AI_SERVICE_TOKEN", ""):
        headers["X-Service-Token"] = settings.AI_SERVICE_TOKEN
    request = urllib.request.Request(f"{settings.AI_SERVICE_URL.rstrip('/')}/v1/resumes/analyze", data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return {"skills": [], "years_experience": 0, "summary": "AI analysis is pending."}
