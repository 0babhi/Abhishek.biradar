
import json
import re
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"
INDEX_FILE = ROOT / "index.html"

START_MARKER = "<!-- AUTO_PROJECT_CARDS_START -->"
END_MARKER = "<!-- AUTO_PROJECT_CARDS_END -->"


def fetch_page_metadata(url):
    """Try to retrieve basic metadata from a public project page."""
    result = {
        "title": "",
        "description": "",
        "image": "",
    }

    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; PortfolioBot/1.0)"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type.lower():
                return result
            html = response.read(2_000_000).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError, OSError):
        return result

    def find_meta(*patterns):
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    result["title"] = find_meta(
        r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"']([^\"']*)",
        r"<meta[^>]+content=[\"']([^\"']*)[\"'][^>]+property=[\"']og:title[\"']",
        r"<title[^>]*>(.*?)</title>",
    )

    result["description"] = find_meta(
        r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']*)",
        r"<meta[^>]+content=[\"']([^\"']*)[\"'][^>]+name=[\"']description[\"']",
        r"<meta[^>]+property=[\"']og:description[\"'][^>]+content=[\"']([^\"']*)",
        r"<meta[^>]+content=[\"']([^\"']*)[\"'][^>]+property=[\"']og:description[\"']",
    )

    result["image"] = find_meta(
        r"<meta[^>]+property=[\"']og:image[\"'][^>]+content=[\"']([^\"']*)",
        r"<meta[^>]+content=[\"']([^\"']*)[\"'][^>]+property=[\"']og:image[\"']",
    )

    return result


def read_projects():
    """Load project.json files from each project folder."""
    projects = []

    if not PROJECTS_DIR.exists():
        return projects

    for config_path in sorted(PROJECTS_DIR.glob("*/project.json")):
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            url = config.get("url", "").strip()

            if not url.startswith(("https://", "http://")):
                print(f"Skipping invalid URL in {config_path}")
                continue

            folder_name = config_path.parent.name
            metadata = fetch_page_metadata(url)

            title = config.get("title") or metadata["title"] or folder_name.replace("-", " ").title()
            description = (
                config.get("description")
                or metadata["description"]
                or "Explore this project and its details on the original project page."
            )
            image = config.get("image") or metadata["image"]

            projects.append({
                "folder": folder_name,
                "title": title,
                "description": description,
                "url": url,
                "image": image,
            })

        except (OSError, json.JSONDecodeError) as error:
            print(f"Skipping {config_path}: {error}")

    return projects


def create_detail_page(project):
    """Generate a standalone HTML page for a project."""
    title = escape(project["title"])
    description = escape(project["description"])
    url = escape(project["url"], quote=True)
    image = escape(project["image"], quote=True)

    image_html = ""
    if image:
        image_html = (
            f'<img class="project-image" src="{image}" '
            f'alt="{title}" loading="lazy">'
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Project Portfolio</title>
  <meta name="description" content="{description}">
  <style>
    body {{
      font-family: Arial, sans-serif;
      max-width: 850px;
      margin: 50px auto;
      padding: 0 20px;
      line-height: 1.7;
      color: #222;
    }}
    .project-image {{
      max-width: 100%;
      max-height: 420px;
      object-fit: contain;
      border-radius: 12px;
    }}
    .button {{
      display: inline-block;
      padding: 12px 18px;
      margin: 10px 10px 10px 0;
      border-radius: 6px;
      background: #155eef;
      color: white;
      text-decoration: none;
    }}
    .back {{ background: #444; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>{description}</p>
  {image_html}
  <p>This page was generated automatically from your portfolio project configuration.</p>
  <a class="button" href="{url}" target="_blank" rel="noopener noreferrer">
    View Original Project
  </a>
  <a class="button back" href="../../index.html">Back to Portfolio</a>
</body>
</html>
"""

    output_file = PROJECTS_DIR / project["folder"] / "index.html"
    output_file.write_text(page, encoding="utf-8")
    print(f"Generated {output_file.relative_to(ROOT)}")


def create_project_card(project):
    """Generate a card linking to the project's detail page."""
    title = escape(project["title"])
    description = escape(project["description"])
    folder = escape(project["folder"], quote=True)

    image_html = ""
    if project["image"]:
        image = escape(project["image"], quote=True)
        image_html = (
            f'<img src="{image}" alt="{title}" '
            'loading="lazy" style="width:100%;max-height:180px;'
            'object-fit:cover;border-radius:8px;">'
        )

    return f"""
    <a class="project-card" href="projects/{folder}/"
       style="text-decoration:none;color:inherit;">
      {image_html}
      <h3>{title}</h3>
      <p>{description}</p>
      <span>View Project &rarr;</span>
    </a>
"""


def update_homepage(projects):
    """Replace only the generated section in index.html."""
    if not INDEX_FILE.exists():
        raise FileNotFoundError("index.html was not found in the repository root.")

    html = INDEX_FILE.read_text(encoding="utf-8")

    if html.count(START_MARKER) != 1 or html.count(END_MARKER) != 1:
        raise ValueError(
            "Add exactly one AUTO_PROJECT_CARDS_START and "
            "AUTO_PROJECT_CARDS_END marker inside the project grid in index.html."
        )

    start = html.index(START_MARKER) + len(START_MARKER)
    end = html.index(END_MARKER)

    if end < start:
        raise ValueError("The automatic project markers are in the wrong order.")

    cards = "\n".join(create_project_card(project) for project in projects)
    replacement = "\n" + cards + "\n"

    updated_html = html[:start] + replacement + html[end:]
    INDEX_FILE.write_text(updated_html, encoding="utf-8")
    print(f"Updated index.html with {len(projects)} automatic project card(s).")


def main():
    projects = read_projects()

    for project in projects:
        create_detail_page(project)

    update_homepage(projects)


if __name__ == "__main__":
    main()
```
