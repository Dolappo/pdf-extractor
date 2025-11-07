# urls_config.py - Configuration file for NERDC PDF downloads

# Simple list of URLs
BASIC_URLS = [
"https://nerdc.gov.ng/content_manager/primary/pri1-3_basic_science_intro.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_cca.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_english_studies.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_french.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_maths.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_yoruba.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_prevoc.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_national_values.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_igbo.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri1-3_hausa.pdf", 
"https://nerdc.gov.ng/content_manager/primary/pri4-6_basic_science_intro.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_cca.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_english_studies.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_french.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_maths.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_yoruba.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_prevoc.pdf",
"https://nerdc.gov.ng/content_manager/primary/pri4-6_national_values.pdf",
    # Add more URLs here...
]

# URLs with custom filenames and metadata
DETAILED_URLS = [
    {
        "url": "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_basic_science_intro.pdf",
        "filename": "Primary_1-3_Basic_Science.pdf",
        "description": "Basic Science curriculum for Primary 1-3"
    },
    {
        "url": "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_basic_science_intro.pdf", 
        "filename": "Primary_4-6_Basic_Science.pdf",
        "description": "Basic Science curriculum for Primary 4-6"
    },
    {
        "url": "https://nerdc.gov.ng/content_manager/view_sec.html?pdf=jss1-3_basic_science_intro.pdf",
        "filename": "JSS_1-3_Basic_Science.pdf", 
        "description": "Basic Science curriculum for Junior Secondary 1-3"
    },
    # Add more detailed entries here...
]

# Subject-specific collections
MATHEMATICS_URLS = [
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_mathematics_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_mathematics_intro.pdf",
    # Add more math URLs...
]

ENGLISH_URLS = [
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_english_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_english_intro.pdf",
    # Add more English URLs...
]

# Complete curriculum download (example)
ALL_PRIMARY_SUBJECTS = [
    # Primary 1-3
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_basic_science_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_mathematics_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_english_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_social_studies_intro.pdf",
    
    # Primary 4-6  
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_basic_science_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_mathematics_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_english_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_social_studies_intro.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_cca.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_french.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_yoruba.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_prevoc.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_national_values.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_igbo.pdf",
    "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri4-6_hausa.pdf",
    # Add more as needed...
]