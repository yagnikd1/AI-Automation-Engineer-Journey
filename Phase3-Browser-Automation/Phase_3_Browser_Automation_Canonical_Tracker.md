# Phase 3 — Browser Automation Canonical Roadmap Tracker

## Purpose

This file is the authoritative continuity tracker for Phase 3 of the AI Automation Engineer Journey. Use it at the beginning of every Phase 3 conversation to verify the current day, completed work, unfinished work, and the next topic before teaching begins.

## Tracking rules

- Phase 3 began on Day 66.
- The original roadmap defines Phase 3 as Weeks 9–12 rather than numbered days.
- The four roadmap weeks are mapped to Days 66–93: 28 learning days.
- Never mark a day complete until its listed topics and subtopics have been taught, practised, checked, and confirmed.
- At the start of every new chat, verify the previous day's actual completion against this tracker.
- Before starting a day, list anything unfinished from earlier days and explain how the new topic fits the original roadmap.
- Cover every listed subtopic; do not silently skip, merge, or assume completion.
- Begin each lesson with one guided syntax-revision program combining Python fundamentals and web-scraping knowledge, using a different program and no genius tests.
- Use simple English, reason-first debugging, international names only, and safe/ethical browser-automation practices.
- Produce one detailed Python learning file and one detailed handbook document when requested after the day is completed.

## Phase 3 original-roadmap coverage

The original roadmap requires:

### Selenium — Weeks 9–10

1. Setting Up Selenium
2. Finding Elements
3. Interacting with Pages
4. Waits
5. Handling Dynamic Content
6. Taking Screenshots

### Playwright and advanced automation — Weeks 11–12

1. Why Playwright?
2. Playwright Basics
3. Headless Mode
4. Handling CAPTCHAs
5. Async Automation
6. Network Interception

## Verified progress before Day 70

### Day 66 — Completed

**Topic:** Selenium Fundamentals and Environment Setup

Completed coverage:

- Purpose of Selenium
- Browser automation compared with ordinary HTTP requests
- Selenium installation inside the `myenv` virtual environment
- Why `myenv` must be active
- Importing Selenium WebDriver
- Starting Microsoft Edge with Selenium
- Opening `https://example.com`
- Understanding that `driver.get()` tells the controlled browser to navigate to a URL
- Understanding browser–WebDriver communication
- Reading basic page information
- Using `driver.quit()` for cleanup
- Confirming that Edge closed automatically
- Completing the first successful Selenium browser session

Roadmap equivalence:

- The original roadmap describes Chrome and ChromeDriver.
- Day 66 used Microsoft Edge and Edge WebDriver, which fulfils the same browser-driver objective.
- Day 67 retains a short compatibility comparison covering Selenium Manager, ChromeDriver, EdgeDriver, browser versions, and the third-party `webdriver-manager` package so no literal setup subtopic is missed.

### Day 67 — Completed

**Topic:** Finding Elements: Foundations

Completed coverage:

- Selenium Manager, ChromeDriver, EdgeDriver, browser-version compatibility, and the third-party `webdriver-manager` package
- DOM introduction
- HTML tags and attributes
- Inspecting webpages with browser developer tools
- `find_element()`
- `find_elements()`
- `By.ID`
- `By.NAME`
- `By.TAG_NAME`
- Single WebElement versus a collection of WebElements
- Behaviour when no matching element exists
- `NoSuchElementException`
- Safe locator fallbacks and diagnostic output

Practical verification:

- Microsoft Edge opened successfully through the Phase 3 virtual environment.
- The practice page loaded and its title and URL were verified.
- Selenium found the countries container and 250 country cards.
- The first 10 country records were extracted.
- Google Chrome completed the same locator workflow successfully and closed automatically.
- Brave compatibility was tested but remained unreliable because of `DevToolsActivePort` and renderer-timeout failures. These browser-specific startup failures do not leave any Day 67 finding-elements subtopic unfinished.

Deliverables:

- `Day_67_Selenium_Element_Finder.py` was uploaded to `Phase3-Browser-Automation` with a relevant commit.
- `Day_67_Finding_Elements_Foundations_Complete_Handbook.docx` was uploaded to the Phase 3 Google Drive study-guide folder.

### Day 68 — Completed

**Topic:** Text- and Class-Based Locators

Completed coverage:

- `By.CLASS_NAME`
- Limitations of compound class names
- `By.LINK_TEXT`
- `By.PARTIAL_LINK_TEXT`
- Extracting visible text with `.text`
- Reading standard and custom attributes with `get_attribute()`
- `is_displayed()`
- `is_enabled()`
- `is_selected()`
- Gap lesson: `urllib.parse.quote()`, percent encoding, data URLs, and the distinction between encoding and encryption

Practical verification:

- Microsoft Edge opened the authorised embedded practice page.
- The page title and data URL were verified.
- Two course cards were found by class.
- Visible headings and custom `data-id` attributes were extracted.
- Exact and partial link-text locators returned the expected links.
- A compound-class element was found with the correct CSS selector.
- Displayed, enabled, selected, disabled, and hidden states returned the expected Boolean results.
- The browser session ended safely.
- The final knowledge check passed after corrections.

Deliverables:

- `Day_68_Text_and_Class_Locators.py` was uploaded to `Phase3-Browser-Automation` with the Day 68 tracker update.
- `Day_68_Text_and_Class_Locators_Complete_Handbook.docx` was uploaded to the Phase 3 Google Drive study-guide folder.

### Day 69 — Completed

**Topic:** CSS Selectors

Completed coverage:

- Tag, ID, class, and compound-class selectors
- Attribute existence and exact-value selectors
- Attribute starts-with, ends-with, and contains operators
- Descendant and direct-child selectors
- Combined selector conditions
- Comma-separated selector lists
- Testing selectors in DevTools
- Stable versus fragile selector decisions
- `querySelector()`, `querySelectorAll()`, and `.length`

Practical verification:

- Chrome opened the offline Equipment Management Portal through the Phase 3 virtual environment.
- The data URL and page title were verified.
- All three products were located; Sensor Kit was the single available featured product.
- Attribute, descendant, direct-child, combined-condition, and comma-separated selectors returned the expected results.
- DevTools returned 38 links and one body element after the correct top document context was selected.
- The final knowledge check passed after correcting the distinction between compound classes and descendant selectors.

Troubleshooting record:

- System Python initially caused `ModuleNotFoundError: No module named 'selenium'`; the Phase 3 `myenv` interpreter resolved it.
- A later `KeyboardInterrupt` occurred during Selenium imports; Python, `urllib.request`, and Selenium diagnostic commands passed, and the unchanged complete program then ran successfully.

Deliverables:

- `Day_69_CSS_Selectors.py` was committed to `Phase3-Browser-Automation` with a relevant commit.
- `Day_69_CSS_Selectors_Complete_Handbook.docx` was uploaded to the Phase 3 Google Drive study-guide folder.

## Canonical day-by-day Phase 3 plan

### Week 9 equivalent — Days 66–72: Selenium foundations

#### Day 66 — Selenium setup and first browser session — COMPLETED

- Selenium purpose
- Browser automation versus HTTP requests
- Virtual-environment activation
- Selenium installation
- WebDriver concept
- Microsoft Edge startup
- `driver.get()` and navigation
- Browser-driver bridge
- Reading page information
- `driver.quit()` and safe cleanup

#### Day 67 — Finding elements: foundations — COMPLETED

- Quick setup gap check: Selenium Manager, ChromeDriver, EdgeDriver, browser-version compatibility, and `webdriver-manager`
- DOM introduction
- HTML tags and attributes
- Inspecting a webpage with browser developer tools
- `find_element()`
- `find_elements()`
- `By.ID`
- `By.NAME`
- `By.TAG_NAME`
- Single WebElement versus a collection of WebElements
- What happens when no element is found
- `NoSuchElementException`

#### Day 68 — Text- and class-based locators — COMPLETED

- `By.CLASS_NAME`
- Limitations of compound class names
- `By.LINK_TEXT`
- `By.PARTIAL_LINK_TEXT`
- Extracting visible text with `.text`
- Reading attributes with `get_attribute()`
- `is_displayed()`
- `is_enabled()`
- `is_selected()`

#### Day 69 — CSS selectors — COMPLETED

- Tag selectors
- ID selectors
- Class selectors
- Attribute selectors
- Descendant selectors
- Child selectors
- Combining selector conditions
- Testing selectors with DevTools
- Stable versus fragile selectors

#### Day 70 — XPath — COMPLETED

- Absolute versus relative XPath
- Tag, wildcard, and attribute matching
- Multiple attributes with `and` and `or`
- Exact text matching with `text()` and `normalize-space()`
- Partial and prefix matching with `contains()` and `starts-with()`
- Parent, ancestor, child, descendant, and sibling relationships
- Positional indexes, parentheses, and `last()`
- Stable versus fragile XPath construction
- DevTools XPath testing
- Selenium XPath execution in Microsoft Edge
- Current-element searches with `.//`
- `find_element()`, `find_elements()`, and safe `NoSuchElementException` handling
- XPath versus CSS selectors
- When XPath is justified

Completion verification on 18 August 2026:

- The two previously pending comparison and decision topics were taught.
- The corrected knowledge check passed.
- No Day 70 topic or subtopic remains pending.

#### Day 71 — Reliable locator strategy — COMPLETED

- Locator-priority strategy
- Unique versus non-unique elements
- Dynamic IDs and classes
- Stable `data-*` attributes
- Reusable locator constants
- Handling missing elements
- Avoiding brittle selectors
- Clear diagnostic output for locator failures

Practical verification on 18 August 2026:

- The guided revision program produced the expected course-availability report.
- Microsoft Edge successfully ran the authorised offline Support Ticket Locator Audit.
- Stable locator constants returned unique intended elements.
- A broad class locator correctly reported two matches as non-unique.
- A missing optional element returned `None` with clear diagnostic output.
- The program continued safely and closed the browser through `finally`.
- All Day 71 knowledge checks passed after corrections.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_71_Reliable_Locator_Strategy.py`
- Python commit: `09a82b3b0fcbc80e04b8834561b3bd55ce5d7b4b`
- Google Drive handbook: `Day_71_Reliable_Locator_Strategy_Complete_Handbook.docx`
- Google Drive file ID: `17Uu4-U2FEWha2mULAz1-f_08x-hx7ikQ`

#### Day 72 — Basic page interactions — COMPLETED

- `.click()`
- `.send_keys()`
- `.clear()`
- Typing into input fields
- Clicking buttons and links
- Submitting forms
- Verifying the resulting page state

Practical verification on 19 August 2026:

- The required Workshop Seat Availability Report guided revision combined Python fundamentals and web scraping, produced two available workshops with 12 total seats, calculated the $30.62 average fee, and exported `available_workshops.csv`.
- Microsoft Edge successfully ran the authorised offline Service Request Submission Portal.
- `.send_keys()` entered customer and request values; `.clear()` removed the initial request before replacement.
- `.click()` activated the submit button and confirmation link.
- The submit button's `type="submit"` triggered the form workflow.
- Resulting state was verified through input `value`, visible text, custom `data-state` attributes, and `is_displayed()`.
- The link interaction changed the confirmation section from hidden to visible.
- The encoded data-page fragment check and a `NameError` were diagnosed and corrected without leaving a learning gap.
- The final knowledge check passed after clarifying DOM existence versus visibility and `.clear()` versus `.send_keys()`.
- The browser closed safely through `finally`.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_72_Basic_Page_Interactions.py`
- Python commit: `ff60873bb73e8e5605dd99fcbb16204359d66675`
- Google Drive handbook: `Day_72_Basic_Page_Interactions_Complete_Handbook.docx`
- Google Drive file ID: `1WnZKfz4ZoROgNsrOltvdMs1tyrEdrMFz`

Completion audit:

- Every canonical Day 72 topic and subtopic was taught, practised, executed, and checked.
- Text areas, checkboxes, radio buttons, dropdowns, keyboard keys, and validation messages remain correctly assigned to Day 73 rather than being Day 72 gaps.
- No Day 72 or earlier learning topic remains unfinished.

### Week 10 equivalent — Days 73–79: Selenium interaction and dynamic content

#### Day 73 — Forms and controls — COMPLETED

- Text inputs
- Text areas
- Checkboxes
- Radio buttons
- Native HTML dropdowns
- Selenium `Select`
- Selecting options by visible text, value, and zero-based index
- Submit buttons
- Keyboard keys
- Reading native HTML validation messages

Practical verification:

- The required Community Event Registration Report guided revision combined Python fundamentals and BeautifulSoup scraping, retained two available events, calculated 13 total seats and a $21.25 average fee, identified the highest-fee event, and exported `available_community_events.csv`.
- Microsoft Edge successfully ran the authorised offline Event Registration Portal.
- A text input and textarea accepted input and their live values were read through `get_attribute("value")`.
- The email-updates checkbox was selected conditionally and verified through `is_selected()`.
- Beginner and Intermediate radio buttons shared `name="experience"`; selecting Intermediate changed Beginner to `False` and Intermediate to `True`, verifying radio-group exclusivity.
- A native HTML dropdown was wrapped with Selenium `Select`.
- Options were selected by visible text, value, and zero-based index, returning Morning, Afternoon, and Evening Session respectively.
- `Keys.CONTROL + "a"` replaced existing textarea content and `Keys.TAB` moved keyboard focus.
- Clearing the required participant name produced the browser validation message and blocked invalid form submission.
- Valid submission revealed the confirmation section and changed `data-state` from `pending` to `submitted`.
- The browser closed safely through `finally`.

Knowledge verification:

- The final knowledge check passed after correcting input-value reading, the scope of `is_selected()`, zero-based dropdown indexes, and the reason native validation blocked the submit event.
- A second roadmap audit found and corrected the initially unverified radio-group exclusivity behaviour.
- No Day 73 or earlier learning topic remains unfinished.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_73_Forms_and_Controls.py`
- Python commit: `04bc24e333c072419c90169cde4f3b927452d6a8`
- Google Drive handbook: `Day_73_Forms_and_Controls_Complete_Handbook.docx`
- Google Drive file ID: `1cIXzlUewDTicCGoW6w6ZbirMgNEloSa5`

#### Day 74 — Navigation and browser state — COMPLETED

- Back navigation
- Forward navigation
- Refresh
- Current URL
- Page title
- Page source
- Tabs and windows
- Window handles
- Switching windows/tabs
- Closing the intended tab safely

Practical verification on 21 August 2026:

- The required Browser Activity Report guided revision combined Python fundamentals and BeautifulSoup scraping, extracted three records, sorted visit counts, calculated 34 total visits and an 11.33 average, identified Project Reports as most visited, and exported `browser_activity_report.csv`.
- Microsoft Edge successfully ran the authorised offline navigation-and-browser-state program.
- `driver.back()` restored Customer Dashboard and `driver.forward()` restored Order History; titles and exact URLs verified both operations.
- `driver.refresh()` reloaded Order History while the expected URL and title remained unchanged.
- `driver.current_url`, `driver.title`, and `driver.page_source` were read and verified.
- Selenium page source was confirmed as a string, searched for expected content, and parsed with BeautifulSoup.
- Selenium opened Activity Report in a new tab and Help Centre in a separate window.
- `current_window_handle` and `window_handles` identified the active context and all open contexts.
- Explicit handle-based switching returned control to the intended original, report, and help contexts.
- The report tab and Help Centre window were each selected and verified before `driver.close()`; the original Order History tab survived and was restored.
- `driver.quit()` ran through `finally` and closed the browser safely.

Knowledge verification:

- The rapid knowledge check passed.
- The assessment clarified that “survivor tab” correctly expresses why the original handle is saved and restored; concise correct understanding does not require copying one prescribed sentence.
- No Day 74 or earlier learning topic remains unfinished.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_74_Navigation_and_Browser_State.py`
- Google Drive handbook: `Day_74_Navigation_and_Browser_State_Complete_Handbook.docx`

#### Day 75 — Selenium waits

- Why dynamic pages require waiting
- Implicit waits
- Explicit waits
- `WebDriverWait`
- Polling behaviour
- Timeout values
- Why `time.sleep()` must not be the only wait strategy

#### Day 76 — Expected conditions

- Presence of an element
- Visibility of an element
- Element clickability
- Element invisibility
- URL conditions
- Title conditions
- Waiting for text
- Timeout handling
- Diagnosing timing-related failures

#### Day 77 — JavaScript-loaded and scrolling content

- Recognising JavaScript-loaded content
- Scrolling with JavaScript
- Scrolling an element into view
- Load-more buttons
- Infinite scrolling
- Reliable stopping conditions
- Duplicate prevention during repeated loads

#### Day 78 — Complex browser components

- Native dropdowns compared with custom dropdowns
- Pop-ups and overlays
- JavaScript alerts
- Confirm dialogs
- Prompt dialogs
- Iframes
- Switching into an iframe
- Returning to the main document

#### Day 79 — Screenshots and Selenium checkpoint — COMPLETED

- `driver.save_screenshot()`
- Element-level screenshots
- Screenshot success return values
- Evidence directories and resolved paths
- Timestamped evidence files and overwrite prevention
- Capturing screenshots after failures
- Structured logging
- Exception preservation with `raise`
- Complete Selenium practice project
- Form interaction
- Dynamic-content handling
- Result verification
- Reliable cleanup with `finally`

Practical verification on 26 August 2026:

- The guided Refund Case Monitor found four cases, skipped RF-704 for invalid numeric data, filtered the completed case, retained RF-701 and RF-703, calculated 62 total waiting minutes and a 31.00-minute average, identified RF-701 as highest priority, exported CSV, and verified the dynamic dashboard result `Pending cases: 2`.
- A deliberate `Pending cases: 99` mismatch proved the failure workflow: traceback logging, timestamped failure evidence, exception re-raising, and safe Edge cleanup.
- Microsoft Edge completed the authorised offline Warranty Claim checkpoint with claim WC-901 for Morgan Reed, Laptop selected, purchase proof checked, dynamic loader appearance and disappearance, approved-inspection status, matching reference, final-title verification, viewport evidence, and result-panel evidence.
- A real stale-element failure was diagnosed: JavaScript removed the overlay from the DOM, so the stored WebElement became stale. Capturing `overlay.is_displayed()` before the removal fixed it.
- The final knowledge check and canonical roadmap audit passed. No Day 79 or earlier assigned learning subtopic remains unfinished.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_79_Screenshots_and_Selenium_Checkpoint.py`
- Python commit: `31ea36af6d2a45c61f8f1d65df8ab5f0fc3dcce4`
- Google Drive handbook: `Day_79_Screenshots_and_Selenium_Checkpoint_Complete_Handbook.docx`
- Google Drive file ID: `1hV1K-ItxFJFlA6vxnZWMhDuzgoiqE4Gb`

### Week 11 equivalent — Days 80–86: Playwright foundations

#### Day 80 — Why Playwright and installation — COMPLETED

- Why Playwright exists
- Selenium versus Playwright
- Supported browser engines
- Installing the Python package
- Installing Playwright browsers
- Browser, context, and page architecture
- Synchronous versus asynchronous APIs
- First Playwright browser session

Practical verification:

- Playwright 1.62.0 was installed inside the Phase 3 `myenv` virtual environment with Python 3.14.
- Chromium-only browser binaries were installed in Playwright's shared per-user cache.
- The accidental global Playwright, pyee, and greenlet packages were removed; the global interpreter no longer imports Playwright, while the Phase 3 virtual environment does.
- The first headed Chromium Playwright session passed: title and heading were both `Automation Operations Portal`, two job cards were found, and the screenshot was created.
- BrowserContext, Page, synchronous versus asynchronous APIs, Selenium comparison, supported browser engines, and package-versus-browser installation were checked.
- Knowledge correction recorded: `context.new_page()` is the method that creates and returns a `Page` object.
- No Day 80 or earlier assigned learning subtopic remains unfinished.

Deliverables:

- GitHub Python file: `Phase3-Browser-Automation/Day_80_Why_Playwright_and_Installation.py`
- Python commit: `5a6fd63e43e7a0278f70950ad57560a75ea136f9`
- Google Drive handbook: `Day_80_Why_Playwright_and_Installation_Complete_Handbook.docx`
- Google Drive file ID: `1weXZxHAqEIxs4D98olPPkkHXQCch5eS8`

#### Day 81 — Playwright navigation and locators

- `page.goto()`
- Page title and URL
- CSS selectors
- Text selectors
- Role-based locators
- Label locators
- Placeholder locators
- Strict locator behaviour

#### Day 82 — Playwright interactions

- `click()`
- `fill()`
- Typing and pressing keys
- `text_content()`
- `inner_text()`
- Reading attributes
- Checkboxes
- Radio buttons
- Dropdowns

#### Day 83 — Auto-waiting and dynamic pages

- Playwright auto-waiting
- Actionability checks
- Locator waiting
- Timeouts
- Assertions
- Waiting for dynamic content
- Reducing flaky browser automation

#### Day 84 — Python `async`/`await` foundations

- Coroutines
- `async def`
- `await`
- Event-loop concept
- Sequential versus concurrent work
- Common beginner async mistakes

#### Day 85 — Async Playwright

- `async_playwright()`
- Launching a browser asynchronously
- Awaiting navigation
- Awaiting element interactions
- Safe asynchronous cleanup
- Async error handling

#### Day 86 — Headless mode

- Headed versus headless execution
- `headless=True`
- Why servers require headless execution
- Viewport configuration
- Browser launch arguments
- Debugging headless-only failures
- Screenshots and traces for headless diagnosis

### Week 12 equivalent — Days 87–93: Advanced Playwright and checkpoint

#### Day 87 — Sessions and login state

- Browser contexts
- Cookies
- Local storage
- Session storage
- `storage_state`
- Saving authenticated state
- Restoring authenticated state
- Protecting credentials and session files

#### Day 88 — CAPTCHAs and automation boundaries

- Why CAPTCHAs exist
- Recognising CAPTCHA challenges
- Ethical and Terms-of-Service boundaries
- Manual handoff
- Avoiding prohibited CAPTCHA bypasses
- Legitimate automation in authorised test environments

#### Day 89 — Network inspection

- Requests and responses
- Network event listeners
- Resource types
- HTTP status codes
- Request and response headers
- Identifying hidden API calls

#### Day 90 — Network interception

- Capturing JSON responses
- Request routing
- Blocking unnecessary resources
- Modifying requests in authorised testing
- Choosing API data versus rendered HTML
- Network-error handling

#### Day 91 — Concurrent browser automation

- `asyncio.gather()`
- Multiple pages
- Multiple browser contexts
- Concurrency limits
- Resource cleanup
- Partial-failure handling
- Responsible request rates

#### Day 92 — Selenium and Playwright comparison project

- Perform the same approved automation task with Selenium and Playwright
- Compare syntax
- Compare locators
- Compare wait behaviour
- Compare speed
- Compare reliability
- Compare headless execution
- Compare maintainability

#### Day 93 — Complete Phase 3 checkpoint

- Complete login or form workflow on an authorised practice website
- Handle dynamic content
- Perform browser actions
- Verify the final state
- Save screenshot evidence
- Run in headless mode
- Demonstrate Selenium and Playwright versions of the task
- Explain the differences between both tools
- Conduct final topic and subtopic gap audit

## Phase 3 checkpoint requirements from the original roadmap

Phase 3 is complete only when all five conditions are verified:

- [ ] Automate a complete login and action on an authorised website.
- [ ] Build a Selenium script that handles dynamic or JavaScript-loaded content.
- [ ] Perform the same task in Playwright and compare the two tools.
- [ ] Run browser automation in headless mode with no visible browser window.
- [ ] Build at least one complete form filler, login bot for an authorised practice site, or page screenshotter.

## Corrected earlier-item status

The following three items were previously listed as pending. The user has confirmed that all three are already completed:

- [x] Phase 1 combined 100-URL checkpoint exercise — COMPLETED
- [x] Price-tracker alert exercise — COMPLETED
- [x] Phase 2 GitHub README — COMPLETED

There is no pending carryover from this three-item list.

## Current continuation point

- Last verified completed day: **Day 80**
- Next day: **Day 81 — Playwright navigation and locators**
- Current original-roadmap area: **Playwright foundations**
- Phase 3 officially completed status: **15 of 28 days completed**
- Remaining Phase 3 days after Day 80: **13**
- Unfinished earlier learning topics or subtopics: **none**
- Day 81 must begin with the required rapid guided Python + web-scraping revision program.
- Do not begin Day 81's navigation-and-locators topic without the user's approval.

Day 80 completion evidence:

- Program: **Why Playwright and Installation**
- Browser: **Chromium**
- Environment: **Phase 3 myenv with Python 3.14 and Playwright 1.62.0**
- Verified terminal result: title and heading `Automation Operations Portal`, two job cards, and screenshot creation
- GitHub Python file: `Phase3-Browser-Automation/Day_80_Why_Playwright_and_Installation.py`
- Python commit: `5a6fd63e43e7a0278f70950ad57560a75ea136f9`
- Drive handbook: `Day_80_Why_Playwright_and_Installation_Complete_Handbook.docx`
- Drive file ID: `1weXZxHAqEIxs4D98olPPkkHXQCch5eS8`

## Permanent cross-chat source

- The canonical repository copy is `Phase3-Browser-Automation/Phase_3_Browser_Automation_Canonical_Tracker.md` on the `main` branch of `yagnikd1/AI-Automation-Engineer-Journey`.
- At the beginning of every new Phase 3 chat, retrieve the repository copy and compare it with the actual previous-day chat before replying or teaching.
- Update this repository file only after a day's completion has been verified from the actual lesson chat.
- If the tracker and previous-day chat disagree, identify the mismatch and ask the user instead of assuming a completion status.
