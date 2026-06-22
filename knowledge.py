# This program will serve as the core manual knowledge which is the base layer. These are facts that are encoded as a safety net in case the website or documents don't cover something.

# knowledge.py
from scraper import scrape_all
from document_loader import load_all_documents

# ── Layer 1: Manual / Hardcoded Knowledge ────────────────────────────────────
MANUAL_KNOWLEDGE = """
=== UP MINDANAO — CORE FACTS ===

IDENTITY:
- Full name: University of the Philippines Mindanao
- Part of the UP System (8th constituent university)
- Location: Mintal, Davao City, 8022, Philippines
- Founded: 1995
- Website: https://www.upmin.edu.ph

COLLEGES:
- College of Science and Mathematics (CSM)
- College of Humanities and Social Sciences (CHSS)
- School of Management (SOM)

PROGRAMS OFFERED:
CSM  → BS Biology, BS Applied Mathematics, BS Computer Science, BS Food Technology, BS Data Science, MS Food Science, MS Biology, MS Civil Engineering, MS Industrial Engineering, MEng Industrial Engineering
CHSS → BS Architecture, MA Urban and Regional Planning, BA English (Creative Writing), BA Communication and Media Arts, AA Sports Studies, B Sports Science, Diploma in Exercise and Sports Science, BS Anthropology, MS Human Movement Science
SOM  → BS Agribusiness Economics, Master in Management, PhD by Research


ADMISSION:
- Freshmen enter via UPCAT (UP College Admission Test)
- Applications open around August to September each year
- Transferees may apply within first 2 weeks of the semester
- Shiftees follow internal UP Mindanao procedures

ACADEMIC CALENDAR:
- 1st Semester: August – December
- 2nd Semester: January – May
- Midyear: June – July (limited course offerings)

STUDENT SERVICES:
- Office of Student Affairs (OSA): scholarships, orgs, student concerns
- University Library: open to all bonafide students
- University Dormitory: available, apply through OSA

FEES:
- UP uses Socialized Tuition System (STS)
- UP is eligible for free tuition under the Universal Access to Quality Tertiary Education Act (RA 10931). However, you can opt to pay voluntarily if you are financially capable and wish to support the university.

CONTACT:
- Email: ovca@up.edu.ph
- Location: Mintal, Davao City

=== END CORE FACTS ===
"""


# ── Combine All 3 Layers ─────────────────────────────────────────────────────
def build_knowledge_base():
    """Combine manual facts + website scrape + documents into one knowledge base."""

    print("Building knowledge base...")

    # Layer 1: always available
    manual = MANUAL_KNOWLEDGE

    # Layer 2: from the website
    website = scrape_all()

    # Layer 3: from uploaded documents
    documents = load_all_documents()

    combined = f"""
{manual}

{website}

{documents}
""".strip()

    print(f"Knowledge base ready. ({len(combined):,} characters total)\n")
    return combined


# ── Build the System Prompt ───────────────────────────────────────────────────
def get_system_prompt():
    knowledge = build_knowledge_base()

    return f"""
You are an AI assistant for UP Mindanao (University of the Philippines Mindanao).
You help students, prospective applicants, faculty, and visitors.

RULES:
1. Only answer based on the knowledge provided below.
2. If something is not in the knowledge base, say:
   "I don't have that information right now. Please check
   https://www.upmin.edu.ph or contact the relevant office directly."
3. Be friendly, clear, and concise.
4. If asked about admission, always mention UPCAT and the official website.
5. Never make up names, dates, or figures.

=== KNOWLEDGE BASE ===
{knowledge}
=== END KNOWLEDGE BASE ===
"""


# Test standalone
if __name__ == "__main__":
    prompt = get_system_prompt()
    print(f"System prompt length: {len(prompt):,} characters")
    print("\nFirst 1000 characters preview:")
    print(prompt[:1000])