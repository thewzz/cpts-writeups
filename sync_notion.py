import os
import re
import httpx
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client
import subprocess

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID")
DOCS_DIR = Path("docs")
MACHINES_DIR = DOCS_DIR / "machines"

notion = Client(auth=NOTION_TOKEN)

def get_markdown_from_block(block_id):
    """Converts Notion blocks to Markdown."""
    try:
        block = notion.blocks.retrieve(block_id=block_id)
        block_type = block["type"]
        content = ""

        if block_type == "paragraph":
            text = "".join([r["plain_text"] for r in block["paragraph"]["rich_text"]])
            content = f"{text}\n\n"
        elif block_type == "heading_1":
            text = "".join([r["plain_text"] for r in block["heading_1"]["rich_text"]])
            content = f"# {text}\n\n"
        elif block_type == "heading_2":
            text = "".join([r["plain_text"] for r in block["heading_2"]["rich_text"]])
            content = f"## {text}\n\n"
        elif block_type == "heading_3":
            text = "".join([r["plain_text"] for r in block["heading_3"]["rich_text"]])
            content = f"### {text}\n\n"
        elif block_type == "bulleted_list_item":
            text = "".join([r["plain_text"] for r in block["bulleted_list_item"]["rich_text"]])
            content = f"- {text}\n"
        elif block_type == "numbered_list_item":
            text = "".join([r["plain_text"] for r in block["numbered_list_item"]["rich_text"]])
            content = f"1. {text}\n"
        elif block_type == "code":
            text = block["code"]["rich_text"][0]["plain_text"] if block["code"]["rich_text"] else ""
            lang = block["code"].get("language", "text")
            content = f"```{lang}\n{text}\n```\n\n"

        return content
    except Exception as e:
        print(f"Error processing block {block_id}: {e}")
        return ""

def process_page_content(page_id):
    """Retrieves all blocks of a page and converts them to markdown."""
    all_results = []
    try:
        blocks = notion.blocks.children.list(block_id=page_id)
        all_results.extend(blocks["results"])

        while blocks.get("has_more"):
            blocks = notion.blocks.children.list(block_id=page_id, start_cursor=blocks["next_cursor"])
            all_results.extend(blocks["results"])
    except Exception as e:
        print(f"Error reading blocks for page {page_id}: {e}")
        return ""

    return "".join([get_markdown_from_block(b["id"]) for b in all_results])

def sync_pages():
    print(f"Scanning Root Page {ROOT_PAGE_ID} for writeups...")

    try:
        blocks = notion.blocks.children.list(block_id=ROOT_PAGE_ID)
        all_blocks = blocks["results"]

        while blocks.get("has_more"):
            blocks = notion.blocks.children.list(block_id=ROOT_PAGE_ID, start_cursor=blocks["next_cursor"])
            all_blocks.extend(blocks["results"])
    except Exception as e:
        print(f"Error scanning root page: {e}")
        return

    for block in all_blocks:
        if block["type"] == "child_page":
            page_id = block["id"]
            try:
                # Use a more aggressive way to get the title
                page = notion.pages.retrieve(page_id=page_id)

                title = "Untitled"
                # The 'title' property in Notion pages is always in 'properties'
                props = page.get("properties", {})
                for p_name, p_val in props.items():
                    if p_val.get("type") == "title":
                        title_list = p_val.get("title", [])
                        if title_list and len(title_list) > 0:
                            rich_text = title_list[0].get("rich_text", [])
                            title = "".join([r.get("plain_text", "") for r in rich_text])
                        break

                print(f"Found page: '{title}'")

                if title.strip().lower().startswith("writeup -"):
                    original_title = title
                    title = title.replace("Writeup -", "").strip()
                    print(f"Matched Writeup Pattern: {original_title} -> {title}")

                    slug = title.lower().replace(" ", "_").replace("-", "_")
                    target_dir = MACHINES_DIR / slug
                    target_dir.mkdir(parents=True, exist_ok=True)

                    content = process_page_content(page_id)

                    with open(target_dir / "index.md", "w", encoding="utf-8") as f:
                        f.write(f"# {title}\n\n{content}")
                else:
                    print(f"Skipping page '{title}' (doesn't match 'Writeup -')")

            except Exception as e:
                print(f"Error retrieving page {page_id}: {e}")

        elif block["type"] == "child_database":
            db_id = block["id"]
            print(f"Found database: {db_id}. Attempting to query contents...")
            try:
                url = f"https://api.notion.com/v1/databases/{db_id}/query"
                headers = {
                    "Authorization": f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                }
                with httpx.Client() as client:
                    response = client.post(url, headers=headers, json={})
                    if response.status_code == 200:
                        results = response.json().get("results", [])
                        for page in results:
                            title = "Untitled"
                            props = page.get("properties", {})
                            for p_val in props.values():
                                if p_val.get("type") == "title":
                                    title_list = p_val.get("title", [])
                                    if title_list:
                                        title = "".join([r.get("plain_text", "") for r in title_list[0].get("rich_text", [])])
                                    break

                            if title.strip().lower().startswith("writeup -"):
                                original_title = title
                                title = title.replace("Writeup -", "").strip()
                                print(f"Found Writeup in DB: {original_title} -> {title}")

                                page_id = page["id"]
                                slug = title.lower().replace(" ", "_").replace("-", "_")
                                target_dir = MACHINES_DIR / slug
                                target_dir.mkdir(parents=True, exist_ok=True)

                                content = process_page_content(page_id)
                                with open(target_dir / "index.md", "w", encoding="utf-8") as f:
                                    f.write(f"# {title}\n\n{content}")
                            else:
                                print(f"Skipping DB page '{title}'")
                    else:
                        print(f"Could not query database {db_id}: {response.status_code}")
            except Exception as e:
                print(f"Error querying database {db_id}: {e}")

def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
        if status.returncode != 0:
            subprocess.run(["git", "commit", "-m", "Sync: Update writeups from Notion"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Changes pushed to GitHub.")
        else:
            print("No changes detected.")
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")

if __name__ == "__main__":
    try:
        sync_pages()
        git_commit_and_push()
        print("Sincronização concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a sincronização: {e}")
        import traceback
        traceback.print_exc()
