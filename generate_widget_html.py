import json

with open("top100_metas.json", "r", encoding="utf-8") as f:
    shows_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top 100 TV Shows - Stremio Playlist</title>
    <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-4 font-sans">
    <div class="max-w-6xl mx-auto space-y-6">
        <!-- Header & Action Card -->
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 class="text-2xl font-bold tracking-tight text-[var(--foreground)] flex items-center gap-2">
                        <span>🍿</span> Top 100 TV Shows of the 21st Century
                    </h1>
                    <p class="text-sm text-[var(--muted-foreground)] mt-1">
                        Ranked playlist ready for Stremio. Complete with Cinemeta metadata & instant playback links.
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <a href="stremio://127.0.0.1:7070/manifest.json" 
                       class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded-xl shadow transition flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                        Install Stremio Addon
                    </a>
                    <button onclick="copyManifest()" 
                            class="px-4 py-2.5 bg-[var(--accent)] text-[var(--foreground)] border border-[var(--border)] font-medium text-sm rounded-xl hover:opacity-80 transition">
                        📋 Copy Manifest URL
                    </button>
                </div>
            </div>

            <!-- Search & Filter Controls -->
            <div class="mt-6 pt-6 border-t border-[var(--border)] flex flex-col sm:flex-row gap-4 justify-between items-center">
                <div class="relative w-full sm:w-80">
                    <input type="text" id="searchInput" oninput="renderShows()" placeholder="Search show title..." 
                           class="w-full px-4 py-2 text-sm bg-[var(--background)] border border-[var(--border)] rounded-xl text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-indigo-500">
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
                    <button onclick="setFilter('all')" id="btn-all" class="filter-btn active px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white">All (100)</button>
                    <button onclick="setFilter(10)" id="btn-10" class="filter-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-[var(--background)] text-[var(--muted-foreground)] border border-[var(--border)]">Top 10</button>
                    <button onclick="setFilter(25)" id="btn-25" class="filter-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-[var(--background)] text-[var(--muted-foreground)] border border-[var(--border)]">Top 25</button>
                    <button onclick="setFilter(50)" id="btn-50" class="filter-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-[var(--background)] text-[var(--muted-foreground)] border border-[var(--border)]">Top 50</button>
                </div>
            </div>
        </div>

        <!-- Notification Toast -->
        <div id="toast" class="hidden fixed bottom-5 right-5 bg-emerald-600 text-white px-4 py-2 rounded-xl text-sm font-medium shadow-lg z-50 transition">
            Manifest URL copied to clipboard!
        </div>

        <!-- Grid Container -->
        <div id="showsGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            <!-- Dynamically populated -->
        </div>
    </div>

    <script>
        const shows = {json.dumps(shows_data)};
        let currentLimit = 'all';

        function setFilter(limit) {{
            currentLimit = limit;
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.className = 'filter-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-[var(--background)] text-[var(--muted-foreground)] border border-[var(--border)]';
            }});
            const activeBtn = document.getElementById(`btn-${{limit}}`);
            if (activeBtn) {{
                activeBtn.className = 'filter-btn active px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white';
            }}
            renderShows();
        }}

        function copyManifest() {{
            navigator.clipboard.writeText("http://localhost:7070/manifest.json");
            const toast = document.getElementById("toast");
            toast.classList.remove("hidden");
            setTimeout(() => toast.classList.add("hidden"), 2500);
        }}

        function renderShows() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            const grid = document.getElementById('showsGrid');
            grid.innerHTML = '';

            let filtered = shows.filter(s => s.name.toLowerCase().includes(search));

            if (currentLimit !== 'all') {{
                filtered = filtered.filter(s => s.rank <= parseInt(currentLimit));
            }}

            if (filtered.length === 0) {{
                grid.innerHTML = `
                    <div class="col-span-full py-12 text-center text-[var(--muted-foreground)]">
                        No TV shows found matching your search.
                    </div>
                `;
                return;
            }}

            filtered.forEach(show => {{
                const stremioApp = `stremio://detail/series/${{show.id}}`;
                const stremioWeb = `https://web.stremio.com/#/detail/series/${{show.id}}`;
                const posterUrl = show.poster || 'https://via.placeholder.com/300x450?text=No+Poster';

                const card = document.createElement('div');
                card.className = 'group bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between relative';
                card.innerHTML = `
                    <div class="relative aspect-[2/3] bg-neutral-900 overflow-hidden">
                        <img src="${{posterUrl}}" alt="${{show.name}}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" loading="lazy">
                        <span class="absolute top-2 left-2 bg-black/80 backdrop-blur-md text-amber-400 font-extrabold text-xs px-2.5 py-1 rounded-lg border border-amber-500/30">
                            #${{show.rank}}
                        </span>
                        <span class="absolute bottom-2 right-2 bg-black/80 backdrop-blur-md text-slate-300 font-medium text-[10px] px-2 py-0.5 rounded border border-white/10">
                            ${{show.releaseInfo}}
                        </span>
                    </div>
                    <div class="p-3 flex-1 flex flex-col justify-between space-y-2">
                        <div>
                            <h3 class="font-bold text-sm text-[var(--foreground)] line-clamp-1 group-hover:text-indigo-400 transition" title="${{show.name}}">
                                ${{show.name}}
                            </h3>
                            <p class="text-[11px] text-[var(--muted-foreground)] font-mono mt-0.5">
                                ${{show.id}}
                            </p>
                        </div>
                        <div class="flex items-center gap-1.5 pt-1">
                            <a href="${{stremioApp}}" class="flex-1 text-center py-1.5 bg-indigo-600/90 hover:bg-indigo-600 text-white text-xs font-semibold rounded-lg transition" title="Open in Stremio App">
                                🍿 Play
                            </a>
                            <a href="${{stremioWeb}}" target="_blank" class="px-2 py-1.5 bg-[var(--background)] hover:bg-[var(--border)] text-[var(--muted-foreground)] text-xs rounded-lg border border-[var(--border)] transition" title="Open in Stremio Web">
                                🌐
                            </a>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        // Initial render
        renderShows();
    </script>
</body>
</html>
"""

target_path = r"C:\Users\Personal\.gemini\antigravity\brain\d6f0eaed-2e9c-418e-93c4-a2593242bad4\stremio_playlist_widget.html"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generative UI widget created at {target_path}")
