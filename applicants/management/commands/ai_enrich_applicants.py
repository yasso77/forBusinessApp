import os
import json
import re
from django.core.management.base import BaseCommand
from applicants.models import Applicant
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")


# =========================
# Helpers
# =========================
def clean_json(text: str) -> str:
    """
    Remove markdown fences and extra text
    """
    if not text:
        return ""

    # Remove ```json ``` wrappers
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    # Extract JSON object only
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else ""


def calculate_ai_confidence(data: dict) -> float:
    """
    Calculate confidence based on filled AI fields
    """
    fields = [
        "gender",
        "jobTitle",
        "yearsOfExperience",
        "skills",
        "languages",
        "educationLevel",
        "lastUniversity",
        "currentCountry",
        "targetCountry",
        "availability",
    ]

    filled = 0
    for field in fields:
        value = data.get(field)
        if value:
            if isinstance(value, list) and len(value) > 0:
                filled += 1
            elif isinstance(value, (str, int, float)):
                filled += 1

    return round((filled / len(fields)) * 100, 2)


# =========================
# Management Command
# =========================
class Command(BaseCommand):
    help = "AI enrichment of Applicant CV data"

    def handle(self, *args, **options):
        applicants = Applicant.objects.filter(parsedStatus=True)

        self.stdout.write(f"🔍 Enriching {applicants.count()} applicants")

        for applicant in applicants:
            try:
                prompt = f"""
You are an ATS CV parsing engine.

Return STRICT JSON ONLY.
Do NOT add explanations.
Do NOT wrap in markdown.

JSON schema:
{{
  "gender": "Male/Female/Unknown",
  "jobTitle": "",
  "yearsOfExperience": number,
  "skills": [],
  "languages": [{{"language": "", "level": ""}}],
  "educationLevel": "",
  "lastUniversity": "",
  "currentCountry": "",
  "currentCity": "",
  "targetCountry": "",
  "availability": ""
}}

CV TEXT:
{applicant.cvText}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You extract structured CV data."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )

                raw_content = response.choices[0].message.content
                cleaned = clean_json(raw_content)

                if not cleaned:
                    raise ValueError("Empty JSON from model")

                data = json.loads(cleaned)

                # =========================
                # Calculate AI Confidence
                # =========================
                ai_confidence = calculate_ai_confidence(data)

                # =========================
                # Update Applicant
                # =========================
                applicant.gender = data.get("gender") or applicant.gender
                applicant.jobTitle = data.get("jobTitle")
                applicant.yearsOfExperience = data.get("yearsOfExperience")
                applicant.skills = ", ".join(data.get("skills", []))
                applicant.languages = ", ".join(
                    f"{l.get('language')} ({l.get('level')})"
                    for l in data.get("languages", [])
                )
                applicant.educationLevel = data.get("educationLevel")
                applicant.lastUniversity = data.get("lastUniversity")
                applicant.currentCountry = data.get("currentCountry")
                applicant.currentCity = data.get("currentCity")
                applicant.targetCountry = data.get("targetCountry")
                applicant.availability = data.get("availability")

                # ✅ NEW
                applicant.aiConfidence = ai_confidence

                applicant.save(update_fields=[
                    "gender",
                    "jobTitle",
                    "yearsOfExperience",
                    "skills",
                    "languages",
                    "educationLevel",
                    "lastUniversity",
                    "currentCountry",
                    "currentCity",
                    "targetCountry",
                    "availability",
                    "aiConfidence",   # ✅ IMPORTANT
                ])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Enriched {applicant.fullName} (AI Confidence: {ai_confidence}%)"
                    )
                )

            except Exception as e:
                applicant.parsingErrors = str(e)
                applicant.save(update_fields=["parsingErrors"])

                self.stdout.write(
                    self.style.ERROR(f"❌ Failed {applicant.fullName}: {e}")
                )
