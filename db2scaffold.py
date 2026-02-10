def main():
    import os
    from serie_db import SerieDB

    # Load the database
    db = SerieDB('db/serie.json')

    # Get all series, sorted by track number (nummer)
    series = sorted(db.get_all_series(), key=lambda s: s.get('nummer', 0))

    outputs = []  # List to store folder-friendly output lines
    titles = []   # List to store original titles
    cover_art_urls = []  # List to store cover art URLs
    episode_durations = []  # List to store total durations

    # Function to expand German umlauts to their English equivalents
    import re
    def expand_umlauts(text):
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
            'ß': 'ss'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text


    # Read the customizable template for info.txt from external file
    # Read the info.txt template from external file
    with open('templates/tmpl_episode_info.txt', 'r', encoding='utf-8') as tmpl_file:
        tmpl_episode_info_full = tmpl_file.read()
    # Remove non-parsable section (reference/documentation) if present
    split_marker = '---\nDO NOT PARSE BELOW THIS LINE'
    if split_marker in tmpl_episode_info_full:
        tmpl_episode_info = tmpl_episode_info_full.split(split_marker)[0].rstrip()
    else:
        tmpl_episode_info = tmpl_episode_info_full

    import urllib.request
    for serie in series:
        nummer = serie.get('nummer', 0)  # Track number (int)
        titel = serie.get('titel', '')   # Original title (str)
        nummer_str = str(nummer).zfill(3)  # Track number as zero-padded string (e.g. '001')
        gesamtdauer = serie.get('gesamtdauer', None)  # Total duration in ms (int or None)
        beschreibung = serie.get('beschreibung', '')  # Description (str)
        episode_durations.append(str(gesamtdauer) if gesamtdauer is not None else '')
        # Extract cover art URL from 'links' child if present
        links = serie.get('links', {})
        cover_art_url = ''
        if isinstance(links, dict):
            cover_art_url = links.get('cover', '')
        cover_art_urls.append(cover_art_url)
        # Compose info_titel: '<nummer>. Die Drei ??? - <titel>' or '<nummer>. Die Drei ??? <titel>' if titel starts with 'und'
        info_titel_part1 = f"{nummer}. "
        if titel.strip().lower().startswith("und"):
            info_titel_part2 = f"Die Drei ??? {titel}"
        else:
            info_titel_part2 = f"Die Drei ??? - {titel}"
        info_titel = info_titel_part1 + info_titel_part2
        # Convert duration from ms to minutes (int)
        gesamtdauer_min = int(int(gesamtdauer) / 60000)

        # Create a folder name friendly version of the title
        titel_expanded = expand_umlauts(titel)
        # Remove special characters except spaces, preserve case
        titel_folder = re.sub(r'[^a-zA-Z0-9 ]', '', titel_expanded)

        # Format output line for folder name and tracking
        output = f"{nummer_str} - {titel_folder}"
        outputs.append(output)
        titles.append(titel)

        # Create the folder in the dist directory using the output string
        folder_path = os.path.join('dist', output)
        if output and not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Download the cover art if URL is present and file does not already exist
        if cover_art_url:
            cover_path = os.path.join(folder_path, f'{nummer_str}.jpg')
            if os.path.exists(cover_path):
                print(f"Cover art already exists for {output} at {cover_path}, skipping download.")
            else:
                try:
                    urllib.request.urlretrieve(cover_art_url, cover_path)
                    print(f"Downloaded cover art for {output} to {cover_path}")
                except Exception as e:
                    print(f"Failed to download cover art for {output}: {e}")

        # Write episode_info to info.txt in the respective folder using the template
        info_path = os.path.join(folder_path, 'info.txt')
        episode_info = tmpl_episode_info.format(
            nummer=nummer,                # Track number (int)
            nummer_str=nummer_str,        # Track number as zero-padded string (str)
            titel=titel,                  # Original title (str)
            beschreibung=beschreibung,    # Description (str)
            gesamtdauer=gesamtdauer if gesamtdauer is not None else '',           # Duration in ms
            gesamtdauer_min=gesamtdauer_min if gesamtdauer is not None else '',   # Duration in min
            info_titel=info_titel,        # Formatted info title
            cover_art_url=cover_art_url   # Cover art URL
        )
        with open(info_path, 'w', encoding='utf-8') as info_file:
            info_file.write(episode_info)

    # Write folder-friendly names to file
    output_file = 'dist/folder-names.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(outputs) + '\n')
    print(f"Folder-friendly names written to: {output_file}")

    # Write original titles to file
    titles_file = 'dist/titles.txt'
    with open(titles_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(titles) + '\n')
    print(f"Original titles written to: {titles_file}")

    # Write cover art URLs to file
    cover_art_file = 'dist/cover-art-urls.txt'
    with open(cover_art_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cover_art_urls) + '\n')

    # Write episode durations to file
    durations_file = 'dist/episodes-time-ms.txt'
    with open(durations_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(episode_durations) + '\n')

    # Print the location of the folder-names file
    print(f"Output written to: {output_file}")

if __name__ == '__main__':
    main()
