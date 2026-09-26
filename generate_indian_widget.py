import json

with open("indian_movies_metas.json", "r", encoding="utf-8") as f:
    indian_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>50 Underrated Indian Films - Stremio Addon</title>
    <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-4 font-sans">
    <div class="max-w-6xl mx-auto space-y-6">
        <!-- Header & Action Card -->
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 class="text-2xl font-bold tracking-tight text-[var(--foreground)] flex items-center gap-2">
                        <span>🇮🇳</span> 50 Underrated Indian Films Across Languages
                    </h1>
                    <p class="text-sm text-[var(--muted-foreground)] mt-1">
                        Curated Indian cinema: Hindi, Malayalam, Tamil, Bengali, Marathi, Assamese & Classics.
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <a href="stremio://stremio-top100-barunbordoloi40-2977s-projects.vercel.app/indian/manifest.json" 
                       class="px-5 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-medium text-sm rounded-xl shadow transition flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                        Install Indian Movies Addon
                    </a>
                    <button onclick="copyManifest()" 
                            class="px-4 py-2.5 bg-[var(--accent)] text-[var(--foreground)] border border-[var(--border)] font-medium text-sm rounded-xl hover:opacity-80 transition">
                        📋 Copy Link
                    </button>
                </div>
            </div>

            <!-- Search -->
            <div class="mt-6 pt-6 border-t border-[var(--border)] flex justify-between items-center">
                <div class="relative w-full sm:w-80">
                    <input type="text" id="searchInput" oninput="renderMovies()" placeholder="Search title or language..." 
                           class="w-full px-4 py-2 text-sm bg-[var(--background)] border border-[var(--border)] rounded-xl text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-orange-500">
                </div>
                <span class="text-xs text-[var(--muted-foreground)] font-mono">50/50 Films Loaded</span>
            </div>
        </div>

        <!-- Notification Toast -->
        <div id="toast" class="hidden fixed bottom-5 right-5 bg-emerald-600 text-white px-4 py-2 rounded-xl text-sm font-medium shadow-lg z-50 transition">
            Manifest URL copied to clipboard!
        </div>

        <!-- Grid Container -->
        <div id="moviesGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            <!-- Dynamically populated -->
        </div>
    </div>

    <script>
        const indianMovies = {json.dumps(indian_data)};

        function copyManifest() {{
            navigator.clipboard.writeText("https://stremio-top100-barunbordoloi40-2977s-projects.vercel.app/indian/manifest.json");
            const toast = document.getElementById("toast");
            toast.classList.remove("hidden");
            setTimeout(() => toast.classList.add("hidden"), 2500);
        }}

        function renderMovies() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            const grid = document.getElementById('showsGrid') || document.getElementById('moviesGrid');
            grid.innerHTML = '';

            let filtered = indianMovies.filter(m => m.name.toLowerCase().includes(search));

            if (filtered.length === 0) {{
                grid.innerHTML = `
                    <div class="col-span-full py-12 text-center text-[var(--muted-foreground)]">
                        No Indian films found matching your search.
                    </div>
                `;
                return;
            }}

            filtered.forEach(movie => {{
                const stremioApp = `stremio://detail/movie/${{movie.id}}`;
                const stremioWeb = `https://web.stremio.com/#/detail/movie/${{movie.id}}`;
                const posterUrl = movie.poster || 'https://via.placeholder.com/300x450?text=No+Poster';

                const card = document.createElement('div');
                card.className = 'group bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between relative';
                card.innerHTML = `
                    <div class="relative aspect-[2/3] bg-neutral-900 overflow-hidden">
                        <img src="${{posterUrl}}" alt="${{movie.name}}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" loading="lazy">
                        <span class="absolute top-2 left-2 bg-black/80 backdrop-blur-md text-amber-400 font-extrabold text-xs px-2.5 py-1 rounded-lg border border-amber-500/30">
                            #${{movie.rank}}
                        </span>
                        <span class="absolute bottom-2 right-2 bg-black/80 backdrop-blur-md text-slate-300 font-medium text-[10px] px-2 py-0.5 rounded border border-white/10">
                            ${{movie.releaseInfo}}
                        </span>
                    </div>
                    <div class="p-3 flex-1 flex flex-col justify-between space-y-2">
                        <div>
                            <h3 class="font-bold text-sm text-[var(--foreground)] line-clamp-1 group-hover:text-orange-400 transition" title="${{movie.name}}">
                                ${{movie.name}}
                            </h3>
                            <p class="text-[11px] text-[var(--muted-foreground)] font-mono mt-0.5">
                                ${{movie.id}}
                            </p>
                        </div>
                        <div class="flex items-center gap-1.5 pt-1">
                            <a href="${{stremioApp}}" class="flex-1 text-center py-1.5 bg-orange-600/90 hover:bg-orange-600 text-white text-xs font-semibold rounded-lg transition" title="Open in Stremio App">
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
        renderMovies();
    </script>
</body>
</html>
"""

target_path = r"C:\Users\Personal\.gemini\antigravity\brain\d6f0eaed-2e9c-418e-93c4-a2593242bad4\indian_movies_widget.html"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Indian Movies widget created at {target_path}")
