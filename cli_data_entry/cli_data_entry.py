from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
import json
import os

console = Console()

def display_example_data():
    console.print(Panel.fit(
        "[bold cyan]Food as Cultural Artifacts Database[/bold cyan]\n"
        "[dim]Exploring digital representations of food culture[/dim]",
        border_style="cyan"
    ))
    console.print("\n[bold yellow]📊 Example Entries:[/bold yellow]\n")
    
    # example data
    table = Table()
    
    table.add_column("Platform", style="cyan", width=12)
    table.add_column("Content Type", style="green", width=20)
    table.add_column("Cultural Theme", style="yellow", width=25)
    table.add_column("Engagement", style="red", width=12)
    
    # Add example rows
    table.add_row(
        "TikTok",
        "Recipe Video",
        "Authentic vs Americanized",
        "2.3M views"
    )
    table.add_row(
        "Instagram",
        "Food Photography",
        "Clean Eating Aesthetic",
        "45K likes"
    )
    table.add_row(
        "Twitter/X",
        "Discourse Thread",
        "Cultural Appropriation",
        "8.5K RTs"
    )
    table.add_row(
        "TikTok",
        "Mukbang/ASMR",
        "Performance & Identity",
        "5.1M views"
    )
    
    console.print(table)
    console.print()


def collect_artifact_data():
    
    console.print("[bold green]➕ Add New Food Cultural Artifact[/bold green]\n")
    
    # data fields
    platform = console.input("[cyan]Platform[/cyan] (e.g., TikTok, Instagram, YouTube): ").strip()
    content_type = console.input("[cyan]Content Type[/cyan] (e.g., Recipe Video, Photo, Thread): ").strip()
    creator = console.input("[cyan]Creator/Username[/cyan]: ").strip()
    title = console.input("[cyan]Title/Description[/cyan]: ").strip()
    url = console.input("[cyan]URL[/cyan] (link to content): ").strip()
    hashtags = console.input("[cyan]Hashtags[/cyan] (comma-separated): ").strip()
    cultural_theme = console.input("[cyan]Cultural Theme[/cyan] (e.g., authenticity, identity, fusion): ").strip()
    engagement = console.input("[cyan]Engagement Metrics[/cyan] (e.g., views, likes, comments): ").strip()
    notes = console.input("[cyan]Additional Notes[/cyan]: ").strip()
    
    # artifact dictionary
    artifact = {
        "platform": platform,
        "content_type": content_type,
        "creator": creator,
        "title": title,
        "url": url,
        "hashtags": hashtags,
        "cultural_theme": cultural_theme,
        "engagement": engagement,
        "notes": notes
    }
    
    return artifact


def display_artifact(artifact):
    console.print("\n[bold yellow]📝 Your Entry:[/bold yellow]\n")
    display_text = f"""
[cyan]Platform:[/cyan] {artifact['platform']}
[cyan]Content Type:[/cyan] {artifact['content_type']}
[cyan]Creator:[/cyan] {artifact['creator']}
[cyan]Title:[/cyan] {artifact['title']}
[cyan]URL:[/cyan] {artifact['url']}
[cyan]Hashtags:[/cyan] {artifact['hashtags']}
[cyan]Cultural Theme:[/cyan] {artifact['cultural_theme']}
[cyan]Engagement:[/cyan] {artifact['engagement']}
[cyan]Notes:[/cyan] {artifact['notes']}
    """
    
    console.print(Panel(display_text.strip(), border_style="green", title="Artifact Data"))
    console.print()


def save_to_file(artifacts, filename="food_artifacts_data.json"):
    filepath = os.path.abspath(filename)
    existing_data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    existing_data.extend(artifacts)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():

    display_example_data()
    confirmed_artifacts = []
    console.print("[bold]Would you like to add your own food cultural artifacts?[/bold]\n")
    add_more = True
    
    while add_more:
        artifact = collect_artifact_data()
        display_artifact(artifact)
        is_correct = Confirm.ask("[bold green]Is this data correct?[/bold green]")
        if is_correct:
            confirmed_artifacts.append(artifact)
            console.print("[bold green]✓ Artifact added successfully![/bold green]\n")
            add_more = Confirm.ask("[bold]Would you like to add another artifact?[/bold]")
        else:
            console.print("[bold yellow]⚠ Let's re-enter the data.[/bold yellow]\n")

    if confirmed_artifacts:
        filepath = save_to_file(confirmed_artifacts)
        
        console.print(Panel.fit(
            f"[bold green]✓ Data saved successfully![/bold green]\n\n"
            f"[cyan]Number of artifacts saved:[/cyan] {len(confirmed_artifacts)}\n"
            f"[cyan]File location:[/cyan] {filepath}",
            border_style="green",
            title="Success"
        ))
    else:
        console.print("[yellow]No data was saved (no confirmed entries).[/yellow]")
    console.print("\n[bold cyan]Thank you for contributing to the database![/bold cyan]")

if __name__ == "__main__":
    main()