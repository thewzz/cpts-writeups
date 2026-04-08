import os
import re
import httpx
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client
import subprocess

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_ROOT_PAGE_ID")
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

def sync_database():
    print(f"Querying Database {DATABASE_ID} using HTTPX...")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json={})
            response.raise_for_status()
            results = response.json().get("results", [])
    except Exception as e:
        print(f"Error querying database: {e}")
        return

    if not results:
        print("No results found in database. Make sure the bot is connected to the database page!")
        return

    for page in results:
        title = "Untitled"
        props = page["properties"]
        for p_name, p_val in props.items():
            if p_val["type"] == "title":
                title_list = p_val.get("title", [])
                if title_list:
                    # Safely extract plain_text from rich_text
                    text_parts = []
                    for rich_text_item in title_list[0].get("rich_text", []):
                        text_parts.append(rich_text_item.get("plain_text", ""))
                    title = "".join(text_parts)
                break

        print(f"Processing: {title}")
        page_id = page["id"]

        slug = title.lower().replace(" ", "_")
        target_dir = MACHINES_DIR / slug
        target_dir.mkdir(parents=True, exist_ok=True)

        content = process_page_content(page_id)

        with open(target_dir / "index.md", "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")

def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
        if status.returncode != 0:
            subprocess.run(["git", "commit", "-m", "Sync: Update writeups from Notion Database"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Changes pushed to GitHub.")
        else:
            print("No changes detected.")
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")

if __name__ == "__main__":
    try:
        sync_database()
        git_commit_and_push()
        print("Sincronização concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a sincronização: {e}")
        import traceback
        traceback.print_exc()
