# src/detect_tech.py

def detect_tech_stack(readme_text, file_list=None):
    tech_keywords = {
        "Python": ["pandas", "numpy", "tensorflow", "flask", "django", ".py"],
        "JavaScript": ["react", "vue", "angular", "node.js", "express", ".js"],
        "Java": ["spring", "hibernate", "maven", ".java"],
        "C++": ["boost", "openmp", ".cpp", ".hpp"],
        "R": ["ggplot2", "dplyr", ".r"],
        "Ruby": ["rails", "sinatra", ".rb"],
        "Go": ["gin", "beego", ".go"],
    }

    detected = set()
    # Check README content
    readme_lower = readme_text.lower()
    for tech, keywords in tech_keywords.items():
        if any(keyword.lower() in readme_lower for keyword in keywords):
            detected.add(tech)

    # Check file extensions if file_list is provided
    if file_list:
        for file_path in file_list:
            file_lower = file_path.lower()
            for tech, keywords in tech_keywords.items():
                if any(file_lower.endswith(keyword) for keyword in keywords if keyword.startswith(".")):
                    detected.add(tech)

    return ", ".join(detected) if detected else "Unknown"