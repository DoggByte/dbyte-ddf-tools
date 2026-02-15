import os
import logging
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Union

# Try to import mutagen, but allow the script to be defined even if not installed yet
try:
    from mutagen.flac import FLAC
except ImportError:
    FLAC = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CONFIG = {
    'filename_flac_list': 'flac-files-list.txt',
    'filename_all_flac_files': 'all-flac-files.txt',
    'filename_serie_flac': 'serie_flac.json',
    'script_version': '1.00.00',
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'flac_source': 'Amazon',
    # Note: filename_flac_vorbis_comment is used here to refer to the pattern requirement
}

def get_vorbis_comments_dict(flac_path: str) -> Dict[str, List[str]]:
    """Extracts Vorbis comments from a FLAC file as a dictionary."""
    if FLAC is None:
        return {"error": "mutagen library not installed"}
    
    try:
        audio = FLAC(flac_path)
        if audio.tags:
            # mutagen tags are already a dict-like object where values are lists
            return dict(audio.tags)
        return {}
    except Exception as e:
        return {"error": f"Error extracting Vorbis comments: {e}"}

def get_vorbis_comments(flac_path: str) -> str:
    """Extracts Vorbis comments from a FLAC file as a formatted string."""
    tags_dict = get_vorbis_comments_dict(flac_path)
    if "error" in tags_dict and len(tags_dict) == 1:
        return tags_dict["error"]
    
    comments = []
    for key, values in tags_dict.items():
        for value in values:
            comments.append(f"{key}={value}")
    return "\n".join(comments)

def main():
    if FLAC is None:
        logger.warning("mutagen is not installed. Vorbis comment extraction will fail.")
        logger.info("Please install it using: pip install mutagen")

    root_dir = os.getcwd()
    all_flac_files: List[str] = []
    serie_data = []
    
    # Walk through all folders
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter for FLAC files in the current folder
        flac_in_folder = sorted([f for f in filenames if f.lower().endswith('.flac')])
        
        if not flac_in_folder:
            continue
            
        folder_flac_paths = []
        folder_vorbis_comments = []
        for flac_file in flac_in_folder:
            full_path = os.path.abspath(os.path.join(dirpath, flac_file))
            folder_flac_paths.append(full_path)
            all_flac_files.append(full_path)
            
            # 1. Create 1 txt file per FLAC with vorbis_comment block
            # Requirement: "the filename containing the content of this variable with be the same as the filename of the flac file but with a txt extension"
            vorbis_base_path = os.path.splitext(full_path)[0]
            
            vorbis_txt_path = vorbis_base_path + '.txt'
            comments_str = get_vorbis_comments(full_path)
            with open(vorbis_txt_path, 'w', encoding='utf-8') as f:
                f.write(comments_str)
            
            # 1b. Create 1 json file per FLAC with vorbis_comment block
            vorbis_json_path = vorbis_base_path + '.json'
            comments_dict = get_vorbis_comments_dict(full_path)
            folder_vorbis_comments.append(comments_dict)
            with open(vorbis_json_path, 'w', encoding='utf-8') as f:
                json.dump(comments_dict, f, ensure_ascii=False, indent=2)
                
        # 2. Create flac-files-list.txt in the current folder
        # Requirement: "1 txt file with the full path of each flac file within each folder"
        list_file_path = os.path.join(dirpath, CONFIG['filename_flac_list'])
        with open(list_file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(folder_flac_paths) + "\n")
        
        # Add folder data to serie_data
        # Sort kapitel by discnumber and then tracknumber
        def get_sort_key(k):
            dn = k.get('discnumber', [1])[0]
            tn = k.get('tracknumber', [0])[0]
            
            try:
                # Handle cases like "1/2" for discnumber
                dn_val = int(str(dn).split('/')[0])
            except (ValueError, TypeError, IndexError):
                dn_val = 1
                
            try:
                # Handle cases like "1/10" for tracknumber
                tn_val = int(str(tn).split('/')[0])
            except (ValueError, TypeError, IndexError):
                tn_val = 0
                
            return (dn_val, tn_val)

        folder_vorbis_comments.sort(key=get_sort_key)

        serie_data.append({
            "kapitel": folder_vorbis_comments
        })
            
        logger.info(f"Processed {len(flac_in_folder)} FLAC files in {dirpath}")

    # 3. Create all-flac-files.txt in current working directory
    # Requirement: "1 txt file with the full path of each flac file sorted by folder and sort order on a per folder basis"
    if all_flac_files:
        # Sort by folder and then filename
        all_flac_files.sort()
        
        all_files_path = os.path.join(root_dir, CONFIG['filename_all_flac_files'])
        with open(all_files_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(all_flac_files) + "\n")
        
        logger.info(f"Created global list of {len(all_flac_files)} FLAC files at {all_files_path}")
        
        # 4. Create aggregated serie_flac.json
        # Requirement: "The structure of the json file will follow the structure of the serie.json. in this case only serie and kapitel will be used."
        
        # Sort serie_data by the numeric value of the first three digits of the first chapter's title
        def get_serie_sort_key(s):
            if not s['kapitel']:
                return 0
            # Get the title of the first chapter
            first_kapitel = s['kapitel'][0]
            title_list = first_kapitel.get('title', [])
            if not title_list:
                return 0
            title = str(title_list[0])
            # Extract the first three digits
            prefix = title[:3]
            try:
                return int(prefix)
            except (ValueError, TypeError):
                return 0

        serie_data.sort(key=get_serie_sort_key)
        
        final_json_data = {
            "dbInfo": {
                "version": CONFIG['script_version'],
                "lastModified": CONFIG['timestamp'],
                "source": CONFIG['flac_source']
            },
            "serie": serie_data
        }
        
        serie_flac_path = os.path.join(root_dir, CONFIG['filename_serie_flac'])
        with open(serie_flac_path, 'w', encoding='utf-8') as f:
            json.dump(final_json_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Created aggregated Vorbis comments JSON at {serie_flac_path}")
    else:
        logger.info("No FLAC files found.")

if __name__ == '__main__':
    main()
