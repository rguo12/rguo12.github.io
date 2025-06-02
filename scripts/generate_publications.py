#!/usr/bin/env python3

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import os
from collections import defaultdict

def parse_bibtex(bib_file):
    """Parse BibTeX file and return entries grouped by status and year."""
    with open(bib_file, 'r', encoding='utf-8') as bibtex_file:
        content = bibtex_file.read()
    
    # Find the preprints section
    lines = content.split('\n')
    in_preprints_section = False
    preprint_entry_ids = set()
    
    for line in lines:
        line = line.strip()
        if line.startswith('% Preprints'):
            in_preprints_section = True
            continue
        elif line.startswith('%') and 'Publications' in line:
            in_preprints_section = False
            continue
        elif in_preprints_section and line.startswith('@'):
            # Extract entry ID
            if '{' in line:
                entry_id = line.split('{')[1].split(',')[0].strip()
                preprint_entry_ids.add(entry_id)
    
    # Parse the BibTeX
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.loads(content, parser=parser)
    
    # Group entries by status and year
    grouped_entries = defaultdict(lambda: defaultdict(list))
    
    for entry in bib_database.entries:
        # Determine if this is a preprint
        is_preprint = (
            entry.get('status') == 'preprint' or
            'arxiv preprint' in entry.get('journal', '').lower() or
            entry.get('ID') in preprint_entry_ids
        )
        
        status = 'preprint' if is_preprint else 'accepted'
        year = entry.get('year', '2024')
        grouped_entries[status][year].append(entry)
    
    return grouped_entries

def format_authors(author_string):
    """Format author string for display."""
    if not author_string:
        return ""
    
    # Handle "and others" case
    if 'and others' in author_string:
        author_string = author_string.replace(' and others', ', et al.')
    
    # Split authors by 'and'
    authors = [author.strip() for author in author_string.split(' and ')]
    
    # Format each author (convert from "LAST, FIRST" to "First Last" if needed)
    formatted_authors = []
    for author in authors:
        if ', ' in author:
            # Format: "LAST, FIRST" -> "First Last"
            parts = author.split(', ')
            if len(parts) == 2:
                last, first = parts
                # Handle case where names are in ALL CAPS
                if last.isupper() and first.isupper():
                    formatted_name = f"{first.title()} {last.title()}"
                else:
                    formatted_name = f"{first} {last}"
            else:
                formatted_name = author
        else:
            formatted_name = author
        
        # Highlight my name in bold
        if any(name in formatted_name.lower() for name in ['ruocheng guo', 'guo, ruocheng']):
            formatted_name = f"**{formatted_name}**"
        
        formatted_authors.append(formatted_name)
    
    # Join authors with commas and "and" for the last one
    if len(formatted_authors) == 1:
        return formatted_authors[0]
    elif len(formatted_authors) == 2:
        return f"{formatted_authors[0]} and {formatted_authors[1]}"
    else:
        return f"{', '.join(formatted_authors[:-1])}, and {formatted_authors[-1]}"

def format_venue(entry):
    """Format the venue (conference/journal) with abbreviated names and year."""
    # Use the full venue name from booktitle or journal
    venue = entry.get('booktitle') or entry.get('journal', '')
    year = entry.get('year', '')
    
    # Map full conference names to their base abbreviations (without year)
    venue_abbreviations = {
        'Annual Meeting of the Association for Computational Linguistics': 'ACL',
        'Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining': 'KDD',
        'Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining': 'KDD',
        'Proceedings of the 34th International Joint Conference on Artificial Intelligence': 'IJCAI',
        'Proceedings of the 34th International Joint Conference on Artificial Intelligence (IJCAI)': 'IJCAI',
        'Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval': 'SIGIR',
        'Advances in Neural Information Processing Systems': 'NeurIPS',
        'Proceedings of the 12th International Conference on Learning Representations': 'ICLR',
        'Companion Proceedings of the ACM Web Conference 2024': 'WWW',
        'Proceedings of the 2024 SIAM International Conference on Data Mining (SDM)': 'SDM',
        'Proceedings of the 18th ACM Conference on Recommender Systems': 'RecSys',
        'ACM Transactions on Information Systems': 'TOIS'
    }
    
    # Get base abbreviation
    base_venue = venue_abbreviations.get(venue, venue)
    
    # Add year for conferences (but not for journals like TOIS or arXiv preprints)
    if base_venue in ['ACL', 'KDD', 'IJCAI', 'SIGIR', 'NeurIPS', 'ICLR', 'WWW', 'SDM', 'RecSys'] and year:
        return f"{base_venue} {year}"
    else:
        return base_venue

def format_links(entry):
    """Format links for arXiv, code, and paper."""
    links = []
    
    # arXiv link
    arxiv_url = entry.get('arxiv', '').strip()
    if arxiv_url and arxiv_url != '':
        links.append(f"[[arxiv]({arxiv_url})]")
    elif entry.get('status') != 'preprint':  # Only add empty arxiv for non-preprints
        links.append("[[arxiv]()]")
    
    # Paper link
    paper_url = entry.get('paperurl', '').strip()
    if paper_url and paper_url != '':
        links.append(f"[[paper]({paper_url})]")
    
    # Code link
    code_url = entry.get('code', '').strip()
    if code_url and code_url != '':
        links.append(f"[[code]({code_url})]")
    
    return ' '.join(links)

def generate_publication_item(entry):
    """Generate a single publication item in markdown format."""
    title = entry.get('title', '').replace('{', '').replace('}', '')
    authors = format_authors(entry.get('author', ''))
    venue = format_venue(entry)
    links = format_links(entry)
    
    # Create lines with bullets for venue and authors
    title_line = f"- {title} {links}"
    venue_line = f"  - {venue}" if venue else ""
    author_line = f"  - *{authors}*" if authors else ""
    
    # Combine lines
    result_lines = [title_line]
    if venue_line:
        result_lines.append(venue_line)
    if author_line:
        result_lines.append(author_line)
    
    return '\n'.join(result_lines)

def generate_markdown(grouped_entries):
    """Generate the complete markdown for all publications."""
    markdown_lines = []
    
    # Preprints section
    if 'preprint' in grouped_entries:
        markdown_lines.append("## Preprints")
        for year in sorted(grouped_entries['preprint'].keys(), reverse=True):
            for entry in grouped_entries['preprint'][year]:
                markdown_lines.append(generate_publication_item(entry))
        markdown_lines.append("")
    
    # Accepted papers section
    if 'accepted' in grouped_entries:
        markdown_lines.append("## Accepted Papers")
        
        # Sort years in descending order
        years = sorted(grouped_entries['accepted'].keys(), reverse=True)
        
        for year in years:
            markdown_lines.append(f"### {year}")
            for entry in grouped_entries['accepted'][year]:
                markdown_lines.append(generate_publication_item(entry))
            markdown_lines.append("")
    
    return '\n'.join(markdown_lines).rstrip() + '\n'

def main():
    """Main function to generate publications markdown."""
    # Get the script directory and construct paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    bib_file = os.path.join(project_root, '_data', 'publications.bib')
    output_file = os.path.join(project_root, '_includes', 'all_publications.md')
    
    if not os.path.exists(bib_file):
        print(f"Error: BibTeX file not found at {bib_file}")
        return
    
    try:
        # Parse BibTeX and generate markdown
        grouped_entries = parse_bibtex(bib_file)
        markdown_content = generate_markdown(grouped_entries)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Successfully generated {output_file}")
        print("To update publications, edit _data/publications.bib and run this script again.")
        
    except Exception as e:
        print(f"Error generating publications: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 