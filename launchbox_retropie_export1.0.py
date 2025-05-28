import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
import difflib
from PIL import Image

# ==== DATA ENTRY SECTION ====
# Set these two paths before running!
lb_dir = r'C:\Users\derek\LaunchBox'  # <-- CHANGE THIS TO WHERE LAUNCHBOX IS
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ready_for_export")  # Output to script location

# List the platforms you want to export: {LaunchBox platform name: output subfolder name}
platforms = {
    "Nintendo Entertainment System": "nes",
    #"Sega Genesis": "megadrive",
    #"Sony Playstation": "psx",
    # Add/remove as needed!
}

# Media types to look for. Key = ES field, Value = (LaunchBox subfolder, output subfolder, allowed extensions)
media_types = {
    "image":      ("Box - Front",        "images",      ['.png', '.jpg', '.jpeg']),
    "marquee":    ("Clear Logo",         "marquee",     ['.png', '.jpg', '.jpeg']),
    "video":      ("",                   "videos",      ['.mp4', '.avi']),
    "thumbnail":  ("Screenshot - Gameplay", "thumbnails",  ['.png', '.jpg', '.jpeg']),
    # Use "Screenshot - Gameplay" or whatever LaunchBox subdir you prefer!
}


# All EmulationStation fields that could be relevant
fields = [
    "name", "sortname", "desc", "image", "video", "marquee", "thumbnail", "screenshot",
    "releasedate", "developer", "publisher", "genre", "path"
]
# ==== END DATA ENTRY SECTION ====


def get_xml_text(node, tag):
    found = node.find(tag)
    return found.text if found is not None else ""

#def copy_media(game_title, lb_media_dir, export_media_dir, extensions):
    """Searches for a media file for game_title and copies it to export_media_dir. Returns the ES local path."""
    if not os.path.isdir(lb_media_dir):
        print(f"    !! No media dir: {lb_media_dir}")
        return ""
    # Fuzzy match best file
    candidates = []
    for fname in os.listdir(lb_media_dir):
        for ext in extensions:
            if fname.lower().endswith(ext):
                ratio = difflib.SequenceMatcher(None, game_title.lower(), fname.lower()).ratio()
                candidates.append((ratio, fname))
    if not candidates:
        print(f"    -- No media files with allowed extensions in {lb_media_dir}")
        return ""
    best_ratio, best_match = max(candidates, key=lambda x: x[0])
    if best_ratio > 0.6:  # threshold for "close enough"
        src_path = os.path.join(lb_media_dir, best_match)
        dest_path = os.path.join(export_media_dir, best_match)
        print(f"    [FUZZY COPY] {src_path} -> {dest_path} (score={best_ratio:.2f})")
        if not os.path.isfile(dest_path):
            shutil.copy2(src_path, dest_path)
        return "./" + os.path.relpath(dest_path, start=os.path.dirname(export_media_dir))
    else:
        print(f"    -- No fuzzy match for '{game_title}' in {lb_media_dir} (best: '{best_match}', score={best_ratio:.2f})")
        return ""

#def copy_media(game_title, lb_media_dir, export_media_dir, extensions):
    """Recursively searches for a media file for game_title, copies it to export_media_dir. Returns the ES local path."""
    if not os.path.isdir(lb_media_dir):
        print(f"    !! No media dir: {lb_media_dir}")
        return ""
    # Fuzzy match best file in all subdirs
    candidates = []
    for root, dirs, files in os.walk(lb_media_dir):
        for fname in files:
            for ext in extensions:
                if fname.lower().endswith(ext):
                    ratio = difflib.SequenceMatcher(None, game_title.lower(), fname.lower()).ratio()
                    candidates.append((ratio, os.path.join(root, fname)))
    if not candidates:
        print(f"    -- No media files with allowed extensions in {lb_media_dir}")
        return ""
    best_ratio, best_match_fullpath = max(candidates, key=lambda x: x[0])
    if best_ratio > 0.6:  # threshold for "close enough"
        dest_path = os.path.join(export_media_dir, os.path.basename(best_match_fullpath))
        print(f"    [FUZZY RECURSIVE COPY] {best_match_fullpath} -> {dest_path} (score={best_ratio:.2f})")
        if not os.path.isfile(dest_path):
            shutil.copy2(best_match_fullpath, dest_path)
        return "./" + os.path.relpath(dest_path, start=os.path.dirname(export_media_dir))
    else:
        print(f"    -- No fuzzy match for '{game_title}' in {lb_media_dir} (best: '{os.path.basename(best_match_fullpath)}', score={best_ratio:.2f})")
        return ""

def copy_media(game_title, lb_media_dir, export_media_dir, extensions, max_image_size=500):
    """Recursively searches for a media file for game_title, copies & resizes to export_media_dir. Returns the ES local path."""
    if not os.path.isdir(lb_media_dir):
        print(f"    !! No media dir: {lb_media_dir}")
        return ""
    candidates = []
    for root, dirs, files in os.walk(lb_media_dir):
        for fname in files:
            for ext in extensions:
                if fname.lower().endswith(ext):
                    ratio = difflib.SequenceMatcher(None, game_title.lower(), fname.lower()).ratio()
                    candidates.append((ratio, os.path.join(root, fname)))
    if not candidates:
        print(f"    -- No media files with allowed extensions in {lb_media_dir}")
        return ""
    best_ratio, best_match_fullpath = max(candidates, key=lambda x: x[0])
    if best_ratio > 0.6:  # threshold for "close enough"
        dest_path = os.path.join(export_media_dir, os.path.basename(best_match_fullpath))
        print(f"    [FUZZY RECURSIVE COPY/RESIZE] {best_match_fullpath} -> {dest_path} (score={best_ratio:.2f})")
        if not os.path.isfile(dest_path):
            try:
                with Image.open(best_match_fullpath) as img:
                    w, h = img.size
                    if max(w, h) > max_image_size:
                        img.thumbnail((max_image_size, max_image_size), Image.LANCZOS)
                        img.save(dest_path, optimize=True, quality=85)
                        print(f"      ...resized to {img.size}")
                    else:
                        img.save(dest_path, optimize=True, quality=85)
            except Exception as e:
                print(f"      !! Could not resize image, falling back to copy: {e}")
                shutil.copy2(best_match_fullpath, dest_path)
        return "./" + os.path.relpath(dest_path, start=os.path.dirname(export_media_dir))
    else:
        print(f"    -- No fuzzy match for '{game_title}' in {lb_media_dir} (best: '{os.path.basename(best_match_fullpath)}', score={best_ratio:.2f})")
        return ""


def main():
    print(f"Exporting from LaunchBox directory: {lb_dir}")
    print(f"Exporting to: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    for lb_platform, out_folder in platforms.items():
        print(f"\nProcessing platform: {lb_platform} --> {out_folder}")

        lb_platform_xml = os.path.join(lb_dir, "Data", "Platforms", f"{lb_platform}.xml")
        platform_export_dir = os.path.join(output_dir, out_folder)
        os.makedirs(platform_export_dir, exist_ok=True)

        # Set up all media output subfolders
        media_out_dirs = {}
        for k, (_, subfolder, _) in media_types.items():
            media_out_dirs[k] = os.path.join(platform_export_dir, subfolder)
            os.makedirs(media_out_dirs[k], exist_ok=True)

        # Assume ROMs live in LaunchBox\Games\<Platform> or let user adjust here:
        roms_source_dir = os.path.join(lb_dir, "Games", lb_platform)
        if not os.path.isdir(roms_source_dir):
            print(f"  !! ROM source directory not found: {roms_source_dir}")
            continue

        # Parse LaunchBox platform XML
        try:
            tree = ET.parse(lb_platform_xml)
            root = tree.getroot()
        except Exception as e:
            print(f"  !! Failed to parse XML: {lb_platform_xml}\n  {e}")
            continue

        games = []
        for game in root.findall("Game"):
            title = get_xml_text(game, "Title")
            print(f"  > Processing game: {title}")
            sortname = get_xml_text(game, "SortTitle") or title
            desc = get_xml_text(game, "Notes")
            release = get_xml_text(game, "ReleaseDate")
            developer = get_xml_text(game, "Developer")
            publisher = get_xml_text(game, "Publisher")
            genre = get_xml_text(game, "Genre")
            app_path = get_xml_text(game, "ApplicationPath")
            rom_filename = os.path.basename(app_path)

            # Copy ROM file (if it exists in the source dir)
            rom_src_path = os.path.join(roms_source_dir, rom_filename)
            rom_dest_path = os.path.join(platform_export_dir, rom_filename)
            if os.path.isfile(rom_src_path):
                shutil.copy2(rom_src_path, rom_dest_path)
                print(f"    [ROM COPY] {rom_src_path} -> {rom_dest_path}")
            elif os.path.isfile(app_path):  # fallback for absolute paths
                shutil.copy2(app_path, rom_dest_path)
                print(f"    [ROM COPY] {app_path} -> {rom_dest_path}")
            else:
                print(f"    -- ROM not found for game: {title}  (looked for {rom_src_path})")

            # Gather and copy all media
            media_paths = {}
            for key, (lb_subdir, subfolder, exts) in media_types.items():
                if key == "video":
                    lb_media_dir = os.path.join(lb_dir, "Videos", lb_platform)
                else:
                    lb_media_dir = os.path.join(lb_dir, "Images", lb_platform, lb_subdir)
                media_paths[key] = copy_media(title, lb_media_dir, media_out_dirs[key], exts)

            game_entry = {
                "name": title,
                "sortname": sortname,
                "desc": desc,
                "image": media_paths.get("image", ""),
                "video": media_paths.get("video", ""),
                "marquee": media_paths.get("marquee", ""),
                "thumbnail": media_paths.get("thumbnail", ""),
                "screenshot": media_paths.get("screenshot", ""),
                "releasedate": release,
                "developer": developer,
                "publisher": publisher,
                "genre": genre,
                "path": "./" + rom_filename
            }
            games.append(game_entry)

        # Write gamelist.xml
        top = ET.Element('gameList')
        for game in games:
            child = ET.SubElement(top, 'game')
            for key in fields:
                field_el = ET.SubElement(child, key)
                field_el.text = game.get(key, "")

        xmlstr = minidom.parseString(ET.tostring(top)).toprettyxml(indent="    ")
        with open(os.path.join(platform_export_dir, "gamelist.xml"), "w", encoding="utf-8") as f:
            f.write(xmlstr)

        print(f"  {len(games)} games exported to: {platform_export_dir}")

if __name__ == "__main__":
    main()
