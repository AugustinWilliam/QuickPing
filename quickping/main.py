#!/usr/bin/env python3
"""
QuickPing - Internet Speed Test
"""

import signal
import sys
import time
from datetime import datetime
import argparse

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn

# Import pyfiglet for responsive ASCII banners
from pyfiglet import Figlet

console = Console()

# ------------------ Global Ctrl+C Handler ------------------
signal.signal(signal.SIGINT, lambda sig, frame: (_ for _ in ()).throw(KeyboardInterrupt))

# ------------------ Helper Functions ------------------
def format_speed(bytes_per_sec):
    """Convert bytes per second to human-readable format."""
    units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
    size = bytes_per_sec
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.2f} {units[idx]}"

def show_banner():
    """Display a left-aligned QuickPing banner using pyfiglet, no border."""
    width = console.size.width  # Terminal width
    fig = Figlet(font="slant", width=width)
    banner_text = fig.renderText("QuickPing")

    console.print(
        f"[bold cyan]{banner_text}[/bold cyan]\n"
        "[bold green]⚡ QuickPing — Internet Speed Monitor ⚡[/bold green]\n"
        "[dim]Fast • Clean • Terminal Friendly[/dim]\n"
        "[bold red]Created by[/bold red] [bold white]Augustin William[/bold white]\n"
    )
    time.sleep(0.6)

def taskmanager_bar(label, speed_text, color):
    """Display a Task Manager–style speed bar."""
    console.print(f"[bold]{speed_text}[/bold]")
    try:
        progress = Progress(
            TextColumn(f"[bold]{label}[/bold]"),
            BarColumn(bar_width=60, complete_style=color),
            TextColumn("[bold green]100%[/bold green]"),
            expand=False
        )
        with progress:
            task = progress.add_task("", total=100)
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.01)
    except KeyboardInterrupt:
        console.print("\n[bold red]⚡ QuickPing stopped by user! Exiting...[/bold red]")
        sys.exit(0)
    console.print("\n")

def run_speed_test(server_id=None):
    """Run the internet speed test and display results."""
    try:
        import speedtest
    except ImportError:
        console.print("[bold red]Error:[/bold red] speedtest-cli not installed")
        console.print("Install with: [bold green]pip install speedtest-cli[/bold green]")
        return

    st = speedtest.Speedtest()

    console.print("\n[bold cyan]🌐 Finding best server...[/bold cyan]")
    if server_id:
        st.get_servers([server_id])
    server = st.get_best_server()

    console.print(f"[bold green]Server:[/bold green] {server['name']} ({server['country']})")
    console.print(f"[bold blue]Host:[/bold blue] {server['host']}\n")

    # DOWNLOAD
    console.print("[bold cyan]⬇ Download test[/bold cyan]\n")
    download = st.download()
    download_text = f"Download Speed: {format_speed(download)}"
    taskmanager_bar("DOWNLOAD", download_text, "cyan")

    # UPLOAD
    console.print("[bold magenta]⬆ Upload test[/bold magenta]\n")
    upload = st.upload()
    upload_text = f"Upload Speed: {format_speed(upload)}"
    taskmanager_bar("UPLOAD", upload_text, "magenta")

    ping = st.results.ping

    # Capture the test completion time
    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ------------------ Result Table ------------------
    table = Table(title="🌐 Internet Speed Test (Result)", title_style="bold yellow")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold green")

    table.add_row("Download", format_speed(download))
    table.add_row("Upload", format_speed(upload))
    table.add_row("Ping", f"{ping:.2f} ms")
    table.add_row("Server", f"{server['name']} ({server['country']})")
    table.add_row("Time", test_time)

    console.print("\n")
    console.print(table) 

    # ------------------ Top 10 Available Servers ------------------
    console.print("\n[bold cyan]📋 Available Servers (Top 10):[/bold cyan]")
    
    # Flatten the servers dict into a list of dicts
    all_servers = []
    for v in st.get_servers().values():
        all_servers.extend(v)

    server_list = []
    for s in all_servers[:10]:
        server_list.append(f"[bold green]{s['id']}[/bold green] - {s['name']} ({s['country']})")

    console.print("\n".join(server_list))

    # Example command for user
    console.print("\n[bold yellow]💡 Example:[/bold yellow] Run with a specific server:")
    console.print("[bold white]quickping --server-id 48809[/bold white]\n")

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="QuickPing - Internet Speed Test")
    parser.add_argument("--server-id", type=int, help="Specific server ID")
    args = parser.parse_args()

    try:
        run_speed_test(args.server_id)
    except KeyboardInterrupt:
        console.print("\n[bold red]⚡ QuickPing stopped by user! Exiting...[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
