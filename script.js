// ==========================================================================
// SPA JavaScript Logic for flutter.prstart.hu
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const searchInput = document.getElementById('search_input');
    const themeToggle = document.getElementById('theme_toggle');
    const progressBarInner = document.getElementById('progress_bar_inner');
    const progressPercentage = document.getElementById('progress_percentage');
    const sidebarNav = document.getElementById('sidebar_nav');
    const syllabusContent = document.getElementById('syllabus_content');

    // State Variables
    let parsedSections = []; // Hierarchical sections and pages
    let allPagesMap = new Map(); // Flat map of id -> page
    let completedPages = JSON.parse(localStorage.getItem('flutter_completed_pages') || '{}');
    let activePageId = '';

    // Initialize Markdown parser configurations (marked.js)
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: true,
        headerPrefix: 'content-h-',
        highlight: function(code, lang) {
            if (Prism.languages[lang]) {
                return Prism.highlight(code, Prism.languages[lang], lang);
            }
            return code;
        }
    });

    // 1. Fetch & Parse Tananyag Markdown
    async function loadTananyag() {
        try {
            const response = await fetch('assets/tananyag.md');
            if (!response.ok) {
                throw new Error('Sikertelen betöltés: assets/tananyag.md');
            }
            const mdText = await response.text();
            
            parsedSections = parseMarkdown(mdText);
            
            // Populate the flat map and ensure we have an active page
            parsedSections.forEach(section => {
                section.pages.forEach(page => {
                    allPagesMap.set(page.id, page);
                });
            });

            // Build navigation in sidebar
            renderSidebar();
            
            // Set initial active page from Hash or default to home dashboard
            const hashId = window.location.hash.replace('#', '');
            if (hashId === 'home' || hashId === 'blogs' || hashId.startsWith('blog-')) {
                activePageId = hashId;
            } else if (hashId && allPagesMap.has(hashId)) {
                activePageId = hashId;
            } else {
                activePageId = 'home';
            }

            // Render current page
            showPage(activePageId);

            // Add click listener on the brand logo
            const brandLogo = document.getElementById('brand_logo');
            if (brandLogo) {
                brandLogo.addEventListener('click', () => {
                    showPage('home');
                });
            }
            
            // Update progress bar
            updateProgress();

        } catch (error) {
            console.error('Error loading tananyag:', error);
            syllabusContent.innerHTML = `
                <div class="loading-content error-state">
                    <i class="fa-solid fa-triangle-exclamation" style="color: var(--accent-primary);"></i>
                    <p>Nem sikerült a tananyag betöltése.</p>
                    <span style="font-size: 13px; color: var(--text-secondary);">${error.message}</span>
                </div>
            `;
        }
    }

    // Helper to generate clean, ASCII-safe slugs from Hungarian titles
    function slugify(text) {
        return text.toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Remove Hungarian accent marks
            .replace(/[^a-z0-9]/g, '-')
            .replace(/-+/g, '-')
            .replace(/^-|-$/g, '');
    }

    // 2. Custom Markdown Slicer (splits into sections and weeks/topics)
    function parseMarkdown(mdText) {
        const lines = mdText.split('\n');
        const sections = [];
        
        // Create a default Bevezetés section for headers before the first main section
        let currentSection = {
            id: 'section-intro',
            title: 'Bevezetés',
            pages: []
        };
        sections.push(currentSection);

        let currentPage = null;
        let currentPageLines = [];

        function closeCurrentPage() {
            if (currentPage && currentPageLines.length > 0) {
                currentPage.content = currentPageLines.join('\n');
                currentSection.pages.push(currentPage);
            }
            currentPage = null;
            currentPageLines = [];
        }

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // 1. Match H1 Section header (e.g., "# I. SZAKASZ — Alapozás")
            // Exclude the main title header
            if (line.startsWith('# ') && !line.includes('teljes tananyag nulláról')) {
                closeCurrentPage();
                
                const title = line.replace('# ', '').trim();
                const sectionId = 'sec-' + slugify(title);

                currentSection = {
                    id: sectionId,
                    title: title,
                    pages: []
                };
                sections.push(currentSection);
                continue;
            }

            // 2. Match H2 Week/Page header (e.g., "## 1. hét — Fejlesztői környezet...")
            if (line.startsWith('## ')) {
                closeCurrentPage();

                const title = line.replace('## ', '').trim();
                const pageId = 'page-' + slugify(title);

                currentPage = {
                    id: pageId,
                    title: title,
                    content: ''
                };
                continue;
            }

            // Collect lines for the current active page
            if (currentPage) {
                currentPageLines.push(line);
            }
        }
        
        // Close last page
        closeCurrentPage();

        // Filter out empty sections if any
        return sections.filter(sec => sec.pages.length > 0);
    }

    // 3. Render Sidebar DOM structure
    function renderSidebar(filteredPagesSet = null) {
        sidebarNav.innerHTML = '';

        // Render top shortcuts (Kezdőlap, Blogok)
        const shortcutsEl = document.createElement('div');
        shortcutsEl.className = 'sidebar-shortcuts';
        shortcutsEl.innerHTML = `
            <ul class="nav-list" style="margin-bottom: 0;">
                <li class="nav-item">
                    <a href="#home" class="nav-link ${activePageId === 'home' ? 'active' : ''}" data-id="home">
                        <span><i class="fa-solid fa-house nav-icon"></i> Kezdőlap</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#blogs" class="nav-link ${activePageId === 'blogs' || activePageId.startsWith('blog-') ? 'active' : ''}" data-id="blogs">
                        <span><i class="fa-solid fa-newspaper nav-icon"></i> Blog bejegyzések</span>
                    </a>
                </li>
            </ul>
            <div class="sidebar-divider" style="height: 1px; background: var(--border-color); margin: 15px 0 10px 0;"></div>
        `;
        sidebarNav.appendChild(shortcutsEl);

        // Add event listeners to the shortcuts
        shortcutsEl.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                showPage(link.dataset.id);
            });
        });
        
        parsedSections.forEach(section => {
            // Filter section pages if search is active
            const visiblePages = filteredPagesSet 
                ? section.pages.filter(p => filteredPagesSet.has(p.id)) 
                : section.pages;

            if (visiblePages.length === 0) return;

            const sectionEl = document.createElement('div');
            sectionEl.className = 'nav-section';

            const sectionTitle = document.createElement('div');
            sectionTitle.className = 'nav-section-title';
            sectionTitle.textContent = section.title;
            sectionEl.appendChild(sectionTitle);

            const ul = document.createElement('ul');
            ul.className = 'nav-list';

            visiblePages.forEach(page => {
                const li = document.createElement('li');
                li.className = 'nav-item';

                const a = document.createElement('a');
                a.className = `nav-link ${page.id === activePageId ? 'active' : ''} ${completedPages[page.id] ? 'completed' : ''}`;
                a.dataset.id = page.id;

                // Determine dynamic icon (checkbox vs text/gear)
                const isCompleted = completedPages[page.id];
                const checkIconClass = isCompleted ? 'fa-regular fa-square-check' : 'fa-regular fa-square';
                
                a.innerHTML = `
                    <span>
                        <i class="${checkIconClass} nav-icon check-indicator"></i>
                        ${page.title}
                    </span>
                `;

                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    showPage(page.id);
                });

                li.appendChild(a);
                ul.appendChild(li);
            });

            sectionEl.appendChild(ul);
            sidebarNav.appendChild(sectionEl);
        });

        if (sidebarNav.children.length === 0) {
            sidebarNav.innerHTML = '<div class="no-results">Nincs találat.</div>';
        }
    }

    // Helper to calculate progress stats
    function getProgressStats() {
        const total = allPagesMap.size;
        const completed = Object.keys(completedPages).length;
        const percent = total > 0 ? Math.round((completed / total) * 100) : 0;
        return { total, completed, percent };
    }

    // Help function to find first incomplete lesson and jump to it
    function startOrContinueCourse() {
        let targetId = '';
        for (let [id, page] of allPagesMap) {
            if (!completedPages[id]) {
                targetId = id;
                break;
            }
        }
        if (!targetId && allPagesMap.size > 0) {
            targetId = allPagesMap.keys().next().value;
        }
        if (targetId) {
            showPage(targetId);
        }
    }

    // Render Home Landing Dashboard
    function renderHomePage() {
        const { total, completed, percent } = getProgressStats();
        
        syllabusContent.innerHTML = `
            <div class="hero-section">
                <div class="hero-content">
                    <span class="hero-badge"><i class="fa-solid fa-rocket"></i> PRSTART Mobil Akadémia</span>
                    <h1>Flutter Mobilfejlesztés Profi Módon</h1>
                    <p>Sajátítsd el a modern mobilalkalmazás-fejlesztést a nulláról a Google hivatalos UI keretrendszerével. Strukturált 24 hetes ingyenes tananyag, gyakorlati feladatok, mini projektek és szakmai blogok egy helyen.</p>
                    <div class="hero-buttons">
                        <button id="start_course_btn" class="primary-btn"><i class="fa-solid fa-play"></i> Tanfolyam megkezdése</button>
                        <button id="view_blogs_btn" class="secondary-btn"><i class="fa-solid fa-newspaper"></i> Blogok olvasása</button>
                    </div>
                </div>
            </div>

            <div class="home-grid">
                <!-- Left Column: Progress & Core Sections -->
                <div class="home-left">
                    <div class="dashboard-card">
                        <h3><i class="fa-solid fa-chart-line"></i> Tanulási folyamat</h3>
                        <div class="dashboard-progress-container">
                            <div class="dashboard-stats">
                                <div>
                                    <span id="home_completed_count">${completed}</span>
                                    <label>Teljesített lecke</label>
                                </div>
                                <div>
                                    <span id="home_total_count">${total}</span>
                                    <label>Összes lecke</label>
                                </div>
                                <div>
                                    <span id="home_percentage">${percent}%</span>
                                    <label>Elkészült</label>
                                </div>
                            </div>
                            <div class="progress-bar-outer" style="height: 12px; margin-top: 10px;">
                                <div id="home_progress_bar" class="progress-bar-inner" style="width: ${percent}%"></div>
                            </div>
                        </div>
                        <button id="continue_course_btn" class="primary-btn continue-btn" style="width: 100%; margin-top: 15px; justify-content: center;">
                            <i class="fa-solid fa-forward"></i> Tanulás folytatása
                        </button>
                    </div>

                    <div class="phases-section">
                        <h3><i class="fa-solid fa-graduation-cap"></i> A tanfolyam szakaszai</h3>
                        <div class="phase-list">
                            <div class="phase-item" data-target="page-1-het-fejlesztoi-kornyezet-es-dart-alapok">
                                <div class="phase-num">1</div>
                                <div class="phase-info">
                                    <h4>Alapozás és Dart alapok</h4>
                                    <p>Környezet beállítás, Dart nyelvi elemek, OOP, típusok (1-2. hét)</p>
                                </div>
                            </div>
                            <div class="phase-item" data-target="page-3-het-layout-melyebben">
                                <div class="phase-num">2</div>
                                <div class="phase-info">
                                    <h4>UI, Layout és Navigáció</h4>
                                    <p>Widgetek, flexibilis elrendezések, reszponzivitás, navigáció és route-ok (3-5. hét)</p>
                                </div>
                            </div>
                            <div class="phase-item" data-target="page-6-het-state-management-alapok">
                                <div class="phase-num">3</div>
                                <div class="phase-info">
                                    <h4>Adat, Állapotkezelés és API</h4>
                                    <p>Provider, Riverpod/Bloc, űrlap validáció, HTTP kérések, JSON (6-9. hét)</p>
                                </div>
                            </div>
                            <div class="phase-item" data-target="page-10-het-tiszta-architektura-flutterben">
                                <div class="phase-num">4</div>
                                <div class="phase-info">
                                    <h4>Profi Appok & Tesztelés</h4>
                                    <p>Clean Architecture, SQLite, Auth, Offline sync, Tesztelés, CI/CD (10-24. hét)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column: Blog Feed -->
                <div class="home-right">
                    <div class="blogs-preview-card">
                        <div class="card-header-flex">
                            <h3><i class="fa-solid fa-newspaper"></i> Friss blog bejegyzések</h3>
                            <a href="#blogs" class="view-all-link" id="home_view_all_blogs">Összes megtekintése</a>
                        </div>
                        <div class="blog-feed-list">
                            <div class="blog-feed-item" data-id="flutter-3-44-ujdonsagok">
                                <div class="blog-meta">
                                    <span class="blog-tag"><i class="fa-solid fa-rocket"></i> Új verzió</span>
                                    <span class="blog-date">2026-06-20</span>
                                </div>
                                <h4>Mi újság a Flutter 3.44-ben? Android Impeller, SwiftPM és UI leválasztás</h4>
                                <p>Ismerd meg a legújabb kiadás kiemelkedő teljesítménybeli és architektúrális fejlesztéseit.</p>
                                <span class="read-more">Elolvasom <i class="fa-solid fa-arrow-right"></i></span>
                            </div>

                            <div class="blog-feed-item" data-id="dart-3-ujdonsagok">
                                <div class="blog-meta">
                                    <span class="blog-tag"><i class="fa-solid fa-code"></i> Dart</span>
                                    <span class="blog-date">2026-06-20</span>
                                </div>
                                <h4>Dart 3.0: Rekordok, minták és az új osztálymódosítók</h4>
                                <p>Sajátítsd el az új rekord és mintailesztés funkciókat, amelyekkel tisztább kódokat írhatsz.</p>
                                <span class="read-more">Elolvasom <i class="fa-solid fa-arrow-right"></i></span>
                            </div>

                            <div class="blog-feed-item" data-id="bloc-vs-riverpod">
                                <div class="blog-meta">
                                    <span class="blog-tag"><i class="fa-solid fa-layer-group"></i> State</span>
                                    <span class="blog-date">2026-06-20</span>
                                </div>
                                <h4>A nagy Flutter State Management vita: Bloc vagy Riverpod?</h4>
                                <p>Részletes összehasonlító elemzés a két legnépszerűbb állapotkezelési megoldásról.</p>
                                <span class="read-more">Elolvasom <i class="fa-solid fa-arrow-right"></i></span>
                            </div>

                            <div class="blog-feed-item" data-id="offline-first-appok">
                                <div class="blog-meta">
                                    <span class="blog-tag"><i class="fa-solid fa-wifi"></i> Architecture</span>
                                    <span class="blog-date">2026-06-20</span>
                                </div>
                                <h4>Hogyan építsünk offline-first alkalmazásokat Flutterben?</h4>
                                <p>Az Outbox minta, sqlite cache sorok és kapcsolatfigyelő szolgáltatás felépítése.</p>
                                <span class="read-more">Elolvasom <i class="fa-solid fa-arrow-right"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Event listeners for CTA buttons
        document.getElementById('start_course_btn').addEventListener('click', startOrContinueCourse);
        document.getElementById('continue_course_btn').addEventListener('click', startOrContinueCourse);
        document.getElementById('view_blogs_btn').addEventListener('click', () => showPage('blogs'));
        document.getElementById('home_view_all_blogs').addEventListener('click', (e) => {
            e.preventDefault();
            showPage('blogs');
        });

        // Phase item clicks
        syllabusContent.querySelectorAll('.phase-item').forEach(item => {
            item.addEventListener('click', () => {
                const target = item.dataset.target;
                showPage(target);
            });
        });

        // Blog feed item clicks
        syllabusContent.querySelectorAll('.blog-feed-item').forEach(item => {
            item.addEventListener('click', () => {
                const blogId = 'blog-' + item.dataset.id;
                showPage(blogId);
            });
        });
    }

    // Render Blogs Directory Page
    function renderBlogsPage() {
        syllabusContent.innerHTML = `
            <div class="blogs-page-container">
                <h1>Szakmai Blogok & Cikkek</h1>
                <p class="section-desc">Mélyedj el a Flutter és Dart haladó témaköreiben, újdonságaiban és a legjobb gyakorlatokban.</p>
                
                <div class="blogs-grid">
                    <!-- Blog Card 0 -->
                    <div class="blog-card" data-id="flutter-3-44-ujdonsagok">
                        <div class="blog-card-icon"><i class="fa-solid fa-rocket"></i></div>
                        <div class="blog-card-content">
                            <div class="blog-meta">
                                <span class="blog-tag">Új verzió</span>
                                <span class="blog-date">2026-06-20</span>
                            </div>
                            <h3>Mi újság a Flutter 3.44-ben? Android Impeller, SwiftPM és UI leválasztás</h3>
                            <p>Az új verzió hozza az Impeller motort Androidra alapértelmezettként, leváltja a CocoaPods-ot a SwiftPM-mel, és elindítja a UI elemek különálló csomagokká szervezését.</p>
                            <span class="blog-card-link">Elolvasom a cikket <i class="fa-solid fa-chevron-right"></i></span>
                        </div>
                    </div>

                    <!-- Blog Card 1 -->
                    <div class="blog-card" data-id="dart-3-ujdonsagok">
                        <div class="blog-card-icon"><i class="fa-solid fa-code"></i></div>
                        <div class="blog-card-content">
                            <div class="blog-meta">
                                <span class="blog-tag">Dart</span>
                                <span class="blog-date">2026-06-20</span>
                            </div>
                            <h3>Dart 3.0: Rekordok, minták és az új osztálymódosítók</h3>
                            <p>A Google Dart 3-as frissítésének részletes elemzése kódpéldákkal: Sound Null Safety, Records, Pattern matching és sealed osztályok használata.</p>
                            <span class="blog-card-link">Elolvasom a cikket <i class="fa-solid fa-chevron-right"></i></span>
                        </div>
                    </div>

                    <!-- Blog Card 2 -->
                    <div class="blog-card" data-id="bloc-vs-riverpod">
                        <div class="blog-card-icon"><i class="fa-solid fa-layer-group"></i></div>
                        <div class="blog-card-content">
                            <div class="blog-meta">
                                <span class="blog-tag">State Management</span>
                                <span class="blog-date">2026-06-20</span>
                            </div>
                            <h3>A nagy Flutter State Management vita: Bloc vagy Riverpod?</h3>
                            <p>Melyik a jobb választás a projektedhez? Cubit, Bloc vagy a globális reaktív Riverpod? Összehasonlító táblázat és gyakorlati iránymutatások.</p>
                            <span class="blog-card-link">Elolvasom a cikket <i class="fa-solid fa-chevron-right"></i></span>
                        </div>
                    </div>

                    <!-- Blog Card 3 -->
                    <div class="blog-card" data-id="offline-first-appok">
                        <div class="blog-card-icon"><i class="fa-solid fa-wifi"></i></div>
                        <div class="blog-card-content">
                            <div class="blog-meta">
                                <span class="blog-tag">Architektúra</span>
                                <span class="blog-date">2026-06-20</span>
                            </div>
                            <h3>Hogyan építsünk offline-first alkalmazásokat Flutterben?</h3>
                            <p>Tanulja meg, hogyan tarthatja az alkalmazást reszponzív módon működésben internetkapcsolat nélkül SQLite cache-sel és Outbox szinkronizációs sorral.</p>
                            <span class="blog-card-link">Elolvasom a cikket <i class="fa-solid fa-chevron-right"></i></span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add click events to blog cards
        syllabusContent.querySelectorAll('.blog-card').forEach(card => {
            card.addEventListener('click', () => {
                const blogId = 'blog-' + card.dataset.id;
                showPage(blogId);
            });
        });
    }

    // Render Individual Blog Post
    async function renderBlogDetailPage(pageId) {
        const blogId = pageId.replace('blog-', '');
        
        syllabusContent.innerHTML = `
            <div class="loading-content">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
                <p>Cikk betöltése folyamatban...</p>
            </div>
        `;

        try {
            const response = await fetch(`assets/blog/${blogId}.md`);
            if (!response.ok) {
                throw new Error('A keresett cikk nem található.');
            }
            const mdText = await response.text();
            const htmlContent = marked.parse(mdText);

            syllabusContent.innerHTML = `
                <div class="blog-navigation-header">
                    <a href="#blogs" class="back-link" id="blog_back_btn"><i class="fa-solid fa-arrow-left"></i> Vissza a blogok listájához</a>
                </div>
                <div class="rendered-markdown">
                    ${htmlContent}
                </div>
            `;

            // Back button event listener
            document.getElementById('blog_back_btn').addEventListener('click', (e) => {
                e.preventDefault();
                showPage('blogs');
            });

            // Highlight syntax
            Prism.highlightAll();

        } catch (error) {
            syllabusContent.innerHTML = `
                <div class="blog-navigation-header">
                    <a href="#blogs" class="back-link"><i class="fa-solid fa-arrow-left"></i> Vissza a blogok listájához</a>
                </div>
                <div class="loading-content error-state">
                    <i class="fa-solid fa-triangle-exclamation" style="color: var(--accent-primary);"></i>
                    <p>Nem sikerült betölteni a cikket.</p>
                    <span style="font-size: 13px; color: var(--text-secondary);">${error.message}</span>
                </div>
            `;
        }
    }

    // 4. Render Active Page Content in SPA View
    async function showPage(pageId) {
        activePageId = pageId;
        window.location.hash = pageId;

        // Set page active in Sidebar
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.dataset.id === pageId) {
                link.classList.add('active');
            } else if (pageId.startsWith('blog-') && link.dataset.id === 'blogs') {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Scroll to top of reading area smoothly
        syllabusContent.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // A. Handle Kezdőlap (Home Dashboard)
        if (pageId === 'home') {
            renderHomePage();
            return;
        }

        // B. Handle Blog list page
        if (pageId === 'blogs') {
            renderBlogsPage();
            return;
        }

        // C. Handle Individual Blog post
        if (pageId.startsWith('blog-')) {
            renderBlogDetailPage(pageId);
            return;
        }

        // D. Handle Standard Lesson pages
        const page = allPagesMap.get(pageId);
        if (!page) return;

        // Show spinner inside reading area while fetching the full article
        syllabusContent.innerHTML = `
            <div class="loading-content">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
                <p>Lecke betöltése folyamatban...</p>
            </div>
        `;

        let rawMarkdownContent = page.content;

        try {
            // Try fetching the detailed week/topic markdown from assets/weeks/
            const response = await fetch(`assets/weeks/${pageId}.md`);
            if (response.ok) {
                rawMarkdownContent = await response.text();
            } else {
                console.warn(`Nem található részletes lecke: assets/weeks/${pageId}.md, vázlatos verzió megjelenítése.`);
            }
        } catch (error) {
            console.error(`Hiba a részletes lecke betöltésekor (${pageId}):`, error);
        }

        // Generate content HTML with marked.js
        const htmlContent = marked.parse(rawMarkdownContent);

        // Render week heading card, checkmark toggle and parsed markdown content
        const isCompleted = completedPages[pageId] || false;
        
        syllabusContent.innerHTML = `
            <h1>${page.title}</h1>
            
            <div class="week-completion-card">
                <label class="week-completion-label">
                    <input type="checkbox" id="complete_checkbox" class="week-completion-checkbox" ${isCompleted ? 'checked' : ''}>
                    <span>Elolvastam és teljesítettem ezt a leckét</span>
                </label>
                <span class="status-badge" style="color: ${isCompleted ? 'var(--success-color, #00FFCC)' : 'var(--text-secondary)'}; font-weight: 700;">
                    ${isCompleted ? '<i class="fa-solid fa-check-double"></i> Teljesítve' : '<i class="fa-regular fa-circle"></i> Folyamatban'}
                </span>
            </div>

            <div class="rendered-markdown">
                ${htmlContent}
            </div>
        `;

        // Trigger Prism syntax highlighting for the newly rendered code blocks
        Prism.highlightAll();

        // Listen for lesson completion checkbox toggle
        const checkbox = document.getElementById('complete_checkbox');
        checkbox.addEventListener('change', (e) => {
            togglePageCompletion(pageId, e.target.checked);
        });

        // Scroll to top of reading area smoothly
        syllabusContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // 5. Toggle completion state of a page/lesson
    function togglePageCompletion(pageId, isChecked) {
        if (isChecked) {
            completedPages[pageId] = true;
        } else {
            delete completedPages[pageId];
        }
        localStorage.setItem('flutter_completed_pages', JSON.stringify(completedPages));

        // Update sidebar links completed indicators
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.dataset.id === pageId) {
                const icon = link.querySelector('.check-indicator');
                if (isChecked) {
                    link.classList.add('completed');
                    icon.className = 'fa-regular fa-square-check nav-icon check-indicator';
                } else {
                    link.classList.remove('completed');
                    icon.className = 'fa-regular fa-square nav-icon check-indicator';
                }
            }
        });

        // Update status badge on page
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.style.color = isChecked ? 'var(--success-color, #00FFCC)' : 'var(--text-secondary)';
            statusBadge.innerHTML = isChecked 
                ? '<i class="fa-solid fa-check-double"></i> Teljesítve' 
                : '<i class="fa-regular fa-circle"></i> Folyamatban';
        }

        updateProgress();
    }

    // 6. Recalculate and update Progress Bar
    function updateProgress() {
        const total = allPagesMap.size;
        if (total === 0) return;

        const completed = Object.keys(completedPages).length;
        const percent = Math.round((completed / total) * 100);

        progressBarInner.style.width = `${percent}%`;
        progressPercentage.textContent = `${percent}%`;
    }

    // 7. Search Filter logic
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (query === '') {
            renderSidebar();
            return;
        }

        const filteredPages = new Set();

        allPagesMap.forEach((page, id) => {
            // Search inside title or markdown content
            if (page.title.toLowerCase().includes(query) || page.content.toLowerCase().includes(query)) {
                filteredPages.add(id);
            }
        });

        renderSidebar(filteredPages);
    });

    // 8. Theme Switcher (Dark / Light)
    const savedTheme = localStorage.getItem('flutter_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('flutter_theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fa-solid fa-moon';
        } else {
            icon.className = 'fa-solid fa-sun';
        }
    }

    // Start loading tananyag
    loadTananyag();
});
