import os
import re
import httpx
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID")
DOCS_DIR = Path("docs")
MACHINES_DIR = DOCS_DIR / "machines"

notion = Client(auth=NOTION_TOKEN)

def extract_notion_title(page_object):
    """
    Robustly extracts the title of a Notion page.
    1. Checks 'properties' for type 'title'.
    2. Fallback: retrieves the first child block if it's a heading_1.
    """
    # Method 1: Check properties for 'title' type
    props = page_object.get("properties", {})
    for p_val in props.values():
        if p_val.get("type") == "title":
            title_list = p_val.get("title", [])
            if title_list and len(title_list) > 0:
                rich_text = title_list[0].get("rich_text", [])
                return "".join([r.get("plain_text", "") for r in rich_text])

    # Method 2: Fallback to first block if it's heading_1
    try:
        blocks = notion.blocks.children.list(block_id=page_object["id"], page_size=1)
        if blocks["results"]:
            first_block = blocks["results"][0]
            if first_block["type"] == "heading_1":
                rich_text = first_block["heading_1"].get("rich_text", [])
                return "".join([r.get("plain_text", "") for r in rich_text])
    except Exception:
        pass

    return None

def convert_block_to_markdown(block, img_dir=None):
    """
    Converts a Notion block to Markdown, supporting recursion for nested blocks.
    """
    block_type = block["type"]
    content = ""

    # Text extraction helper
    def get_text(block_data):
        rich_text = block_data.get("rich_text", [])
        return "".join([r.get("plain_text", "") for r in rich_text])

    if block_type == "paragraph":
        content = f"{get_text(block['paragraph'])}\n\n"
    elif block_type == "heading_1":
        content = f"# {get_text(block['heading_1'])}\n\n"
    elif block_type == "heading_2":
        content = f"## {get_text(block['heading_2'])}\n\n"
    elif block_type == "heading_3":
        content = f"### {get_text(block['heading_3'])}\n\n"
    elif block_type == "bulleted_list_item":
        content = f"- {get_text(block['bulleted_list_item'])}\n"
    elif block_type == "numbered_list_item":
        content = f"1. {get_text(block['numbered_list_item'])}\n"
    elif block_type == "code":
        text = block["code"]["rich_text"][0]["plain_text"] if block["code"]["rich_text"] else ""
        lang = block["code"].get("language", "text")
        content = f"```{lang}\n{text}\n```\n\n"
    elif block_type == "divider":
        content = "---\n\n"
    elif block_type == "quote":
        content = f"> {get_text(block['quote'])}\n\n"
    elif block_type == "callout":
        # Convert Notion Callout to MkDocs Admonition
        text = get_text(block["callout"])
        content = f"!!! info\n    {text}\n\n"
    elif block_type == "image":
        try:
            image_url = block["image"].get("file") or block["image"].get("external")
            if image_url:
                filename = f"img_{block['id']}.png"
                img_path = img_dir / filename if img_dir else Path(f"img/{filename}")

                # Download image
                with httpx.get(image_url) as resp:
                    if resp.status_code == 200:
                        with open(img_path, "wb") as f:
                            f.write(resp.content)

                # Link as relative path from index.md
                rel_path = f"img/{filename}" if img_dir else filename
                content = f"![Image]({rel_path})\n\n"
        except Exception as e:
            print(f"Error downloading image: {e}")
            content = "![Image Error]\n\n"

    # Recursive processing for children (nested lists, callouts, etc)
    if "children" in block and block["children"]: # This is usually not in the initial list
        pass # Notion API requires separate child retrieval

    return content

def process_page_content(page_id, machine_slug):
    """Retrieves all blocks recursively and converts to markdown."""
    all_markdown = ""
    img_dir = MACHINES_DIR / machine_slug / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    try:
        blocks = notion.blocks.children.list(block_id=page_id)
        results = blocks["results"]
        while blocks.get("has_more"):
            blocks = notion.blocks.children.list(block_id=page_id, start_cursor=blocks["next_cursor"])
            results.extend(blocks["results"])

        for block in results:
            # If block has children, we should process them recursively
            # but for simple write-ups, we'll handle the top-level and then any children if present.
            all_markdown += convert_block_to_markdown(block, img_dir)

            # Handle children for specific blocks like callouts or nested lists
            if block["has_children"]:
                child_blocks = notion.blocks.children.list(block_id=block["id"])
                # Basic indentation for nested content
                nested_md = "".join([convert_block_to_markdown(cb, img_dir) for cb in child_blocks["results"]])
                all_markdown += "    " + nested_md.replace("\n", "\n    ")

    except Exception as e:
        print(f"Error reading blocks for page {page_id}: {e}")

    return all_markdown

def sync_notion():
    print(f"Starting comprehensive scan of Root Page: {ROOT_PAGE_ID}")

    try:
        # 1. Get all children of the root page
        blocks = notion.blocks.children.list(block_id=ROOT_PAGE_ID)
        all_blocks = blocks["results"]
        while blocks.get("has_more"):
            blocks = notion.blocks.children.list(block_id=ROOT_PAGE_ID, start_cursor=blocks["next_cursor"])
            all_blocks.extend(blocks["results"])
    except Exception as e:
        print(f"Failed to scan root page: {e}")
        return

    for block in all_blocks:
        # Case A: The item is a child page
        if block["type"] == "child_page":
            page_id = block["id"]
            try:
                page = notion.pages.retrieve(page_id=page_id)
                title = extract_notion_title(page)

                if not title:
                    print(f"Could not extract title for page {page_id}, skipping.")
                    continue

                # Pattern matching for "Writeup -"
                if title.strip().lower().startswith("writeup -"):
                    original_title = title
                    clean_title = re.sub(r'^writeup\s*-\s*', '', title, flags=re.IGNORECASE).strip()
                    print(f"Matched: {original_title} -> {clean_title}")

                    slug = clean_title.lower().replace(" ", "_").replace("-", "_")
                    target_dir = MACHINES_DIR / slug
                    target_dir.mkdir(parents=True, exist_ok=True)

                    content = process_page_content(page_id, slug)
                    with open(target_dir / "index.md", "w", encoding="utf-8") as f:
                        f.write(f"# {clean_title}\n\n{content}")
                else:
                    print(f"Skipping page '{title}' (not a writeup)")

            except Exception as e:
                print(f"Error processing child page {page_id}: {e}")

        # Case B: The item is a database
        elif block["type"] == "child_database":
            db_id = block["id"]
            print(f"Scanning Database: {db_id}")
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
                            title = extract_notion_title(page)
                            if title and title.strip().lower().startswith("writeup -"):
                                original_title = title
                                clean_title = re.sub(r'^writeup\s*-\s*', '', title, flags=re.IGNORECASE).strip()
                                print(f"Matched in DB: {original_title} -> {clean_title}")

                                page_id = page["id"]
                                slug = clean_title.lower().replace(" ", "_").replace("-", "_")
                                target_dir = MACHINES_DIR / slug
                                target_dir.mkdir(parents=True, exist_ok=True)

                                content = process_page_content(page_id, slug)
                                with open(target_dir / "index.md", "w", encoding="utf-8") as f:
                                    f.write(f"# {clean_title}\n\n{content}")
                            else:
                                t = title if title else "Unknown"
                                print(f"Skipping DB item '{t}'")
                    else:
                        print(f"DB Query failed: {response.status_code}")
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
        sync_notion()
        git_commit_and_push()
        print("Sincronização concluída com sucesso!")
    except Exception as e:
        print(f"Erro crítico: {e}")
        import traceback
        traceback.print_exc()
