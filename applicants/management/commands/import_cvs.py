import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
from tqdm import tqdm

from applicants.models import Applicant
from applicants.utils.cv_parser import (
    extract_pdf_text,
    extract_docx_text,
    normalize_text,
    detect_cv_language,
    extract_email,
    extract_mobile,
    extract_gender,
    extract_full_name,
    extract_job_title,
    extract_years_of_experience,
    extract_skills,
    extract_languages,
    extract_location,
    extract_target_country,
    extract_availability,
    extract_education_level,
    extract_university
)


class Command(BaseCommand):
    help = "Import CV files (PDF/DOCX) from local folder into Applicant table"

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            required=True,
            help='Absolute path to folder containing CV files'
        )

    def handle(self, *args, **options):
        cv_folder = options['path']

        if not os.path.exists(cv_folder):
            self.stdout.write(self.style.ERROR("❌ Folder does not exist"))
            return

        files = [
            f for f in os.listdir(cv_folder)
            if f.lower().endswith(('.pdf', '.docx'))
        ]

        if not files:
            self.stdout.write(self.style.WARNING("⚠ No CV files found"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"📂 Found {len(files)} CV files")
        )

        imported = 0
        skipped = 0
        failed = 0

        for filename in tqdm(files, desc="Importing CVs"):
            file_path = os.path.join(cv_folder, filename)

            # Skip already imported CVs
            if Applicant.objects.filter(cvOriginalFileName=filename).exists():
                skipped += 1
                continue

            try:
                # =====================================================
                # Extract CV Text
                # =====================================================
                if filename.lower().endswith('.pdf'):
                    cv_text = extract_pdf_text(file_path)
                else:
                    cv_text = extract_docx_text(file_path)

                if not cv_text.strip():
                    raise ValueError("Empty CV content")

                normalized_text = normalize_text(cv_text)
                cv_language = detect_cv_language(cv_text)

                # =====================================================
                # Extract Structured Fields
                # =====================================================
                email = extract_email(cv_text)
                mobile = extract_mobile(cv_text)
                gender = extract_gender(cv_text)

                extracted_name = extract_full_name(cv_text)
                full_name = extracted_name or os.path.splitext(filename)[0].replace('_', ' ')

                job_title = extract_job_title(cv_text)
                years_experience = extract_years_of_experience(cv_text)
                skills = extract_skills(cv_text)
                languages = extract_languages(cv_text)

                current_city, current_country = extract_location(cv_text)
                target_country = extract_target_country(cv_text)
                availability = extract_availability(cv_text)

                education_level = extract_education_level(cv_text)
                last_university = extract_university(cv_text)

                # =====================================================
                # Save Applicant
                # =====================================================
                with transaction.atomic():
                    applicant = Applicant(
                        fullName=full_name,
                        fullNameNormalized=normalize_text(full_name),
                        email=email,
                        mobile=mobile,
                        gender=gender,
                        cvLanguage=cv_language,
                        jobTitle=job_title,
                        yearsOfExperience=years_experience,
                        skills=skills,
                        languages=languages,
                        currentCountry=current_country,
                        currentCity=current_city,
                        targetCountry=target_country,
                        availability=availability,
                        educationLevel=education_level,
                        lastUniversity=last_university,
                        cvOriginalFileName=filename,
                        cvText=cv_text,
                        cvTextNormalized=normalized_text,
                        parsedStatus=True,
                        source="Local CV Batch Import"
                    )

                    with open(file_path, 'rb') as f:
                        applicant.cvFile.save(filename, File(f), save=False)

                    applicant.save()

                imported += 1

            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed {filename}: {str(e)}")
                )

        # =====================================================
        # Summary
        # =====================================================
        self.stdout.write(self.style.SUCCESS("✅ Import completed"))
        self.stdout.write(f"✔ Imported: {imported}")
        self.stdout.write(f"⏭ Skipped: {skipped}")
        self.stdout.write(f"❌ Failed: {failed}")
